#!/usr/bin/python
##############################################################################
#
# partners_list.py
#
# List first 3 addresses of first 5 partners
#
# Changes:
# Sean Boran 2008-05-05  For Tinyerp 4.2
#            2009-07-22  Also works on Openerp5
#            2010-02-24  Tweaks. Use 'openerp.cfg'
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


print "----- List first 2 addresses of the first 5 partners -----------------------------------"

partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [], 0, 10)
print "First 5 Partners found:", (partner_ids), "\n"

#partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids)
partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids,
  ['name','credit','debit','state','partner_id','title','ref','comment','date','user_id','active'])

for partner in partners:
  print "\nPartner", partner['id'], ":", partner
  addr_ids = sock.execute(db, uid, pwd, 'res.partner.address', 'search', [('partner_id','=',partner['id'])], 0, 2)
  print "Addresses found:", (addr_ids), "" 

  # Get specific fields:
  #addrs    = sock.execute(db, uid, pwd, 'res.partner.address', 'read', addr_ids,
  #  ['id','type','title','firstname','lastname','street','city','zip','phone','email'])
  #addrs    = sock.execute(db, uid, pwd, 'res.partner.address', 'read', addr_ids,
  #  ['id','private_phone', 'firstname','lastname','street'])
  # Get ALL fields:
  addrs    = sock.execute(db, uid, pwd, 'res.partner.address', 'read', addr_ids)

  for addr in addrs:
    print "Contact", addr['id'], ":", addrs


