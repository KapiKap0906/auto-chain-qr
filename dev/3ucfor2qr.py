import cv2
import time
import sqlite3
from datetime import datetime

# Initialize video capture objects for the external, internal, and third webcams
external_cam_index = 1  # Change to 0 if the external webcam is the primary
internal_cam_index = 2   # Assuming the internal webcam is indexed as 2
third_cam_index = 3      # Assuming the third camera is indexed as 3
cap_external = cv2.VideoCapture(external_cam_index)
cap_internal = cv2.VideoCapture(internal_cam_index)
cap_third = cv2.VideoCapture(third_cam_index)

# Create a QRCodeDetector object
detector = cv2.QRCodeDetector()

# Variables to track scanned codes
scanned_codes = {}

# Time buffer in seconds
buffer_time = 5

# Connect to the SQLite database
conn = sqlite3.connect('qr_code_scanner.db')
cursor = conn.cursor()

def insert_scan_data(product_id, station_number, in_time, out_time, live):
    cursor.execute('''
    INSERT INTO qr_codes (product_id, station_number, in_time, out_time, live)
    VALUES (?, ?, ?, ?, ?)
    ''', (product_id, station_number, in_time, out_time, live))
    conn.commit()

while True:
    # Capture frames from all three cameras
    ret_external, frame_external = cap_external.read()
    ret_internal, frame_internal = cap_internal.read()
    ret_third, frame_third = cap_third.read()

    # Check if the external camera successfully captured a frame
    if ret_external:
        data_external, bbox_external, _ = detector.detectAndDecode(frame_external)

        if data_external:
            # Ensure the data matches expected QR code names exactly
            if data_external not in scanned_codes:
                scanned_codes[data_external] = {'count': 0, 'station_number': '1'}

            current_time = time.time()
            if scanned_codes[data_external]['count'] < 2:
                last_capture_time = scanned_codes[data_external].get('last_capture_time', 0)
                if current_time - last_capture_time >= buffer_time:
                    scanned_codes[data_external]['count'] += 1
                    scanned_codes[data_external]['last_capture_time'] = current_time

                    if scanned_codes[data_external]['count'] == 1:
                        in_time = datetime.now()
                        scanned_codes[data_external]['in_time'] = in_time
                        insert_scan_data(data_external, "1", in_time, None, True)
                        print(f"QR Code data from External Webcam (1): {data_external}, in_time recorded at {in_time}")
                    elif scanned_codes[data_external]['count'] == 2:
                        out_time = datetime.now()
                        scanned_codes[data_external]['out_time'] = out_time
                        insert_scan_data(data_external, "1", scanned_codes[data_external]['in_time'], out_time, False)
                        print(f"QR Code data from External Webcam (1): {data_external}, out_time recorded at {out_time}")

                    # Save the captured frame as an image
                    cv2.imwrite(f"captured_qr_code_external_{data_external}.png", frame_external)

        # Show the external camera feed in a window
        cv2.imshow("External Webcam (1)", frame_external)

    # Check if the internal camera successfully captured a frame
    if ret_internal:
        data_internal, bbox_internal, _ = detector.detectAndDecode(frame_internal)

        if data_internal:
            # Ensure the data matches expected QR code names exactly
            if data_internal not in scanned_codes:
                scanned_codes[data_internal] = {'count': 0, 'station_number': '2'}

            current_time = time.time()
            if scanned_codes[data_internal]['count'] < 2:
                last_capture_time = scanned_codes[data_internal].get('last_capture_time', 0)
                if current_time - last_capture_time >= buffer_time:
                    scanned_codes[data_internal]['count'] += 1
                    scanned_codes[data_internal]['last_capture_time'] = current_time

                    if scanned_codes[data_internal]['count'] == 1:
                        in_time = datetime.now()
                        scanned_codes[data_internal]['in_time'] = in_time
                        insert_scan_data(data_internal, "2", in_time, None, True)
                        print(f"QR Code data from Internal Webcam (2): {data_internal}, in_time recorded at {in_time}")
                    elif scanned_codes[data_internal]['count'] == 2:
                        out_time = datetime.now()
                        scanned_codes[data_internal]['out_time'] = out_time
                        insert_scan_data(data_internal, "2", scanned_codes[data_internal]['in_time'], out_time, False)
                        print(f"QR Code data from Internal Webcam (2): {data_internal}, out_time recorded at {out_time}")

                    # Save the captured frame as an image
                    cv2.imwrite(f"captured_qr_code_internal_{data_internal}.png", frame_internal)

        # Show the internal camera feed in a window
        cv2.imshow("Internal Webcam (2)", frame_internal)

    # Check if the third camera successfully captured a frame
    if ret_third:
        data_third, bbox_third, _ = detector.detectAndDecode(frame_third)

        if data_third:
            # Ensure the data matches expected QR code names exactly
            if data_third not in scanned_codes:
                scanned_codes[data_third] = {'count': 0, 'station_number': '3'}

            current_time = time.time()
            if scanned_codes[data_third]['count'] < 2:
                last_capture_time = scanned_codes[data_third].get('last_capture_time', 0)
                if current_time - last_capture_time >= buffer_time:
                    scanned_codes[data_third]['count'] += 1
                    scanned_codes[data_third]['last_capture_time'] = current_time

                    if scanned_codes[data_third]['count'] == 1:
                        in_time = datetime.now()
                        scanned_codes[data_third]['in_time'] = in_time
                        insert_scan_data(data_third, "3", in_time, None, True)
                        print(f"QR Code data from Third Webcam (3): {data_third}, in_time recorded at {in_time}")
                    elif scanned_codes[data_third]['count'] == 2:
                        out_time = datetime.now()
                        scanned_codes[data_third]['out_time'] = out_time
                        insert_scan_data(data_third, "3", scanned_codes[data_third]['in_time'], out_time, False)
                        print(f"QR Code data from Third Webcam (3): {data_third}, out_time recorded at {out_time}")

                    # Save the captured frame as an image
                    cv2.imwrite(f"captured_qr_code_third_{data_third}.png", frame_third)

        # Show the third camera feed in a window
        cv2.imshow("Third Webcam (3)", frame_third)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture objects and close all windows
cap_external.release()
cap_internal.release()
cap_third.release()
cv2.destroyAllWindows()

# Close the database connection
conn.close()
