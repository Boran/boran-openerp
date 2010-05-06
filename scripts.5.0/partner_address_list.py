##############################################################################
#
# partner_address_list.py: 
#
# List first 5 partners and their fields.
#
# Changes:
# Sean Boran 2008-05-05  For Tinyerp 4.2
#            2009-07-22  Also works on Openerp5
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
partner_ids = sock.execute(db, uid, pwd, 'res.partner.address', 'search', [], 0, 5)
print "First 5 Partners found:", (partner_ids), "\n"

partners    = sock.execute(db, uid, pwd, 'res.partner.address', 'read', partner_ids,
# Get all fields:
  [])
#Only specific fields:
#  ['title','partner_id','firstname','lastname','street','city','zip','fax','phone','mobile','email','country_id','comment'])
for partner in partners:
        print "partner address", partner['id'], ":", partner


