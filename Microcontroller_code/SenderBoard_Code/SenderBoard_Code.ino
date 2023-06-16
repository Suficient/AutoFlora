#include <esp_now.h>
#include <WiFi.h>
#include <DHT.h>


#define DHTPIN 23 //change this to the right one, faizan.
#define DHTTYPE 11
#define soilPin 34// this one too

DHT dht(DHTPIN, DHTTYPE);

int humidity;
int temperature;
int soilMoisture;

// REPLACE WITH THE RECEIVER'S MAC Address
uint8_t broadcastAddress[] = {0xCC, 0xDB, 0xA7, 0x16, 0x98, 0xC8};

// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
    int id; // must be unique for each sender board
    int humidity;
    int temperature;
    int soilmoisture;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// Create peer interface
esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);

  dht.begin(); //init DHT sensor

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  pinMode(soilPin, INPUT);  

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}
 
void loop() {
  //loop triggers every 5 seconds
  delay(5000);

  // read soil moisture from capacitive sensor
  soilMoisture = map(analogRead(soilPin), 0, 200, 0, 100);
  // soilMoisture = analogRead(soilPin);
      
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  Serial.print("humidity:");
  Serial.println(humidity);
  Serial.print("temperature:");
  Serial.println(temperature);
  Serial.print("soilMoisture:");
  Serial.println(soilMoisture);

  // Set values to send
  myData.id = 1;
  myData.humidity = humidity;
  myData.temperature = temperature;
  myData.soilmoisture = soilMoisture;

  // Check if DHT reads failed
  if (isnan(myData.humidity) || isnan(myData.temperature)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  //Check if soil moisture reads failed
  if (isnan(myData.soilmoisture)) {
    Serial.println("Failed to read from Soil Moisture sensor");
    return;
  }

  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(10000);
}
