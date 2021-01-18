ports = []
with open('app/libs/nmap-services', 'r') as f:
    for line in f.readlines():
        if not line[0] == '#':
            service = line.split('\t')
            if not service[0] in ports:
                ports.append(service[0])

if __name__ == "__main__":
    print(ports)