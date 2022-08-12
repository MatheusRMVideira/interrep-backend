from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db


class FemPlayerPoints(db.Model):
    player_id = db.Column(mysql.INTEGER(50), db.ForeignKey('fem_player.id'), primary_key=True)
    player = db.relationship("FemPlayer", lazy="joined")
    round = db.Column(mysql.INTEGER(50), primary_key=True)
    value = db.Column(db.Float, unique=False, nullable=False)
    points = db.Column(db.Float)


    def __repr__(self):
        return 'player_id:%r round:%r points:%r' % (self.player_id,self.round,self.points)

    def toJSON(self):
        return {
            'player': self.player.toJSONmin(),
            'round': self.round,
            'points': self.points,
            'value': self.value
            }

    def toJSONmin(self):
        return {
            'round': self.round,
            'points': self.points,
            'value': self.value
            }
