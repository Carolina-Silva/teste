"""Chat da Dalia no terminal (não precisa subir o servidor).

Uso:  python chat_terminal.py
Comandos: /limpar apaga a memória da conversa | /sair encerra
"""
from fastapi import HTTPException

from main import ChatRequest, Message, chat

historico: list[Message] = []  # memória só na RAM, igual ao app Kotlin

print("Dalia 💜  (digite /limpar para apagar a conversa, /sair para encerrar)\n")
while True:
    try:
        texto = input("Você: ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if not texto:
        continue
    if texto == "/sair":
        break
    if texto == "/limpar":
        historico.clear()
        print("Conversa apagada.\n")
        continue

    historico.append(Message(role="user", content=texto))
    print("Dalia está digitando...", flush=True)
    try:
        resposta = chat(ChatRequest(messages=historico)).reply
    except HTTPException as e:
        historico.pop()  # descarta a pergunta que falhou
        print(f"[erro {e.status_code}] {e.detail} (veja o [ERRO GEMINI] acima)\n")
        continue

    historico.append(Message(role="assistant", content=resposta))
    print(f"\nDalia: {resposta}\n")
