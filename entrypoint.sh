#!/bin/sh

set -e  # Encerra o script se qualquer comando falhar

DB_HOST=${DB_HOST:-database}
DB_PORT=${DB_PORT:-5432}

echo "⏳ Aguardando o banco de dados em $DB_HOST:$DB_PORT..."

# Espera o banco de dados ficar disponível
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "✅ Banco de dados está pronto."

# Executa as migrações, se alembic estiver configurado
echo "🚀 Executando migrações..."
alembic upgrade head

# Inicia a aplicação
echo "📦 Iniciando a aplicação FastAPI..."
exec poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000 --reload
