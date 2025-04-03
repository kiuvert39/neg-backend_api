from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.system_messages import USER_NOT_FOUND

class AuthService:
    @staticmethod
    def register_user(email, username, password):
        # Check if the user already exists
        if User.find_by_email(email):
            return {"error": "User already exists"}, 400

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Save the new user in the database
        user = User(email=email, username=username, password=hashed_password)
        user.save()

        return {
            "message": "User registered successfully",
            "user": {"username": user.username}
        }, 201

    @staticmethod
    def login_user(email, password):
        # Check if the user exists by email
        user = User.find_by_email(email)

        if not user:
            return {"error": USER_NOT_FOUND}, 404

        # Validate the password
        if check_password_hash(user["password"], password):
            # Create a token for the user
            token = create_access_token(identity=email)

            # Create a response object
            response = make_response(jsonify({"message": "User logged in successfully"}))

            # Set the token as an HttpOnly cookie
            response.set_cookie("token", token, httponly=True, samesite="Lax", secure=True)

            return response  # Returning the response directly, no need for status code here

        # If credentials are invalid, return an error
        return jsonify({"error": "Invalid credentials"}), 401