from sqlalchemy.dialects import mysql
from functools import reduce

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.femPlayercall import fem_playercall_table
from models.femTeampoints import FemTeamPoints
from models.femPlayer import FemPlayer

class FemTeam(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", lazy="joined", back_populates="fem_teams")
    players = db.relationship(FemPlayer,secondary=fem_playercall_table)
    points = db.relationship("FemTeamPoints", lazy="joined", cascade="delete")


    def __repr__(self):
        return '<id:%r>' % (self.id)

    def getLastPoints(self):
        if not self.points:
            return 0
        return self.points[-1].points

    def getPoints(self):
        if not self.points:
            return 0
        return reduce((lambda x, y: x + y), [p.points for p in self.points])

    def newScore(self,score,round):
        point = FemTeamPoints.query.filter_by(team_id=self.id,round=round).first()
        if not point:
            newPoints = FemTeamPoints(
                team_id = self.id,
                round = round,
                points = 0
                )
            db.session.add(newPoints)
            self.points.append(newPoints)
            point = FemTeamPoints.query.filter_by(team_id=self.id,round=round).first()
        point.points += score
        db.session.merge(point)
        return self

    def getPosition(self):
        teams = FemTeam.query.all()
        teams = teams = [t.toJSONmin() for t in teams]
        teams.sort(key=lambda team: team['points'], reverse=True)
        position = 1
        for t in teams:
            if t['id'] == self.id:
                return position
            position += 1

    def toJSON(self):
        players = [p.toJSON() for p in self.players]
        return {
            'id': self.id,
            'name': self.name,
            'position': self.getPosition(),
            'points':float("{0:.2f}".format(self.getPoints())),
            'user': self.user.toJSONmin(),
            'players':[p.toJSON() for p in self.players],
            'last': float("{0:.2f}".format(self.getLastPoints())),
            }

    def toJSONmin(self):
        return {
            'id': self.id,
            'name': self.name,
            'points':float("{0:.2f}".format(self.getPoints())),
            'user': self.user.toJSONmin(),
            'last': float("{0:.2f}".format(self.getLastPoints())),
            }
