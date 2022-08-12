from sqlalchemy.dialects import mysql
import enum
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.republic import Republic

class Game(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    republic_home_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic_away_id = db.Column(db.Integer, db.ForeignKey('republic.id'),nullable=False)
    republic_home = db.relationship(Republic, foreign_keys=[republic_home_id])
    republic_away = db.relationship(Republic, foreign_keys=[republic_away_id])
    score_home = db.Column(mysql.INTEGER(50), unique=False, nullable=True)
    score_away = db.Column(mysql.INTEGER(50), unique=False, nullable=True)
    time = db.Column(db.String(100), unique=False, nullable=True)
    place = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        return {
            'id': self.id,
            'republic_home': self.republic_home.toJSONmin(),
            'republic_away':self.republic_away.toJSONmin(),
            'score_home': self.score_home,
            'score_away':self.score_away,
            'time': self.time,
            'place': self.place
            }
