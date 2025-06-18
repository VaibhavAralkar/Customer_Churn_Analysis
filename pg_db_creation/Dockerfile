FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pg_db_creation.py .

CMD ["python", "pg_db_creation.py"]
