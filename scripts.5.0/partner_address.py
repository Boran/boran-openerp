##############################################################################
#
# partner_address.py
#   Tested with terp v4.2.2/python 2.5
#   add comments and user prints
#   Sean Boran 2008-05-05
#
# partner_address.txt Format:
# partner_id,title,firstname,lastname,street,city,zip,fax,phone,mobile,email,country_code
#
# Note that the partner_id must reference a current partner.
# use partners_list.py for example, to get ids.
#
# to do:
#   function, type
#   add event to say contact imported?
#   keys: where are categories? language
#   create partner if new?
#
# License: GNU General Public License v2
##############################################################################

import xmlrpclib
import csv
import datetime

db='prod_isp'     # Your DB
username='admin'
pwd = 'admin'  # 
host = 'localhost'
port = 8069

nr_cols=12   # we expect this number
#partner_id,title,firstname,lastname,street,city,zip,fax,phone,mobile,email,country_code


#uid = 4
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(db, username, pwd)
sock = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/object' % (host, port))

rowcount=0
reader = csv.reader(file('partner_address.txt').readlines(), delimiter=',')
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

    ids = sock.execute(db, uid, pwd, 'res.partner', 'search', [('id','=',row[0])])
    if not ids:
        print 'Skipping: This partner does not exist id=', row[0]
        continue

    ## country
    country=row[11]
    ids = sock.execute(db, uid, pwd, 'res.country', 'search', [('code','=',country)])
    if ids:
        countryid = ids[0]
        print 'Country', country, 'has id=', countryid
    else:
        print 'Country', country, 'not found (use default=Suisse/41)'
        countryid='41' 
        #id =  sock.execute(db, uid, pwd, 'res.country', 'create', {'name':row[4]})

    ## title
    title=row[1]         # the table below wants the name, not the index
    ids = sock.execute(db, uid, pwd, 'res.partner.title', 'search', [('shortcut','like',title)])
    if not ids:
        print 'Title', row[0], 'not found (use default=M.)'
        title='M.'        
        #id =  sock.execute(db, uid, pwd, 'res.partner.title', 'create', {'name':row[0]})    
    
    from datetime import date
    d = {
        'partner_id': row[0],
        'title': title,            
        'firstname': row[2],
        'lastname': row[3],         
        'street':  row[4],
        'city': row[5],
        'zip': row[6],
        'fax': row[7],
        'phone': row[8],   
        'mobile': row[9],   
        'email': row[10],
        'country_id': countryid
    }
    id =  sock.execute(db, uid, pwd, 'res.partner.address', 'create', d)
    print "id attributed=", id

