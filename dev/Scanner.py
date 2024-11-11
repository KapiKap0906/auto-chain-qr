import cv2
import pyzbar.pyzbar as pyzbar
from main import update_database, dispose_product

def Scanner1(img):
    STATION_NUMBER = "1"

    decoded_id = pyzbar.decode(img)

    # print(decoded_id[0].data.decode())

    # For multiple QRs in a single image

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)

def Scanner2(img):
    STATION_NUMBER = "2"

    decoded_id = pyzbar.decode(img)

    # print(decoded_id[0].data.decode())

    # For multiple QRs in a single image

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)
    
def Scanner3(img):
    STATION_NUMBER = "3"

    decoded_id = pyzbar.decode(img)

    # print(decoded_id[0].data.decode())

    # For multiple QRs in a single image

    for code in decoded_id:
        update_database(code.data.decode(), STATION_NUMBER)

def DisposalScanner(img):

    decoded_id = pyzbar.decode(img)

    # print(decoded_id[0].data.decode())

    # For multiple QRs in a single image

    for code in decoded_id:
        dispose_product(code.data.decode())