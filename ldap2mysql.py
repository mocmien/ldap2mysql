#!/usr/bin/env python
# encoding: utf-8

# Author:   Nguyen Van Minh <nguyenvanminh_at_gmail.com>
# Purpose:  Read something from Iredmail Ldap then update to MySql
# Note:		You can change ldap attributes (line 43) and queuery command of mysql base on yours
# Date:     2015-04-20

import sys
import ldap
import MySQLdb, string

# Note:
#   * bind_dn must have write privilege on LDAP server.
uri = 'ldap://127.0.0.1:389'
basedn = 'dc=domainname,dc=com,dc=vn'
bind_dn = 'cn=Manager,dc=domainname,dc=com,dc=vn'
bind_pw = 'con gai 20 02 2009'

# Initialize LDAP connection.
print >> sys.stderr, "* Connecting to LDAP server: %s" % uri
conn = ldap.initialize(uri=uri, trace_level=0,)
conn.bind_s(bind_dn, bind_pw)

db = MySQLdb.connect(host = 'localhost', user = 'user', \
    passwd = 'password', db = 'database_name')

if (db):
    print "Connection successful"
else:
    return


# Creation of a cursor
cursor = db.cursor()
cursor.execute ("select contact_email,contact_mobile from tblcontacts limit 100")
# Get all mail users.
print >> sys.stderr, "* Get all mail accounts..."

allUsers = conn.search_s(basedn,
                         ldap.SCOPE_SUBTREE,
                         "(objectClass=mailUser)",
                         ['mail', 'mobile'])
total = len(allUsers)
#print allUsers
print >> sys.stderr, "* Total %d user(s)." % (total)

# Values of 'enabledService' which need to be added.
services = ['indexer-worker']

# Counter.
count = 0

for user in allUsers:
    (dn, entry) = user
    luser = len(entry)
    if luser == 2:
        mail = entry['mail'][0]
        mobile = entry['mobile'][0]
#        print >>  sys.stderr, "* ( email %s have mobile %s" % (mail,mobile)
#        cursor.execute ("update tblcontacts set contact_mobile = %s  where contact_email = %s", (mobile,mail))
        cursor.execute ("select contact_mobile, contact_email from tblcontacts where contact_email = %s", (mobile,mail))
#        cursor.connection.commit()
        row =
        count += 1
#print >> sys.stderr, " Total %d have email mobile" % (count)

#Unbind Mysql
# Close the cursor
cursor.close()
# Unbind connection.
print >> sys.stderr, "* Unbind LDAP server."
conn.unbind()

print >> sys.stderr, "* Update completed."
