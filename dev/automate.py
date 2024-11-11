import time
import cv2
from dev.Scanner import Scanner1, Scanner2, Scanner3, DisposalScanner

img = cv2.imread('QR Codes\image5.png')

Scanner1(img)

time.sleep(10)

Scanner2(img)

time.sleep(10)

Scanner3(img)

time.sleep(10)

DisposalScanner(img)