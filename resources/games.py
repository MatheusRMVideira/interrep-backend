from flask import Blueprint, jsonify, request
from sqlalchemy import or_

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.game import Game
from models.player import Player
from guard import Auth, GetUserID, CheckPermission
import requests


bp_games = Blueprint('bp_games', __name__)

@bp_games.route('/', methods = ['GET'])
@Auth
def GetAllGames():
    games = Game.query.all()
    return jsonify([m.toJSON() for m in games]),200;

@bp_games.route('/current', methods = ['GET'])
@Auth
def GetCurrentGames():
    games = Game.query.filter(or_(game.score_home==None,game.score_away==None)).all()
    return jsonify([m.toJSON() for m in games]),200;

@bp_games.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreateGame():
    if request.form['republic_home_id'] == request.form['republic_away_id']:
        return jsonify({'error':'Dois times iguais foram selecionados'}),400;
    game = Game(
        republic_home_id = request.form['republic_home_id'],
        republic_away_id = request.form['republic_away_id'],
        time = request.form['time'],
        place = request.form['place'],
        )
    db.session.add(game)
    db.session.commit()
    return jsonify(game.toJSON()),201;

@bp_games.route('/<int:game_id>', methods = ['PUT'])
@Auth
@CheckPermission
def UpdateGame(game_id):
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return jsonify({'error':'Partida não encontrada'}),400;
    game.score_home = request.form['score_home']
    game.score_away = request.form['score_away']
    db.session.merge(game)
    db.session.commit()
    return jsonify(game.toJSON()),201;



@bp_games.route('/<int:game_id>', methods = ['DELETE'])
@Auth
@CheckPermission
def DeleteGame(game_id):
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return jsonify({'error':'Partida não encontrada'}),400;
    db.session.delete(game)
    db.session.commit()
    return jsonify({'status':'Partida apagada com sucesso'}),201;
