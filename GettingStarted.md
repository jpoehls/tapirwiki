# Introduction #

TapirWiki is a wiki engine for couchDB. It's all HTML and Javascript - a couchapp! All the pages are stored in couchDB.


# Installing #
To use TapirWiki you need couchapp.

  1. Install couchapp - Instructions are [here](http://github.com/couchapp/couchapp) (section 3).
  1. Download the wiki.zip file from the project site
  1. Extract the zip and fire up a terminal, cd into the wiki folder
  1. Enter the following command: couchapp init
  1. Enter the following command: couchapp push http://127.0.0.1:5984/wiki
  1. Open your new wiki at http://127.0.0.1:5984/wiki/_design/tapir/wiki.html

TapirWiki will set up a few default pages for you, refresh the page and you should be in to your new wiki! More help is provided within TapirWiki itself.


## Development (trunk) version ##

You can also grab the latest trunk version from the code repository at http://code.google.com/p/tapirwiki/source/checkout instead of the zip file referred to above and have access to all the latest features. Please note however that there are two branches in the repository, after cloning the repository you still need to issue an `hg update dev` command as the trunk is on the dev branch and if you clone the repository your working file set is by default a checkout of the latest change set of the default branch.

## Virtual Appliance ##

Another alternative is to download the [tapirwiki virtual appliance](http://oeo.la/_UWcx_) created and tested with [VirtualBox](http://www.virtualbox.org). This gives you a fully configured system (including indexing and searching) with a pre-installed wiki (called tapirwiki). If you want to create new wiki's, you can replicate this wiki within the same database using the 'replicator' available in futon (`http://ip-of-virtual-appliance:5984/_utils`) or you can 'couchapp push' from your host. The latter option would require couchapp installed and downloaded tapirwiki code on the host system.