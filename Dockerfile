FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dockerfile (CORREGIDO PARA COINCIDIR)
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app.__init__:app", "--bind", "0.0.0.0:8001"]