from app.models.scanModel import ScanModel
from app.models.reportModel import ReportModel

from app.libs.gen_id import generate_short_id

def ab_threading(app):
    # start scan

    # update scans status and finish time
    with app.app_context():
        scan = ScanModel.find_by_id(scan_id)
        if scan is not None:
            if (code == 400):
                ScanModel.update_status_finish_time(scan_id, 'failed')
                report = ReportModel(scan_id, 'failed', str(result), str(result_xml))
                report.add_to_db()
            else:
                ScanModel.update_status_finish_time(scan_id, 'scanned')
                report = ReportModel(scan_id, 'succeeded', str(result), str(result_xml))
                report.add_to_db()











