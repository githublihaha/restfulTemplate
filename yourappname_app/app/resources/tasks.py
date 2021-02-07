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
from app.models.taskModel import TaskModel

UPLOAD_FOLDER = '/tmp'

resource_fields_id = {
    'id': fields.Integer,
    'host': fields.String,
    'port': fields.String
}

def prepare_args_for_parser(parser):
    """ Modifies all the args of a Parser to better defaults. """
    if not isinstance(parser, reqparse.RequestParser):
        raise ValueError('Expecting a parser')
    for arg in parser.args:
        arg.store_missing = False
        arg.help = "Error: {error_msg}. Field description: %s" % arg.help
    return parser

class Tasks(Resource):
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
