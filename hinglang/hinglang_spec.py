# ============================================
# HingLang Language Specification
# Phase 1 Implementation
# ============================================

class HingLangSpec:

    # -----------------------------
    # Language Name
    # -----------------------------
    LANGUAGE_NAME = "HingLang"

    # -----------------------------
    # Keywords
    # -----------------------------
    KEYWORDS = {
        "shuru": "START",
        "khatam": "END",
        "bol": "PRINT",
        "line": "STR_DECL",
        "num": "INT_DECL",
        "agar": "IF",
        "warna": "ELSE",
        "jabtak": "WHILE",
        "sun": "INPUT"
    }

    # -----------------------------
    # Arithmetic Operators
    # -----------------------------
    ARITHMETIC_OPERATORS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MUL",
        "/": "DIV"
    }

    # -----------------------------
    # Relational Operators
    # -----------------------------
    RELATIONAL_OPERATORS = {
        "<": "LT",
        ">": "GT",
        "<=": "LE",
        ">=": "GE",
        "==": "EQ"
    }

    # -----------------------------
    # Assignment Operator
    # -----------------------------
    ASSIGNMENT_OPERATOR = "="

    # -----------------------------
    # Valid Identifier Rules
    # -----------------------------
    @staticmethod
    def is_valid_identifier(name):
        if not name:
            return False

        if not name[0].isalpha():
            return False

        for ch in name:
            if not (ch.isalnum()):
                return False

        return True

    # -----------------------------
    # Language Grammar (Informal)
    # -----------------------------
    GRAMMAR = {
        "program": "SHURU stmt_list KHATAM",

        "stmt": [
            "declaration",
            "assignment",
            "print_stmt",
            "while_stmt",
            "if_stmt"
        ],

        "declaration": "num ID = expr",

        "assignment": "ID = expr",

        "print_stmt": "bol expr",

        "while_stmt": "jabtak condition stmt_list khatam",

        "if_stmt": "agar condition stmt_list warna stmt_list khatam",

        "condition": "expr REL_OP expr",

        "expr": "term ((+ | -) term)*"
    }

    # -----------------------------
    # Sample Programs
    # -----------------------------
    SAMPLE_PROGRAMS = {

        "simple_print":
        """
        shuru
        num a = 5
        bol a
        khatam
        """,

        "loop":
        """
        shuru
        num a = 1
        jabtak a <= 5
        bol a
        a = a + 1
        khatam
        khatam
        """,

        "if_else":
        """
        shuru
        num a = 7
        agar a > 5
        bol a
        warna
        bol 0
        khatam
        khatam
        """
    }
    PARENTHESES = {
        "(": "LPAREN",
        ")": "RPAREN"
    }

# ============================================
# Utility function to print full language spec
# ============================================

def show_language_spec():
    print("Language:", HingLangSpec.LANGUAGE_NAME)

    print("\nKeywords:")
    for k, v in HingLangSpec.KEYWORDS.items():
        print(f"{k} -> {v}")

    print("\nArithmetic Operators:")
    for k, v in HingLangSpec.ARITHMETIC_OPERATORS.items():
        print(f"{k} -> {v}")

    print("\nRelational Operators:")
    for k, v in HingLangSpec.RELATIONAL_OPERATORS.items():
        print(f"{k} -> {v}")

    print("\nGrammar Rules:")
    for k, v in HingLangSpec.GRAMMAR.items():
        print(f"{k} -> {v}")

    print("\nSample Programs Available:")
    for k in HingLangSpec.SAMPLE_PROGRAMS:
        print("-", k)


# ============================================
# Run Phase-1 Demo
# ============================================

if __name__ == "__main__":
    show_language_spec()