import csv
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    filename='/volume1/docker/logs/app.log',
    level=logging.DEBUG,  # Cambiado a DEBUG para mayor detalle
    format='%(asctime)s %(levelname)s:%(message)s'
)

def fetch_stock_data(ticker):
    """
    Obtiene los datos de stock para el ticker especificado usando yfinance.

    :param ticker: Símbolo de la acción (por ejemplo, 'TSLA')
    :return: Diccionario con los datos de la acción o None si hay un error
    """
    try:
        stock = yf.Ticker(ticker)
        # Obtener datos históricos recientes (últimos 2 días) para mayor precisión
        data = stock.history(period='2d', interval='1m')
        logging.debug(f"Datos obtenidos para {ticker}:\n{data}")

        if data.empty:
            logging.warning(f"No se encontraron datos para el ticker {ticker}. Puede que el mercado esté cerrado.")
            return None

        if 'Close' not in data.columns:
            logging.error(f"Columna 'Close' no encontrada en los datos de {ticker}.")
            return None

        # Obtener el último dato válido
        latest = data.dropna().tail(1)
        if latest.empty:
            logging.warning(f"No hay datos válidos para el ticker {ticker}.")
            return None

        price = latest['Close'].values[0]
        timestamp = latest.index[0].to_pydatetime()
        logging.debug(f"Precio: {price}, Hora: {timestamp}")

        return {
            "ticker": ticker,
            "price": price,
            "time": timestamp.isoformat()  # Formato ISO para consistencia
        }
    except Exception as e:
        logging.error(f"Error obteniendo datos de stock: {e}")
        return None

def analyze_sentiment(text):
    """
    Analiza el sentimiento de un texto utilizando VADER.

    :param text: Texto a analizar
    :return: Diccionario con las puntuaciones de sentimiento
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(text)
        logging.debug(f"Texto analizado para sentimiento: '{text}' | Resultado: {sentiment}")
        return sentiment
    except Exception as e:
        logging.error(f"Error analizando sentimiento: {e}")
        return {"neg": 0, "neu": 1, "pos": 0, "compound": 0}

def ensure_csv_exists(filename):
    """
    Asegura que el archivo CSV existe y contiene el encabezado adecuado.

    :param filename: Ruta al archivo CSV
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not os.path.isfile(filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["ticker", "price", "time", "neg", "neu", "pos", "compound"])
                writer.writeheader()
                logging.info(f"Archivo CSV creado con encabezados: {filename}")
        else:
            logging.debug(f"Archivo CSV ya existe: {filename}")
    except Exception as e:
        logging.error(f"Error asegurando la existencia del archivo CSV: {e}")

def save_to_csv(data, filename):
    """
    Guarda un diccionario de datos en un archivo CSV.

    :param data: Diccionario con los datos a guardar
    :param filename: Ruta al archivo CSV
    """
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["ticker", "price", "time", "neg", "neu", "pos", "compound"])
            writer.writerow(data)
            logging.info(f"Datos guardados en CSV: {data}")
    except Exception as e:
        logging.error(f"Error escribiendo en el archivo CSV: {e}")

def main():
    ticker = "TSLA"
    csv_file = os.getenv('CSV_FILE', '/volume1/docker/logs/stock_data.csv')

    ensure_csv_exists(csv_file)

    stock_data = fetch_stock_data(ticker)
    if stock_data:
        logging.info(f"Stock: {stock_data['ticker']}, Price: {stock_data['price']}, Time: {stock_data['time']}")

        # Generar texto para análisis de sentimiento
        sentiment_text = f"El precio de la acción de {stock_data['ticker']} es {stock_data['price']} dólares."
        sentiment = analyze_sentiment(sentiment_text)
        logging.info(f"Análisis de Sentimiento: {sentiment}")

        # Actualizar los datos de stock con el análisis de sentimiento
        stock_data.update(sentiment)

        # Guardar los datos en el CSV
        save_to_csv(stock_data, csv_file)
    else:
        logging.warning("No se pudieron obtener los datos de stock.")

if __name__ == "__main__":
    main()

