import cv2

cap = cv2.VideoCapture('http://192.168.0.158:8081')

if not cap.isOpened():
    print("Error: Could not open video stream")
else:
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame")
            break
        else:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()