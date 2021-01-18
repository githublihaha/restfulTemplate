import re
import os
from werkzeug.utils import secure_filename


def get_scripts():
    scripts = {}
    try:
        with open('/usr/share/nmap/scripts/script.db', 'r') as f:
            str_pat = re.compile(r'\"(.*?)\"')
            for line in f.readlines():
                parts = str_pat.findall(line)
                scripts[parts.pop(0)] = parts
    except FileNotFoundError:
        return {'message':'File not found.'}, 400
    except Exception:
        return {'message':'Other error.'}, 400
    else:
        return scripts, 200

def get_script_by_name(name):
    filename = secure_filename(name)
    file_path = os.path.join('/usr/share/nmap/scripts/',filename)

    try:
        with open(file_path, 'r') as f:
            context = f.read()
        return context, 200
    except FileNotFoundError as e:
        return 'File not found.', 400


if __name__ == "__main__":
    print('get')
    get_scripts()