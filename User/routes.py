from app import app
from flask import request, session, jsonify, make_response, Response
from User.model import utilityUser
import functools

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('userId') is None:
            response = Response("You are not authenticated", status=401)
            response = make_response(
                jsonify({
                    "Error": "You are not authenticated",
                }),
                401
            )
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers["Content-Type"] = "application/json"
            return response

        return func(*args, **kwargs)

    return wrapper

@app.route('/')
def index():
    return 'Hello World'

@app.route("/signup", methods=["POST"])
def signup():
    userName = request.form['userName']
    userEmail = request.form['userEmail']
    userPassword = request.form['userPassword']
    return utilityUser(userName = userName, userEmail = userEmail, userPassword = userPassword).signup()

@app.route("/login", methods=["POST"])
def login():
    userEmail = request.form['userEmail']
    userPassword = request.form['userPassword']
    return utilityUser(userEmail = userEmail, userPassword = userPassword).login()

@app.route("/logout", methods=["GET"])
def logout():
    return utilityUser().logout()

@app.route("/addToDo", methods=["POST"])
@login_required
def addToDo():
    item = request.form['item']
    return utilityUser().addToDo(item)

@app.route('/dash')
@login_required
def dash():
    return utilityUser().dash()
