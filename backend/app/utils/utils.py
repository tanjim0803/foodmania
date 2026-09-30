from fastapi import UploadFile
from pathlib import Path
import uuid

UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_upload_file(upload_file: UploadFile, sub_dir: str) -> str:
    ext = Path(upload_file.filename).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    dir_path = UPLOAD_DIR / sub_dir
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / filename

    content = await upload_file.read()

    with file_path.open("wb") as f:
        f.write(content)

    return str(file_path)
