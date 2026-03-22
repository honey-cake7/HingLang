from .compiler_errors import RuntimeExecutionError


class TACExecutor:

    def __init__(self, code):
        self.code = code
        self.memory = {}
        self.labels = {}
        self.ip = 0

        self.prepare_labels()

    def prepare_labels(self):
        for i, line in enumerate(self.code):
            line = line.strip()
            if line.endswith(":"):
                self.labels[line[:-1]] = i

    def get_value(self, x):
        x = x.strip()
        if x.isdigit() or (x.startswith("-") and x[1:].isdigit()):
            return int(x)
        if x.startswith('"') and x.endswith('"'):
            return x[1:-1]
        if x not in self.memory:
            raise RuntimeExecutionError(
                f"Undefined variable '{x}'",
                line=self.ip + 1,
                token=x
            )

        return self.memory[x]

    def eval_condition(self, cond):
        parts = cond.split()

        if len(parts) != 3:
            raise RuntimeExecutionError(
                f"Malformed condition '{cond}'",
                line=self.ip + 1,
                token=cond
            )

        left = self.get_value(parts[0])
        op = parts[1]
        right = self.get_value(parts[2])

        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        if op == "==":
            return left == right

        return False

    def execute(self):

        while self.ip < len(self.code):

            line = self.code[self.ip].strip()

            if not line:
                self.ip += 1
                continue
            # INPUT
            if line.startswith("input"):

                var = line.split()[1]

                user_val = input()

                # decide type
                if user_val.isdigit():
                    self.memory[var] = int(user_val)
                else:
                    self.memory[var] = user_val

                self.ip += 1
                continue
            # skip labels
            if line.endswith(":"):
                self.ip += 1
                continue

            # PRINT
            if line.startswith("print"):
                content = line[6:].strip()

                if content.startswith('"') and content.endswith('"'):
                    print(content[1:-1])
                else:
                    print(self.memory.get(content, 0))

                self.ip += 1
                continue

            # GOTO
            if line.startswith("goto"):
                label = line.split()[1]
                if label not in self.labels:
                    raise RuntimeExecutionError(
                        f"Unknown label '{label}'",
                        line=self.ip + 1,
                        token=label
                    )
                self.ip = self.labels[label]
                continue

            # IF FALSE
            if line.startswith("ifFalse"):
                temp = line.replace("ifFalse", "").strip()
                cond_part, label_part = temp.split("goto")
                cond_part = cond_part.strip()
                label = label_part.strip()

                if label not in self.labels:
                    raise RuntimeExecutionError(
                        f"Unknown label '{label}'",
                        line=self.ip + 1,
                        token=label
                    )

                if not self.eval_condition(cond_part):
                    self.ip = self.labels[label]
                else:
                    self.ip += 1
                continue

            # ASSIGNMENT
            if "=" in line:

                left, right = line.split("=", 1)

                var = left.strip()
                rhs = right.strip()

                # arithmetic expression
                tokens = rhs.split()

                if len(tokens) == 3:
                    v1 = self.get_value(tokens[0])
                    op = tokens[1]
                    v2 = self.get_value(tokens[2])

                    if op == "+":
                        res = v1 + v2
                    elif op == "-":
                        res = v1 - v2
                    elif op == "*":
                        res = v1 * v2
                    elif op == "/":
                        if v2 == 0:
                            raise RuntimeExecutionError(
                                "Division by zero",
                                line=self.ip + 1,
                                token=rhs
                            )
                        res = v1 // v2
                    else:
                        raise RuntimeExecutionError(
                            f"Unsupported operator '{op}'",
                            line=self.ip + 1,
                            token=rhs
                        )

                    self.memory[var] = res

                else:
                    # simple assign (number / string / variable)
                    self.memory[var] = self.get_value(rhs)

                self.ip += 1
                continue
            self.ip += 1