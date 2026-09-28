import os
from uuid import uuid4
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

print(f"РАБОЧАЯ ДИРЕКТОРИЯ: {os.getcwd()}")
print(f"ПАПКА UPLOADS: {UPLOAD_DIR.resolve()}")
print(f"ПАПКА СУЩЕСТВУЕТ: {UPLOAD_DIR.exists()}")

def save_photos(uploaded_files):
    paths = []
    for file in uploaded_files:
        ext = file.name.split(".")[-1].lower()
        filename = f"{uuid4()}.{ext}"
        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as f:
            f.write(file.getbuffer())

        print(f"ЗАПИСАЛ: {filepath.resolve()}")
        print(f"ПОСЛЕ ЗАПИСИ СУЩЕСТВУЕТ: {filepath.exists()}")
        paths.append(str(filepath))

    return paths


def delete_photos(paths: list[str]) -> None:
    for path in paths:
        print(f"УДАЛЯЮ: {path}")
        if os.path.exists(path):
            os.remove(path)