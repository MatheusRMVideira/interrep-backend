from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.market import Market
from models.team import Team
from guard import Auth, GetUserID, CheckPermission
import requests


bp_market = Blueprint('bp_market', __name__)

@bp_market.route('/', methods = ['GET'])
@Auth
def GetMarket():
    market = Market.query.first()
    return jsonify(market.toJSON()),200;

@bp_market.route('/', methods = ['PUT'])
@Auth
@CheckPermission
def ToggleMarket():
    market = Market.query.first()
    if market.open:
        market.round += 1
    market.open = not market.open
    db.session.merge(market)
    db.session.commit()
    return jsonify(market.toJSON()),200;

@bp_market.route('/deadline', methods = ['PUT'])
@Auth
@CheckPermission
def SetDeadline():
    market = Market.query.first()
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
