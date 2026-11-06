"""Teste rápido para ver qual modelo responde na sua máquina."""
import os
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Execute: pip install google-genai")
    sys.exit(1)

key = os.environ.get("GEMINI_API_KEY")
if not key:
    print("ERRO: GEMINI_API_KEY não encontrada no ambiente!")
    sys.exit(1)

client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=15_000))
modelos = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

print(f"Testando conexão com chave {key[:6]}... nos modelos do Gemini:\n")
for m in modelos:
    print(f"-> Tentando {m}...", end=" ", flush=True)
    try:
        r = client.models.generate_content(
            model=m,
            contents="Diga apenas: 'Dalia online'",
        )
        print(f"SUCESSO! Resposta: {r.text.strip()}")
        break
    except Exception as e:
        msg = str(e)
        if "503" in msg:
            print("Indisponível (503 demanda alta)")
        elif "404" in msg:
            print("Não encontrado (404)")
        else:
            print(f"Erro: {type(e).__name__} - {msg[:70]}")
