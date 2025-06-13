FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install --no-cache-dir poetry

# Instala dependências do projeto (sem criar virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copia o restante do código
COPY . .

# Permite execução do entrypoint
RUN chmod +x entrypoint.sh

# Expõe a porta da aplicação
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["./entrypoint.sh"]