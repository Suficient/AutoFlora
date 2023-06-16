# Automated Farming project for RV hackathon
## AutoFlora 
This project Automates farming in a large scale through soil moisture/content monitoring and environment variable sensing.A mesh network is set up between any number of nodes deployed on farmland. Each Node consists of sensors, an ESP32Cam, an ESP32 microcontroller and solar panels/Battery.

## Sensor Data Collection and Processing
Each node collects sensor data and sends it to the reciever board through the ESPNow communication protocol. This data is stored in sensor_data.csv through the 
serialdatalogger.py script which can be accessed and displayed in a user readable manner through the heatmap.py script. 

## Collection of images and accessing live security cam feed
The ESPCam used in each node doubles as both a means to collect plant leaf images for disease detection, and a security camera for remote surveillance. 
This camera hosts the collected video feed on a local HTTP Server, from which images are taken once every day and stored in the local database[espcamphotosaver.py]. this can also be accessed live from anywhere within the area by simply inputting the IP address of the stream.

## Disease Detection through an Image Classification Model
Disease detection is carried out through a 2D COnvolutional Neural Network model trained on the PlantVillage Dataset. The model has been trained on 7,576 images of leaves spanning 38 classes, and has a real life tested accuracy of 92%. Images, when captured, are passed through this model and then labelled according to the result. This allows the farmer to asses farm health remotely with minimal effort.


