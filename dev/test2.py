import cv2

# Try the first 5 indices to see which cameras are accessible
for i in range(5):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        print(f"Camera {i} is available.")
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Camera {i}", frame)
            cv2.waitKey(2500)  # Display for 1 second
            cv2.destroyAllWindows()
        cap.release()
    else:
        print(f"Camera {i} is not available.")
