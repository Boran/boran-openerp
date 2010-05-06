#!/usr/bin/python
##############################################################################
#
# mass_invoices.py
#   Create a draft invoice, one for each customer.
#   Used together with mass_partners.py to stress test Openerp by 
#   creating (hundreds of) thousands on Invoices.
#
# Changelog:
#   Sean Boran 2000-09-04: Tested with v5.0.2
#
# Issues: See TBDs below, the invoice could be more complete.
#
# GNU General Public License
##############################################################################

## Customise these:
nr_partners=3000000   # first N customers to process, so 1000 means max 1000 invoices
#--------------

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


print "----- Find first " +str(nr_partners) +" partners -----------------------"
partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [], 0, nr_partners)
print "  Partners found:", (partner_ids), "\n"

partners = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids,
  ['partner_id','name'])

# Debugging
#import sys
#sys.exit()
pcount=0

for partner in partners:
  pcount=pcount+1
  print "Partner ", partner['id'], ":", partner
  pid=partner['id']

  invoice  = {
    'type': 'out_invoice',
    'state': 'draft',
    'origin': 'import',
    'account_id': 2,          # Creances envers des tiers suisses
    'date_invoice': date.today().strftime("%Y-%m-%d"),   # today
    #TBD: 'date_due': (date.today()+datetime.timedelta(days=30)).strftime("%Y-%m-%d"),   

    'name' : 'Internet Month ' +date.today().strftime("%Y-%m") +'/' +str(pid),
    'partner_id': pid,         # Customer: Francine lavoine
    'address_invoice_id': 1,  # First Address
    'amount_total': 22.33     # ignored if there are no lines, needed?
  }
  ## TBD: amount_tax, comment, address_contact_id
  ## name, generate 'number' (i.e. sequential)
  ## inv lines: below
  ## Defaults: company_id=currency_id=journal_id=1
  invoice_id = sock.execute(db, uid, pwd, 'account.invoice', 'create', invoice)
  #print 'Invoice id=', invoice_id, 'added'

  # add 5 Detail lines
  for j in range (1, 6):
    line1 = {
        'invoice_id': invoice_id,
        'account_id': 6,     # 3210 - Ventes brutes au comptant
        'name': 'Internet traffic #' +str(j),
        'product_id': 2,     # Some product
        'price_unit': 0.5 +j,
        #'quantity': 5.0 *j
        'quantity': pcount *j
    }
    ## TBD: note, account_analytic_id, sequence
    line_id = sock.execute(db, uid, pwd,
        'account.invoice.line', 'create', line1)
    #print 'Invoice line id=', line_id, 'added'

    # TBD: taxes


#eof
