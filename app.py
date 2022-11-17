#el servidor de desarrollo utiliza el puerto 5000, para acceder a la aplicacion entrar a:
# http://127.0.0.1:5000/login

#paquetes necesarios para correr
#pip install flask
#pip install pyotp
#pip install flask-bootstrap4

#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import pyotp
import generador2FA
import base64

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)


# homepage route
@app.route("/")
def index():
    return "<h1>Prototipo de autenticación TOTP</h1>"

# login page route
@app.route("/login/")
def login():
    return render_template("login.html")        

# login form route
@app.route("/login/", methods=["POST"])
def login_form():
    credentials = {"username": "cripto", "password": "1234"}


    username = request.form.get("username")
    password = request.form.get("password")

    if username == credentials["username"] and password == credentials["password"]:
        # inform users if creds are valid
        flash("Las credenciales ingresadas son correctas", "success")
        return redirect(url_for("login_2fa"))
    else:
        # inform users if creds are invalid
        flash("Las credenciales ingresadas son incorrectas!", "danger")
        return redirect(url_for("login"))
    
# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    # generating random secret key for authentication
    secret = generador2FA.generate_seed()
    totp = generador2FA.generate_totp(secret,6)
    
    return render_template("login_2fa.html", secret=secret, totp=totp)

# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    
    # getting OTP provided by user
    totp = request.form.get("totp")
        
    # verifying submitted OTP
    if generador2FA.verify_totp(totp,secret):
        #inform users if OTP is valid
        flash("El token TOTP ingresado es válido.", "success")
        return redirect(url_for("login_2fa"))
    else:
        # inform users if OTP is invalid
        flash("El token TOTP ingresado es inválido.", "danger")
        return redirect(url_for("login_2fa"))
    
# running flask server
if __name__ == "__main__":
    app.run(debug=True)
