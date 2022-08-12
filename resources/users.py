from flask import Blueprint, jsonify, request, send_file
import time
from werkzeug.utils import secure_filename

import os, sys


parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.user import User
from models.team import Team
from models.femTeam import FemTeam
from utils import encrypt, isValidEmail, allowed_file
from config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from guard import Auth, GetUserID
import requests


bp_users = Blueprint('bp_users', __name__)

@bp_users.route('/<int:user_id>/picture', methods = ['GET'])
@Auth
def GetPicture(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':'user not found'}), 400
    if not user.picture:
        return jsonify({'error':'user picture not found'}), 400
    if len(user.picture.split('.')) > 3:
        return jsonify({'picture_url':user.picture}), 200
    return send_file(user.picture, mimetype='image/gif')

@bp_users.route('/', methods = ['POST'])
def Register():
    if not isValidEmail(request.form['email']):
        return jsonify({'error':'E-mail inválido'}), 400
    if len(request.form['password'])<PASSWORD_MIN_LENGTH:
        return jsonify({'error':'Senha muito curta'}), 400
    if len(request.form['password'])>PASSWORD_MAX_LENGTH:
        return jsonify({'error':'Senha muito longa'}), 400
    exists = User.query.filter_by(email=request.form['email']).first()
    if exists:
        return jsonify({'error':'Email já registrado'}), 400
    name = request.form['name']
    if not len(name):
        return jsonify({'error':'É necessário informar um nome'}), 400
    exists = User.query.filter_by(name=request.form['name']).first()
    if exists:
        return jsonify({'error':'Nome já registrado'}), 400
    user = User(
        email = request.form['email'],
        password = encrypt(request.form['password']),
        name = name,
        role_id = 2,
        regDate = time.time(),
        coins = 50,
        fem_coins = 50
    )
    db.session.add(user)
    db.session.commit()
    team = Team(
        name = 'Time de '+name,
        user_id = user.id
        )
    db.session.add(team)
    db.session.commit()
    femTeam = FemTeam(
        name = 'Time de '+name,
        user_id = user.id
    )
    db.session.add(femTeam)
    db.session.commit()
    return jsonify(user.toJSON()), 201



@bp_users.route('/', methods = ['GET'])
@Auth
def GetAllUsers():
    users = User.query.all()
    users = [u.toJSONmin() for u in users]
    return jsonify(users), 200

@bp_users.route('/me', methods = ['GET'])
@Auth
def GetOwnInfo():
    user_id = GetUserID()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 400
    return jsonify(user.toJSON()), 200

@bp_users.route('/<int:user_id>', methods = ['GET'])
@Auth
def GetUserInfo(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 400
    return jsonify(user.toJSONmin()), 200

@bp_users.route('/me', methods = ['PUT'])
@Auth
def EditProfile():
    user_id = GetUserID()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error':"user not found"}), 400
    user.name = request.form['name']
    user.birthday = request.form['picture']
    db.session.commit()
    return jsonify(user.toJSON()), 201
