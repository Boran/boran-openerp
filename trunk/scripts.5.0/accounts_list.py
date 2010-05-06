#!/usr/bin/python
##############################################################################
#
# accounts_list.py
#
# List fin. accounts and tax codes
#
# Changes:
# Sean Boran 2010-02-24  FCS for Openerp5.06
#
#
##############################################################################

import xmlrpclib
import csv
import datetime
import sys

debuglevel=3
amount=4000     # number of accounts to list

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

def quitnow():
    print "Debug: quitting now!"
    sys.exit(1)
    return

  ## Print accents in a string
def t(string):
  if type(string) == unicode:
    #return string.encode("utf-8")
    return string.encode("latin1")
  return string

def debug(msg, level=1):
  global debuglevel
  if debuglevel>=level:
    print t(msg)


print "----- List account ids -----------------------------------"
account_ids = sock.execute(db, uid, pwd, 'account.account', 'search', [], 0, amount)
print "Searching for " ,amount ," accounts:", "\n"
#print "First " ,amount ," found:", (account_ids), "\n"
accounts=sock.execute(db, uid, pwd, 'account.account', 'read', account_ids, ['id','name','code'])
for account in accounts:
  print "account", account['id'], ":", account['code'], ":", t(account['name'])

print "\n\n TAX accounts found:", "\n"
account_ids = sock.execute(db, uid, pwd, 'account.tax', 'search', [], 0, amount)
accounts=sock.execute(db, uid, pwd, 'account.tax', 'read', account_ids, [])
for account in accounts:
  print "account", account['id'], ":", account['type_tax_use'], ":", t(account['name']), ":", account['amount']



