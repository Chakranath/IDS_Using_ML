from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Route for the home page
@app.route('/')
def home():
    return render_template('login.html')

# Route for handling the login page logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'password':
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
