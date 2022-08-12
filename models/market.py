from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db

class Market(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    deadline = db.Column(mysql.INTEGER(50), unique=False, nullable=False)
    open = db.Column(db.Boolean, unique=False, nullable=False)
    round = db.Column(mysql.INTEGER(50), unique=False, nullable=False)

    def __repr__(self):
        return '<open:%r>' % (self.open)

    def toJSON(self):
        return {
            'deadline': self.deadline,
            'open': self.open,
            'round': self.round
            }
