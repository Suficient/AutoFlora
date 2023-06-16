### Automated Farming project for RV hackathon
## AutoFlora 
#This project Automates farming in a large scale through soil moisture/content monitoring and environment variable sensing.A mesh network is set up between any number of nodes deployed on farmland. Each Node consists of sensors, an ESP32Cam, an ESP32 microcontroller and solar panels/Battery.

#Sensor Data Collection and Processing
Each node collects sensor data and sends it to the reciever board through the ESPNow communication protocol. This data is stored in sensor_data.csv through the 
serialdatalogger.py script which can be accessed and displayed in a user readable manner through the heatmap.py script. 

#
