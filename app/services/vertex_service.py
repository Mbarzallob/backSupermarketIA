from google import genai
from google.genai import types
import json
import os
import re
from app.core.config import settings

PROJECT_ID = settings.VERTEX_PROJECT_ID
LOCATION   = settings.VERTEX_LOCATION
MODEL      = "gemini-2.5-flash"

SAFETY_CATEGORIES_OFF = [
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_HARASSMENT",
]
SAFETY_SETTINGS = [
    types.SafetySetting(category=cat, threshold="OFF")
    for cat in SAFETY_CATEGORIES_OFF
]

def generate(product_name: str) -> dict:
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )

    prompt = (
    f"Dame un JSON de un producto genérico de supermercado llamado «{product_name}». "
    "El JSON debe contener **solo** estos campos:\n"
    "  - nombre: nombre del producto:string\n"
    "  - categoría: p. ej. higiene, limpieza, alimentación, electrónica, etc.:string\n"
    "  - descripción: breve texto de 1-2 frases:string\n"
    "  - presentación: formato en que se vende (botella, paquete, caja…):string\n"
    "  - componentes_principales: lista de ingredientes o materiales clave:string[]\n"
    "  - usos_recomendados: lista de los usos más comunes:string[]\n"
    "  - beneficios: lista de ventajas o efectos deseables:string[]\n"
    "  - instrucciones: cómo usarlo paso a paso:string[]\n"
    "  - vida_util: p. ej. “12 meses después de abierto” o formato “YYYY-MM-DD”:string\n"
    "  - productos_similares: lista con al menos 3 nombres de productos parecidos:string[]\n" 
    "  - descripcion_general: un texto único, resumido en 2-3 frases, que combine toda la info anterior:string"
    )



    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1.0,
        top_p=1.0,
        seed=0,
        max_output_tokens=65535,
        safety_settings=SAFETY_SETTINGS,
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
    )

    full_text = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=config,
    ):
        full_text += chunk.text

    clean = _extract_json(full_text)
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return {"error_parse_json": full_text}
    
def _extract_json(text: str) -> str:
    
    no_fences = re.sub(r"```(?:json)?\n?", "", text)
    no_fences = no_fences.replace("```", "")
    start = no_fences.find("{")
    end   = no_fences.rfind("}") + 1
    return no_fences[start:end]

