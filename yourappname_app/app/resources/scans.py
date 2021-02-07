import os


import werkzeug
from flask import current_app
from flask_restful import marshal_with
from flasgger import swag_from
from flask_restful import fields
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.libs.gen_id import generate_short_id
from app.libs.extract_file import extract_recursion
from app.models.scanModel import ScanModel
from app.models.reportModel import ReportModel


UPLOAD_FOLDER = '/tmp'


resource_fields_id = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'status': fields.String,
    'create_time': fields.DateTime,
    'finish_time': fields.DateTime
}

resource_fields_scanned = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'create_time': fields.DateTime,
    'finish_time': fields.DateTime
}

resource_fields_scanning = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String,
    'arguments': fields.String,
    'create_time': fields.DateTime
}


def prepare_args_for_parser(parser):
    """ Modifies all the args of a Parser to better defaults. """
    if not isinstance(parser, reqparse.RequestParser):
        raise ValueError('Expecting a parser')
    for arg in parser.args:
        arg.store_missing = False
        arg.help = "Error: {error_msg}. Field description: %s" % arg.help
    return parser


class Scans(Resource):
    def __init__(self):
        timemode_choices = ('T0', 'T1', 'T2')

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('port', type=str, location='json')
        self.reqparse.add_argument('timemode', type=str, location='json', choices=timemode_choices)
        self.reqparse = prepare_args_for_parser(self.reqparse)
        super(Scans, self).__init__()
    #
    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        return args

    def get(self):
        pass





class ScanId(Resource):

    @marshal_with(resource_fields_id, envelope='resource')
    @swag_from('specs/scans_get_scanid.yml')
    def get(self, id):
        scan = ScanModel.find_by_id(id)
        if scan is not None:
            return scan
        else:
            return {'message': 'scan id not exists.'}, 400

    @swag_from('specs/scans_delete_scanid.yml')
    def delete(self, id):
        scan = ScanModel.find_by_id(id)
        if scan is not None:
            # delete scan
            ScanModel.delete_by_id(id)
            # delete reports
            ReportModel.delete_by_id(id)

            return {'message': 'ok.'}, 200
        else:
            return {'message': 'scan id not exists.'}, 400


class Scanning(Resource):
    # return all scanning item
    @marshal_with(resource_fields_scanning, envelope='resource')
    @swag_from('specs/scans_scanning.yml')
    def get(self):
        scans = ScanModel.find_by_status('scanning')
        return scans


class Failed(Resource):
    # return all scanning item
    @marshal_with(resource_fields_scanning, envelope='resource')
    @swag_from('specs/scans_failed.yml')
    def get(self):
        scans = ScanModel.find_by_status('failed')
        return scans


class Scanned(Resource):
    # 10 default, user can input the number
    # number must be > 0
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('limit', type=int, location='args')

        super(Scanned, self).__init__()

    @marshal_with(resource_fields_scanned, envelope='resource')
    @swag_from('specs/scans_scanned.yml')
    def get(self):
        args = self.reqparse.parse_args()

        if args.limit is not None:
            if args.limit <= 0:
                return {'message': 'limit must > 0 '}, 400
            else:
                scans = ScanModel.find_by_status('scanned', args.limit)
        else:
            scans = ScanModel.find_by_status('scanned', 10)

        if scans is not None:
            return scans
        else:
            return {'message': 'no scanned scan'}, 400


class Upload(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='args')
        self.reqparse.add_argument('uploadfile', type=werkzeug.datastructures.FileStorage, location='files')

        super(Upload, self).__init__()

    @swag_from('specs/scans_get_file.yml')
    def get(self):
        # get all files in folder
        file_path = UPLOAD_FOLDER
        try:
            result = os.listdir(file_path)
            result_all_path = [os.path.join(file_path, name) for name in result]
        except Exception:
            return {'message': 'error'}, 400
        return {'result': result_all_path}, 200

    @swag_from('specs/scans_upload_file.yml')
    def post(self):
        # get file
        args = self.reqparse.parse_args()
        content = args.get('uploadfile')
        if content is None:
            return {'message': 'No file input.', 'filename': ''}, 400

        # file exists, save file.
        filename = secure_filename(content.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        content.save(file_path)

        extracted_name_list = []
        error_log = []

        try:
            extract_recursion([file_path], UPLOAD_FOLDER, extracted_name_list, error_log)
            #base_name_list = [os.path.basename(name) for name in extracted_name_list]
        except Exception as e:
            message = 'Some error occurred: ' + '  '.join(error_log)
            filename = '  '.join(extracted_name_list)
            code = 400
        else:
            message = 'All files are extracted successfully.'
            filename = '  '.join(extracted_name_list)
            code = 200

        return {'message': message, 'filename': filename, 'error':error_log}, code




class ScanTest(Resource):
    def get(self):
        ScanModel.update_status_finish_time(100)
        return {'message': 'test'}, 400
