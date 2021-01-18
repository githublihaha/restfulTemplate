import os
print(os.getcwd())

from . import check_host
from . import check_port

import nmap


print('--nmapScan-')

def nmapScan(args):
    # choose mode
    mode_choices = {
        'intense':' -T4 -A -v ',
        'intense_udp':' -sS -sU -T4 -A -v ',
        'intense_all_tcp':' -p 1-65535 -T4 -A -v ',
        'intense_no_ping':' -T4 -A -v -Pn ',
        'ping':' -sn ',
        'quick':' -T4 -F ',
        'quick_plus':' -sV -T4 -O -F --version-light ',
        'quick_trace':' -sn --traceroute ',
        'regular':' ',
        'slow_comp':' -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)" '
    }

    tcp_choices = {
        'ACK':'-sA',
        'FIN':'-sF',
        'Maimon':'-sM',
        'Null':'-sN',
        'SYN':'-sS',
        'Connect':'-sT',
        'Window':'-sW',
        'Xmas':'-sX'
    }
    
    nontcp_choices = {
        'UDP':'-sU',
        'IP':'-sO',
        'List':'-sL',
        'Ping':'-sn',
        'SCTP INIT':'-sY',
        'SCTP COOKIE-ECHO':'-sZ'
    }



    host = args.pop('host')
    port = args.pop('port')
    mode = args.pop('mode')
    tcp  = args.pop('tcp')
    nontcp = args.pop('nontcp')
    

    if mode is not None:
        arguments = mode_choices[mode]
    else:
        arguments = ''
    
    if tcp is not None:
        arguments += tcp_choices[tcp]

    if nontcp is not None:
        arguments += nontcp_choices[nontcp]


    for v in args.values():
        if v is not None:
            arguments += " "
            arguments += v
    
    # check host
    try:
        check_host.check_host(host)
    except check_host.HostError:
        code = 400
        message = 'HostError: wrong host'
        return code, message


    # check port
    if port is not None:
        # check ports
        if (arguments.find('sO')>=0):
            # ip protocol scan
            ip_flag = 1
        else:
            ip_flag = 0
        
        try:
            check_port.check_port(port, ip_flag)
        except check_port.PortError as e:
            code = 400
            message = e.value
            return code, message

    try:
        nm = nmap.PortScanner()
        result = nm.scan(host, port, arguments, True)
    except nmap.nmap.PortScannerError as e:
        result = e.value
        code = 400
    else:
        code = 200

    return code, result

