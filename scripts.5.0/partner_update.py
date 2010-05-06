#!/usr/bin/python
##############################################################################
#
# partner_update.py
#
# Example for updating the filed named update_field to the value update_value 
#         for a partner with the name search_name
#
# Changes:
# Sean Boran 2010-04-27
#
##############################################################################

import xmlrpclib
import csv
import datetime

search_name='Cisco';
update_field='comment';
import random
update_value='test write: foo() #' +  random.choice('1234567890')

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


print "------ Write " + update_field +"=" +update_value +" for customer name=" +search_name +"------"
partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('name', '=', search_name)], 0, 5)
#print "Partners found:", (partner_ids)

partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids,
  ['state','partner_id','name','title','ref','comment','vat','website','date','user_id','active','ean13'])

for partner in partners:
  print "Partner", partner['id'], " current:", partner
  result = sock.execute(db, uid, pwd, 'res.partner', 'write', partner['id'], {update_field : update_value})
  print result;
  partner= sock.execute(db, uid, pwd, 'res.partner', 'read', partner['id'],
    ['state','partner_id','name','title','ref','comment','vat','website','date','user_id','active','ean13'])
  print "Partner", partner['id'], " new:", partner


