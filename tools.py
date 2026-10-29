import re
import shutil
import urllib.error
import urllib.request
from pathlib import Path
from typing import Final

__all__ = [
    "check_internet",
    "delete_dir",
    "find_files",
    "format_bytes",
    "unroll_vars",
]

BINARY_UNITS: Final[tuple[str, ...]] = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
DECIMAL_UNITS: Final[tuple[str, ...]] = ("B", "KB", "MB", "GB", "TB", "PB", "EB")

BINARY_FACTOR: Final[int] = 1024
DECIMAL_FACTOR: Final[int] = 1000
MAX_UNIT_EXPONENT: Final[int] = len(BINARY_UNITS) - 1

DEFAULT_CHECK_URL: Final[str] = "http://cp.cloudflare.com/generate_204"
DEFAULT_TIMEOUT: Final[float] = 2.0


def format_bytes(size_bytes: int, use_binary: bool = True, precision: int = 2) -> str:
    if size_bytes < 0:
        raise ValueError("Unreal file size")
    if size_bytes == 0:
        return "0 B"

    factor = BINARY_FACTOR if use_binary else DECIMAL_FACTOR
    units = BINARY_UNITS if use_binary else DECIMAL_UNITS
    exponent = min(_calculate_exponent(size_bytes, factor), MAX_UNIT_EXPONENT)

    if exponent == 0:
        return f"{size_bytes} B"

    value = size_bytes / (factor**exponent)
    return f"{value:.{precision}f} {units[exponent]}"


def _calculate_exponent(size_bytes: int, factor: int) -> int:
    exponent = 0
    while factor ** (exponent + 1) <= size_bytes:
        exponent += 1
    return exponent


def check_internet(host: str = DEFAULT_CHECK_URL, timeout: float = DEFAULT_TIMEOUT) -> bool:
    request = urllib.request.Request(host)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status in (200, 204)
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def delete_dir(path: str | Path) -> None:
    directory = Path(path)
    if directory.is_dir():
        shutil.rmtree(directory)


def find_files(directory: str | Path, words: list[str]) -> list[Path]:
    target_dir = Path(directory)
    matched_files: list[Path] = []

    for path in target_dir.rglob("*"):
        if not path.is_file():
            continue

        content = path.read_text(encoding="utf-8", errors="ignore")
        if all(word in content for word in words):
            matched_files.append(path)

    return matched_files


def unroll_vars(source: Path) -> None:
    decl = re.compile(r"^\s*(?:final\s+)?(?:short|int|byte|long)\s+(\w+)\s*=\s*(-?\d+|0x[0-9a-fA-F]+)[lL]?\s*;\s*$")

    def inline(text: str) -> str:
        values: dict[str, str] = {}
        out: list[str] = []
        for line in text.split("\n"):
            if line.startswith("    }"):
                values.clear()
            match = decl.match(line)
            if match:
                values[match[1]] = match[2]
                continue
            for key, value in values.items():
                line = re.sub(rf"\b{re.escape(key)}\b", value, line)
            out.append(line)
        return "\n".join(out)

    source.write_text(inline(source.read_text(encoding="utf-8")), encoding="utf-8")
