import re
from . import get_nmap_services

ports = 'U:53,111,137,T:21-25,80,139,8080,S:1023,[244-250],1024,[-199],http*,-1037,122-12'
ports = 'U:53,111,137,T:21-25,80,139,8080,S:1023,[244-250],1024,[-199],http*,-1037'

#ports = '[-235,1026],'
# sudo nmap 127.0.0.1 -sU -sS -sY  -p U:53,111,137,T:21-25,80,139,8080,S:1023,1024,http*



class PortError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



def check_port_int(port):
    try:
        port_int = int(port)
    except ValueError:
        return False
    else:
        if 0<=port_int<=65535:
            return True
        else:
            return False





def check_port_nmap_services(port):
    re_temp = port
    new_data_list = list(filter(lambda x: re.match(re_temp, x) != None, get_nmap_services.ports))
    if (len(new_data_list) == 0):
        return False
    else:
        return True




def check_no_colon(port, port_list, flag):
    if (port.find('-')>=0):
        # has -
        port_part = port.split('-')
        if (len(port_part)!=2):
            raise PortError('PortError: wrong port with -')
        else:
            if port_part[0]:
                try:
                    port_part_0_int = int(port_part[0])
                except ValueError:
                    #not int, check if is namp-service name
                    # re_temp = port
                    # new_data_list = list(filter(lambda x: re.match(re_temp, x) != None, get_nmap_services.ports))
                    # if (len(new_data_list) == 0):
                    #     raise PortError('PortError: wrong service name')
                    if not check_port_nmap_services(port):
                        raise PortError('PortError: wrong service name')

                else:
                    #port[0] is int
                    if port_part[1]:
                        try:
                            port_part_1_int = int(port_part[1])
                        except ValueError:
                            raise PortError('PortError: wrong port with - [2]')
                        else:
                            if (port_part_1_int>=port_part_0_int):
                                port_list.append(port_part_0_int)
                                port_list.append(port_part_1_int)
                            else:
                                raise PortError('PortError: the port in right must be bigger than the port in left')
                    else:
                        port_list.append(port_part_0_int)

            else:
                if port_part[1]:
                    try:
                        port_part_1_int = int(port_part[1])            
                    except ValueError:
                        raise PortError('PortError: wrong nmap-services name or wrong port')
                    else:
                        # part 1 is int
                        if (flag == 0):
                            raise PortError('PortError: port must not be negative')  
                        else:
                            port_list.append(port_part_1_int)
                else:
                    #port_part[1] in ''
                    pass


    else:
        # no -
        try:
            port_int = int(port)
            #port_list.append(port_int)
        except ValueError:
            #port is not int
            #port has - or is in nmap-services
            re_temp = port
            new_data_list = list(filter(lambda x: re.match(re_temp, x) != None, get_nmap_services.ports))

            if (len(new_data_list) == 0):
                raise PortError('PortError: wrong service name')
        else:
            # no exception
            # judge the range of int_port
            if (0<=port_int<=65535):
                port_list.append(port_int)
            else:
                #port not in right range
                raise PortError('PortError: port not in right range')





def check_port(ports,ip_flag):
    # flag
    ip  = 0
    tcp = 0
    udp = 0
    sctp= 0
    nmap_service = 0

    # store ports 
    port_list = []

    # check [ ]
    # remove [ ]
    pattern = re.compile('\[(.*?)\]')
    pattern_list = pattern.findall(ports)
    for item in pattern_list:
        ports = ports.replace('[' + item + ']','')
    pattern_list.append(ports)


    # 
    for pattern_list_item in pattern_list:
        for port in pattern_list_item.split(','):
            if port is not None:
                if (port.find(':')>=0):
                    colon_parts = port.split(':')
                    if len(colon_parts)!=2:
                        raise PortError('PortError: unknown :')
                    else:
                        if colon_parts[0] == 'U':
                            udp = 1
                        elif colon_parts[0] == 'T':
                            tcp = 1
                        elif colon_parts[0] == 'S':
                            sctp = 1
                        elif colon_parts[0] == 'P':
                            ip = 1
                        else:
                            raise PortError('PortError: unknown protocol name, use U,T,S or P')
                        check_no_colon(colon_parts[1], port_list, 1)
                else:
                    check_no_colon(port, port_list, 1)

    if (ip == 1 or ip_flag == 1):
        for item in port_list:
            if item>255:
                raise PortError('PortError: if ip is set, port must be in range of 1-255')

    return port_list

if __name__ == '__main__':
    print(check_port(ports,0))
