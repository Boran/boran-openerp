##############################################################################
#
# partner_contact_list.py: 
#
# List first 5 contacts and their fields.
#
# Changes:
# Sean Boran 2009-09-03 
#
# to do:
#
##############################################################################

import xmlrpclib
import csv
import datetime

## Read DB settings from the config file
import ConfigParser, os
config = ConfigParser.ConfigParser()
config.read(['openerp.cfg', os.path.expanduser('~/.openerp.cfg')])
db      =config.get('dbaccess','db')
username=config.get('dbaccess','username')
pwd     =config.get('dbaccess','pwd')
host    =config.get('dbaccess','host')
port    =config.getint('dbaccess','port')

sock_common = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/common' % (host, port))
uid = sock_common.login(db, username, pwd)
sock = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/object' % (host, port))

print "----------------------------------------"
partner_ids = sock.execute(db, uid, pwd, 'res.partner.contact', 'search', [], 0, 250)
print "First 5 contacts found:", (partner_ids), "\n"

partners    = sock.execute(db, uid, pwd, 'res.partner.contact', 'read', partner_ids,
  [])
for partner in partners:
        print "contact", partner['id'], ":", partner


