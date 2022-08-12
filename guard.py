from flask import request, jsonify
import time
from functools import wraps
import requests
import jwt

from models.user import User
from config import JWT_KEY, PERMISSIONS_REQUIRED
from utils import DecodeToken

def Auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get('authorization'):
            return jsonify({'error':'a token is required'}), 401
        auth = request.headers.get('authorization').split(" ", 2)[1]
        try:
            token = jwt.decode(auth, JWT_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'token timeout'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error':'invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

def GetUserID():
    if not request.headers.get('authorization'):
        return jsonify({'error':'a token is required'}), 401
    token = request.headers.get('authorization').split(" ", 2)[1]
    token = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
    return token['user_id']

def getUserFromRequest():
    auth = request.headers.get('authorization')
    token = DecodeToken(auth)
    user = User.query.filter_by(id=token['user_id']).first()
    return user

def CheckPermission(f):
    def decorated(*args, **kwargs):
        permissions_required = PERMISSIONS_REQUIRED[f.__name__]
        user = getUserFromRequest()
        for p in permissions_required:
            if not getattr(user.role,p):
                return jsonify({'error':'Você não tem permissão para fazer isso'}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated
