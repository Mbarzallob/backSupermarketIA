from fastapi import APIRouter, UploadFile, HTTPException
import os
import aiofiles
from app.services import generate, recognize_product
from app.infrastructure.supabase import insert_product, get_products

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
    try:
        for item in data:
            insert_product(item["nombre"], item["descripcion"], item["descripcion_general"])
    except Exception as e:
        print(f"Error al insertar producto: {e}")
    return data

@router.get("/")
async def get_all_products():
    try:
        products = get_products()
        return products
    except Exception as e:
        raise HTTPException(500, detail=f"Error al obtener productos: {str(e)}")

