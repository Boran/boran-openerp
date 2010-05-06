#!/usr/bin/python
##############################################################################
#
# partners.py: Import partners.txt
#
# Changelog:
#   add comments and user prints
#   Sean Boran 2008-05-05: working with terp v4.2.2/python 2.5
#          based on example in svn \scripts\import\partners.py
#          add comments and user prints
#
# to do:
#   >> Does not work with Openerp5
#
#   'title' must match exactly a lookup list: why do we give an ID, not a name?
#   add event to say partner imported?
#   keys: where are categories? language
#   update partner if he already exists?
#
# partners.txt format:
# title,custcode,name,comment1,comment2,comment3,vat,website
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
##############################################################################

import xmlrpclib
import csv
import datetime


nr_cols=8   # we expect this number
#title,custcode,name,comment1,comment2,comment3,vat,website

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


rowcount=0
reader = csv.reader(file('partners.txt').readlines(), delimiter=',')
for row in reader:
    rowcount=rowcount+1
    if rowcount==1:            # skip title row
        print 'Title row (skipped):', row
        continue
    if len(row)<>nr_cols:
        print 'row skipped, there is not', nr_cols, 'columns', row
        continue
    print 'Row ', rowcount, row
    
    for r in range(len(row)):
        row[r] = (row[r] or '').decode('latin1')

    ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('name','=',row[1])])
    if ids:
        print 'Skipping: This partner name exists already id=', ids[0]
        continue
    ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('ref','=',row[2])])
    if ids:
        print 'Skipping: This partner reference exists already id=', ids[0]
        continue

    ids = sock.execute(db, uid, pwd, 'res.partner.title', 'search', [('shortcut','like',row[0])])
    if ids:
        titleid = ids[0]
        #print 'Title', row[0], 'has id=', id
        title=row[0]         # the table below wants the name, not the index
    else:
        print 'Title', row[0], 'not found (use default=M.)'
        title='M. '        
        #id =  sock.execute(db, uid, pwd, 'res.partner.title', 'create', {'name':row[0]})
    
    comment=''
    if len(row[3])>0:
        comment= comment +row[3] +'\n'
    if len(row[4])>0:
        comment= comment +row[4] +'\n' 
    if len(row[5])>0:
        comment= comment +row[5]
    #print comment

    from datetime import date
    d = {
        'title': title,            
        'name': row[1],
        'ref': row[2],         
        'comment': comment,
        'vat': row[6],
        'website': row[7]
        , 'date' : date.today().strftime("%Y-%m-%d")
    }
    id =  sock.execute(db, uid, pwd, 'res.partner', 'create', d)
    print "id attributed=", id

