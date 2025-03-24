import bcrypt
from flask_jwt_extended import create_access_token
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    @staticmethod
    def register_user(email, username, password):
        if User.find_by_email(email):
            return {"error": "User already exists"}, 400
        
        hashed_password = generate_password_hash(password)

        user = User(email=email, username=username, password=hashed_password)        
        user.save()
        return {
            "message": "User registered successfully",
            "user": {"username": user.username}}, 201

    @staticmethod
    def login_user(email, password):

        user = User.find_by_email(email)

        if user and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=email)
            return {"message" : "User loggedin successfully","access_token": access_token}, 200
        
        return {"error": "Invalid credentials"}, 401
