#!/usr/bin/python
##############################################################################
#
# invoice_create.py
#   Create a new invoice
#
# Changelog:
#   Sean Boran 2008-05-06: Tested with terp v4.2.2/python 2.5
#   Sean Boran 2009-09-01: Tested with terp v5.0.2
#
# GNU General Public License
##############################################################################

import xmlrpclib
import datetime
from datetime import date

print "----------------------------------------"
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

invoice  = {
    'type': 'out_invoice',
    'state': 'draft',
    'origin': 'import xmlrpc',
    'account_id': 2,          # Creances envers des tiers suisses
    'date_invoice': date.today().strftime("%Y-%m-%d"),   # today

    # Change the following each time:
    'name' : '2008/Axxx',   # TBD
    'partner_id': 3,          # Customer: Francine lavoine
    'address_invoice_id': 2,  # Address: 24, 'Lavoine Bill'
    'amount_total': 22.33     # ignored if there are no lines, needed?
}
# Account IDs are lookedup in Pgadmin
## TBD: amount_tax, comment, address_contact_id
## name, generate 'number' (i.e. sequential)
## inv lines: below
## Defaults: company_id=currency_id=journal_id=1

invoice_id = sock.execute(db, uid, pwd, 'account.invoice', 'create', invoice)
print 'Invoice id=', invoice_id, 'added'

line1 = {
    'invoice_id': invoice_id,
    'account_id': 6,     # 3210 - Ventes brutes au comptant
    'name': 'Internet traffic, in MB',
    'product_id': 2,     # Product id with 2
    # Change the following each time:    
    'price_unit': 0.5,  # get it to take this from the product code?
    'quantity': 150.0
}
## TBD: note, account_analytic_id, sequence
line_id = sock.execute(db, uid, pwd, 'account.invoice.line', 'create', line1)
print 'Invoice line id=', line_id, 'added'

# TBD: taxes


#eof
