import cv2
import pyzbar.pyzbar as pyzbar
import time

#________________________________________________________________________________
#   This code takes inputs from mutiple cameras and scans
#   Use this one
#________________________________________________________________________________

import cv2
import threading
from main import update_database

def Scanner1(img):
    STATION_NUMBER = "1"

    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)
    
    time.sleep(2)

def Scanner2(img):
    STATION_NUMBER = "2"

    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)

    time.sleep(2)


def Scanner3(img):
    STATION_NUMBER = "3"

    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)

    time.sleep(2)


# Function to capture frames from each camera and pass to its Scanner function
def capture_camera(cam_index, scanner_function):
    cap = cv2.VideoCapture(cam_index)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {cam_index}")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to grab frame from camera {cam_index}")
            break
        
        # Process the frame with the corresponding Scanner function
        scanner_function(frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=capture_camera, args=(0, Scanner1)),  # Laptop webcam
        threading.Thread(target=capture_camera, args=(1, Scanner2)),  # First USB webcam
        threading.Thread(target=capture_camera, args=(2, Scanner3))   # Second USB webcam
    ]
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    cv2.destroyAllWindows()
