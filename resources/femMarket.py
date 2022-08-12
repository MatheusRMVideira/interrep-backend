from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.femMarket import FemMarket
from models.femTeam import FemTeam
from guard import Auth, GetUserID, CheckPermission
import requests


bp_market_fem = Blueprint('bp_market_fem', __name__)

@bp_market_fem.route('/', methods = ['GET'])
@Auth
def GetMarket():
    market = FemMarket.query.first()
    return jsonify(market.toJSON()),200;

@bp_market_fem.route('/', methods = ['PUT'])
@Auth
@CheckPermission
def ToggleMarket():
    market = FemMarket.query.first()
    if market.open:
        market.round += 1
    market.open = not market.open
    db.session.merge(market)
    db.session.commit()
    return jsonify(market.toJSON()),200;

@bp_market_fem.route('/deadline', methods = ['PUT'])
@Auth
@CheckPermission
def SetDeadline():
    market = FemMarket.query.first()
    deadline = 0
    try:
        deadline = int(request.form['deadline']);
    except:
        pass
    if not deadline > 0:
        return jsonify({'error':'Por favor, selecione data, hora e turno'}),400;
    market.deadline = deadline
    db.session.merge(market)
    db.session.commit()
    return jsonify(market.toJSON()),200;
