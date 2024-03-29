import uuid

from fastapi import APIRouter, UploadFile, File, Depends

router = APIRouter()


@router.post("")
async def create_upload_file(file: UploadFile = File(...)):
    file_name = uuid.uuid4()
    ext = file.filename.split(".")[-1]
    path = f"static/{file_name}.{ext}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return {"file_path": path}
