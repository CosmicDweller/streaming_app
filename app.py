from flask import Flask, Response, render_template, request, redirect, session, url_for
import cv2
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

PASSWORD = os.getenv('PASSWORD')
SERVER = 'https://d254a7b0dc4113e0.p21.rt3.io/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(PASSWORD)
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['authenticated'] = False
    return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if request.method == 'POST':
        SERVER = request.form.get('server')
        return redirect(url_for('index'))
    return render_template('index.html')


def generate_frames():
    cap = cv2.VideoCapture(SERVER)
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


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
