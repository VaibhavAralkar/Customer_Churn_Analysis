FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY data_cleaning.py .

CMD ["python", "data_cleaning.py"]
