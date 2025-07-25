from supabase import create_client, Client
from app.core.config import settings


url = settings.SUPABASE_URL
key = settings.SUPABASE_KEY
supabase: Client = create_client(url, key)

def insert_product(nombre:str, descripcion:str, resumen:str):
    data = {
        "nombre": nombre,
        "descripcion": descripcion,
        "resumen": resumen
    }
    supabase.table("productos").insert(data).execute()
    
def get_products():
    response = supabase.table("productos").select("*").execute()
    return response.data if response.data else []
