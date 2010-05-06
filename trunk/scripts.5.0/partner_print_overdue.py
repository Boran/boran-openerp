#!/usr/bin/python
##############################################################################
#
# partner_print_overdue.py
# Issues: header/footer are not printed.
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

partner_ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('name','=','Swisscom Innovations')], 0, 1)
partners    = sock.execute(db, uid, pwd, 'res.partner', 'read', partner_ids,
  ['name','credit','state','partner_id','comment','date','user_id','active'])

for partner in partners:
  print "\nPartner", partner['id'], ":", partner

  part_id=partner['id']
  filename='/tmp/paymentdue' +str(part_id) +'.pdf'
  print 'Printing Payment Due to file ', filename

  # print  to PDF: get report id, wait, calls report, wait, save as pdf
  #id_report = printsock.report(db, uid, pwd, 'res.partner', partners, {'model': 'account.overdue', 'id': part_id, 'report_type':'pdf'})
  id_report = printsock.report(db, uid, pwd, 'account.overdue', partners, {'model': 'account.overdue', 'id': part_id, 'report_type':'pdf'})
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

#eof
