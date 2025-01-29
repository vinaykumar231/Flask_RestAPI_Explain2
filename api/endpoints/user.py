from flask import Blueprint, request, jsonify
from api.models.user import User
from database import get_db
#from auth.auth_bearer import JWTBearer, get_current_user, get_admin, get_user, get_admin_or_user
from auth.auth_handler import sign_jwt
import bcrypt
from enum import Enum

auth_bp = Blueprint('auth', __name__)

class UserType(Enum):
    admin = 'admin'
    user = 'user'

class UserLogin:
    email: str
    password: str

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json() 
    db = get_db()
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user:
        return jsonify({"error": f"Record with Email: {data['email']} not found"}), 404

    if bcrypt.checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
        token, exp = sign_jwt(user.user_id, user.user_type)
        response = {
            'token': token,
            'exp': exp,
            'user_id': user.user_id,
            'user_name': user.user_name,
            'user_email': user.email,
            'user_type': user.user_type,
            'created_on': user.updated_on,
            
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


class UserData:
    user_name: str
    password: str
    email: str
    user_type: str = UserType.user.value 

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json() 
    try:
        db = get_db()
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user_db = User(
            user_name=data["user_name"],
            password=hashed_password,
            email=data["email"],
            user_type=data.get("user_type", UserType.user.value)  
        )

        db.add(user_db)
        db.commit()

        return jsonify({"message": "User registered successfully", "user": user_db.user_id}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "User registration failed"}), 500
