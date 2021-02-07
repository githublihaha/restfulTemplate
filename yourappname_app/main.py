import os

from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from app.libs.database import db
from app.resources.scans import Scans

app = Flask(__name__)

# sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['UPLOAD_FOLDER'] = '/tmp/tmp'

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
api.add_resource(tasks, '/v1.0/tasks')



