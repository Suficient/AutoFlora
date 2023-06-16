#include <esp_now.h>
#include <WiFi.h>

// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
  int id;
  int humidity;
  int temperature;
  int soilmoisture;
}struct_message;


int soilMoistureRelayPin = 23;  // soil moisture relay pin
int sm;

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the readings from each board
struct_message board1;
struct_message board2;
struct_message board3;

// Create an array with all the structures
struct_message boardsStruct[3] = {board1, board2, board3};

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.printf("Board ID: %u\n", myData.id);
  // Update the structures with the new incoming data
  boardsStruct[myData.id-1].humidity = myData.humidity;
  boardsStruct[myData.id-1].temperature = myData.temperature;
  boardsStruct[myData.id-1].soilmoisture = myData.soilmoisture;
  Serial.printf("Humidity value: %d \n", boardsStruct[myData.id-1].humidity);
  Serial.printf("Temperature value: %d \n", boardsStruct[myData.id-1].temperature);
  Serial.printf("Soil Moisture value: %d \n", boardsStruct[myData.id-1].soilmoisture); 
  Serial.println();
}
 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);
  
  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  pinMode(soilMoistureRelayPin, OUTPUT); 

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(OnDataRecv);

  //int HumidityValue = boardsStruct[0].humidity
  // ^ do this to access a value from something. change index accordingly
}
 
void loop() {
  // Acess the variables for each board
  int sm1 = boardsStruct[0].soilmoisture;
  int sm2 = boardsStruct[1].soilmoisture;
  sm = (sm1 + sm2)/2;


  if (sm <= 60) {
      if (sm <= 70) {
        digitalWrite(soilMoistureRelayPin, HIGH);
      } else {
        digitalWrite(soilMoistureRelayPin, LOW);
      }
    } else {
      digitalWrite(soilMoistureRelayPin, LOW);
    }


  delay(1000);  
}
