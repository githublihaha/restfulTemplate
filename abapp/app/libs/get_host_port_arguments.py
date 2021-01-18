def get_host_port_arguments(args):
    mode_choices = {
        'intense': ' -T4 -A -v ',
        'intense_udp': ' -sS -sU -T4 -A -v ',
        'intense_all_tcp': ' -p 1-65535 -T4 -A -v ',
        'intense_no_ping': ' -T4 -A -v -Pn ',
        'ping': ' -sn ',
        'quick': ' -T4 -F ',
        'quick_plus': ' -sV -T4 -O -F --version-light ',
        'quick_trace': ' -sn --traceroute ',
        'regular': ' ',
        'slow_comp': ' -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)" '
    }

    tcp_choices = {
        'ACK': '-sA',
        'FIN': '-sF',
        'Maimon': '-sM',
        'Null': '-sN',
        'SYN': '-sS',
        'Connect': '-sT',
        'Window': '-sW',
        'Xmas': '-sX'
    }

    nontcp_choices = {
        'UDP': '-sU',
        'IP': '-sO',
        'List': '-sL',
        'Ping': '-sn',
        'SCTP INIT': '-sY',
        'SCTP COOKIE-ECHO': '-sZ'
    }

    host = args.pop('host')
    port = args.pop('port')
    mode = args.pop('mode')
    tcp = args.pop('tcp')
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

    return host, port, arguments
