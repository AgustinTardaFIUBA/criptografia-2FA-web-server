#cambiarle el nombre al archivo 2FA por uno que comience con una letra, se cambio a generador2FA

from flask import *
from flask_bootstrap import Bootstrap
import generador2FA
from flask_cors import CORS, cross_origin
from flask_caching import Cache
import time
import sys

# configuring flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
serverGeneratorSeed = None
serverName = "Nameless Server"

# WEB PAGE
# homepage route
@app.route("/")
def index():
    print(serverGeneratorSeed)
    print("Server OTP generation: {}".format(generador2FA.generate_totp(serverGeneratorSeed,6)))
    return "<h1>Prototipo de autenticación TOTP</h1>"

#API Server/APP

# login form route
@app.route("/login/", methods=["POST"])
def login_form():
    credentials = {"username": "cripto@gmail.com", "password": "1234"}

    username = request.get_json().get("username")
    password = request.get_json().get("password")

    if username == credentials["username"] and password == credentials["password"]:
        return 'Success', 200
    else:
        return {"error": "The Token is invalid, the user is not authenticated"}, 401

def isTimeBlocked( ip ):
    timeBlockedUsers = cache.get('timeBlockedUsers')
    if ip in timeBlockedUsers:
        initialBlockTime = timeBlockedUsers[ip]
        return (time.time() - initialBlockTime) <= 120

    return False

def timeBlockUser( ip ):
    timeBlockedUsers = cache.get('timeBlockedUsers')
    timeBlockedUsers[ip] = time.time()
    cache.set("timeBlockedUsers", timeBlockedUsers)

def validateUserBlock( ip ):
    usersAttempts = cache.get('usersAttempts')
    if len(usersAttempts[ip]) >= 5:
        fiveCallWindowDifference = usersAttempts[ip][len(usersAttempts[ip])-1] - usersAttempts[ip][len(usersAttempts[ip])-5] 
        if fiveCallWindowDifference <= 60:
            timeBlockUser(ip)

def increaseAttemptsWindow( ip ):
    usersAttempts = cache.get('usersAttempts')
    if not (ip in usersAttempts):
        usersAttempts[ip] = []

    usersAttempts[ip].append(time.time())    
    cache.set("usersAttempts", usersAttempts)
    validateUserBlock(ip)

# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    
    if( isTimeBlocked(request.remote_addr) ):
        return {"error": "Number of attempts exceeded, wait 2 minutes to retry"}, 403

    # getting OTP provided by user
    totp = request.get_json().get("totp")
        
    # verifying submitted OTP
    if generador2FA.verify_totp(totp,serverGeneratorSeed):
        #inform users if OTP is valid
        flash("El token TOTP ingresado es válido.", "success")
        return 'Success', 200
    else:
        # inform users if OTP is invalid
        increaseAttemptsWindow(request.remote_addr)
        flash("El token TOTP ingresado es inválido.", "danger")
        return {"error": "The Token is invalid, the user is not authenticated"}, 401

@app.route("/sync", methods=["GET"])
def sync_with_app():
    return serverGeneratorSeed
    
# running flask server
if __name__ == "__main__":
    print(sys.argv)
    serverName = sys.argv[2]

    usersAttempts = {}
    timeBlockedUsers = {}
    cache.set("usersAttempts", usersAttempts)
    cache.set("timeBlockedUsers", timeBlockedUsers)

    serverGeneratorSeed = generador2FA.generate_seed()

    app.run(port = sys.argv[1], debug=True)


