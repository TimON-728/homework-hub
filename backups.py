import os
import io
import zipfile
import streamlit as st
from pathlib import Path

# Пути — относительно корня проекта
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "homework.db"
UPLOAD_DIR = PROJECT_ROOT / "uploads"


def render_backup_page():
    st.title("💾 Резервная копия")

    # Получаем код из secrets
    try:
        SECRET_CODE = os.getenv("DB_BACKUP_CODE")   
    except KeyError:
        st.error("Код не настроен в secrets")
        return

    code = st.text_input("Введите код доступа", type="password")

    if not code:
        return

    if code != SECRET_CODE:
        st.error("Неверный код")
        return

    st.success("Доступ разрешён")

    # --- СКАЧИВАНИЕ ---
    st.markdown("### ⬇️ Скачать бэкап")

    if st.button("Создать архив", use_container_width=True):
        if not DB_PATH.exists():
            st.error("БД не найдена")
            return

        # Создаём zip в памяти
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            # 1. БД
            zf.write(DB_PATH, arcname="homework.db")

            # 2. Фото
            if UPLOAD_DIR.exists():
                for file in UPLOAD_DIR.iterdir():
                    if file.is_file():
                        zf.write(file, arcname=f"uploads/{file.name}")

        buf.seek(0)

        st.download_button(
            label="⬇️ Скачать .zip",
            data=buf.getvalue(),
            file_name="homework_backup.zip",
            mime="application/zip",
            use_container_width=True
        )