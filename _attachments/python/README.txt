TAPIRWIKI FULL TEXT INDEXING WITH XAPPY/XAPIAN 

The program files in this directory should be installed in a directory CouchDB has access to.
Make sure that this directory and the program files itself are owned by couchdb if you run couchdb as a daemon owned by that user.

To enable full text indexing with TapirWiki you must do the following:

1. Install the Xapian libraries through your package manager if not on your system yet. (on ubuntu sudo apt-get install python-xapian)

2. Instal easy_install if not on your system yet (on Ubuntu: sudo apt-get install python-setuptools python-dev build-essential).

3. Install the dependencies:

sudo easy_install couchDB 

sudo easy_install couchutil

sudo easy_install couchfti

sudo easy_install xappy

4. Unfortunately, as couchfti has a serious bug an the author has not yet updated (as of 2010-06-06) the module you need to replace the search.py program with the one in this directory. The file to be replaced can be found in the couchfti package directory of your python directory (perhaps /usr/local/lib/python2.6/dist-packages or /usr/lib/python2.5/site-packages) the couchfti directory could also be contained in the couchfti-0.1.2dev-py2.6.egg at that location.

5. Update local.ini of CouchDB (probably in /etc/couchdb) by adding the below lines between the dashes (please change the directory names appropriately):

-------------------------------------

[external]
fti=/usr/bin/python /opt/tapirwiki/twquery.py -d /opt/tapirwiki/xappy -l /opt/tapirwiki/twquery.log

[httpd_db_handlers]
_fti = {couch_httpd_external, handle_external_req, <<"fti">>}

[update_notification]
indexer = /usr/bin/python /opt/couchfti-indexing/twindex.py -d /opt/tapirwiki/xappy -l /opt/tapirwiki/xappy/twindex.log


--------------------------------------

6. Add the Search system page to your menu in TAPIRWIKISETTINGS 

