FROM python:3.11-slim

WORKDIR /app

# copier tout le projet
COPY .. /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api/app.py"]
