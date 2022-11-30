#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import generador2FA
import requests
from flask_cors import CORS, cross_origin
from flask_caching import Cache
import sys
 
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# configuring flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

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
@app.route("/register-service", methods=["POST"])
def registerService():
    generatorSeed = request.get_json().get("secret")
    pageName = request.get_json().get("pageName")

    generatorSeeds = cache.get('generatorSeeds')
    generatorSeeds[pageName] = generatorSeed
    cache.set("generatorSeeds", generatorSeeds)

    return jsonify('App registered'), 200

# login form route
@app.route("/generate-token", methods=["GET"])
def generateToken():
    if cache.get('generatorSeeds') == None:
        return {"error": "The generator seed is empty"}, 400
    else:
        generatorSeeds = cache.get('generatorSeeds')
        tokensPerPage = {}
        for generatorSeed in generatorSeeds.keys():
            tokensPerPage[generatorSeed] = generador2FA.generate_totp(generatorSeeds[generatorSeed],6)
            print(tokensPerPage)
        return {"tokens":tokensPerPage}, 200


# running flask server
if __name__ == "__main__":
    generatorSeeds = {}
    cache.set("generatorSeeds", generatorSeeds)
    app.run(debug=True, port=5001)



