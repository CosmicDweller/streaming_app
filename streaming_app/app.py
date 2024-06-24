from flask import Flask, Response, render_template, request, jsonify
import cv2
from pydub import AudioSegment
from pydub.playback import play
import io

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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio part in the request'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the audio file into memory
        audio_data = audio_file.read()
        audio = AudioSegment.from_file(io.BytesIO(audio_data))
        
        # Play the audio using pydub
        play(audio)
        
        return jsonify({'message': 'File played successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
