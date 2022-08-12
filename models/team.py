from sqlalchemy.dialects import mysql
from functools import reduce

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db
from models.playercall import playercall_table
from models.teampoints import TeamPoints
from models.player import Player

class Team(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", lazy="joined", back_populates="teams")
    players = db.relationship(Player,secondary=playercall_table)
    points = db.relationship("TeamPoints", lazy="joined", cascade="delete")


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
        point = TeamPoints.query.filter_by(team_id=self.id,round=round).first()
        if not point:
            newPoints = TeamPoints(
                team_id = self.id,
                round = round,
                points = 0
                )
            db.session.add(newPoints)
            self.points.append(newPoints)
            point = TeamPoints.query.filter_by(team_id=self.id,round=round).first()
        point.points += score
        db.session.merge(point)
        return self

    def getPosition(self):
        teams = Team.query.all()
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
