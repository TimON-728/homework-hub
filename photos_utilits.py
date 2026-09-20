import os
from uuid import uuid4


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_SIZE_MB = 10


def save_photos(uploaded_files: list) -> list[str]:
    paths = []

    try:
        for file in uploaded_files:
            ext = file.name.split(".")[-1].lower()

            if ext not in ALLOWED_EXT:
                raise ValueError(f"Недопустимое расширение: {ext}")

            if file.size > MAX_SIZE_MB * 1024 * 1024:
                raise ValueError(f"Файл больше {MAX_SIZE_MB} MB")

            filename = f"{uuid4()}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

            paths.append(filepath)

    except ValueError:
        delete_photos(paths)
        raise

    return paths


def delete_photos(paths: list[str]) -> None:
    for path in paths:
        if os.path.exists(path):
            os.remove(path)