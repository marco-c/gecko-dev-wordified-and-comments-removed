#
-
*
-
coding
:
utf
-
8
-
*
-
from
collections
import
deque
import
logging
from
.
exceptions
import
InvalidTableIndex
log
=
logging
.
getLogger
(
__name__
)
def
table_entry_size
(
name
value
)
:
    
"
"
"
    
Calculates
the
size
of
a
single
entry
    
This
size
is
mostly
irrelevant
to
us
and
defined
    
specifically
to
accommodate
memory
management
for
    
lower
level
implementations
.
The
32
extra
bytes
are
    
considered
the
"
maximum
"
overhead
that
would
be
    
required
to
represent
each
entry
in
the
table
.
    
See
RFC7541
Section
4
.
1
    
"
"
"
    
return
32
+
len
(
name
)
+
len
(
value
)
class
HeaderTable
(
object
)
:
    
"
"
"
    
Implements
the
combined
static
and
dynamic
header
table
    
The
name
and
value
arguments
for
all
the
functions
    
should
ONLY
be
byte
strings
(
b
'
'
)
however
this
is
not
    
strictly
enforced
in
the
interface
.
    
See
RFC7541
Section
2
.
3
    
"
"
"
    
DEFAULT_SIZE
=
4096
    
STATIC_TABLE
=
(
        
(
b
'
:
authority
'
b
'
'
)
        
(
b
'
:
method
'
b
'
GET
'
)
        
(
b
'
:
method
'
b
'
POST
'
)
        
(
b
'
:
path
'
b
'
/
'
)
        
(
b
'
:
path
'
b
'
/
index
.
html
'
)
        
(
b
'
:
scheme
'
b
'
http
'
)
        
(
b
'
:
scheme
'
b
'
https
'
)
        
(
b
'
:
status
'
b
'
200
'
)
        
(
b
'
:
status
'
b
'
204
'
)
        
(
b
'
:
status
'
b
'
206
'
)
        
(
b
'
:
status
'
b
'
304
'
)
        
(
b
'
:
status
'
b
'
400
'
)
        
(
b
'
:
status
'
b
'
404
'
)
        
(
b
'
:
status
'
b
'
500
'
)
        
(
b
'
accept
-
charset
'
b
'
'
)
        
(
b
'
accept
-
encoding
'
b
'
gzip
deflate
'
)
        
(
b
'
accept
-
language
'
b
'
'
)
        
(
b
'
accept
-
ranges
'
b
'
'
)
        
(
b
'
accept
'
b
'
'
)
        
(
b
'
access
-
control
-
allow
-
origin
'
b
'
'
)
        
(
b
'
age
'
b
'
'
)
        
(
b
'
allow
'
b
'
'
)
        
(
b
'
authorization
'
b
'
'
)
        
(
b
'
cache
-
control
'
b
'
'
)
        
(
b
'
content
-
disposition
'
b
'
'
)
        
(
b
'
content
-
encoding
'
b
'
'
)
        
(
b
'
content
-
language
'
b
'
'
)
        
(
b
'
content
-
length
'
b
'
'
)
        
(
b
'
content
-
location
'
b
'
'
)
        
(
b
'
content
-
range
'
b
'
'
)
        
(
b
'
content
-
type
'
b
'
'
)
        
(
b
'
cookie
'
b
'
'
)
        
(
b
'
date
'
b
'
'
)
        
(
b
'
etag
'
b
'
'
)
        
(
b
'
expect
'
b
'
'
)
        
(
b
'
expires
'
b
'
'
)
        
(
b
'
from
'
b
'
'
)
        
(
b
'
host
'
b
'
'
)
        
(
b
'
if
-
match
'
b
'
'
)
        
(
b
'
if
-
modified
-
since
'
b
'
'
)
        
(
b
'
if
-
none
-
match
'
b
'
'
)
        
(
b
'
if
-
range
'
b
'
'
)
        
(
b
'
if
-
unmodified
-
since
'
b
'
'
)
        
(
b
'
last
-
modified
'
b
'
'
)
        
(
b
'
link
'
b
'
'
)
        
(
b
'
location
'
b
'
'
)
        
(
b
'
max
-
forwards
'
b
'
'
)
        
(
b
'
proxy
-
authenticate
'
b
'
'
)
        
(
b
'
proxy
-
authorization
'
b
'
'
)
        
(
b
'
range
'
b
'
'
)
        
(
b
'
referer
'
b
'
'
)
        
(
b
'
refresh
'
b
'
'
)
        
(
b
'
retry
-
after
'
b
'
'
)
        
(
b
'
server
'
b
'
'
)
        
(
b
'
set
-
cookie
'
b
'
'
)
        
(
b
'
strict
-
transport
-
security
'
b
'
'
)
        
(
b
'
transfer
-
encoding
'
b
'
'
)
        
(
b
'
user
-
agent
'
b
'
'
)
        
(
b
'
vary
'
b
'
'
)
        
(
b
'
via
'
b
'
'
)
        
(
b
'
www
-
authenticate
'
b
'
'
)
    
)
    
STATIC_TABLE_LENGTH
=
len
(
STATIC_TABLE
)
    
def
__init__
(
self
)
:
        
self
.
_maxsize
=
HeaderTable
.
DEFAULT_SIZE
        
self
.
_current_size
=
0
        
self
.
resized
=
False
        
self
.
dynamic_entries
=
deque
(
)
    
def
get_by_index
(
self
index
)
:
        
"
"
"
        
Returns
the
entry
specified
by
index
        
Note
that
the
table
is
1
-
based
ie
an
index
of
0
is
        
invalid
.
This
is
due
to
the
fact
that
a
zero
value
        
index
signals
that
a
completely
unindexed
header
        
follows
.
        
The
entry
will
either
be
from
the
static
table
or
        
the
dynamic
table
depending
on
the
value
of
index
.
        
"
"
"
        
original_index
=
index
        
index
-
=
1
        
if
0
<
=
index
:
            
if
index
<
HeaderTable
.
STATIC_TABLE_LENGTH
:
                
return
HeaderTable
.
STATIC_TABLE
[
index
]
            
index
-
=
HeaderTable
.
STATIC_TABLE_LENGTH
            
if
index
<
len
(
self
.
dynamic_entries
)
:
                
return
self
.
dynamic_entries
[
index
]
        
raise
InvalidTableIndex
(
"
Invalid
table
index
%
d
"
%
original_index
)
    
def
__repr__
(
self
)
:
        
return
"
HeaderTable
(
%
d
%
s
%
r
)
"
%
(
            
self
.
_maxsize
            
self
.
resized
            
self
.
dynamic_entries
        
)
    
def
add
(
self
name
value
)
:
        
"
"
"
        
Adds
a
new
entry
to
the
table
        
We
reduce
the
table
size
if
the
entry
will
make
the
        
table
size
greater
than
maxsize
.
        
"
"
"
        
size
=
table_entry_size
(
name
value
)
        
if
size
>
self
.
_maxsize
:
            
self
.
dynamic_entries
.
clear
(
)
            
self
.
_current_size
=
0
        
else
:
            
self
.
dynamic_entries
.
appendleft
(
(
name
value
)
)
            
self
.
_current_size
+
=
size
            
self
.
_shrink
(
)
    
def
search
(
self
name
value
)
:
        
"
"
"
        
Searches
the
table
for
the
entry
specified
by
name
        
and
value
        
Returns
one
of
the
following
:
            
-
None
no
match
at
all
            
-
(
index
name
None
)
for
partial
matches
on
name
only
.
            
-
(
index
name
value
)
for
perfect
matches
.
        
"
"
"
        
offset
=
HeaderTable
.
STATIC_TABLE_LENGTH
+
1
        
partial
=
None
        
for
(
i
(
n
v
)
)
in
enumerate
(
HeaderTable
.
STATIC_TABLE
)
:
            
if
n
=
=
name
:
                
if
v
=
=
value
:
                    
return
i
+
1
n
v
                
elif
partial
is
None
:
                    
partial
=
(
i
+
1
n
None
)
        
for
(
i
(
n
v
)
)
in
enumerate
(
self
.
dynamic_entries
)
:
            
if
n
=
=
name
:
                
if
v
=
=
value
:
                    
return
i
+
offset
n
v
                
elif
partial
is
None
:
                    
partial
=
(
i
+
offset
n
None
)
        
return
partial
    
property
    
def
maxsize
(
self
)
:
        
return
self
.
_maxsize
    
maxsize
.
setter
    
def
maxsize
(
self
newmax
)
:
        
newmax
=
int
(
newmax
)
        
log
.
debug
(
"
Resizing
header
table
to
%
d
from
%
d
"
newmax
self
.
_maxsize
)
        
oldmax
=
self
.
_maxsize
        
self
.
_maxsize
=
newmax
        
self
.
resized
=
(
newmax
!
=
oldmax
)
        
if
newmax
<
=
0
:
            
self
.
dynamic_entries
.
clear
(
)
            
self
.
_current_size
=
0
        
elif
oldmax
>
newmax
:
            
self
.
_shrink
(
)
    
def
_shrink
(
self
)
:
        
"
"
"
        
Shrinks
the
dynamic
table
to
be
at
or
below
maxsize
        
"
"
"
        
cursize
=
self
.
_current_size
        
while
cursize
>
self
.
_maxsize
:
            
name
value
=
self
.
dynamic_entries
.
pop
(
)
            
cursize
-
=
table_entry_size
(
name
value
)
            
log
.
debug
(
"
Evicting
%
s
:
%
s
from
the
header
table
"
name
value
)
        
self
.
_current_size
=
cursize
