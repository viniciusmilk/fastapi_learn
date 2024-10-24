# Description: Dockerfile for the Python 3.12-slim image
FROM python:3.12-slim

# 
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD poetry run uvicorn --host 0.0.0.0 fast_zero.app:app