import os

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")


def verify_upload_exists(filename: str) -> bool:
    return filename and os.path.exists(os.path.join(UPLOAD_DIR, filename))
