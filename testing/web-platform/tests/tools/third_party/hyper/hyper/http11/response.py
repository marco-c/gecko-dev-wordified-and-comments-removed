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
"
"
"
hyper
/
http11
/
response
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
Contains
the
HTTP
/
1
.
1
equivalent
of
the
HTTPResponse
object
defined
in
httplib
/
http
.
client
.
"
"
"
import
logging
import
weakref
import
zlib
from
.
.
common
.
decoder
import
DeflateDecoder
from
.
.
common
.
exceptions
import
ChunkedDecodeError
InvalidResponseError
from
.
.
common
.
exceptions
import
ConnectionResetError
log
=
logging
.
getLogger
(
__name__
)
class
HTTP11Response
(
object
)
:
    
"
"
"
    
An
HTTP11Response
wraps
the
HTTP
/
1
.
1
response
from
the
server
.
It
    
provides
access
to
the
response
headers
and
the
entity
body
.
The
response
    
is
an
iterable
object
and
can
be
used
in
a
with
statement
.
    
"
"
"
    
def
__init__
(
self
code
reason
headers
sock
connection
=
None
)
:
        
self
.
reason
=
reason
        
self
.
status
=
code
        
self
.
headers
=
headers
        
self
.
trailers
=
None
        
self
.
_sock
=
sock
        
self
.
_expect_close
=
False
        
if
b
'
close
'
in
self
.
headers
.
get
(
b
'
connection
'
[
]
)
:
            
self
.
_expect_close
=
True
        
try
:
            
self
.
_length
=
int
(
self
.
headers
[
b
'
content
-
length
'
]
[
0
]
)
        
except
KeyError
:
            
self
.
_length
=
None
        
self
.
_chunked
=
(
            
b
'
chunked
'
in
self
.
headers
.
get
(
b
'
transfer
-
encoding
'
[
]
)
        
)
        
assert
self
.
_expect_close
or
self
.
_length
is
not
None
or
self
.
_chunked
        
if
b
'
gzip
'
in
self
.
headers
.
get
(
b
'
content
-
encoding
'
[
]
)
:
            
self
.
_decompressobj
=
zlib
.
decompressobj
(
16
+
zlib
.
MAX_WBITS
)
        
elif
b
'
deflate
'
in
self
.
headers
.
get
(
b
'
content
-
encoding
'
[
]
)
:
            
self
.
_decompressobj
=
DeflateDecoder
(
)
        
else
:
            
self
.
_decompressobj
=
None
        
if
connection
is
not
None
:
            
self
.
_parent
=
weakref
.
ref
(
connection
)
        
else
:
            
self
.
_parent
=
None
        
self
.
_buffered_data
=
b
'
'
        
self
.
_chunker
=
None
    
def
read
(
self
amt
=
None
decode_content
=
True
)
:
        
"
"
"
        
Reads
the
response
body
or
up
to
the
next
amt
bytes
.
        
:
param
amt
:
(
optional
)
The
amount
of
data
to
read
.
If
not
provided
all
            
the
data
will
be
read
from
the
response
.
        
:
param
decode_content
:
(
optional
)
If
True
will
transparently
            
decode
the
response
data
.
        
:
returns
:
The
read
data
.
Note
that
if
decode_content
is
set
to
            
True
the
actual
amount
of
data
returned
may
be
different
to
            
the
amount
requested
.
        
"
"
"
        
if
self
.
_sock
is
None
:
            
return
b
'
'
        
if
self
.
_chunked
:
            
return
self
.
_normal_read_chunked
(
amt
decode_content
)
        
if
amt
is
None
:
            
if
self
.
_length
is
not
None
:
                
amt
=
self
.
_length
            
elif
self
.
_expect_close
:
                
return
self
.
_read_expect_closed
(
decode_content
)
            
else
:
                
raise
InvalidResponseError
(
                    
"
Response
must
either
have
length
or
Connection
:
close
"
                
)
        
if
self
.
_length
is
not
None
:
            
amt
=
min
(
amt
self
.
_length
)
        
to_read
=
amt
        
chunks
=
[
]
        
while
to_read
>
0
:
            
chunk
=
self
.
_sock
.
recv
(
amt
)
.
tobytes
(
)
            
if
not
chunk
:
                
if
self
.
_length
is
not
None
or
not
self
.
_expect_close
:
                    
self
.
close
(
socket_close
=
True
)
                    
raise
ConnectionResetError
(
"
Remote
end
hung
up
!
"
)
                
break
            
to_read
-
=
len
(
chunk
)
            
chunks
.
append
(
chunk
)
        
data
=
b
'
'
.
join
(
chunks
)
        
if
self
.
_length
is
not
None
:
            
self
.
_length
-
=
len
(
data
)
        
end_of_request
=
(
self
.
_length
=
=
0
or
                          
(
self
.
_expect_close
and
len
(
data
)
<
amt
)
)
        
if
decode_content
and
self
.
_decompressobj
and
data
:
            
data
=
self
.
_decompressobj
.
decompress
(
data
)
        
if
decode_content
and
self
.
_decompressobj
and
end_of_request
:
            
data
+
=
self
.
_decompressobj
.
flush
(
)
        
if
end_of_request
:
            
self
.
close
(
socket_close
=
self
.
_expect_close
)
        
return
data
    
def
read_chunked
(
self
decode_content
=
True
)
:
        
"
"
"
        
Reads
chunked
transfer
encoded
bodies
.
This
method
returns
a
generator
:
        
each
iteration
of
which
yields
one
chunk
*
unless
*
the
chunks
are
        
compressed
in
which
case
it
yields
whatever
the
decompressor
provides
        
for
each
chunk
.
        
.
.
warning
:
:
This
may
yield
the
empty
string
without
that
being
the
                     
end
of
the
body
!
        
"
"
"
        
if
not
self
.
_chunked
:
            
raise
ChunkedDecodeError
(
                
"
Attempted
chunked
read
of
non
-
chunked
body
.
"
            
)
        
if
self
.
_sock
is
None
:
            
return
        
while
True
:
            
chunk_length
=
int
(
self
.
_sock
.
readline
(
)
.
tobytes
(
)
.
strip
(
)
16
)
            
data
=
b
'
'
            
if
not
chunk_length
:
                
self
.
_sock
.
readline
(
)
                
if
decode_content
and
self
.
_decompressobj
:
                    
yield
self
.
_decompressobj
.
flush
(
)
                
self
.
close
(
socket_close
=
self
.
_expect_close
)
                
break
            
while
chunk_length
>
0
:
                
chunk
=
self
.
_sock
.
recv
(
chunk_length
)
.
tobytes
(
)
                
data
+
=
chunk
                
chunk_length
-
=
len
(
chunk
)
            
assert
chunk_length
=
=
0
            
self
.
_sock
.
readline
(
)
            
if
decode_content
and
self
.
_decompressobj
and
data
:
                
data
=
self
.
_decompressobj
.
decompress
(
data
)
            
yield
data
        
return
    
def
close
(
self
socket_close
=
False
)
:
        
"
"
"
        
Close
the
response
.
This
causes
the
Response
to
lose
access
to
the
        
backing
socket
.
In
some
cases
it
can
also
cause
the
backing
connection
        
to
be
torn
down
.
        
:
param
socket_close
:
Whether
to
close
the
backing
socket
.
        
:
returns
:
Nothing
.
        
"
"
"
        
if
socket_close
and
self
.
_parent
is
not
None
:
            
parent
=
self
.
_parent
(
)
            
if
parent
is
not
None
:
                
parent
.
close
(
)
        
self
.
_sock
=
None
    
def
_read_expect_closed
(
self
decode_content
)
:
        
"
"
"
        
Implements
the
logic
for
an
unbounded
read
on
a
socket
that
we
expect
        
to
be
closed
by
the
remote
end
.
        
"
"
"
        
chunks
=
[
]
        
while
True
:
            
try
:
                
chunk
=
self
.
_sock
.
recv
(
65535
)
.
tobytes
(
)
                
if
not
chunk
:
                    
break
            
except
ConnectionResetError
:
                
break
            
else
:
                
chunks
.
append
(
chunk
)
        
self
.
close
(
socket_close
=
True
)
        
data
=
b
'
'
.
join
(
chunks
)
        
if
decode_content
and
self
.
_decompressobj
:
            
data
=
self
.
_decompressobj
.
decompress
(
data
)
            
data
+
=
self
.
_decompressobj
.
flush
(
)
        
return
data
    
def
_normal_read_chunked
(
self
amt
decode_content
)
:
        
"
"
"
        
Implements
the
logic
for
calling
read
(
)
on
a
chunked
response
.
        
"
"
"
        
if
amt
is
None
:
            
return
self
.
_buffered_data
+
b
'
'
.
join
(
self
.
read_chunked
(
)
)
        
if
self
.
_chunker
is
None
:
            
self
.
_chunker
=
self
.
read_chunked
(
)
        
current_amount
=
len
(
self
.
_buffered_data
)
        
extra_data
=
[
self
.
_buffered_data
]
        
while
current_amount
<
amt
:
            
try
:
                
chunk
=
next
(
self
.
_chunker
)
            
except
StopIteration
:
                
self
.
close
(
socket_close
=
self
.
_expect_close
)
                
break
            
current_amount
+
=
len
(
chunk
)
            
extra_data
.
append
(
chunk
)
        
data
=
b
'
'
.
join
(
extra_data
)
        
self
.
_buffered_data
=
data
[
amt
:
]
        
return
data
[
:
amt
]
    
def
__enter__
(
self
)
:
        
return
self
    
def
__exit__
(
self
*
args
)
:
        
self
.
close
(
)
        
return
False
