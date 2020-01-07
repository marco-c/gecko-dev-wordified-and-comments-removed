"
"
"
The
httplib2
algorithms
ported
for
use
with
requests
.
"
"
"
import
logging
import
re
import
calendar
import
time
from
email
.
utils
import
parsedate_tz
from
pip9
.
_vendor
.
requests
.
structures
import
CaseInsensitiveDict
from
.
cache
import
DictCache
from
.
serialize
import
Serializer
logger
=
logging
.
getLogger
(
__name__
)
URI
=
re
.
compile
(
r
"
^
(
(
[
^
:
/
?
#
]
+
)
:
)
?
(
/
/
(
[
^
/
?
#
]
*
)
)
?
(
[
^
?
#
]
*
)
(
\
?
(
[
^
#
]
*
)
)
?
(
#
(
.
*
)
)
?
"
)
def
parse_uri
(
uri
)
:
    
"
"
"
Parses
a
URI
using
the
regex
given
in
Appendix
B
of
RFC
3986
.
        
(
scheme
authority
path
query
fragment
)
=
parse_uri
(
uri
)
    
"
"
"
    
groups
=
URI
.
match
(
uri
)
.
groups
(
)
    
return
(
groups
[
1
]
groups
[
3
]
groups
[
4
]
groups
[
6
]
groups
[
8
]
)
class
CacheController
(
object
)
:
    
"
"
"
An
interface
to
see
if
request
should
cached
or
not
.
    
"
"
"
    
def
__init__
(
self
cache
=
None
cache_etags
=
True
serializer
=
None
)
:
        
self
.
cache
=
cache
or
DictCache
(
)
        
self
.
cache_etags
=
cache_etags
        
self
.
serializer
=
serializer
or
Serializer
(
)
    
classmethod
    
def
_urlnorm
(
cls
uri
)
:
        
"
"
"
Normalize
the
URL
to
create
a
safe
key
for
the
cache
"
"
"
        
(
scheme
authority
path
query
fragment
)
=
parse_uri
(
uri
)
        
if
not
scheme
or
not
authority
:
            
raise
Exception
(
"
Only
absolute
URIs
are
allowed
.
uri
=
%
s
"
%
uri
)
        
scheme
=
scheme
.
lower
(
)
        
authority
=
authority
.
lower
(
)
        
if
not
path
:
            
path
=
"
/
"
        
request_uri
=
query
and
"
?
"
.
join
(
[
path
query
]
)
or
path
        
defrag_uri
=
scheme
+
"
:
/
/
"
+
authority
+
request_uri
        
return
defrag_uri
    
classmethod
    
def
cache_url
(
cls
uri
)
:
        
return
cls
.
_urlnorm
(
uri
)
    
def
parse_cache_control
(
self
headers
)
:
        
"
"
"
        
Parse
the
cache
control
headers
returning
a
dictionary
with
values
        
for
the
different
directives
.
        
"
"
"
        
retval
=
{
}
        
cc_header
=
'
cache
-
control
'
        
if
'
Cache
-
Control
'
in
headers
:
            
cc_header
=
'
Cache
-
Control
'
        
if
cc_header
in
headers
:
            
parts
=
headers
[
cc_header
]
.
split
(
'
'
)
            
parts_with_args
=
[
                
tuple
(
[
x
.
strip
(
)
.
lower
(
)
for
x
in
part
.
split
(
"
=
"
1
)
]
)
                
for
part
in
parts
if
-
1
!
=
part
.
find
(
"
=
"
)
            
]
            
parts_wo_args
=
[
                
(
name
.
strip
(
)
.
lower
(
)
1
)
                
for
name
in
parts
if
-
1
=
=
name
.
find
(
"
=
"
)
            
]
            
retval
=
dict
(
parts_with_args
+
parts_wo_args
)
        
return
retval
    
def
cached_request
(
self
request
)
:
        
"
"
"
        
Return
a
cached
response
if
it
exists
in
the
cache
otherwise
        
return
False
.
        
"
"
"
        
cache_url
=
self
.
cache_url
(
request
.
url
)
        
logger
.
debug
(
'
Looking
up
"
%
s
"
in
the
cache
'
cache_url
)
        
cc
=
self
.
parse_cache_control
(
request
.
headers
)
        
if
'
no
-
cache
'
in
cc
:
            
logger
.
debug
(
'
Request
header
has
"
no
-
cache
"
cache
bypassed
'
)
            
return
False
        
if
'
max
-
age
'
in
cc
and
cc
[
'
max
-
age
'
]
=
=
0
:
            
logger
.
debug
(
'
Request
header
has
"
max_age
"
as
0
cache
bypassed
'
)
            
return
False
        
cache_data
=
self
.
cache
.
get
(
cache_url
)
        
if
cache_data
is
None
:
            
logger
.
debug
(
'
No
cache
entry
available
'
)
            
return
False
        
resp
=
self
.
serializer
.
loads
(
request
cache_data
)
        
if
not
resp
:
            
logger
.
warning
(
'
Cache
entry
deserialization
failed
entry
ignored
'
)
            
return
False
        
if
resp
.
status
=
=
301
:
            
msg
=
(
'
Returning
cached
"
301
Moved
Permanently
"
response
'
                   
'
(
ignoring
date
and
etag
information
)
'
)
            
logger
.
debug
(
msg
)
            
return
resp
        
headers
=
CaseInsensitiveDict
(
resp
.
headers
)
        
if
not
headers
or
'
date
'
not
in
headers
:
            
if
'
etag
'
not
in
headers
:
                
logger
.
debug
(
'
Purging
cached
response
:
no
date
or
etag
'
)
                
self
.
cache
.
delete
(
cache_url
)
            
logger
.
debug
(
'
Ignoring
cached
response
:
no
date
'
)
            
return
False
        
now
=
time
.
time
(
)
        
date
=
calendar
.
timegm
(
            
parsedate_tz
(
headers
[
'
date
'
]
)
        
)
        
current_age
=
max
(
0
now
-
date
)
        
logger
.
debug
(
'
Current
age
based
on
date
:
%
i
'
current_age
)
        
resp_cc
=
self
.
parse_cache_control
(
headers
)
        
freshness_lifetime
=
0
        
if
'
max
-
age
'
in
resp_cc
and
resp_cc
[
'
max
-
age
'
]
.
isdigit
(
)
:
            
freshness_lifetime
=
int
(
resp_cc
[
'
max
-
age
'
]
)
            
logger
.
debug
(
'
Freshness
lifetime
from
max
-
age
:
%
i
'
                         
freshness_lifetime
)
        
elif
'
expires
'
in
headers
:
            
expires
=
parsedate_tz
(
headers
[
'
expires
'
]
)
            
if
expires
is
not
None
:
                
expire_time
=
calendar
.
timegm
(
expires
)
-
date
                
freshness_lifetime
=
max
(
0
expire_time
)
                
logger
.
debug
(
"
Freshness
lifetime
from
expires
:
%
i
"
                             
freshness_lifetime
)
        
if
'
max
-
age
'
in
cc
:
            
try
:
                
freshness_lifetime
=
int
(
cc
[
'
max
-
age
'
]
)
                
logger
.
debug
(
'
Freshness
lifetime
from
request
max
-
age
:
%
i
'
                             
freshness_lifetime
)
            
except
ValueError
:
                
freshness_lifetime
=
0
        
if
'
min
-
fresh
'
in
cc
:
            
try
:
                
min_fresh
=
int
(
cc
[
'
min
-
fresh
'
]
)
            
except
ValueError
:
                
min_fresh
=
0
            
current_age
+
=
min_fresh
            
logger
.
debug
(
'
Adjusted
current
age
from
min
-
fresh
:
%
i
'
                         
current_age
)
        
if
freshness_lifetime
>
current_age
:
            
logger
.
debug
(
'
The
response
is
"
fresh
"
returning
cached
response
'
)
            
logger
.
debug
(
'
%
i
>
%
i
'
freshness_lifetime
current_age
)
            
return
resp
        
if
'
etag
'
not
in
headers
:
            
logger
.
debug
(
                
'
The
cached
response
is
"
stale
"
with
no
etag
purging
'
            
)
            
self
.
cache
.
delete
(
cache_url
)
        
return
False
    
def
conditional_headers
(
self
request
)
:
        
cache_url
=
self
.
cache_url
(
request
.
url
)
        
resp
=
self
.
serializer
.
loads
(
request
self
.
cache
.
get
(
cache_url
)
)
        
new_headers
=
{
}
        
if
resp
:
            
headers
=
CaseInsensitiveDict
(
resp
.
headers
)
            
if
'
etag
'
in
headers
:
                
new_headers
[
'
If
-
None
-
Match
'
]
=
headers
[
'
ETag
'
]
            
if
'
last
-
modified
'
in
headers
:
                
new_headers
[
'
If
-
Modified
-
Since
'
]
=
headers
[
'
Last
-
Modified
'
]
        
return
new_headers
    
def
cache_response
(
self
request
response
body
=
None
)
:
        
"
"
"
        
Algorithm
for
caching
requests
.
        
This
assumes
a
requests
Response
object
.
        
"
"
"
        
cacheable_status_codes
=
[
200
203
300
301
]
        
if
response
.
status
not
in
cacheable_status_codes
:
            
logger
.
debug
(
                
'
Status
code
%
s
not
in
%
s
'
                
response
.
status
                
cacheable_status_codes
            
)
            
return
        
response_headers
=
CaseInsensitiveDict
(
response
.
headers
)
        
if
(
body
is
not
None
and
                
"
content
-
length
"
in
response_headers
and
                
response_headers
[
"
content
-
length
"
]
.
isdigit
(
)
and
                
int
(
response_headers
[
"
content
-
length
"
]
)
!
=
len
(
body
)
)
:
            
return
        
cc_req
=
self
.
parse_cache_control
(
request
.
headers
)
        
cc
=
self
.
parse_cache_control
(
response_headers
)
        
cache_url
=
self
.
cache_url
(
request
.
url
)
        
logger
.
debug
(
'
Updating
cache
with
response
from
"
%
s
"
'
cache_url
)
        
no_store
=
False
        
if
cc
.
get
(
'
no
-
store
'
)
:
            
no_store
=
True
            
logger
.
debug
(
'
Response
header
has
"
no
-
store
"
'
)
        
if
cc_req
.
get
(
'
no
-
store
'
)
:
            
no_store
=
True
            
logger
.
debug
(
'
Request
header
has
"
no
-
store
"
'
)
        
if
no_store
and
self
.
cache
.
get
(
cache_url
)
:
            
logger
.
debug
(
'
Purging
existing
cache
entry
to
honor
"
no
-
store
"
'
)
            
self
.
cache
.
delete
(
cache_url
)
        
if
self
.
cache_etags
and
'
etag
'
in
response_headers
:
            
logger
.
debug
(
'
Caching
due
to
etag
'
)
            
self
.
cache
.
set
(
                
cache_url
                
self
.
serializer
.
dumps
(
request
response
body
=
body
)
            
)
        
elif
response
.
status
=
=
301
:
            
logger
.
debug
(
'
Caching
permanant
redirect
'
)
            
self
.
cache
.
set
(
                
cache_url
                
self
.
serializer
.
dumps
(
request
response
)
            
)
        
elif
'
date
'
in
response_headers
:
            
if
cc
and
cc
.
get
(
'
max
-
age
'
)
:
                
if
cc
[
'
max
-
age
'
]
.
isdigit
(
)
and
int
(
cc
[
'
max
-
age
'
]
)
>
0
:
                    
logger
.
debug
(
'
Caching
b
/
c
date
exists
and
max
-
age
>
0
'
)
                    
self
.
cache
.
set
(
                        
cache_url
                        
self
.
serializer
.
dumps
(
request
response
body
=
body
)
                    
)
            
elif
'
expires
'
in
response_headers
:
                
if
response_headers
[
'
expires
'
]
:
                    
logger
.
debug
(
'
Caching
b
/
c
of
expires
header
'
)
                    
self
.
cache
.
set
(
                        
cache_url
                        
self
.
serializer
.
dumps
(
request
response
body
=
body
)
                    
)
    
def
update_cached_response
(
self
request
response
)
:
        
"
"
"
On
a
304
we
will
get
a
new
set
of
headers
that
we
want
to
        
update
our
cached
value
with
assuming
we
have
one
.
        
This
should
only
ever
be
called
when
we
'
ve
sent
an
ETag
and
        
gotten
a
304
as
the
response
.
        
"
"
"
        
cache_url
=
self
.
cache_url
(
request
.
url
)
        
cached_response
=
self
.
serializer
.
loads
(
            
request
            
self
.
cache
.
get
(
cache_url
)
        
)
        
if
not
cached_response
:
            
return
response
        
excluded_headers
=
[
            
"
content
-
length
"
        
]
        
cached_response
.
headers
.
update
(
            
dict
(
(
k
v
)
for
k
v
in
response
.
headers
.
items
(
)
                 
if
k
.
lower
(
)
not
in
excluded_headers
)
        
)
        
cached_response
.
status
=
200
        
self
.
cache
.
set
(
            
cache_url
            
self
.
serializer
.
dumps
(
request
cached_response
)
        
)
        
return
cached_response
