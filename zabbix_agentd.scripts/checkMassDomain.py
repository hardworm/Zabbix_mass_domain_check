#!/usr/bin/python3

import whois, sys, getopt, json
from datetime import date, datetime


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:d:", ["ifile=", "domain="])
    except getopt.GetoptError:
        print('checkMassDomain.py -i <inputfile> -d <domain>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('checkMassDomain.py -i <inputfile> -d <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            get_list_domain(inputfile)
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
            get_domain_info(domain)
            sys.exit()


def get_list_domain(file):
    list_domain = []
    try:
        f = open(file, 'r')
    except:
        print('File ' + file + ' not be read')
        sys.exit()

    for line in f:
        if len(line) > 3:
            list_domain.append(line.strip())

    print(json.dumps(list_domain))
    return True


def get_domain_info(domain):
    try:
        info = whois.query(domain)
        diff_expiration = info.expiration_date - datetime.today()
        diff_create = datetime.today() - info.creation_date

        info.expiration_date_diff = diff_expiration.days
        info.create_date_diff = diff_create.days
        info.name_servers = ', '.join(info.name_servers)

        print(json.dumps(info.__dict__, default=json_serial))
    except:
        print('error')
        sys.exit()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


if __name__ == "__main__":
    main(sys.argv[1:])
