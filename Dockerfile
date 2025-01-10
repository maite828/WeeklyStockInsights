FROM python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

# Ejecutar la aplicación Python
CMD ["python", "main.py"]

