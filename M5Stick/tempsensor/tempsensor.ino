#include <M5StickCPlus.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include "DHT.h"
#define DHTTYPE DHT22

// Credenziali Wi-Fi
const char* ssid = "***";
const char* password = "***";

const int DHT1PIN = 26;
const int DHT2PIN = 0; 

DHT dht1(DHT1PIN, DHTTYPE);
DHT dht2(DHT2PIN, DHTTYPE);

// Creazione server
AsyncWebServer server(80);

void setup(){
  M5.begin();
  M5.Lcd.setTextSize(2);
  M5.Lcd.setRotation(3);
  
  delay(2000);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setCursor(0, 15);

  Serial.begin(115200);

  // Connessione Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connessione a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  dht1.begin();
  dht2.begin();

  // Endpoint API per leggere i dati del sensore 1
  server.on("/api/sensors", HTTP_GET, [](AsyncWebServerRequest *request) {
    float temperature1 = dht1.readTemperature();
    float humidity1 = dht1.readHumidity();
    float temperature2 = dht2.readTemperature();
    float humidity2 = dht2.readHumidity();

    // Controlla errori di lettura
    if (isnan(temperature1) || isnan(humidity1) || isnan(temperature2) || isnan(humidity2)) {
      request->send(500, "application/json", "{\"error\":\"Errore nella lettura dei sensori\"}");
      return;
    }

    String jsonResponse = "{";
    jsonResponse += "\"sensor1\": {\"temperature\": " + String(temperature1) + ", \"humidity\": " + String(humidity1) + "}, ";
    jsonResponse += "\"sensor2\": {\"temperature\": " + String(temperature2) + ", \"humidity\": " + String(humidity2) + "}";
    jsonResponse += "}";

    request->send(200, "application/json", jsonResponse);
  });

  // Endpoint API per leggere i dati del sensore 2
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    float temperature1 = dht1.readTemperature();
    float humidity1 = dht1.readHumidity();
    float temperature2 = dht2.readTemperature();
    float humidity2 = dht2.readHumidity();

    String htmlPage = "<!DOCTYPE html><html><head><title>DHT22 Sensor Data</title></head><body>";
    htmlPage += "<h1>Dati dei Sensori DHT22</h1>";

    if (isnan(temperature1) || isnan(humidity1) || isnan(temperature2) || isnan(humidity2)) {
      htmlPage += "<p>Errore nella lettura dei sensori.</p>";
    } else {
      htmlPage += "<h2>Sensor 1</h2>";
      htmlPage += "<p>Temperatura: " + String(temperature1) + " &deg;C</p>";
      htmlPage += "<p>Umidità: " + String(humidity1) + " %</p>";
      htmlPage += "<h2>Sensor 2</h2>";
      htmlPage += "<p>Temperatura: " + String(temperature2) + " &deg;C</p>";
      htmlPage += "<p>Umidità: " + String(humidity2) + " %</p>";
    }

    htmlPage += "</body></html>";
    request->send(200, "text/html", htmlPage);
  });

  // Avvia il server
  server.begin();
}


void loop() {

   // Wait a few seconds between measurements.
   delay(2000);
   M5.Lcd.fillScreen(BLACK);
   M5.Lcd.setCursor(0, 15);

   M5.Lcd.print(F("IP: "));
   M5.Lcd.println(WiFi.localIP());
   M5.Lcd.println();

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float humidity1 = dht1.readHumidity();
  // Read temperature as Celsius (the default)
  float temperature1 = dht1.readTemperature();

  float humidity2 = dht2.readHumidity();
  // Read temperature as Celsius (the default)
  float temperature2 = dht2.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity1) || isnan(temperature1)) {
    M5.Lcd.println(F("Failed to read from DHT sensor 1!"));
    return;
  }

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity2) || isnan(temperature2)) {
    M5.Lcd.println(F("Failed to read from DHT sensor 2!"));
    return;
  }
  // Compute heat index in Celsius (isFahreheit = false)
  float heatIndex = dht1.computeHeatIndex(temperature1, humidity1, false);

  M5.Lcd.print(F(" T1 "));
  M5.Lcd.print(temperature1);
  M5.Lcd.print(F(" % "));
  M5.Lcd.println(humidity1);

  M5.Lcd.print(F(" T2 "));
  M5.Lcd.print(temperature2);
  M5.Lcd.print(F(" % "));
  M5.Lcd.println(humidity2);
}
