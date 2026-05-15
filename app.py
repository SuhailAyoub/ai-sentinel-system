from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
template_folder="templates",
static_folder='static'
# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- LOGIN ----------------
@app.route('/login')
def login():
    return render_template('login.html')

# ---------------- SIGNUP ----------------
@app.route('/signup')
def signup():
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

    settings_data['real_time_detection'] = bool(request.form.get('real_time_detection'))
    settings_data['alert_notifications'] = bool(request.form.get('alert_notifications'))
    settings_data['dark_mode'] = bool(request.form.get('dark_mode'))

    settings_data['detection_sensitivity'] = request.form.get('detection_sensitivity')
    settings_data['camera_source'] = request.form.get('camera_source')

    print(settings_data)

    return redirect('/settings')

# ---------------- STATUS API ----------------
@app.route('/status')
def status():

    data = {
        'emotion': 'Angry',
        'alert': 'Warning detected',
        'noise': '65 dB'
    }

    return jsonify(data)

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)