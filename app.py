from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_session import Session
from datetime import timedelta
from flask_cors import CORS

load_dotenv()
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()
db.init_app(app)

SECRET_KEY = os.environ.get("SECRET_KEY")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_SQLALCHEMY'] = db
#app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)

sess = Session(app)
#sess.init_app(app)

#run it only once
#with app.app_context():
#    sess.app.session_interface.db.create_all()

#with app.app_context():
#   db.create_all()


from User import routes


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
