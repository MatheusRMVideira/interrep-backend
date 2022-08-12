from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.femPlayer import FemPlayer, Positions
from models.femRepublic import FemRepublic
from models.femMarket import FemMarket
from models.femPlayerpoints import FemPlayerPoints
from models.femPlayercall import fem_playercall_table
from guard import Auth, GetUserID, CheckPermission
import requests


bp_players_fem = Blueprint('bp_players_fem', __name__)

@bp_players_fem.route('/', methods = ['GET'])
@Auth
def GetAllPlayers():
    player = FemPlayer.query.all()
    return jsonify([p.toJSON() for p in player]), 200

@bp_players_fem.route('/active', methods = ['GET'])
@Auth
def GetActivePlayers():
    player = FemPlayer.query.filter_by(benched=False).all()
    players = [p.toJSON() for p in player]
    players.sort(key=lambda player: player['average'], reverse=True)
    return jsonify(players), 200

@bp_players_fem.route('/<int:player_id>', methods = ['GET'])
@Auth
def GetPlayer(player_id):
    player = FemPlayer.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 400
    return jsonify(player.toJSON()), 200

@bp_players_fem.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreatePlayer():
    rep_exists = FemRepublic.query.filter_by(id=request.form['republic_id']).first()
    if not rep_exists:
        return jsonify({'error':'republic not found'}), 400
    benched = request.form['benched']
    if benched in ["false","0","False"]:
        benched = False
    else:
        benched = True
    if float(request.form['value']) <= 0:
        return jsonify({'error':'Valor inválido'}), 400
    player = FemPlayer(
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched
    )
    db.session.add(player)
    db.session.commit()
    if player.position=="":
        db.session.delete(player)
        db.session.commit()
        return jsonify({'error':'Posição inválida'}), 400
    return jsonify(player.toJSON()), 201

@bp_players_fem.route('/<int:player_id>', methods = ['DELETE'])
@Auth
@CheckPermission
def DeletePlayer(player_id):
    player = FemPlayer.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    db.session.delete(player)
    db.session.commit()
    return jsonify({'status':'deleted'}), 201

@bp_players_fem.route('/most-points', methods = ['GET'])
@Auth
def MostPoints():
    market = FemMarket.query.first()
    print("market")
    points = FemPlayerPoints.query.filter_by(round=market.round).order_by(FemPlayerPoints.points.desc()).all()
    print("points")
    ids = [p.player_id for p in points]
    print(len(ids))
    print("ids")
    players = [p.toJSONmin() for p in db.session.query(FemPlayer).filter(FemPlayer.id.in_(ids)).all()]
    print(len(players))
    print("players")
    #return jsonify([p.toJSONmin() for p in players]),200
    points = [{"points":p.points,"player":list(filter(lambda x: x['id'] == p.player_id, players))[0]} for p in points]
    print("json")
    pointsGoleira = list(filter(lambda x: x['player']['position'] == "Goleira", points))
    pointsLinha = list(filter(lambda x: x['player']['position'] == "Linha", points))
    return jsonify({"Goleira":pointsGoleira[:1],"Linha":pointsLinha[:4]}), 200

@bp_players_fem.route('/most-choosen', methods = ['GET'])
@Auth
def MostChoosen():
    players = FemPlayer.query.all()
    for index in range(len(players)):
        n_teams = len(players[index].teams)
        players[index] = players[index].toJSON()
        players[index]['n_teams']  = n_teams
    players.sort(key=lambda player: player['n_teams'], reverse=True)
    goleiros = list(filter(lambda x: x['position'] == "Goleira", players))
    linhas = list(filter(lambda x: x['position'] == "Linha", players))
    return jsonify({"Goleira":goleiros[:1],"Linha":linhas[:4]}), 200

@bp_players_fem.route('/<int:player_id>/bench', methods = ['PUT'])
@Auth
@CheckPermission
def BenchPlayer(player_id):
    player = FemPlayer.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    player.benched = not player.benched;
    db.session.merge(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201

@bp_players_fem.route('/<int:player_id>/points', methods = ['POST'])
@Auth
@CheckPermission
def GivePlayerPoints(player_id):
    player = FemPlayer.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    player.value = request.form['value']
    db.session.merge(player)
    db.session.commit()
    return jsonify(player.toJSON()),200

@bp_players_fem.route('/<int:player_id>', methods = ['PUT'])
@Auth
@CheckPermission
def ModifyPlayer(player_id):
    player = FemPlayer.query.filter_by(id=player_id).first()
    if not player:
        return jsonify({'error':'player not found'}), 404
    rep_exists = FemRepublic.query.filter_by(id=request.form['republic_id']).first()
    if not rep_exists:
        return jsonify({'error':'republic not found'}), 404
    benched = request.form['benched']
    if benched in ["false","0","False"]:
        benched = False
    else:
        benched = True
    db.session.delete(player)
    player = FemPlayer(
        id = player_id,
        name = request.form['name'],
        republic_id = request.form['republic_id'],
        position = request.form['position'],
        value = request.form['value'],
        benched = benched
    )
    db.session.add(player)
    db.session.commit()
    return jsonify(player.toJSON()), 201


@bp_players_fem.route('/scores', methods = ['PUT'])
@Auth
@CheckPermission
def GivePlayersScore():
    market = FemMarket.query.first()
    if market.open:
        return jsonify({'error':'Você não pode dar pontos a um jogador enquanto o mercado estiver aberto'}),400;
    playersids = request.form.getlist('players')
    for pid in playersids:
        player = FemPlayer.query.filter_by(id=pid).first()
        if not player:
            return jsonify({'error':'Um dos jogadores relacionados não foi encontrado. ID: '+pid}),400;
    players = [FemPlayer.query.filter_by(id=pid).first() for pid in playersids]
    points = request.form.getlist('points')
    if not len(points) == len(players):
        return jsonify({'error':'Número de argumentos inválido'}),400;
    for pindex in range(len(players)):
        playerpoints = FemPlayerPoints.query.filter_by(player_id = players[pindex].id,round=market.round).first()
        if playerpoints:
            for t in players[pindex].teams:
                t.newScore(-1*players[pindex].getPointsInRound(market.round),market.round)
        players[pindex].newScore(float(points[pindex]),market.round)
        for t in players[pindex].teams:
            t.newScore(float(points[pindex]),market.round)
    for p in players:
        db.session.merge(p)
    db.session.commit()
    return jsonify([p.toJSON() for p in players]),201;
