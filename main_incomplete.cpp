#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>


// Workshop Part 1
// Configure the Wi-Fi connection


// TODO 1
// Fill in the Wi-Fi network name
const char* ssid = "________________";


// TODO 2
// Fill in the Wi-Fi password
const char* password = "________________";


// TODO 3
// This must match DEVICE_SECRET in the Python program
const char* AUTH_TOKEN = "________________";



// Workshop Part 2
// Configure the hardware


// TODO 4
// Fill in the GPIO pin connected to the LED
const int LED_PIN = ;


// TODO 5
// Fill in the HTTP server port
WebServer server(________________);



// Workshop Part 3
// Create the LED control endpoint


void handleLedControl() {


  // TODO 6
  // Check whether the request contains the authentication header

  if (!server.hasHeader("________________") ||
      server.header("________________") != AUTH_TOKEN) {

    server.send(
      401,
      "application/json",
      "{\"error\":\"Unauthorized: Invalid Token\"}"
    );

    return;
  }



  // Workshop Part 4
  // Read JSON sent from the Python agent


  StaticJsonDocument<200> doc;


  // TODO 7
  // Convert the HTTP request body from JSON into Arduino data

  DeserializationError err =
    ________________(doc, server.arg("plain"));


  if (err) {

    server.send(
      400,
      "application/json",
      "{\"error\":\"Invalid JSON\"}"
    );

    return;
  }



  // Workshop Part 5
  // Read the commands from the JSON


  // TODO 8
  // Read the state field

  String state =
    doc["________________"] | "off";


  // TODO 9
  // Read the duration field

  int duration =
    doc["________________"] | 0;



  // Workshop Part 6
  // Control the LED


  // TODO 10
  // Check whether Gemini requested the LED to turn on

  if (state == "________________") {


    // TODO 11
    // Turn the GPIO pin on

    digitalWrite(
      LED_PIN,
      ________________
    );



    // Workshop Part 7
    // Pulse the LED if a duration was provided


    if (duration > 0) {


      // TODO 12
      // Limit the maximum pulse duration to 5000 milliseconds

      if (duration > ________________) {

        duration = ________________;
      }



      // TODO 13
      // Keep the LED on for the requested time

      ________________(duration);



      // TODO 14
      // Turn the LED off after the pulse

      digitalWrite(
        LED_PIN,
        ________________
      );



      server.send(
        200,
        "application/json",

        "{\"status\":\"pulsed\",\"duration_ms\":" +
        String(duration) +
        "}"
      );


      return;
    }



    // Workshop Part 8
    // Keep the LED on if duration is zero


    server.send(
      200,
      "application/json",
      "{\"status\":\"turned_on\"}"
    );

  }

  else {


    // TODO 15
    // Turn the LED off

    digitalWrite(
      LED_PIN,
      ________________
    );


    server.send(
      200,
      "application/json",
      "{\"status\":\"turned_off\"}"
    );
  }
}



// Workshop Part 9
// Create the ESP32 status endpoint


void handleStatus() {


  // TODO 16
  // Return the ESP32 status and uptime

  server.send(

    ________________,

    "application/json",

    "{\"device\":\"ESP32\","
    "\"state\":\"ready\","
    "\"uptime_ms\":" +

    String(________________()) +

    "}"
  );
}



// Workshop Part 10
// Configure the ESP32 when it starts


void setup() {


  // TODO 17
  // Start the Serial Monitor

  Serial.begin(________________);



  // TODO 18
  // Configure the LED pin as an output

  pinMode(
    LED_PIN,
    ________________
  );



  // TODO 19
  // Start with the LED turned off

  digitalWrite(
    LED_PIN,
    ________________
  );



  // Workshop Part 11
  // Connect the ESP32 to Wi-Fi


  // TODO 20
  // Start the Wi-Fi connection

WiFi.________________(
    ssid,
    password
);


Serial.print(
    "Connecting to Wi-Fi"
);



  // TODO 21
  // Wait until the ESP32 connects to Wi-Fi

  while (
    WiFi.status() != ________________
  ) {

    delay(500);

    Serial.print(".");
  }



  Serial.println(
    "\nConnected!"
  );


  Serial.println(
    "ESP32 IP Address: " +
    WiFi.localIP().toString()
  );



  // Workshop Part 12
  // Create the HTTP routes


  // TODO 22
  // Register the LED control route

  server.on(
    "/________________",
    HTTP_POST,
    ________________
  );



  // TODO 23
  // Register the status route

  server.on(
    "/________________",
    HTTP_GET,
    ________________
  );



  // Workshop Part 13
  // Tell the ESP32 to collect the authentication header


  const char* headerKeys[] = {
    "________________"
  };


  server.collectHeaders(
    headerKeys,
    1
  );



  // TODO 24
  // Start the web server

  server.________________();


  Serial.println(
    "ESP32 HTTP server started"
  );
}



// Workshop Part 14
// Continuously process HTTP requests


void loop() {


  // TODO 25
  // Check whether the ESP32 received a new web request

  server.________________();
}