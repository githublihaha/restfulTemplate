from flasgger import swag_from
from flask_restful import Resource
from flask_restful import fields, marshal_with
from app.models.reportModel import ReportModel

resource_fields = {
    'id': fields.Integer,
    'scan_id': fields.Integer,
    'status': fields.String,
    'result': fields.String,
    'result_xml': fields.String
}

class Reports(Resource):
    @marshal_with(resource_fields, envelope='resource')
    @swag_from('specs/reports_get.yml')
    def get(self, id):
        report = ReportModel.find_by_id(id)
        if report is not None:
            return report
        else:
            return {'message':'report id not exists.'}, 400


    @swag_from('specs/reports_delete.yml')
    def delete(self, id):
        report = ReportModel.find_by_id(id)
        if report is not None:
            ReportModel.delete_by_id(id)
            return {'message':'ok.'}, 200
        else:
            return {'message':'report id not exists.'}, 200