#!/usr/bin/python
##############################################################################
#
# attach_list.py
#   List first 6 attachements (headers).
#
# Changelog:
#   Sean Boran 2010.05.04
#
# GNU General Public License
##############################################################################

import xmlrpclib

count=5        # how many do we want to see


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
attach_ids = sock.execute(db, uid, pwd, 'ir.attachment', 'search', [], 0, count)
print "First " +str(count) +" Attachments found:", (attach_ids), "\n"
print "Name, title, model, partner, filename, id:\n"

attachs = sock.execute(db, uid, pwd, 'ir.attachment', 'read', attach_ids, [])
for attach in attachs:
    #print "attach ", attach['id'], ":", attach
    print attach['name'], ":", attach['title'], ":", attach['res_model'], ":",attach['partner_id'], ":",attach['store_fname'], ": ID=", attach['id'], "\n"


#eof
