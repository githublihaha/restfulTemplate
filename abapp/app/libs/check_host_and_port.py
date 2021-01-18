from . import check_host
from . import check_port
from . import get_host_port_arguments

def check_host_and_port(args):

    # init return code, message
    code = 200
    message = ''

    host, port, arguments = get_host_port_arguments.get_host_port_arguments(args)


    code, message = check_host.check_host(host)
    if (code == 400):
        # host is wrong
        return code, message
    else:
        # host is right
        if port is not None:
            # check ports
            if (arguments.find('sO') >= 0):
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
        else:
            return code, message

        return code, message

