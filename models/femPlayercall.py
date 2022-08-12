from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

fem_playercall_table = db.Table('fem_playercall',
    db.Column('player_id', mysql.INTEGER(50), db.ForeignKey('fem_player.id'), primary_key=True),
    db.Column('team_id', mysql.INTEGER(50), db.ForeignKey('fem_team.id'), primary_key=True)
    )
