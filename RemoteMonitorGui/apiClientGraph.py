import requests
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv

# Configurazione API
API_URL = "http://192.168.0.126/api/sensor"
POLLING_INTERVAL = 5  # secondi tra una richiesta e l'altra
CSV_FILE = "sensor_data.csv"

# Liste per memorizzare i dati
timestamps = []
temperatures = []
humidities = []

# Creazione e inizializzazione file CSV
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Temperatura (°C)", "Umidità (%)"])

print("Inizio lettura dati dal sensore...")

try:
    while True:
        # Richiesta dati al server API
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if temperature is not None and humidity is not None:
                print(f"{current_time} - Temperatura: {temperature}°C, Umidità: {humidity}%")

                # Memorizzazione dei dati
                timestamps.append(current_time)
                temperatures.append(temperature)
                humidities.append(humidity)

                # Salvataggio su CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, temperature, humidity])

                # Aggiornamento grafico
                plt.clf()
                plt.plot(timestamps, temperatures, label='Temperatura (°C)', color='orange')
                plt.plot(timestamps, humidities, label='Umidità (%)', color='blue')
                plt.xlabel('Tempo')
                plt.ylabel('Valori')
                plt.title('Lettura Sensore DHT11')
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.pause(0.1)

        except (requests.RequestException, ValueError) as e:
            print(f"Errore nella lettura dei dati: {e}")

        time.sleep(POLLING_INTERVAL)

except KeyboardInterrupt:
    print("Programma interrotto dall'utente.")
    plt.show()
