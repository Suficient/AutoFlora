import cv2
import urllib.request
import numpy as np
import os
import time
from disease_predictor import predict_disease

#Size of the image for resizing
DEFAULT_IMAGE_SIZE = tuple((256, 256))

# IP address and port of the ESP32-CAM stream
esp32cam_ip = '192.168.10.203'
esp32cam_port = 80

# Folder to save the captured photos
save_folder = 'C:/Users/Faizan Tabassum/Desktop/GardenWatch/ESPphotos'

#healthy and unhealthy classes
healthy_classes = [3,4,6,10,14,15,17,19,22,23,24,27,33,36]


def capture_photo():
    # Read the stream from the ESP32-CAM
    stream_url = 'http://192.168.10.203'
    stream = urllib.request.urlopen(stream_url)
    byte_data = bytes()

    byte_data += stream.read(1024)
    a = byte_data.find(b'\xff\xd8')
    b = byte_data.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = byte_data[a:b + 2]
        byte_data = byte_data[b + 2:]
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, DEFAULT_IMAGE_SIZE)

        # Save the captured photo
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        photo_name = f'{save_folder}/photo_{timestamp}.jpg'
        cv2.imwrite(photo_name, frame)
        photo_class = predict_disease(photo_name)
        if photo_class in healthy_classes:
            photo_class = 'healthy'
        else:
            photo_class = 'unhealthy'
        new_photo_name = f'{save_folder}/NODE1_{photo_class}_{timestamp}.jpg'
        cv2.imwrite(new_photo_name, frame)
        print(f'Saved photo: {new_photo_name}')
        try:
            os.remove(photo_name)
        except:
            pass

# Start capturing photos
capture_photo()
