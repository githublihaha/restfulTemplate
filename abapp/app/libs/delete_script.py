import os
from werkzeug.utils import secure_filename
from . import nmap_updatedb

def delete_script(name):
    filename = secure_filename(name)
    if filename == 'script.db':
        return {'message': 'Can not delete script.db'}, 400
    file_path = os.path.join('/usr/share/nmap/scripts/', filename)

    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        print(e)
        return {'message': 'File not found'}, 400
    except Exception as e:
        return {'message': str(e)}, 400
    else:
        message, code = nmap_updatedb.nmap_updatedb()
        return {'message': 'delete ' + filename + ' ok'}, 200


if __name__ == "__main__":

    message, code = delete_script('testy.nse')
    print(message)
    print(code)
