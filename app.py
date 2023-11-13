from flask import Flask, render_template, request, redirect, url_for
import pyotp

app = Flask(__name__)

# Зберігаємо секретні ключі користувачів у словник
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    secret_key = generate_otp_secret()
    users[username] = {'secret_key': secret_key}
    return render_template('registered.html', username=username, secret_key=secret_key)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    otp_input = request.form['otp']

    if username in users and verify_otp(users[username]['secret_key'], otp_input):
        return f"Ви успішно автентифікувалися, {username}!"
    else:
        return "Невірні дані автентифікації. Спробуйте знову."

def generate_otp_secret():
    # Генерація секретного ключа
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.secret

def generate_otp(secret):
    # Генерація OTP за секретним ключем
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_otp(secret, user_input):
    # Перевірка OTP
    totp = pyotp.TOTP(secret)
    return totp.verify(user_input)

if __name__ == '__main__':
    app.run(debug=True)
