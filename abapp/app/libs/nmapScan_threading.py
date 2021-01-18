import nmap

from app.models.scanModel import ScanModel
from app.models.reportModel import ReportModel


def nmapScan_threading(app, host, port, arguments, scan_id):
    # start scan
    try:
        nm = nmap.PortScanner()
        # if the runner is not root, use sudo, put the last parameter to True
        # result = nm.scan(host, port, arguments, True)

        # if the runner is root, do not use sudo
        result = nm.scan(host, port, arguments, False)
        result_xml = nm.get_nmap_last_output()


    except nmap.nmap.PortScannerError as e:
        result = e.value
        result_xml = ''
        code = 400
    except AssertionError as e:
        result = e
        result_xml = ''
        code = 400
    except Exception:
        result = 'other error'
        result_xml = ''
        code = 400
    else:
        code = 200

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











