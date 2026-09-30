#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid = "Bill Lam";
const char* password = "12345678";
const char* AUTH_TOKEN = "workshop-secret-2026";

const int LED_PIN = 23;
WebServer server(80);

void handleLedControl() {
  if (!server.hasHeader("X-Device-Auth") || server.header("X-Device-Auth") != AUTH_TOKEN) {
    server.send(401, "application/json", "{\"error\":\"Unauthorized: Invalid Token\"}");
    return;
  }

  StaticJsonDocument<200> doc;
  DeserializationError err = deserializeJson(doc, server.arg("plain"));
  if (err) {
    server.send(400, "application/json", "{\"error\":\"Invalid JSON\"}");
    return;
  }

  String state = doc["state"] | "off";
  int duration = doc["duration_ms"] | 0;

  if (state == "on") {
    digitalWrite(LED_PIN, HIGH);
    if (duration > 0) {
      if (duration > 5000) duration = 5000; // 5s hardware safety ceiling
      delay(duration);
      digitalWrite(LED_PIN, LOW);
      server.send(200, "application/json", "{\"status\":\"pulsed\",\"duration_ms\":" + String(duration) + "}");
      return;
    }
    server.send(200, "application/json", "{\"status\":\"turned_on\"}");
  } else {
    digitalWrite(LED_PIN, LOW);
    server.send(200, "application/json", "{\"status\":\"turned_off\"}");
  }
}

void handleStatus() {
  server.send(200, "application/json", "{\"device\":\"ESP32\",\"state\":\"ready\",\"uptime_ms\":" + String(millis()) + "}");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW); // Fail-safe default

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP Address: " + WiFi.localIP().toString());

  server.on("/led", HTTP_POST, handleLedControl);
  server.on("/status", HTTP_GET, handleStatus);

  const char* headerKeys[] = {"X-Device-Auth"};
  server.collectHeaders(headerKeys, 1);

  server.begin();
}

void loop() {
  server.handleClient();
}
