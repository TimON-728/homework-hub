import os
from filestack import Client

FILESTACK_API_KEY = os.getenv("FILESTACK_API_KEY")


def save_photos(uploaded_files: list) -> list[str]:
    client = Client(FILESTACK_API_KEY)
    urls = []
    for file in uploaded_files:
        # Streamlit UploadedFile — file-like объект
        new_filelink = client.upload(file_obj=file)
        urls.append(new_filelink.url)
    return urls


def delete_photos(urls: list[str]) -> None:
    if not urls:
        return
    client = Client(FILESTACK_API_KEY)
    for url in urls:
        # Filestack handle — это последняя часть URL после последнего /
        handle = url.rstrip("/").split("/")[-1]
        try:
            client.delete(handle)
        except Exception as e:
            print(f"Не удалось удалить {handle}: {e}")