#!/usr/bin/python
##############################################################################
#
# partners_export.py
#
# Export first 3 addresses of first 5 partners to a CSV file
#
# Changes:
# Sean Boran 2010.05.17
#
##############################################################################

import xmlrpclib
import csv
import datetime

## Read DB settings from the config file
import ConfigParser, os
config = ConfigParser.ConfigParser()
config.read(['openerp.cfg', os.path.expanduser('~/.openerp.cfg')])
#print config.items('dbaccess')
db      =config.get('dbaccess','db')
username=config.get('dbaccess','username')
pwd     =config.get('dbaccess','pwd')
host    =config.get('dbaccess','host')
port    =config.getint('dbaccess','port')

sock_common = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/common' % (host, port))
uid = sock_common.login(db, username, pwd)
sock = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/object' % (host, port))


#------------
partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [], 0, 3)
print "First few Partners found:", (partner_ids), "\n"

#pfields =['id','name','active']
pfields =['id','name','credit','debit','state','title','ref','comment','date','active']

#partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids)
partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids, pfields)

#writer = csv.writer(open('partners_export.csv', 'w'), delimiter=',')
#writer.writerow(pfields)
#writer = csv.DictWriter(open('partners_export.csv', 'a'), pfields, delimiter=',')
writer = csv.DictWriter(open('partners_export.csv', 'w'), pfields, delimiter=',', dialect='excel')
# header row
writer.writerow( dict( zip(pfields, pfields) ) )

for partner in partners:
  #print "Partner", partner['id'], ":", partner
  writer.writerow(dict(partner))


