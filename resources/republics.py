from flask import Blueprint, jsonify, request

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.republic import Republic
from guard import Auth, GetUserID, CheckPermission
import requests


bp_republics = Blueprint('bp_republics', __name__)

@bp_republics.route('/', methods = ['GET'])
@Auth
def GetAllReps():
    reps = Republic.query.all()
    return jsonify([r.toJSON() for r in reps]), 200

@bp_republics.route('/<int:rep_id>', methods = ['GET'])
@Auth
def GetRep(rep_id):
    rep = Republic.query.filter_by(id=rep_id).first()
    if not rep:
        return jsonify({'error':'republic not found'}), 404
    return jsonify(rep.toJSON()), 200

@bp_republics.route('/', methods = ['POST'])
@Auth
@CheckPermission
def CreateRepublic():
    rep_exists = Republic.query.filter_by(name=request.form['name']).first()
    if rep_exists:
        return jsonify({'error':'republic already registered'}), 400
    rep = Republic(
        name = request.form['name']
        #picture = request.form['picture']
    )
    db.session.add(rep)
    db.session.commit()
    return jsonify(rep.toJSON()), 201

@bp_republics.route('/<int:rep_id>', methods = ['DELETE'])
@Auth
@CheckPermission
def DeleteRepublic(rep_id):
    rep = Republic.query.filter_by(id=rep_id).first()
    if not rep:
        return jsonify({'error':'republic not found'}), 404
    db.session.delete(rep)
    db.session.commit()
    return jsonify({'status':'deleted'}), 201

@bp_republics.route('/<int:rep_id>', methods = ['PUT'])
@Auth
@CheckPermission
def ModifyRepublic(rep_id):
    rep = Republic.query.filter_by(id=rep_id).first()
    if not rep:
        return jsonify({'error':'republic not found'}), 404
    rep.name = request.form['name']
    #rep.picture = request.form['picture']
    db.session.merge(rep)
    db.session.commit()
    return jsonify(rep.toJSON()), 201
