#! /usr/bin/env python
#
# twquery.py - TapirWiki full text indexing with couchfti, xappy, xapian
# Copyright (C) 2010 Jeroen Vet jeroen.vet@gmail.com (on changes only)
# based on couchdb-xapian-query (C) Paul J. Davis 
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
# with this program; if not, write to the Free Software Foundati

from couchfti import search
import xappy
import simplejson
import os
import sys
import couchdb
import logging
from optparse import OptionParser, make_option

indexes= { 'wikipageidx':{ 
                           'path'     : "tapirwiki.idx",
                         }
         }

couch=couchdb.Server()


def queries():
    line = sys.stdin.readline()
    while line:
        if not line:
            return
        obj = simplejson.loads(line)
        yield obj
        line = sys.stdin.readline()

def send(data):
       sys.stdout.write(simplejson.dumps(data))
       sys.stdout.write('\n')
       sys.stdout.flush()

def main(dir, url, exclude):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    searchers = {}
    for quert in queries():
         qs = quert.get('query', {}).get('q', '')
         suml = int(quert.get('query', {}).get('sl', ''))
         perp = int(quert.get('query', {}).get('pp', ''))
         skip = int(quert.get('query', {}).get('sk', ''))
         qdbn=quert.get('info',{}).get('db_name','')
         if qdbn not in searchers:
            qdb=couch[qdbn]
            searchers[qdbn] = search.Searcher(qdb, os.path.join(dir, qdbn), indexes)
         ret = searchers[qdbn].search('wikipageidx',unicode(qs),skip,skip+perp) # we are getting back xappy search results 
         cnt=1
         reta=[{'totmatches':ret.matches_estimated}]
         for result in ret:
              reta.append({})      
              reta[cnt]['rank']=result.rank
              reta[cnt]['_id']=result.id
              reta[cnt]['edited_by']=result.data['edited_by'][0] 
              reta[cnt]['edited_on']=result.data['edited_on'][0]
              reta[cnt]['summary']=result.summarise('body', maxlen=suml)
              cnt=cnt+1
         send({'code': 200, 'json': reta, 'headers': {}})

       
if __name__ == '__main__':
    options = [
        make_option('-d', '--dir', dest='dir', metavar="DIRECTORY", default="./xappy",
            help="Directory in which to store xapian databases. [%default]"),
        make_option('-u', '--url', dest='url', metavar="URL", default="http://localhost:5984",
            help="URL of the couchdb server. [%default]"),
        make_option('-e', '--exclude', dest='exclude', metavar='DB_NAME', default=[],
            help="Exclude a database from indexing. Can be used multiple times."),
        make_option('-l', '--log', dest='log', metavar="FILE", default='./xapian/query.log',
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
        log.exception("Querying shutting down due to high stress. Relaxation needed.")


