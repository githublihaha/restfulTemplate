# check nmap argument hosts, only ipv4 and domain, not support ipv6!
import shlex
import re

arg = 'scanme.nmap.org/24 192.168.0.0/8 10.0.0,1,3-7.- '

pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)

class Ipv4Error(Exception):
    pass

class HostError(Exception):
    pass

def is_domain(value):
    return True if pattern.match(value) else False



def is_ipv4(value):

    print(value)
    parts = value.split('.')
    if (len(parts)==4):
        for part in parts:
            if (part.find(',') >= 0):
                comma_parts = part.split(',')
                for comma_part in comma_parts:
                    if (comma_part.find('-') >= 0):
                        bar_parts = comma_part.split('-')

                        if bar_parts[0] == '':
                            bar_parts[0] = 0
                        if bar_parts[1] == '':
                            bar_parts[1] = 255
                        for bar_part in bar_parts:
                            if not 0<=int(bar_part)<=255:
                                raise Ipv4Error
                        if int(bar_parts[0])>int(bar_parts[1]):
                            raise Ipv4Error
                    else:
                        if not 0<=int(comma_part)<=255:
                            raise Ipv4Error
            else:
                if (part.find('-') >= 0):
                        bar_parts = part.split('-')
                        if bar_parts[0] == '':
                            bar_parts[0] = 0
                        if bar_parts[1] == '':
                            bar_parts[1] = 255
                        for bar_part in bar_parts:
                            if not 0<=bar_part<=255:
                                raise Ipv4Error
                        if bar_parts[0]>bar_parts[1]:
                            raise Ipv4Error
                else:
                    if not 0<=int(part)<=255:
                        raise Ipv4Error
    else:
        raise Ipv4Error




def check_ipv4_or_domain(host):
    if  is_domain(host):
        code = 200
        message = 'host is domain'
        return code, message
    else:
        try:
            isIpv4 = is_ipv4(host)
        except Ipv4Error:
            code = 400
            message = 'host is not domain or Ipv4 address'
            return code, message
        else:
            code = 200
            message = 'host is Ipv4 address'
            return code, message




# return code, message
# 200 is ok
# 400 is error, check message
def check_host(arg):
    hosts = shlex.split(arg)

    # init return message
    code = 200
    message = ''

    # ip segment / 
    for host in hosts:
        ip_segment = host.split('/')
        # for example, 192.168.0.0/8
        # ip_segment[0] is 192.168.0.0
        # ip_segment[1] is 8

        length = len(ip_segment)
        if length == 2:
            if ((int(ip_segment[1]) < 0) or (int(ip_segment[1]) > 32)):
                code = 400
                message = 'wrong mask, between 0 and 32 for ipv4'
                return code, message
            else:
                code, message = check_ipv4_or_domain(ip_segment[0])
                if (code == 400):
                    return code, message
        elif length == 1:
            code, message = check_ipv4_or_domain(ip_segment[0])
            if (code == 400):
                return code, message
        else:
            return 400, 'host is wrong'

    return code, message

if __name__ == '__main__':
    code, message = check_host(arg)
    print(code)
    print(message)




    



