import cv2
import pyzbar.pyzbar as pyzbar
from main import handle_scan
import time

# Define each scanner function for respective stations
def Scanner1(img):
    STATION_NUMBER = "1"
    decoded_id = pyzbar.decode(img)
    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

def Scanner2(img):
    STATION_NUMBER = "2"
    decoded_id = pyzbar.decode(img)
    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

def Scanner3(img):
    STATION_NUMBER = "3"
    decoded_id = pyzbar.decode(img)
    for code in decoded_id:
        product_id = code.data.decode()
        handle_scan(product_id, STATION_NUMBER)

# Updated indices based on the index verification step
cap1 = cv2.VideoCapture(0)  # Laptop webcam or external camera
cap2 = cv2.VideoCapture(1)  # First USB camera
cap3 = cv2.VideoCapture(2)  # Second USB camera

# Set lower resolution and frame rate to reduce USB bandwidth usage
for cap in [cap1, cap2, cap3]:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Check if cameras are opened successfully
if not (cap1.isOpened() and cap2.isOpened() and cap3.isOpened()):
    print("Error: Could not open one or more of the cameras.")
    cap1.release()
    cap2.release()
    cap3.release()
    exit()

# Main loop for capturing frames and running scanners
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    if ret1:
        Scanner1(frame1)
        cv2.imshow("Camera 1 - Laptop Webcam", frame1)
    else:
        print("Failed to read from Camera 1")

    if ret2:
        Scanner2(frame2)
        cv2.imshow("Camera 2 - USB Webcam 1", frame2)
    else:
        print("Failed to read from Camera 2")

    if ret3:
        Scanner3(frame3)
        cv2.imshow("Camera 3 - USB Webcam 2", frame3)
    else:
        print("Failed to read from Camera 3")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()
