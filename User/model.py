from app import db
from flask import jsonify, make_response, session
import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    todos = relationship("ToDo", back_populates="user")

    def todos_as_array(self):
        todos = []
        for item in self.todos:
            todos.append(item.as_dict())
        return todos

    def __repr__(self):
        return '<User %r>' % self.name

class ToDo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    user = relationship("Usuario", back_populates="todos")
                        #className of the Parent   #field on the parent to backprop to
    def as_dict(self):
     return {'name': self.name, 'done': self.done, 'id': self.id}

    def __repr__(self):
        return '<Item %r>' % self.name

class utilityUser():
    def __init__(self, userName = '', userEmail = '', userPassword = ''):
        self.userName = userName
        self.userEmail = userEmail
        self.userPassword = userPassword

    def setSession(self):
        session['userName'] = self.userName
        session['userEmail'] = self.userEmail
        session['userId'] = self.userId

    def verifySession(self):
        if session.get('userId') is None:
            return False
        return True

    def setInfoFromSession(self):
        self.userName = session.get('userName')
        self.userEmail = session.get('userEmail')
        self.userId = session.get('userId')

    def logout(self):
        try:
            session.clear()
            response = make_response(
                jsonify({
                    "Message": "You have been logout",
                }),
                200
            )

        except Exception as e:
            print("Erro", e)
            response = make_response(
                jsonify({
                    "Error": "Erro interno do servidor",
                }),
                500
            )
        response.headers["Content-Type"] = "application/json"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def hashPassword(self):
        hashed = bcrypt.hashpw(self.userPassword.encode('utf8'), bcrypt.gensalt(14))
        self.userPassword = hashed.decode('utf8')

    def checkPassword(self, hashed):
        #print('hashed', hashed)
        if bcrypt.checkpw(self.userPassword.encode('utf8'), hashed.encode('utf8')):
            return True
        return False

    def signup(self):
        self.hashPassword()

        try:
            user = Usuario(name=self.userName, email=self.userEmail, password=self.userPassword)
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            print("Error", e)
            db.session.rollback()
            response = make_response(
                jsonify({
                    "Error": "email já cadastrado",
                }),
                409
            )

        except Exception as e:
            print("Erro", e)
            db.session.rollback()
            response = make_response(
                jsonify({
                    "Error": "Erro interno do servidor",
                }),
                500
            )

        else:
            self.userId = user.id
            self.setSession()
            response = make_response(
                jsonify({
                    "inserted_id": str(self.userId )
                }),
                200
            )

        finally:
            db.session.close()

        response.headers["Content-Type"] = "application/json"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def login(self):
        #print('userEmail', self.userEmail)
        #print('userPassword', self.userPassword)
        try:
            user = db.session.query(Usuario).filter_by(email=self.userEmail).first()
            #print('user', user)
            if(user):

                if(self.checkPassword(user.password)):
                    response = make_response(
                        jsonify({
                            "user_id": user.id
                        }),
                        200
                    )
                    self.userId = user.id
                    self.userName = user.name
                    self.setSession()

                else:
                    response = make_response(
                        jsonify({
                            "Error": 'Credentials do not match'
                        }),
                        401
                    )

            else:
                response = make_response(
                    jsonify({
                        "Error": "User not found",
                    }),
                    401
                )

        except Exception as e:
            print("Error", e)
            response = make_response(
                jsonify({
                    "Error": "Erro interno do servidor",
                }),
                500
            )

        finally:
            db.session.close()

        response.headers["Content-Type"] = "application/json"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def addToDo(self, item):
        self.setInfoFromSession()
        #print('self.userEmail', self.userEmail)
        #print('session.get(userName)', session.get('userName'))
        #print('session.get(userEmail)', session.get('userEmail'))
        #print('session.get(userId)', session.get('userId'))

        try:
            user = db.session.query(Usuario).filter_by(email=self.userEmail).first()
            if(user):
                user.todos.append(ToDo(name=item, done=False))
                db.session.commit()
                response = make_response(
                    jsonify({
                        "Message": "Item Added",
                    }),
                    200
                )

            else:
                response = make_response(
                    jsonify({
                        "Error": "User not found",
                    }),
                    401
                )

        except Exception as e:
            print("Error", e)
            db.session.rollback()
            response = make_response(
                jsonify({
                    "Error": "Erro interno do servidor",
                }),
                500
            )

        finally:
            db.session.close()

        response.headers["Content-Type"] = "application/json"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def dash(self):
        self.setInfoFromSession()
        try:
            user = db.session.query(Usuario).filter_by(email=self.userEmail).first()

            #print('user.todos_as_array', user.todos_as_array())
            if(user):
                response = make_response(
                    jsonify({
                        "user_name": session.get('userName', 'not set'),
                        "user_email": session.get('userEmail', 'not set'),
                        "todos": user.todos_as_array()
                    }),
                    200
                )

            else:
                response = make_response(
                    jsonify({
                        "Error": "User not found",
                    }),
                    401
                )

        except Exception as e:
            print("Error", e)
            response = make_response(
                jsonify({
                    "Error": "Erro interno do servidor",
                }),
                500
            )

        finally:
            db.session.close()

        response.headers["Content-Type"] = "application/json"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
