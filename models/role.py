from sqlalchemy.dialects import mysql

import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from main import db


class Role(db.Model):
    id = db.Column(mysql.INTEGER(50), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship("User")
    create_player = db.Column(db.Boolean, unique=False, nullable=False)
    modify_player = db.Column(db.Boolean, unique=False, nullable=False)
    delete_player = db.Column(db.Boolean, unique=False, nullable=False)
    create_rep = db.Column(db.Boolean, unique=False, nullable=False)
    modify_rep = db.Column(db.Boolean, unique=False, nullable=False)
    delete_rep = db.Column(db.Boolean, unique=False, nullable=False)
    toggle_market = db.Column(db.Boolean, unique=False, nullable=False)
    give_points = db.Column(db.Boolean, unique=False, nullable=False)
    create_game = db.Column(db.Boolean, unique=False, nullable=False)
    update_game = db.Column(db.Boolean, unique=False, nullable=False)
    delete_game = db.Column(db.Boolean, unique=False, nullable=False)
    admin_panel = db.Column(db.Boolean, unique=False, nullable=False)


    def __repr__(self):
        return 'id:%r name:%r' % (self.id,self.name)

    def toJSON(self):
        permissions = ['create_player','modify_player','delete_player','create_rep','modify_rep','delete_rep','toggle_market','give_points','create_game','update_game','delete_game','admin_panel']
        has_permissions = []
        for p in permissions:
            if getattr(self,p):
                has_permissions.append(p)
        return {
            'id': self.id,
            'name': self.name,
            'permissions':has_permissions
            }
