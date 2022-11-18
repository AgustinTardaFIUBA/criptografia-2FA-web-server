#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import generador2FA

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
serverGeneratorSeed = generador2FA.generate_seed()

# WEB PAGE
# homepage route
@app.route("/")
def index():
    print("Server OTP generation: {}".format(generador2FA.generate_totp(serverGeneratorSeed,6)))
    return "<h1>Prototipo de autenticación TOTP</h1>"

#API Server/APP

# login form route
@app.route("/login/", methods=["POST"])
def login_form():
    credentials = {"username": "cripto", "password": "1234"}

    username = request.form.get("username")
    password = request.form.get("password")

    if username == credentials["username"] and password == credentials["password"]:
        return 200
    else:
        return {"error": "The Token is invalid, the user is not authenticated"}, 401

# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    
    # getting OTP provided by user
    totp = request.form.get("totp")
        
    # verifying submitted OTP
    if generador2FA.verify_totp(totp,serverGeneratorSeed):
        #inform users if OTP is valid
        flash("El token TOTP ingresado es válido.", "success")
        return 200
    else:
        # inform users if OTP is invalid
        flash("El token TOTP ingresado es inválido.", "danger")
        return {"error": "The Token is invalid, the user is not authenticated"}, 401

@app.route("/sync", methods=["GET"])
def sync_with_app():
    return serverGeneratorSeed
    
# running flask server
if __name__ == "__main__":
    app.run(debug=True)



