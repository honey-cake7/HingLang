"""Minimal PEP 517 backend for the HingLang project.

This backend is intentionally self-contained so the project can be installed
with `pip install .` without requiring setuptools or any other build package.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import tarfile
import zipfile
from pathlib import Path


NAME = "hinglang"
VERSION = "0.1.0"
WHEEL_TAG = "py3-none-any"
DIST_INFO = f"{NAME}-{VERSION}.dist-info"
PROJECT_ROOT = Path(__file__).resolve().parent


def _metadata_text() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.1",
            f"Name: {NAME}",
            f"Version: {VERSION}",
            "Summary: An educational compiler pipeline for HingLang",
            "Requires-Python: >=3.10",
            "",
        ]
    )


def _wheel_text() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: hinglang.build_backend",
            "Root-Is-Purelib: true",
            f"Tag: {WHEEL_TAG}",
            "",
        ]
    )


def _entry_points_text() -> str:
    return "\n".join(
        [
            "[console_scripts]",
            "hinglang = main:main",
            "hinglang-demos = run_demos:main",
            "",
        ]
    )


def _hash_bytes(data: bytes) -> tuple[str, int]:
    digest = hashlib.sha256(data).digest()
    encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return f"sha256={encoded}", len(data)


def _iter_source_files():
    include_roots = ["hinglang", "examples", "tests"]
    include_files = {"main.py", "run_demos.py", "run_tests.py", "README.md", "pyproject.toml", "MANIFEST.in", "build_backend.py"}

    for relative_path in sorted(include_files):
        source_path = PROJECT_ROOT / relative_path
        if source_path.is_file():
            yield relative_path, source_path

    for root_name in include_roots:
        root_path = PROJECT_ROOT / root_name
        if not root_path.exists():
            continue
        for source_path in sorted(root_path.rglob("*")):
            if source_path.is_file():
                yield source_path.relative_to(PROJECT_ROOT).as_posix(), source_path


def _write_wheel_metadata(zip_file: zipfile.ZipFile) -> list[tuple[str, bytes]]:
    metadata_files = [
        (f"{DIST_INFO}/METADATA", _metadata_text().encode("utf-8")),
        (f"{DIST_INFO}/WHEEL", _wheel_text().encode("utf-8")),
        (f"{DIST_INFO}/entry_points.txt", _entry_points_text().encode("utf-8")),
    ]

    for archive_name, data in metadata_files:
        zip_file.writestr(archive_name, data)

    return metadata_files


def _write_record(zip_file: zipfile.ZipFile, records: list[tuple[str, bytes]]) -> None:
    record_rows = []
    for archive_name, data in records:
        digest, size = _hash_bytes(data)
        record_rows.append((archive_name, digest, str(size)))

    record_rows.append((f"{DIST_INFO}/RECORD", "", ""))
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerows(record_rows)
    zip_file.writestr(f"{DIST_INFO}/RECORD", buffer.getvalue().encode("utf-8"))


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_sdist(config_settings=None):
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    dist_info_dir = Path(metadata_directory) / DIST_INFO
    dist_info_dir.mkdir(parents=True, exist_ok=True)
    (dist_info_dir / "METADATA").write_text(_metadata_text(), encoding="utf-8")
    (dist_info_dir / "WHEEL").write_text(_wheel_text(), encoding="utf-8")
    (dist_info_dir / "entry_points.txt").write_text(_entry_points_text(), encoding="utf-8")
    return DIST_INFO


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_name = f"{NAME}-{VERSION}-{WHEEL_TAG}.whl"
    wheel_path = Path(wheel_directory) / wheel_name

    written_records: list[tuple[str, bytes]] = []
    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for archive_name, source_path in _iter_source_files():
            data = source_path.read_bytes()
            zip_file.writestr(archive_name, data)
            written_records.append((archive_name, data))

        metadata_records = _write_wheel_metadata(zip_file)
        written_records.extend(metadata_records)
        _write_record(zip_file, written_records)

    return wheel_name


def build_sdist(sdist_directory, config_settings=None):
    sdist_name = f"{NAME}-{VERSION}.tar.gz"
    sdist_path = Path(sdist_directory) / sdist_name
    base_dir = f"{NAME}-{VERSION}"

    with tarfile.open(sdist_path, "w:gz") as archive:
        for archive_name, source_path in _iter_source_files():
            tar_info = archive.gettarinfo(str(source_path), arcname=f"{base_dir}/{archive_name}")
            with source_path.open("rb") as file_handle:
                archive.addfile(tar_info, file_handle)

    return sdist_name