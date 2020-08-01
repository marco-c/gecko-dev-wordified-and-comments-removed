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
pipenv
.
patched
.
notpip
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
status_codes
=
None
    
)
:
        
self
.
cache
=
DictCache
(
)
if
cache
is
None
else
cache
        
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
        
self
.
cacheable_status_codes
=
status_codes
or
(
200
203
300
301
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
        
known_directives
=
{
            
"
max
-
age
"
:
(
int
True
)
            
"
max
-
stale
"
:
(
int
False
)
            
"
min
-
fresh
"
:
(
int
True
)
            
"
no
-
cache
"
:
(
None
False
)
            
"
no
-
store
"
:
(
None
False
)
            
"
no
-
transform
"
:
(
None
False
)
            
"
only
-
if
-
cached
"
:
(
None
False
)
            
"
must
-
revalidate
"
:
(
None
False
)
            
"
public
"
:
(
None
False
)
            
"
private
"
:
(
None
False
)
            
"
proxy
-
revalidate
"
:
(
None
False
)
            
"
s
-
maxage
"
:
(
int
True
)
        
}
        
cc_headers
=
headers
.
get
(
"
cache
-
control
"
headers
.
get
(
"
Cache
-
Control
"
"
"
)
)
        
retval
=
{
}
        
for
cc_directive
in
cc_headers
.
split
(
"
"
)
:
            
if
not
cc_directive
.
strip
(
)
:
                
continue
            
parts
=
cc_directive
.
split
(
"
=
"
1
)
            
directive
=
parts
[
0
]
.
strip
(
)
            
try
:
                
typ
required
=
known_directives
[
directive
]
            
except
KeyError
:
                
logger
.
debug
(
"
Ignoring
unknown
cache
-
control
directive
:
%
s
"
directive
)
                
continue
            
if
not
typ
or
not
required
:
                
retval
[
directive
]
=
None
            
if
typ
:
                
try
:
                    
retval
[
directive
]
=
typ
(
parts
[
1
]
.
strip
(
)
)
                
except
IndexError
:
                    
if
required
:
                        
logger
.
debug
(
                            
"
Missing
value
for
cache
-
control
"
"
directive
:
%
s
"
                            
directive
                        
)
                
except
ValueError
:
                    
logger
.
debug
(
                        
"
Invalid
value
for
cache
-
control
directive
"
"
%
s
must
be
%
s
"
                        
directive
                        
typ
.
__name__
                    
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
"
no
-
cache
"
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
"
max
-
age
"
in
cc
and
cc
[
"
max
-
age
"
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
"
No
cache
entry
available
"
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
"
Cache
entry
deserialization
failed
entry
ignored
"
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
                
"
(
ignoring
date
and
etag
information
)
"
            
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
"
date
"
not
in
headers
:
            
if
"
etag
"
not
in
headers
:
                
logger
.
debug
(
"
Purging
cached
response
:
no
date
or
etag
"
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
"
Ignoring
cached
response
:
no
date
"
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
"
date
"
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
"
Current
age
based
on
date
:
%
i
"
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
"
max
-
age
"
in
resp_cc
:
            
freshness_lifetime
=
resp_cc
[
"
max
-
age
"
]
            
logger
.
debug
(
"
Freshness
lifetime
from
max
-
age
:
%
i
"
freshness_lifetime
)
        
elif
"
expires
"
in
headers
:
            
expires
=
parsedate_tz
(
headers
[
"
expires
"
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
"
max
-
age
"
in
cc
:
            
freshness_lifetime
=
cc
[
"
max
-
age
"
]
            
logger
.
debug
(
                
"
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
"
freshness_lifetime
            
)
        
if
"
min
-
fresh
"
in
cc
:
            
min_fresh
=
cc
[
"
min
-
fresh
"
]
            
current_age
+
=
min_fresh
            
logger
.
debug
(
"
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
"
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
"
%
i
>
%
i
"
freshness_lifetime
current_age
)
            
return
resp
        
if
"
etag
"
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
"
etag
"
in
headers
:
                
new_headers
[
"
If
-
None
-
Match
"
]
=
headers
[
"
ETag
"
]
            
if
"
last
-
modified
"
in
headers
:
                
new_headers
[
"
If
-
Modified
-
Since
"
]
=
headers
[
"
Last
-
Modified
"
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
status_codes
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
status_codes
or
self
.
cacheable_status_codes
        
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
                
"
Status
code
%
s
not
in
%
s
"
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
"
no
-
store
"
in
cc
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
"
no
-
store
"
in
cc_req
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
no_store
:
            
return
        
if
"
*
"
in
response_headers
.
get
(
"
vary
"
"
"
)
:
            
logger
.
debug
(
'
Response
header
has
"
Vary
:
*
"
'
)
            
return
        
if
self
.
cache_etags
and
"
etag
"
in
response_headers
:
            
logger
.
debug
(
"
Caching
due
to
etag
"
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
"
Caching
permanant
redirect
"
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
"
date
"
in
response_headers
:
            
if
"
max
-
age
"
in
cc
and
cc
[
"
max
-
age
"
]
>
0
:
                
logger
.
debug
(
"
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
"
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
"
expires
"
in
response_headers
:
                
if
response_headers
[
"
expires
"
]
:
                    
logger
.
debug
(
"
Caching
b
/
c
of
expires
header
"
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
