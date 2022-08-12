from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

class Republic(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    players = db.relationship("Player", cascade="delete", lazy="joined")
    picture = db.Column(db.Text, unique=False, nullable=True)


    def __repr__(self):
        return '<id:%r>' % (self.id)

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'picture': self.picture,
            'players':[p.toJSONmin() for p in self.players]
            }

    def toJSONmin(self):
        return {
            'id': self.id,
            'name': self.name,
            'picture': self.picture
            }
