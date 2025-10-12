from pathlib import Path
from typing import Union, Optional
import requests
import pyzipper
import shutil

PathLike = Union[str, Path]


def download_to_file(url: str, dest: PathLike, chunk_size: int = 8192) -> Path:
    """
    Download a file from `url` and save it to `dest` safely.
    """
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        tmp_path = dest_path.with_suffix(dest_path.suffix + ".part")
        with tmp_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
    tmp_path.replace(dest_path)
    return dest_path


def _safe_extract_zipfile(zf: pyzipper.AESZipFile, target_dir: Path) -> None:
    """
    Safely extract all files from a pyzipper ZipFile, preventing path traversal.
    """
    target_dir = target_dir.resolve()

    for member in zf.namelist():
        member_path = Path(member)
        resolved_path = (target_dir / member_path).resolve()

        # prevent path traversal (e.g., ../../etc/passwd)
        if not str(resolved_path).startswith(str(target_dir)):
            raise RuntimeError(f"Unsafe zip entry detected: {member!r}")

        if member.endswith("/"):
            resolved_path.mkdir(parents=True, exist_ok=True)
        else:
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as source, resolved_path.open("wb") as target:
                shutil.copyfileobj(source, target)


def extract_zip(zip_path: PathLike, output_dir: PathLike, password: Optional[str] = None) -> Path:
    """
    Extracts a zip (ZipCrypto or AES) using pyzipper only, safely.
    """
    zip_path = Path(zip_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with pyzipper.AESZipFile(zip_path) as zf:
        if password:
            zf.pwd = password.encode()
        _safe_extract_zipfile(zf, output_dir)
    return output_dir.resolve()
