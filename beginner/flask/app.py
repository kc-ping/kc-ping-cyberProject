from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "secretKey"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#simulate a user database
users = {}

#Home page (GET requests)
@app.route('/')
def home():
    return render_template('home.html')

#Registration page (GET and POST requests)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            return "Username already exists!"
        if not username or not password:
            return "Invalid input!", 400
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        return redirect(url_for('home'))
    return render_template('register.html')

#Login page (GET and POST requests)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username not in users or not check_password_hash(users[username], password): #check if user exists and password is correct
            return "Invalid credentials!", 401
        session["user"] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Protected Route
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for('login'))
    
    return  render_template('dashboard.html', username=session["user"])

# secure file upload 
@app.route('/upload', methods=['POST'])
def upload():
    if "user" not in session:
        return redirect(url_for('login'))
    file = request.files['file']
    if not file:
        return "No file uploaded!", 400
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return "File uploaded successfully!"

# Logout route
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)