# Dalia – Backend do Chat (Gemini)

IA de apoio à **saúde da mulher** e à **violência doméstica**. O backend é **stateless**:
não salva nada; o app Android (Kotlin) guarda o histórico na RAM e o reenvia a cada pergunta.

```
Kotlin (histórico na RAM) ──POST /chat──▶ FastAPI ──system prompt + histórico──▶ Gemini
        ◀────────── {"reply": "..."} ◀───────────────────────────────────────────┘
```

## 1. Pré-requisitos (Linux)
- Conda (Miniconda ou Anaconda) instalado
- Chave gratuita do Gemini: https://aistudio.google.com/apikey

## 2. Instalação (Conda)
```bash
conda create -n dalia python=3.11 -y
conda activate dalia
python -m pip install -r requirements.txt
```
Nas próximas vezes, basta `conda activate dalia`.

## 3. Configurar a chave
Só para o terminal atual:
```bash
export GEMINI_API_KEY="sua_chave_aqui"
```
Para guardar dentro do ambiente conda (carrega sozinho ao ativar `dalia`):
```bash
conda env config vars set GEMINI_API_KEY="sua_chave_aqui"
conda deactivate && conda activate dalia
```
Nunca coloque a chave no código, no README nem no Git.

## 4. Rodar
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Documentação interativa: http://localhost:8000/docs

Para o celular/emulador alcançar o PC, descubra o IP local com `hostname -I` e libere a porta
se houver firewall (`sudo ufw allow 8000`).

## 5. Testar
### Pelo terminal (sem servidor)
```bash
python chat_terminal.py
```
Converse normalmente; `/limpar` apaga a memória (Modo Disfarce) e `/sair` encerra.

### Pela API
```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Minha menstruação está atrasada 3 dias, posso estar grávida?"}]}'
```

Conversa com memória (o app reenvia tudo):
```json
{"messages": [
  {"role": "user", "content": "Minha menstruação está atrasada 3 dias"},
  {"role": "assistant", "content": "...resposta anterior da Dalia..."},
  {"role": "user", "content": "E se eu fizer o teste hoje?"}
]}
```
Regras: `role` = `user` ou `assistant`; a **última** mensagem deve ser `user`;
até 4000 caracteres por mensagem; só as últimas 20 mensagens são usadas.

## 6. Integração com o Kotlin
- Emulador Android acessa o PC em `http://10.0.2.2:8000/`; celular real usa o IP do PC na rede.
- Mantenha `val historico = mutableListOf<Mensagem>()` em memória (ex.: no ViewModel).
- A cada envio: adicione a mensagem do usuário → `POST /chat` com a lista inteira →
  adicione a `reply` à lista e exiba o balão.
- **Modo Disfarce**: o botão "Sair/Limpar chat" só faz `historico.clear()` e fecha a tela.
  Não use banco de dados, SharedPreferences nem logs com o conteúdo da conversa.
- Em produção use **HTTPS** (ex.: Render, Railway, Cloud Run).

## 7. Como a segurança funciona
| Camada | O que faz |
|---|---|
| System prompt | Persona empática com 3 pilares: saúde (sem diagnóstico/receitas), segurança (protocolo 190/180/DEAM) e encerramento humanizado (sem forçar perguntas ao se despedir) |
| `temperature=0.2` | Respostas consistentes, sem "criatividade" médica |
| Rede de segurança (regex) | Se houver gatilhos de violência ou sintomas graves, o backend **acrescenta** os telefones (180/190/192) mesmo que o modelo esqueça |
| Safety settings | Evita que o filtro do Gemini bloqueie relatos de violência |
| Stateless | Nada gravado no servidor; o backend não registra o conteúdo das conversas |

## 8. Personalização
Tudo em `main.py`: `SYSTEM_PROMPT` (regras e tom), `MODEL`, `MAX_TURNS`, `TRIGGERS`/`HEALTH_URGENT` (gatilhos).

## 9. Limitações (citar no trabalho acadêmico)
- A IA é informativa e **não substitui** atendimento médico, psicológico ou policial.
- Os gatilhos por regex são simples; podem falhar com gírias ou erros de digitação.
- O texto da conversa é enviado ao Google (Gemini): informe isso à usuária.
- Verifique periodicamente se os telefones (Ligue 180, WhatsApp (61) 99610-0180) continuam corretos.
