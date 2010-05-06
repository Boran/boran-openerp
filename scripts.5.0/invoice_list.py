#!/usr/bin/python
##############################################################################
#
# invoice_list.py
#   List first 2 invoices (headers). For an invoices in the 'open' state,
#   list the detail lines and taxes too.
#
# Changelog:
#   Sean Boran 2008-05-06: Tested with terp v4.2.2/python 2.5
#   Sean Boran 2009-09-01: Tested with terp v5.0.2
#
# GNU General Public License
##############################################################################

import xmlrpclib

nr_invs=2        # how many do we want to see
#lookfor='draft'   # open/draft: show details for invoices in this status
lookfor='open'   # open/draft: show details for invoices in this status



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


print "----------------------------------------"

invoice_ids = sock.execute(db, uid, pwd, 'account.invoice', 'search', [], 0, nr_invs)
print "First " +str(nr_invs) +" Invoices found:", (invoice_ids), "\n"

invoices = sock.execute(db, uid, pwd, 'account.invoice', 'read', invoice_ids,
  [])
# if only for specific fields:
# ['state','partner_id','type','date_invoice','amount_total','currency_id','address_invoice_id','account_id'])
#print "Invoice states: ",(invoices)

print "Looking for", lookfor, "invoices:\n"
total = len(invoices)
i = 0
for invoice in invoices:
    print "Invoice ", invoice['id'], ":", invoice
    if invoice['state'] == lookfor:
        # Print the detail lines for those invoices
        inv_nr=invoice['id']
        print '>>>> draft invoice id:', inv_nr
        line_ids = sock.execute(db, uid, pwd, 'account.invoice.line', 'search',
                                [('invoice_id','=',inv_nr)])
        if line_ids:
            print ">>>> line_ids found:", (line_ids)
            lines = sock.execute(db, uid, pwd, 'account.invoice.line', 'read', line_ids,
  [])
  #['id','name','note','price_unit','product_id','quantity','account_id'])
            #print ">>>> Lines: ", lines
            for line in lines:
                print ">>>> Line: ", line
                #taxids = sock.execute(db, uid, pwd, 'account.invoice.line.tax', 'search', [('invoice_line_id','=',line['id'])])
                #print ">>>> Tax id:", taxids
        else:
            print ">>> No lines found\n"

        taxesids = sock.execute(db, uid, pwd, 'account.invoice.tax', 'search', [('invoice_id','=',inv_nr)])
        taxes = sock.execute(db, uid, pwd, 'account.invoice.tax', 'read', taxesids,
                             [])
                             #['id','base_amount','name','tax_amount'])
        print ">>>> Taxes:", taxes

    print "\n"    
    i += 1

#eof
