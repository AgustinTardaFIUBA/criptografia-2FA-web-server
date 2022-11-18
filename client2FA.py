#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import generador2FA
import requests

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)

# WEB PAGE
# homepage route
@app.route("/")
def index():
    # GET THE SECRET KEY FROM THE SERVER
    url = "http://127.0.0.1:5000/sync"
    response = requests.get(url)
    print(response.text)
    serverGeneratorSeed = response.text
    totp= generador2FA.generate_totp(serverGeneratorSeed,6)
    return "<h1>{}</h1>".format(totp)


#API Server/APP

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
    app.run(debug=True, port=5001)



