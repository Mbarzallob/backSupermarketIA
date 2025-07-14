from fastapi import APIRouter, UploadFile, HTTPException
import os
import aiofiles
from app.services import generate, recognize_product

router = APIRouter()


@router.post("/")
async def create_upload_product(file: UploadFile):
    os.makedirs("images", exist_ok=True)
    file_path = os.path.join("images", file.filename)

    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="Sólo imágenes permitidas")

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()       
        await out_file.write(content)     
    
    producto = recognize_product(file_path)


    if not producto:
        raise HTTPException(404, detail="No se pudo reconocer el producto")
    data = generate(producto)
    return data

