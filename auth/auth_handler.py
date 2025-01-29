from functools import wraps
from flask import request, jsonify
import jwt
import time
#from decouple import config
import os

JWT_SECRET = os.getenv('secret')
JWT_ALGORITHM = os.getenv('algorithm')

def sign_jwt(user_id, user_type):
    expiration_time = time.time() + 30 * 24 * 60 * 60  
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, expiration_time


def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token.get("exp") and decoded_token["exp"] < time.time():
            return None
        if "user_id" not in decoded_token or "user_type" not in decoded_token:
            return None
        return decoded_token
    except jwt.PyJWTError:
        return None

