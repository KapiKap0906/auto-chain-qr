import cv2
import pyzbar.pyzbar as pyzbar
import sqlite3
from datetime import datetime
import time
import threading
from main import update_database, stackable_update_database

#________________________________________________________________________________
#   This code takes inputs from mutiple cameras and scans
#   Use this one
#________________________________________________________________________________

def is_stackable(product_id):
    """Determines if a product is stackable based on its product ID."""
    return product_id.startswith('C')

def handle_scan(product_id, station_number):
    """Handles the database update based on whether the product is stackable or not."""
    if is_stackable(product_id):
        # Prompt user to input the number of sacks for stackable items
        try:
            bags_in_stack = int(input(f"Enter the number of sacks in the stack for product {product_id}: "))
            stackable_update_database(product_id, station_number, bags_in_stack)
        except ValueError:
            print("Invalid input. Please enter an integer for the number of sacks.")
    else:
        update_database(product_id, station_number)

# Define each scanner function for respective stations
def Scanner1(img):
    STATION_NUMBER = "1"
    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

    time.sleep(2)

def Scanner2(img):
    STATION_NUMBER = "2"
    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

    time.sleep(2)

def Scanner3(img):
    STATION_NUMBER = "3"
    decoded_id = pyzbar.decode(img)

    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

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

    cv2.destr