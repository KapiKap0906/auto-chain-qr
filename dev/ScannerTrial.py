import cv2
import pyzbar.pyzbar as pyzbar
import time

#________________________________________________________________________________
#   This code scans multiple QRs from 1 camera input
#________________________________________________________________________________
def Scanner(img):
    STATION_NUMBER = "1"

    decoded_id = pyzbar.decode(img)

    # print(decoded_id[0].data.decode())

    # For multiple QRs in a single image

    for code in decoded_id:
        print(code.data.decode(), STATION_NUMBER)

    time.sleep(2)


# img = cv2.imread('QR Codes/multi_image_3.png')

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    Scanner(frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
