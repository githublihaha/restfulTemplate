from datetime import datetime

from app.libs.database import db

class TaskModel(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host = db.Column(db.String(255))
    port = db.Column(db.String(255))
   

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def id_exist(cls, id):
        return bool(cls.query.filter_by(id=id).first())

    @classmethod
    def delete_by_id(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()
