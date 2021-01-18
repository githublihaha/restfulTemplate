from app.libs.database import db


class TestModel(db.Model):
    # ScanModel对应的表格： scans
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def save_to_db(self):
        # insert
        db.session.add(self)
        # commit
        db.session.commit()

    @classmethod
    def find_by_id(cls, username):
        # find
        return cls.query.filter_by(name=username).first()
