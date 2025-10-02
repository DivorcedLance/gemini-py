import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("⚠️ Por favor define GEMINI_API_KEY en tu .env")

# Crear cliente de Gemini
client = genai.Client(api_key=api_key)

# Inicializar app FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile,
    prompt: str = Form("Describe esta imagen en formato JSON con categorías relevantes.")
):
    try:
        # Leer bytes de la imagen
        image_bytes = await file.read()
        mime_type = file.content_type or "image/png"

        contents = [
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        return JSONResponse(content={"result": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Montar carpeta estática AL FINAL para que no interfiera con las rutas de la API
app.mount("/", StaticFiles(directory="static", html=True), name="static")
