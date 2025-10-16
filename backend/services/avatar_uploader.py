import os
import aiofiles
import uuid
from fastapi import UploadFile, File, HTTPException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


class AvatarUploader:
    BASE_DIR = "static/images"

    @staticmethod
    async def upload_avatar(
        object_type: str, object_id: int, file: UploadFile = File(...)
    ) -> str:
        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid image format")

        target_dir = os.path.join(AvatarUploader.BASE_DIR, f"{object_type}s")
        os.makedirs(target_dir, exist_ok=True)

        filename = f"{object_type}_{object_id}_{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(target_dir, filename)

        async with aiofiles.open(file_path, "wb") as image_file:
            while chunk := await file.read(1024 * 1024):
                await image_file.write(chunk)

        return f"/{file_path}"
