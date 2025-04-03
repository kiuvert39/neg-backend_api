from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from app.services.auth_service import AuthService
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS

auth_ns = Namespace("auth", description="Authentication Endpoints")

# Request parsers
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', required=True, type=str)
register_parser.add_argument('password', required=True, type=str)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True, type=str)
login_parser.add_argument('password', required=True, type=str)
@auth_ns.route("/register")
class Register(Resource):
    # @auth_ns.expect(register_model)
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        if not data:
            return {"error": MISSING_JSON_BODY }, 400

        # Extract fields safely
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if not email or not username or not password:
            return {"error": REQUIRE_FIELDS }, 400


        return AuthService.register_user( email, username, password)
    

@auth_ns.route("/login")
class Login(Resource):
    # @auth_ns.expect(login_model)
    def post(self):
        """User login"""
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": REQUIRE_FIELDS }, 400
        
        return AuthService.login_user(email, password)
