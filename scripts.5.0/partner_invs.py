#!/usr/bin/python
##############################################################################
#
# partner_invs.py
# List open invoices for a specific partner
#
# Changelog:
#   Sean Boran 2010.04.27
#
# GNU General Public License
##############################################################################

import xmlrpclib

nr_invs=5        # how many do we want to see
partnername='Mycompany'
lookfor='open'   # open/draft: show details for invoices in this status
#lookfor='draft'   # open/draft: show details for invoices in this status



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
######

partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('name','=',partnername)], 0, 4)
partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids,
  ['name','credit','state','partner_id','comment','date','user_id','active'])

for partner in partners:
  #print "\nPartner", partner['id'], ":", partner
  print "\nPartner name/credit/id:", partner['name'], ",", partner['credit'], ",", partner['id']

  invoice_ids = sock.execute(db, uid, pwd, 'account.invoice', 'search', [('partner_id','=',partner['id'])], 0, nr_invs)
  invoices = sock.execute(db, uid, pwd, 'account.invoice', 'read', invoice_ids, [])
  print "Invoices: (date/number/amount/residual/name)"
  for invoice in invoices:
    #print "Invoice ", invoice['id'], ":", invoice, "\n"
    if invoice['state'] == lookfor:
      # Print the detail lines for those invoices
      inv_nr='INV'+ str(invoice['number']).replace('/','')
      print invoice['date_invoice'], inv_nr, ",", invoice['amount_total'], ",", invoice['residual'], ",", invoice['name'], ",", invoice['state']

      # find invoice attachments
      attach_ids = sock.execute(db, uid, pwd, 'ir.attachment', 'search', [('partner_id','=',partner['id']), ('name','=',inv_nr)], 0, nr_invs)
      attachs = sock.execute(db, uid, pwd, 'ir.attachment', 'read', attach_ids, [])
      for attach in attachs:
        #print "attach ", attach['id'], ":", attach
        print attach['name'], ":", attach['title'], ":",attach['store_fname']

"""  ## All attachements
  print "Attachments: (name/title/path)"
  attach_ids = sock.execute(db, uid, pwd, 'ir.attachment', 'search', [('partner_id','=',partner['id'])], 0, nr_invs)
  attachs = sock.execute(db, uid, pwd, 'ir.attachment', 'read', attach_ids, [])
  for attach in attachs:
    #print "attach ", attach['id'], ":", attach
    print attach['name'], ":", attach['title'], ":",attach['store_fname']
"""


#eof

