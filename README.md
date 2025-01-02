# WeeklyStockInsights
Analysis of sentiments of stocks and their values ​​in weekly series

## Proyecto Docker con Python para Synology

### **1. Estructura del Proyecto**
```
WeeklyStockInsights/
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── main.py
│   ├── requirements.txt
├── README.md
```

---

### **2. Contenidos del Proyecto**

#### **Dockerfile**
```dockerfile
# Usar Python 3.8 slim como base
FROM python:3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de dependencias
COPY app/requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ /app/

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
```

#### **docker-compose.yml**
```yaml
version: "3.9"
services:
  python-app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./app:/app
    ports:
      - "8000:8000"
    container_name: python-env
```

#### **app/requirements.txt**
```plaintext
vaderSentiment
requests
pandas
```

#### **app/main.py**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    print(f"Sentiment Analysis: {sentiment}")

if __name__ == "__main__":
    analyze_sentiment("I love programming in Python!")
```

#### **README.md**
```markdown
# WeeklyStockInsights

## Requisitos
- Docker
- Docker Compose

## Cómo usar
1. Clona el repositorio:
   ```bash
   git clone https://github.com/maite828/WeeklyStockInsights.git
   cd WeeklyStockInsights
   ```

2. Construye y ejecuta el contenedor:
   ```bash
   docker-compose up --build
   ```

3. Accede al contenedor:
   ```bash
   docker exec -it python-env bash
   ```

4. Detén el contenedor:
   ```bash
   docker-compose down
   ```
```

---

### **3. Cómo usar el Proyecto**
1. Clona el repositorio en tu NAS:
   ```bash
   git clone https://github.com/maite828/WeeklyStockInsights.git
   cd WeeklyStockInsights
   ```

2. Construye y ejecuta el contenedor:
   ```bash
   docker-compose up --build -d
   ```

3. Verifica que la aplicación funcione correctamente:
   ```bash
   docker logs python-env
   ```
