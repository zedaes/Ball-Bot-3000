from flask import Flask, render_template, Response, jsonify
import cv2
import time

app = Flask(__name__)

# Dummy data for demonstration
robot_stats = {
    'uptime': 0,
    'num_operations': 0,
    'robot_position': [0, 0]
}

# OpenCV VideoCapture for camera feeds
camera1 = cv2.VideoCapture(0)  # Replace with your camera source
camera2 = cv2.VideoCapture(1)  # Replace with your second camera source

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generate_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream2')
def stream2():
    return Response(generate_frames(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    # Simulate updating the stats
    robot_stats['uptime'] += 1
    robot_stats['num_operations'] += 1
    return jsonify(robot_stats)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Logic to shut down the robot
    return 'Robot is shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
