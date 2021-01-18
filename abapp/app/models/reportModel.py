from datetime import datetime

from app.libs.database import db


class ReportModel(db.Model):
    # ScanModel对应的表格： scans
    __tablename__ = 'reports'

    #
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scan_id = db.Column(db.Integer)
    status = db.Column(db.Enum('succeeded','failed'))
    result = db.Column(db.Text)
    result_xml = db.Column(db.Text)

    def __init__(self, scan_id, status, result, result_xml):
        self.scan_id = scan_id
        self.status = status
        self.result = result
        self.result_xml = result_xml


    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_id(cls, scan_id):
        # find
        return cls.query.filter_by(scan_id=scan_id).first()

    @classmethod
    def delete_by_id(cls, id):
        #print('delete report')
        # db.session.delete(cls.query.filter_by(scan_id=id).first())
        # db.session.commit()
        cls.query.filter_by(scan_id=id).delete()
        db.session.commit()
