from datetime import datetime

from app.libs.database import db


class ScanModel(db.Model):
    # ScanModel对应的表格： scans
    __tablename__ = 'scans'

    #
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host = db.Column(db.String(255))
    port = db.Column(db.String(255))
    arguments = db.Column(db.String(255))
    status = db.Column(db.Enum('scanning','scanned','failed'))
    create_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)

    def __init__(self, host, port, arguments, status, create_time, finish_time):
        self.host = host
        self.port = port
        self.arguments = arguments
        self.status = status
        self.create_time = create_time
        self.finish_time = finish_time


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
    def update_status_finish_time(cls, scan_id, status):
        cls.query.filter_by(id=scan_id).update({'status': status, 'finish_time': datetime.now()})
        db.session.commit()

    @classmethod
    def find_by_status(cls, status, length=10):
        if status == "scanned":
            return cls.query.filter_by(status=status).order_by(ScanModel.create_time.desc()).limit(length).all()
        else:
            return cls.query.filter_by(status=status).order_by(ScanModel.create_time.desc()).all()

    @classmethod
    def delete_by_id(cls, id):
        # db.session.delete(cls.query.filter_by(id=id).first())
        # db.session.commit()
        cls.query.filter_by(id=id).delete()
        db.session.commit()
