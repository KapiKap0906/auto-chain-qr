import cv2
import pyzbar.pyzbar as pyzbar

img = cv2.imread('QR Codes\image4.png')
decoded_id = pyzbar.decode(img)

print(decoded_id[0].data.decode())