import os

from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from app.libs.database import db
from app.resources.scans import Scans
from app.resources.scans import ScanId
from app.resources.scans import Scanning
from app.resources.scans import Scanned
from app.resources.scans import Failed
from app.resources.scans import ScanTest
from app.resources.scans import Upload
from app.resources.reports import Reports
from app.resources.scripts import Scripts
from app.resources.scripts import ScriptsDir

app = Flask(__name__)

# sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nmap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['UPLOAD_FOLDER'] = '/tmp'
# app.config['UPLOAD_FOLDER'] = '/usr/share/nmap/uploadfiles'
# create upload folder
try:
    os.mkdir(app.config['UPLOAD_FOLDER'])
except OSError as e:
    print(e)
else:
    print('create upload folder success')


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

api = Api(app, catch_all_404s=True)
swagger = Swagger(app)

# add resources
api.add_resource(Scans, '/v1.0/scans')
api.add_resource(ScanId, '/v1.0/scans/<int:id>')
api.add_resource(Scanning, '/v1.0/scans/scanning')
api.add_resource(Scanned, '/v1.0/scans/scanned')
api.add_resource(Failed, '/v1.0/scans/failed')
api.add_resource(Upload, '/v1.0/scans/upload')
api.add_resource(ScanTest, '/v1.0/scans/scantest')

api.add_resource(Reports, '/v1.0/reports/<int:id>')

api.add_resource(Scripts, '/v1.0/scripts/')
api.add_resource(ScriptsDir, '/v1.0/scripts/dir')


