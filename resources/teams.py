from flask import Blueprint, jsonify, request
from functools import reduce

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.team import Team
from models.player import Player
from models.market import Market
from guard import Auth, GetUserID, getUserFromRequest
import requests


bp_teams = Blueprint('bp_teams', __name__)

@bp_teams.route('/', methods = ['GET'])
@Auth
def GetAllTeams():
    team = Team.query.all()
    teams = [t.toJSONmin() for t in team]
    teams.sort(key=lambda team: team['points'], reverse=True)
    return jsonify(teams),200;

@bp_teams.route('/me', methods = ['GET'])
@Auth
def GetOwnTeams():
    user = getUserFromRequest()
    if len(user.teams) == 0:
        return jsonify({"error":"you don't have a team"}), 400
    return jsonify(user.teams[0].toJSON()),200;

@bp_teams.route('/', methods = ['POST'])
@Auth
def CreateTeam():
    user = getUserFromRequest()
    if len(user.teams) > 0:
        return jsonify({"error":"you already have a team"}), 400
    team = Team(
        name = request.form['name'],
        user_id = GetUserID()
        )
    db.session.add(team)
    db.session.commit()
    return jsonify(team.toJSON()),201;

@bp_teams.route('/me/name', methods = ['PUT'])
@Auth
def ChangeTeamName():
    team = Team.query.filter_by(user_id = GetUserID()).first()
    if not team:
        return jsonify({"error":"Time não encontrado"}), 400
    team.name = request.form['name']
    db.session.merge(team)
    db.session.commit()
    return jsonify(team.toJSON()),201

@bp_teams.route('/me', methods = ['PUT'])
@Auth
def ChangeTeamPlayers():
    market = Market.query.first()
    if not market.open:
        return jsonify({"error":"O mercado está fechado"}), 400
    team = Team.query.filter_by(user_id = GetUserID()).first()
    if not team:
        return jsonify({"error":"Time não encontrado"}), 400
    playersids = request.form.getlist('players')
    print(playersids)
    for p in playersids:
        if not p or p == 'null':
            return jsonify({"error":"Seu time precisa ter 5 jogadores"}), 400
    players = [Player.query.filter_by(id=p).first() for p in playersids]
    print(playersids)
    if not playersids or len(playersids)<5:
        return jsonify({"error":"Seu time precisa ter 5 jogadores"}), 400
    for p in players:
        if p.benched:
            return jsonify({"error":"Você não pode escalar jogadores que estarão no banco"}), 400
    hasGK = 0
    for p in players:
        print(p)
        if p.position.name == "Goleiro":
            hasGK += 1
    if hasGK != 1:
        return jsonify({"error":"Seu time deve ter exatamente 1 goleiro"}), 400
    user = getUserFromRequest()
    totalValue = reduce((lambda x, y: x + y), [p.value for p in players])
    ownTeamValue = 0
    if len(team.players):
        ownTeamValue = reduce((lambda x, y: x + y), [p.value for p in team.players])
    if totalValue>user.coins+ownTeamValue:
        return jsonify({"error":"Patrimônio insuficiente"}), 400
    team.players = players
    user.coins -= totalValue
    user.coins += ownTeamValue
    db.session.merge(team)
    db.session.merge(user)
    db.session.commit()
    return jsonify(team.toJSON()),201
