# Usa uma imagem leve de Python
FROM python:3.12-slim-bookworm

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala dependências do sistema necessárias para o imgkit/wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependência primeiro (melhoria de cache do Docker)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte para o contêiner
COPY . .

# Expõe as portas que o FastAPI e o Streamlit usam
EXPOSE 8000 8501

# Comando padrão para rodar a aplicação (usaremos um script de entrada)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run src/frontend/app.py --server.port 8501"]