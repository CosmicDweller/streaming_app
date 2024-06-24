from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def generate_frames():
    cap = cv2.VideoCapture('http://192.168.0.158:8081')
    if not cap.isOpened():
        print("Error: could not open video stream!")
        return
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: could not read frame")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)