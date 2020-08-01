import
itertools
import
logging
import
os
import
posixpath
from
pipenv
.
patched
.
notpip
.
_vendor
.
packaging
.
utils
import
canonicalize_name
from
pipenv
.
patched
.
notpip
.
_vendor
.
six
.
moves
.
urllib
import
parse
as
urllib_parse
from
pipenv
.
patched
.
notpip
.
_internal
.
models
.
index
import
PyPI
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
compat
import
has_tls
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
misc
import
normalize_path
redact_auth_from_url
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
List
logger
=
logging
.
getLogger
(
__name__
)
class
SearchScope
(
object
)
:
    
"
"
"
    
Encapsulates
the
locations
that
pip
is
configured
to
search
.
    
"
"
"
    
classmethod
    
def
create
(
        
cls
        
find_links
        
index_urls
    
)
:
        
"
"
"
        
Create
a
SearchScope
object
after
normalizing
the
find_links
.
        
"
"
"
        
built_find_links
=
[
]
        
for
link
in
find_links
:
            
if
link
.
startswith
(
'
~
'
)
:
                
new_link
=
normalize_path
(
link
)
                
if
os
.
path
.
exists
(
new_link
)
:
                    
link
=
new_link
            
built_find_links
.
append
(
link
)
        
if
not
has_tls
(
)
:
            
for
link
in
itertools
.
chain
(
index_urls
built_find_links
)
:
                
parsed
=
urllib_parse
.
urlparse
(
link
)
                
if
parsed
.
scheme
=
=
'
https
'
:
                    
logger
.
warning
(
                        
'
pip
is
configured
with
locations
that
require
'
                        
'
TLS
/
SSL
however
the
ssl
module
in
Python
is
not
'
                        
'
available
.
'
                    
)
                    
break
        
return
cls
(
            
find_links
=
built_find_links
            
index_urls
=
index_urls
        
)
    
def
__init__
(
        
self
        
find_links
        
index_urls
    
)
:
        
self
.
find_links
=
find_links
        
self
.
index_urls
=
index_urls
    
def
get_formatted_locations
(
self
)
:
        
lines
=
[
]
        
if
self
.
index_urls
and
self
.
index_urls
!
=
[
PyPI
.
simple_url
]
:
            
lines
.
append
(
                
'
Looking
in
indexes
:
{
}
'
.
format
(
'
'
.
join
(
                    
redact_auth_from_url
(
url
)
for
url
in
self
.
index_urls
)
)
            
)
        
if
self
.
find_links
:
            
lines
.
append
(
                
'
Looking
in
links
:
{
}
'
.
format
(
'
'
.
join
(
                    
redact_auth_from_url
(
url
)
for
url
in
self
.
find_links
)
)
            
)
        
return
'
\
n
'
.
join
(
lines
)
    
def
get_index_urls_locations
(
self
project_name
)
:
        
"
"
"
Returns
the
locations
found
via
self
.
index_urls
        
Checks
the
url_name
on
the
main
(
first
in
the
list
)
index
and
        
use
this
url_name
to
produce
all
locations
        
"
"
"
        
def
mkurl_pypi_url
(
url
)
:
            
loc
=
posixpath
.
join
(
                
url
                
urllib_parse
.
quote
(
canonicalize_name
(
project_name
)
)
)
            
if
not
loc
.
endswith
(
'
/
'
)
:
                
loc
=
loc
+
'
/
'
            
return
loc
        
return
[
mkurl_pypi_url
(
url
)
for
url
in
self
.
index_urls
]
