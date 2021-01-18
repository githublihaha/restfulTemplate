import subprocess

def nmap_updatedb():

    try:
        out_bytes = subprocess.check_output(['nmap','--script-updatedb'])
    except subprocess.CalledProcessError as e:
        out_bytes = e.output       # Output generated before error
        code      = e.returncode   # Return code

        return out_bytes.decode('utf-8'), 400
    else:
        return '', 200


if __name__ == "__main__":
    nmap_updatedb()