#!/usr/bin/python
##############################################################################
#
# mass_partners.py
#
# FUNCTION: Pump many new 'random' Partners into Openerp
#    (with contacts, addresses, invoices and detail lines)
#    This script allows many many partners to be generated, 
#    for scalability tests:
#
# Changelog:
#   Sean Boran 2009.09.02: working with terp v5.0.2
#
# Issues: See TBD below. Contact inserting has been disable because 
#         partner_id is being ignored after inserting.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
##############################################################################

# --- settings
cust1=1000;    # start reference/index for customer names
custn=2999;    # stop index (=> cust1-custn= how many partners to add)
  # So cust1=1000 custn=2999 would generate 3000 partners


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


# Debugging
#import sys
#sys.exit()

from datetime import date
for i in range (cust1, custn):
  d = {
    #'title': 'Mr.',
    'name' : 'Sample Customer' +str(i),
    'ref'  : 'cust' +str(i),
    'comment': 'Autogenerated partner by part_pump.py: index ' +str(i),
    'vat': 'CH 123456-' +str(i),
    'website': 'www.sample.ch',
    'date' : date.today().strftime("%Y-%m-%d")
  }

  # Insert a new partner, but avoid duplicates
  ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('ref','=',d['ref'])])
  if ids:
        print 'Skipping: This partner name exists already id=', ids[0]
        continue
#
  pid =  sock.execute(db, uid, pwd, 'res.partner', 'create', d)
  print d
  print "Inserted " +d['ref'] +", id attributed=", pid

  # Insert address for that partner
  a = {'name': 'cust' +str(i), 'city': 'Bern', 'fax': '+41 123456', 'zip': '3050', 'country_id': 41, 'email': 'user' +str(i) +'@sample.com', 'phone': '+41 123456', 'street': 'MyStreet, 40', 'partner_id': pid}
  #print a
  aid =  sock.execute(db, uid, pwd, 'res.partner.address', 'create', a)
  print "Inserted address, id attributed=", aid

  # Insert a contact for that partner
  # TBD: The partner_id is ignored and these contacts end up orphaned.
  #c = {'website': 'www.sample.com', 'first_name': 'Joe', 'name': 'Bloggs', 'mobile': '+41 123456', 'country_id': 41, 'email': 'user1@sample.com', 'partner_id': pid}
  #print c
  #cid =  sock.execute(db, uid, pwd, 'res.partner.contact', 'create', c)
  #print "Inserted contact, id attributed=", cid



