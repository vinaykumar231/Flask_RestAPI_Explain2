from functools import wraps
from flask import jsonify, request
from sqlalchemy.orm import Session
from werkzeug.exceptions import Unauthorized
from auth.auth_handler import decode_jwt
from database import get_db
from api.models.user import User
#from auth_handler import decode_jwt



class JWTBearer:
    def __init__(self, auto_error: bool = True):
        """
        Initializes the JWTBearer class.
        """
        self.auto_error = auto_error

    def __call__(self):
        """
        Callable method to extract and verify the JWT token from the request.
        """
        credentials = self.extract_credentials()
        if credentials:
            if credentials["scheme"] != "Bearer":
                if self.auto_error:
                    raise Unauthorized(description="Invalid authentication scheme.")
                return None
            if not self.verify_jwt(credentials["token"]):
                if self.auto_error:
                    raise Unauthorized(description="Invalid token or expired token.")
                return None
            return credentials["token"]
        else:
            if self.auto_error:
                raise Unauthorized(description="Invalid authorization code.")
            return None

    @staticmethod
    def extract_credentials():
        """
        Extracts the scheme and token from the Authorization header.
        """
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return None
        
        parts = authorization_header.split(" ", 1)
        if len(parts) != 2:
            return None
        
        return {"scheme": parts[0], "token": parts[1]}

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        """
        Verifies the JWT token.
        """
        try:
            payload = decode_jwt(jwt_token)
            return payload is not None
        except Exception as e:
            print(f"Token verification failed: {e}")
            return False

def extract_token():
    """
    Extracts the Bearer token from the Authorization header.
    """
    token = JWTBearer().extract_credentials()
    if not token:
        raise Unauthorized(description="Missing authorization token")

    auth_token = token.get("token")
    if not auth_token:
        raise Unauthorized(description="Invalid authorization scheme")

    return auth_token


# Helper function to decode and validate JWT
def get_user_id_from_token():
    """
    Decodes the JWT token to retrieve the user ID.
    """
    token = extract_token()  # Now correctly extracts the token
    payload = decode_jwt(token)  # Decodes the token
    if not payload:
        raise Unauthorized(description="Invalid or expired token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise Unauthorized(description="User ID not found in token")
    
    return user_id


# Function to retrieve the current user
def get_current_user():
    """
    Retrieves the current user based on the token.
    """
    user_id = get_user_id_from_token()
    db: Session = get_db()
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise Unauthorized(description="User not found")
    return user

# Function to get admin user
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()  # Get the authenticated user
        if not user or user.user_type != "admin":
            return jsonify({"error": "Unauthorized: Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Function to get a regular user
def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user.user_type != "user":
            return jsonify({"error": "You are not authorized to perform this action"}), 403
        return f(*args, **kwargs)
    return decorated_function


# Function to get either an admin or regular user
def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user.user_type != "user":
            return jsonify({"error": "You are not authorized to perform this action"}), 403
        return f(*args, **kwargs)
    return decorated_function

