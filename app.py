from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

with open('./Data/mailCreds.json', 'r') as file:
        creds = json.load(file)

# Configure MongoDB
client = MongoClient(creds['mongoConnect']['uri'])  # Replace with your MongoDB server address if needed
db = client[creds['mongoConnect']['db']]
collection = db[creds['mongoConnect']['collection']]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = str(user['_id'])
            flash('Login successful!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Invalid user ID or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username})

        if user:
            flash('User ID already exists', 'danger')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(password)
            collection.insert_one({'username': username, 'password': hashed_password})
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        # Process the file (save it, manipulate it, etc.)
        flash('File uploaded successfully', 'success')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
