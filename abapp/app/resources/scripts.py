import os

import werkzeug
from flasgger import swag_from
from flask_restful import fields
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.libs.get_scripts import get_scripts
from app.libs.get_scripts import get_script_by_name
from app.libs.nmap_updatedb import nmap_updatedb
from app.libs.delete_script import delete_script

resource_fields = {
    'id': fields.Integer,
    'scan_id': fields.Integer,
    'result': fields.String
}


class Scripts(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='args')
        self.reqparse.add_argument('nsefile', type=werkzeug.datastructures.FileStorage, location='files')

        super(Scripts, self).__init__()

    @swag_from('specs/scripts_get.yml')
    def get(self):
        args = self.reqparse.parse_args()
        # print(args.name)
        # print('********************')
        if args.name is not None:
            context, code = get_script_by_name(args.name)
            return {'result':context}, code
        else:
            scripts, code = get_scripts()
            return scripts, code


    @swag_from('specs/scripts_post.yml')
    def post(self):
        args = self.reqparse.parse_args()
        content = args.get('nsefile')
        if content is None:
            return {'message': 'No file input'}, 400

        filename = secure_filename(content.filename)
        if filename == 'script.db':
            return {'message': 'Do not upload script.db'}, 400
        file_path = os.path.join('/usr/share/nmap/scripts', filename)
        content.save(file_path)
        message, code = nmap_updatedb()
        if code == 400:
            # updatedb failed
            # remove the new file
            os.remove(file_path)
        return {'message': message}, code

    @swag_from('specs/scripts_delete.yml')
    def delete(self):
        args = self.reqparse.parse_args()
        if args.name is None:
            return {'message':'Input a file name'}, 400
        return delete_script(args.name)

    @swag_from('specs/scripts_put.yml')
    def put(self):
        args = self.reqparse.parse_args()
        content = args.get('nsefile')
        if content is None:
            return {'message': 'No file input'}, 400

        # file name and path
        filename = secure_filename(content.filename)
        if filename == 'script.db':
            return {'message': 'Do not upload script.db'}, 400
        file_path = os.path.join('/usr/share/nmap/scripts', filename)

        # delete old
        message, code = delete_script(filename)
        if code == 400:
            return message, code

        # save new
        content.save(file_path)
        message, code = nmap_updatedb()
        if code == 400:
            # updatedb failed
            # remove the new file
            os.remove(file_path)
        return {'message': message}, code


class ScriptsDir(Resource):

    @swag_from('specs/scripts_get_dir.yml')
    def get(self):
        file_path = '/usr/share/nmap/scripts'
        try:
            result = os.listdir(file_path)
        except Exception:
            return {'message': 'error' }, 400
        return {'result': result}, 200