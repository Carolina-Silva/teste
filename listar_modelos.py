"""Lista os modelos Gemini disponíveis para a sua chave (GEMINI_API_KEY)."""
import os

from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for m in client.models.list():
    if "generateContent" in (m.supported_actions or []):
        print(m.name.removeprefix("models/"))
