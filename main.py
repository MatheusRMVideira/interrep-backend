from flask import Flask, jsonify, request, session
from flask_cors import CORS
from pymysql import DatabaseError
from config import APPLICATION_PREFIX, JWT_LIFETIME, JWT_KEY, DATABASE_URI,MAX_CONTENT_LENGTH,UPLOAD_FOLDER
from prefix_middleware import PrefixMiddleware
from flask_sqlalchemy import SQLAlchemy
import jwt
import time
from sqlalchemy_utils import create_database, database_exists
if not database_exists(DATABASE_URI):
    create_database(DATABASE_URI)

db = SQLAlchemy()

from models.game import Game
from models.market import Market
from models.player import Player
from models.playerpoints import PlayerPoints
from models.republic import Republic
from models.team import Team
from models.teampoints import TeamPoints
from models.user import User
from models.role import Role
from models.femGame import FemGame
from models.femMarket import FemMarket
from models.femPlayer import FemPlayer
from models.femPlayerpoints import FemPlayerPoints
from models.femRepublic import FemRepublic
from models.femTeam import FemTeam
from models.femTeampoints import FemTeamPoints

from resources.users import bp_users
from resources.market import bp_market
from resources.players import bp_players
from resources.republics import bp_republics
from resources.teams import bp_teams
from resources.session import bp_session
from resources.games import bp_games
from resources.femMarket import bp_market_fem
from resources.femPlayers import bp_players_fem
from resources.femRepublics import bp_republics_fem
from resources.femTeams import bp_teams_fem
from resources.femGames import bp_games_fem

from models.playercall import playercall_table
from models.femPlayercall import fem_playercall_table

app = Flask(__name__)
CORS(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=APPLICATION_PREFIX)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
db.init_app(app)
with app.app_context():
    db.create_all()
    market_aux = Market.query.first()
    if market_aux is None:
        market = Market(
            id = 1, 
            deadline = 0, 
            open = 1, 
            round = 0)

        db.session.add(market)
        db.session.commit()

    role_aux = Role.query.first()
    if role_aux is None:
        role2 = Role(
            id = 2,
            name = "User",
            create_player = 0,
            modify_player = 0,
            delete_player = 0,
            create_rep = 0,
            modify_rep = 0,
            delete_rep = 0,
            toggle_market = 0,
            give_points = 0,
            create_game = 0,
            update_game = 0,
            delete_game = 0,
            admin_panel = 0
        )
        db.session.add(role2)
        db.session.commit()


app.register_blueprint(bp_session, url_prefix='/session')
app.register_blueprint(bp_users, url_prefix='/users')
app.register_blueprint(bp_players, url_prefix='/players')
app.register_blueprint(bp_republics, url_prefix='/republics')
app.register_blueprint(bp_market, url_prefix='/market')
app.register_blueprint(bp_teams, url_prefix='/teams')
app.register_blueprint(bp_games, url_prefix='/games')

app.register_blueprint(bp_players_fem, url_prefix='/feminino/players')
app.register_blueprint(bp_republics_fem, url_prefix='/feminino/republics')
app.register_blueprint(bp_market_fem, url_prefix='/feminino/market')
app.register_blueprint(bp_teams_fem, url_prefix='/feminino/teams')
app.register_blueprint(bp_games_fem, url_prefix='/feminino/games')


@app.route('/', methods=['GET'])
def Ping():
    return "pong!", 200
