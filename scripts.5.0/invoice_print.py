#!/usr/bin/python
##############################################################################
#
# invoice_print.py   print the first open invoice found into a PDF file.
# Issues: header/footer are not printed. This not the same necessarily as the 
#         original invoice (see alo attachments), if for example the address has changed.
#
# Changelog:
#   Sean Boran 2010.04.27
#
# GNU General Public License
##############################################################################

import xmlrpclib

nr_invs=1        # how many do we want to see
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
printsock = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/report' % (host, port))
import time
import base64

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
        filename='/tmp/invoice' +str(inv_nr) +'.pdf'
        print 'Printing invoice to file ', filename

        # print the Invoice to PDF: get report id, wait, calls report, wait, save as pdf
        id_report = printsock.report(db, uid, pwd, 'account.invoice', invoice_ids, {'model': 'account.invoice', 'id': inv_nr, 'report_type':'pdf'})
        time.sleep(5)
        state = False
        attempt = 0
        while not state:
            report = printsock.report_get(db, uid, pwd, id_report)
            state = report['state']
            if not state:
              time.sleep(1)
              attempt += 1
            if attempt>200:
              print 'Printing aborted, too long delay !'

            string_pdf = base64.decodestring(report['result'])
            file_pdf = open(filename,'w')
            file_pdf.write(string_pdf)
            file_pdf.close()

    print "\n"    
    i += 1

#eof
