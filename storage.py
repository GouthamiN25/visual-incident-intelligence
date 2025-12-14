import os, uuid, shutil

UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")

def save_upload(file_obj, filename: str) -> tuple[str, str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    incident_id = str(uuid.uuid4())
    safe_name = filename.replace("/", "_").replace("\\", "_")
    out_path = os.path.join(UPLOAD_DIR, f"{incident_id}__{safe_name}")
    with open(out_path, "wb") as f:
        shutil.copyfileobj(file_obj, f)
    return incident_id, out_path
