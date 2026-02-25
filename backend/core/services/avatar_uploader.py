import os
import aiofiles
import uuid
from fastapi import UploadFile, File
from exceptions import AppException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
BASE_DIR = "static/images"


async def upload_avatar(
    object_type: str, object_id: int, file: UploadFile = File(...)
) -> str:
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise AppException("Invalid image format", status_code=400)

    target_dir = os.path.join(BASE_DIR, f"{object_type}s")
    os.makedirs(target_dir, exist_ok=True)

    filename = f"{object_type}_{object_id}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(target_dir, filename)

    async with aiofiles.open(file_path, "wb") as image_file:
        while chunk := await file.read(1024 * 1024):
            await image_file.write(chunk)

    return f"/{file_path}"
