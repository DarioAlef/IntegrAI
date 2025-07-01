FROM python:3.11-slim
WORKDIR /app
# Instala dependências do sistema
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
# Copia apenas os arquivos de dependências primeiro (para cache)
COPY requirements.txt .
# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt
# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
# Copia o código (será sobrescrito pelo volume em desenvolvimento)
COPY . .
# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]