#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import generador2FA
import requests

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)

generatorSeed = None

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
@app.route("/register-service/", methods=["POST"])
def registerService():
    generatorSeed = request.form.get("secret")

# login form route
@app.route("/generate-token/", methods=["GET"])
def generateToken():
    if generatorSeed == None:
        return {"error": "The Token is invalid, the user is not authenticated "}, 400
    else:
        return generador2FA.generate_totp(generatorSeed,6), 200


    
# running flask server
if __name__ == "__main__":
    app.run(debug=True, port=5001)



