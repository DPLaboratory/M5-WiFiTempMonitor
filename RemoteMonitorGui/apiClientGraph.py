import requests
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv

# Configurazione API
API_URL_SENSOR1 = "http://192.168.1.42/api/sensor1"
API_URL_SENSOR2 = "http://192.168.1.42/api/sensor2"
POLLING_INTERVAL = 5  # secondi tra una richiesta e l'altra
CSV_FILE = "sensor_data.csv"

# Liste per memorizzare i dati
timestamps = []
temperatures_sensor1 = []
temperatures_sensor2 = []
humidities_sensor1 = []
humidities_sensor2 = []

# Creazione e inizializzazione file CSV
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Temperatura Sensor1 (°C)", "Umidità Sensor1 (%)", "Temperatura Sensor2 (°C)", "Umidità Sensor2 (%)"])

print("Inizio lettura dati dai sensori...")

try:
    while True:
        # Richiesta dati al server API per entrambi i sensori
        try:
            response1 = requests.get(API_URL_SENSOR1)
            response2 = requests.get(API_URL_SENSOR2)
            response1.raise_for_status()
            response2.raise_for_status()
            data1 = response1.json()
            data2 = response2.json()

            temperature1 = data1.get("temperature")
            humidity1 = data1.get("humidity")
            temperature2 = data2.get("temperature")
            humidity2 = data2.get("humidity")
            current_time = datetime.now().strftime("%H:%M:%S")

            if temperature1 is not None and temperature2 is not None and humidity1 is not None and humidity2 is not None:
                print(f"{current_time} - Sensor1: {temperature1}°C, {humidity1}%, Sensor2: {temperature2}°C, {humidity2}%")

                # Memorizzazione dei dati
                timestamps.append(current_time)
                temperatures_sensor1.append(temperature1)
                humidities_sensor1.append(humidity1)
                temperatures_sensor2.append(temperature2)
                humidities_sensor2.append(humidity2)

                # Salvataggio su CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, temperature1, humidity1, temperature2, humidity2])

                # Aggiornamento grafico
                plt.clf()
                plt.plot(timestamps, temperatures_sensor1, label='Temperatura Sensor1 (°C)', color='orange')
                plt.plot(timestamps, humidities_sensor1, label='Umidità Sensor1 (%)', color='blue', linestyle='dotted')
                plt.plot(timestamps, temperatures_sensor2, label='Temperatura Sensor2 (°C)', color='green')
                plt.plot(timestamps, humidities_sensor2, label='Umidità Sensor2 (%)', color='purple', linestyle='dotted')
                plt.xlabel('Tempo')
                plt.ylabel('Valori')
                plt.title('Lettura Sensori DHT22')
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

