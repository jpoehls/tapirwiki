TAPIRWIKI FULL TEXT INDEXING WITH XAPPY/XAPIAN 

The program files in this directory should be copied into a directory the process running CouchDB has access to.
Make sure that permissions on the program files allow the user in which name that process is running (usually a user called couchdb) to read the program files.

To enable full text indexing with TapirWiki please do the following:

1. Install the Xapian libraries through your package manager if not on your system yet. (on ubuntu sudo apt-get install python-xapian)

2. Instal easy_install if not on your system yet (on Ubuntu: sudo apt-get install python-setuptools python-dev build-essential).

3. Install the dependencies:

   sudo easy_install couchDB 

   sudo easy_install xappy

4. To be able to index/search PDF documents install pdftotext (most linux distributions have this included in the standard distribution)

5. MSWord indexing/searching requires the program antiword installed.

6. Indexing/searching Excel, PowerPoint or RTF files requires catlog installed.

7. Update local.ini of CouchDB (probably in /etc/couchdb) by adding the below lines between the dashes (please change the directory names appropriately):

-------------------------------------

[external]
fti=/usr/bin/python /opt/tapirwiki/twquery.py -d /opt/tapirwiki/xappy -l /opt/tapirwiki/twquery.log
aix=/usr/bin/python /opt/couchfti-indexing/twindxatt.py -d /opt/couchfti-indexing/xappy -l /opt/couchfti-indexing/xappy/indexatt.log

[httpd_db_handlers]
_fti = {couch_httpd_external, handle_external_req, <<"fti">>}
_aix = {couch_httpd_external, handle_external_req, <<"aix">>}


[update_notification]
indexer = /usr/bin/python /opt/couchfti-indexing/twindex.py -d /opt/tapirwiki/xappy -l /opt/tapirwiki/xappy/twindex.log

--------------------------------------

8. Add the Search system page to your menu in TAPIRWIKISETTINGS 

9. Enable attachment indexing in TAPIRWIKISETTING

