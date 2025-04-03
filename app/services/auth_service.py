from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from app.models.user import User
from datetime import timedelta
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
            return {"error": "User not found"}, 404

        # Validate the password
        if check_password_hash(user["password"], password):
            # Create an access token with a 15-day expiration time
            token = create_access_token(identity=email, expires_delta=timedelta(days=15))

            # Create a JSON response
            response_data = {"message": "User logged in successfully", "token": token}

            # Use `make_response` to set the cookie separately
            response = make_response(jsonify(response_data))
            response.set_cookie("token", token, httponly=True, samesite="Lax", secure=True, max_age=15 * 24 * 60 * 60)  # 15 days in seconds

            return response

        # If credentials are invalid, return an error
        return {"error": "Invalid credentials"}, 401
        

    def logout_user():
            response = make_response(jsonify({"message": "Logged out successfully"}))  # ✅ Ensure response is JSON
            response.set_cookie('token', '', expires=0, httponly=True, secure=True, samesite='None')  # ✅ Clear cookie
            response.headers["Content-Type"] = "application/json"  # ✅ Explicitly set content type
            return response  # ✅ Return only the response (no tuple)
