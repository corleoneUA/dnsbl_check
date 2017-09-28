import dns.resolver
import sys
import os

blk_file_name = 'blklist'
# Your IP's for check
IP = ['8.8.8.8', '8.8.4.4']

#Read file
blk_File = open(os.path.join(os.path.dirname(sys.argv[0]), blk_file_name))

#Add to array
with blk_File as f:
    list = f.readlines()
    list = [x.strip() for x in list]


for bl in list:
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        for i in IP:
            query = '.'.join(reversed(str(i).split("."))) + "." + bl
            answers = resolver.query(query, "A")
            answer_txt = resolver.query(query, "TXT")
            print('IP: %s is listed in %s (%s: %s)' %(i, bl, answers[0], answer_txt[0]))
    except dns.exception.Timeout:
        print(bl +' is not available')
    except dns.resolver.NXDOMAIN:
        print('IP: %s is NOT listed in %s' %(IP, bl))
