# TapirWiki Todo List and Feature Requests #

This page lists the feature requests for TapirWiki. If you want to help implement any of these,  let me know.


# ToDo #

## Search ##
  * Would be useful to be able to search wiki pages for text
## Install / upgrade page ##
  * Remove the need to go to Futon each time a new version is released...
## MarkDown support ##
  * Apart from Textile also support the MarkDown markup language -> add a parser, and a renderer or perhaps generalize the renderer to a lightweight markup language to html renderer so that it can work with both.
  * Put parsing/rendering at the server side?
## Bread crumbs ##
  * Could be path traversed or perhaps shortest path from its root (according to some algorithm), or both.
  * Perhaps some contents page of the entire wiki with structure, not just an index
## Fields ##
  * Would be nice to be able to define fields that correspond with !CouchDB fields. Or when creating a page you can indicate according to what field template (normal wiki page or wiki page with certain added fields). In edit mode you should be able to set the fields, in display mode you can render the fields inside the wiki page with a macro. Macro's can then also be designed to summarize fields using views or other server side routines.
## Cancel Button ##
  * Cancel button while in edit mode.