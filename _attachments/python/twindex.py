#! /usr/bin/env python
#
# twindex.py - TapirWiki full text indexing with couchfti, xappy, xapian
# Copyright (C) 2010 Jeroen Vet jeroen.vet@gmail.com (on changes only)
# based on couchdb-xapian-indexer (C) Paul J. Davis 
# adapted for use with couchfti (which uses Xappy to manage Xapian indices)
# to enable advanced full text indexing and search for TapirWiki
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.



from couchfti import index
import xappy
import couchdb
import time
from optparse import OptionParser, make_option
import logging
import os
import sys
import simplejson

def wikipageclassifier(doc):
    if 'type' in doc:
        if doc['type']=='page':
            return "wikipage"
    return None

def wikipagefactory(db, cdbdoc):
    doc=xappy.UnprocessedDocument()
    doc.id=cdbdoc['_id']
    doc.fields.append(xappy.Field('body', cdbdoc['body']))
    doc.fields.append(xappy.Field('edited_by', cdbdoc['edited_by']))
    dt=time.strptime(cdbdoc['edited_on'][:24],"%a %b %d %Y %H:%M:%S")
    dts=time.strftime("%Y-%m-%d",dt)
    doc.fields.append(xappy.Field('edited_on', dts))
    return doc 

   
indexes= { 'wikipageidx':{ 'classifier': wikipageclassifier, # types of doc in index is determined by the classifier
                           'factories': { 'wikipage' : wikipagefactory  # each type of doc has its own factory
                                         }, 
                           'fields'   : [
                                         (['body', xappy.FieldActions.INDEX_FREETEXT], {'language':'en'}),
					 (['body', xappy.FieldActions.STORE_CONTENT], {}),
                                         (['edited_by', xappy.FieldActions.INDEX_EXACT], {}),
                                         (['edited_by', xappy.FieldActions.STORE_CONTENT], {}),
                                         (['edited_on', xappy.FieldActions.SORTABLE], {'type':'date'}),
                                         (['edited_on', xappy.FieldActions.STORE_CONTENT], {})
                                        ],
                           'path'     : "tapirwiki.idx"
                         }
         }

def updates():
    line = sys.stdin.readline()
    while line:
        if not line:
            return
        obj = simplejson.loads(line)
        yield obj
        line = sys.stdin.readline()

def main(dir, url, exclude):
    couch=couchdb.Server(url)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    indices = {} #these indices hold the (xappy) indexer objects
    for update in updates():
        db = couch[update['db']]
        if db.name in exclude:
            continue
        if db.name not in indices:
            indices[db.name] = index.Indexer(db, os.path.join(dir, db.name), indexes, forever=False) # indexes refer to index configurations
        indices[db.name]()

if __name__ == '__main__':
    options = [
        make_option('-d', '--dir', dest='dir', metavar="DIRECTORY", default="./xappy", 
            help="Directory in which to store xapian/xappy databases. [%default]"),
        make_option('-u', '--url', dest='url', metavar="URL", default="http://localhost:5984",
            help="URL of the couchdb server. [%default]"),
        make_option('-e', '--exclude', dest='exclude', metavar='DB_NAME', default=[],
            help="Exclude a database from indexing. Can be used multiple times."),
        make_option('-l', '--log', dest='log', metavar="FILE", default='./xapian/index.log',
            help="Name of the log file to write to."),
    ]
    parser = OptionParser("usage: %prog [OPTIONS]", option_list=options)
    opts, args = parser.parse_args()
    if len(args) != 0:
        print "Unrecognized arguments: %s" % ' '.join(args)
        parser.print_help()
        exit(-1)
    logging.basicConfig(filename=opts.log, level=logging.DEBUG, format="%(levelname)s %(message)s")
    try:
        main(os.path.abspath(opts.dir), opts.url, opts.exclude)
    except:
        print("Indexer shutting down due to high stress. Relaxation needed.")



