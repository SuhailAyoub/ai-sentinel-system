from flask import Flask, render_template,  Response
from flask import session, request, redirect
from flask import jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from fer import FER
from flask import jsonify
from database import db
import os
import cv2
import random
import sounddevice as sd
import numpy as np
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# ---------- DATABASE TABLE ----------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

app.secret_key = "secret123"

google_bp = make_google_blueprint(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_to="google_login"
)

app.register_blueprint(google_bp, url_prefix="/login")

import sqlite3
template_folder="templates",
static_folder='static'


camera = cv2.VideoCapture(0)
detector = FER(mtcnn=True)

current_emotion = "Neutral"



# =========================
# VIDEO STREAM FUNCTION
# =========================

from deepface import DeepFace

def generate_frames():

    global current_emotion

    while True:

        success, frame = camera.read()

        if not success:
            break

        try:

            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )

            current_emotion = result[0]['dominant_emotion']

            cv2.putText(
                frame,
                current_emotion,
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

        except:
            pass

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n')
        

def detect_sound():

    duration = 1
    fs = 44100

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    volume = np.linalg.norm(recording) * 10

    if volume > 80:
        return "Aggressive Noise", int(volume)

    elif volume > 40:
        return "Moderate Noise", int(volume)

    else:
        return "Low Noise", int(volume)



  
# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        print(email)
        print(password)

        return redirect('/')

    return render_template('login.html')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return "Passwords do not match"

        users.insert_one({
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "password": password
        })

        return redirect('/login')

    return render_template('signup.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



# ---------------- ALERTS ----------------
@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

# ---------------- REPORTS ----------------
@app.route('/reports')
def reports():
    return render_template('reports.html')

# ---------------- SETTINGS ----------------
@app.route('/settings')
def settings():
    return render_template('setting.html')

# ---------------- SAVE SETTINGS ----------------
settings_data = {}

@app.route('/save_settings', methods=['POST'])
def save_settings():

    two_factor = bool(request.form.get('two_factor'))
    login_monitoring = bool(request.form.get('login_monitoring'))
    email_alerts = bool(request.form.get('email_alerts'))
    auto_logout = bool(request.form.get('auto_logout'))
    device_verification =bool(request.form.get('device_verification'))

    settings_data['two_factor'] = two_factor
    settings_data['login_monitoring'] = login_monitoring
    settings_data['email_alerts'] = email_alerts
    settings_data['auto_logout'] = auto_logout
    settings_data['device_verification'] = device_verification

    admin_name = request.form.get('admin_name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        return 'Passwords do not match'

    settings_data['admin_name'] = admin_name
    settings_data['email'] = email
    settings_data['phone'] = phone
    settings_data['password'] = new_password

    settings_data['two_factor'] = bool(request.form.get('two_factor'))
    settings_data['login_monitoring'] = bool(request.form.get('login_monitoring'))
    settings_data['email_alerts'] = bool(request.form.get('email_alerts'))
    settings_data['auto_logout'] = bool(request.form.get('auto_logout'))
    settings_data['device_verification'] = bool(request.form.get('device_verification'))
    detection_sensitivity = request.form.get('detection_sensitivity')
    camera_source = request.form.get('camera_source')

    real_time_detection = bool(request.form.get('real_time_detection'))
    alert_notifications = bool(request.form.get('alert_notifications'))
    dark_mode = bool(request.form.get('dark_mode'))
    settings_data['detection_sensitivity'] = detection_sensitivity
    settings_data['camera_source'] = camera_source
    
    settings_data['real_time_detection'] = real_time_detection
    settings_data['alert_notifications'] = alert_notifications
    settings_data['dark_mode'] = dark_mode
    
    print(settings_data)

    return redirect('/settings')

# ---------------- STATUS API ----------------
@app.route('/status')
def status():

    emotions = ["Happy", "Sad", "Neutral", "Angry"]

    noise_level, db = detect_sound()

    

    if db > 80:
        alert = "Danger! Aggressive Sound Detected"

    elif db > 50:
        alert = "Warning! Loud Environment"
    else:
        alert = "System Normal"    

    return jsonify({
        "emotion": random.choice(emotions),
        "score": random.randint(50, 100),
        "toxicity": random.randint(1, 100),
        "noise":  f"{db} dB",
        "environment": noise_level,
        "alert": alert,
        "ai_status": "Active",
        "camera": "connected",
        "microphone": "monitoring",
        "system": "secure"
        
       
    })

@app.route('/start_ai')
def start_ai():

    os.system('python backend/emotion/emotion_detection.py')

    return "AI Detection Started"


# =========================
# LIVE VIDEO FEED
# =========================

@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/emotion')
def emotion():

    success, frame = camera.read()

    if not success:
        return jsonify({
            "emotion": "No Face"
        })

    result = detector.top_emotion(frame)

    if result is None:
        emotion_name = "Neutral"
    else:
        emotion_name = result[0]

    return jsonify({
        "emotion": emotion_name
    })



@app.route('/data')
def data():

    emotion = "Happy"
    toxicity = 12
    score = 72
    alert = "System Normal"

    connection = sqlite3.connect("ai_dashboard.db")

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO monitoring
    (emotion, toxicity, score, alert)
    VALUES (?, ?, ?, ?)
    """, (emotion, toxicity, score, alert))

    connection.commit()

    connection.close()

    return {
        "score": score,
        "emotion": emotion,
        "toxicity": toxicity,
        "alert": alert
    }

@app.route('/google')
def google_login():

    if not google.authorized:
        return redirect('/login/google')

    resp = google.get("/oauth2/v2/userinfo")

    user_info = resp.json()

    session['user'] = user_info['email']

    return redirect('/dashboard')

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)