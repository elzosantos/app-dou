# app-gemini 🚀🤖

API simples em **FastAPI** que:

- 📰 Busca uma notícia no **SQLite** (`data/diariooficial.db`)
- 🤖 Usa o **Gemini** para explicar a notícia em linguagem simples
- 📌 Gera informações complementares (ramo + impacto em pequenos negócios)
- 🖼️ Cria um **cartão/infográfico em PNG** em `cartoes/` usando `imgkit` + `wkhtmltoimage`
- 💾 Faz **cache** das respostas do Gemini para evitar custo/repetição

---

## Como funciona ✨

O endpoint principal é:

- `GET /explicar/{id}` ✅  
  Retorna a notícia, a explicação da IA, dados complementares e o caminho do PNG gerado (quando disponível).

O fluxo é:

1. Procura a notícia na tabela `diariooficial` pelo `id`
2. Verifica se já existe explicação no cache (`resposta_gemini`)
3. Se não existir, chama o Gemini e salva no cache
4. Chama o Gemini para gerar um JSON curto com **ramo_atividade** e **impacto_pequenos_negocios**
5. Gera um PNG em `cartoes/<id>_<data>.png`

---

## Requisitos ✅

- 🐍 **Python 3.10+** (recomendado 3.12)
- 📦 Bibliotecas Python:
  - `fastapi`
  - `uvicorn`
  - `google-genai`
  - `imgkit`
- 🖼️ Dependência do sistema para gerar imagens:
  - `wkhtmltopdf` (inclui o binário `wkhtmltoimage`)

No Ubuntu/WSL:

```bash
sudo apt update
sudo apt install -y wkhtmltopdf
```

> Observação: o projeto aponta o `wkhtmltoimage` em `/usr/bin/wkhtmltoimage`.

---

## Configuração de ambiente 🔐

Este projeto usa `.env` (ex.: `GEMINI_API_KEY` e `MODEL`).  
Idealmente, a chave deve vir do ambiente (e **não** ficar hardcoded no código).

Exemplo de `.env`:

```env
GEMINI_API_KEY=COLOQUE_SUA_CHAVE_AQUI
MODEL=gemini-2.5-flash
```

---

## Criar o banco de dados 🗄️

Inicialize as tabelas:

```bash
python database.py
```

Isso cria:

- `diariooficial` (notícias)
- `resposta_gemini` (cache das explicações)

---

## Popular notícias (dados de exemplo) 🧪

Para inserir notícias fictícias no banco:

```bash
python popular_banco.py
```

---

## Rodar a API ▶️

Execute com Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Depois, acesse:

- 📚 Docs interativas: `http://localhost:8000/docs`

---

## Rodar a interface (Streamlit) 🖥️

Com a API rodando, execute:

```bash
streamlit run src/frontend/app.py
```

---

## Exemplo de uso 🧾

Chamar o endpoint para explicar a notícia de `id=1`:

```bash
curl "http://localhost:8000/explicar/1"
```

Resposta (resumo do que vem):

- ✅ `explicacao_inteligente`
- ✅ `ramo_atividade`
- ✅ `impacto_pequenos_negocios`
- ✅ `caminho_cartao_virtual` (ex.: `cartoes/1_2026-04-20.png`)

---

## Estrutura do projeto 🧱

- `main.py` — ponto de entrada (orquestrador) que expõe a `app` do FastAPI
- `src/backend/api.py` — rotas FastAPI
- `src/backend/database.py` — conexão/consultas SQLite
- `src/backend/gemini.py` — integração com o Gemini + prompts
- `src/backend/utils.py` — geração do cartão PNG (`imgkit`)
- `src/frontend/app.py` — interface Streamlit
- `database.py` — script para inicializar tabelas (wrapper)
- `popular_banco.py` — script para inserir notícias fictícias
- `data/diariooficial.db` — banco SQLite central
- `cartoes/` — imagens PNG geradas

---

## Dicas e solução de problemas 🛠️

- **Erro ao gerar PNG**:
  - Confirme se o `wkhtmltoimage` existe em `/usr/bin/wkhtmltoimage`
  - Reinstale `wkhtmltopdf` se necessário
- **Gemini indisponível**:
  - O endpoint pode retornar `503` quando a IA falhar
- **Cache**:
  - Se uma notícia já foi explicada, a API reutiliza o texto salvo na tabela `resposta_gemini`

---

## Licença 📄

Defina a licença que preferir (MIT, Apache-2.0, etc.).  
Se quiser, eu posso adicionar um arquivo `LICENSE` também.

