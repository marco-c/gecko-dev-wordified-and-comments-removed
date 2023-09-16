from
__future__
import
annotations
import
dataclasses
import
re
import
warnings
from
typing
import
Callable
Generator
Optional
from
.
import
datastructures
exceptions
MAX_HEADERS
=
256
MAX_LINE
=
4111
MAX_BODY
=
2
*
*
20
def
d
(
value
:
bytes
)
-
>
str
:
    
"
"
"
    
Decode
a
bytestring
for
interpolating
into
an
error
message
.
    
"
"
"
    
return
value
.
decode
(
errors
=
"
backslashreplace
"
)
_token_re
=
re
.
compile
(
rb
"
[
-
!
#
%
&
\
'
*
+
.
^
_
|
~
0
-
9a
-
zA
-
Z
]
+
"
)
_value_re
=
re
.
compile
(
rb
"
[
\
x09
\
x20
-
\
x7e
\
x80
-
\
xff
]
*
"
)
dataclasses
.
dataclass
class
Request
:
    
"
"
"
    
WebSocket
handshake
request
.
    
Attributes
:
        
path
:
Request
path
including
optional
query
.
        
headers
:
Request
headers
.
    
"
"
"
    
path
:
str
    
headers
:
datastructures
.
Headers
    
_exception
:
Optional
[
Exception
]
=
None
    
property
    
def
exception
(
self
)
-
>
Optional
[
Exception
]
:
        
warnings
.
warn
(
            
"
Request
.
exception
is
deprecated
;
"
            
"
use
ServerConnection
.
handshake_exc
instead
"
            
DeprecationWarning
        
)
        
return
self
.
_exception
    
classmethod
    
def
parse
(
        
cls
        
read_line
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
    
)
-
>
Generator
[
None
None
Request
]
:
        
"
"
"
        
Parse
a
WebSocket
handshake
request
.
        
This
is
a
generator
-
based
coroutine
.
        
The
request
path
isn
'
t
URL
-
decoded
or
validated
in
any
way
.
        
The
request
path
and
headers
are
expected
to
contain
only
ASCII
        
characters
.
Other
characters
are
represented
with
surrogate
escapes
.
        
:
meth
:
parse
doesn
'
t
attempt
to
read
the
request
body
because
        
WebSocket
handshake
requests
don
'
t
have
one
.
If
the
request
contains
a
        
body
it
may
be
read
from
the
data
stream
after
:
meth
:
parse
returns
.
        
Args
:
            
read_line
:
generator
-
based
coroutine
that
reads
a
LF
-
terminated
                
line
or
raises
an
exception
if
there
isn
'
t
enough
data
        
Raises
:
            
EOFError
:
if
the
connection
is
closed
without
a
full
HTTP
request
.
            
SecurityError
:
if
the
request
exceeds
a
security
limit
.
            
ValueError
:
if
the
request
isn
'
t
well
formatted
.
        
"
"
"
        
try
:
            
request_line
=
yield
from
parse_line
(
read_line
)
        
except
EOFError
as
exc
:
            
raise
EOFError
(
"
connection
closed
while
reading
HTTP
request
line
"
)
from
exc
        
try
:
            
method
raw_path
version
=
request_line
.
split
(
b
"
"
2
)
        
except
ValueError
:
            
raise
ValueError
(
f
"
invalid
HTTP
request
line
:
{
d
(
request_line
)
}
"
)
from
None
        
if
method
!
=
b
"
GET
"
:
            
raise
ValueError
(
f
"
unsupported
HTTP
method
:
{
d
(
method
)
}
"
)
        
if
version
!
=
b
"
HTTP
/
1
.
1
"
:
            
raise
ValueError
(
f
"
unsupported
HTTP
version
:
{
d
(
version
)
}
"
)
        
path
=
raw_path
.
decode
(
"
ascii
"
"
surrogateescape
"
)
        
headers
=
yield
from
parse_headers
(
read_line
)
        
if
"
Transfer
-
Encoding
"
in
headers
:
            
raise
NotImplementedError
(
"
transfer
codings
aren
'
t
supported
"
)
        
if
"
Content
-
Length
"
in
headers
:
            
raise
ValueError
(
"
unsupported
request
body
"
)
        
return
cls
(
path
headers
)
    
def
serialize
(
self
)
-
>
bytes
:
        
"
"
"
        
Serialize
a
WebSocket
handshake
request
.
        
"
"
"
        
request
=
f
"
GET
{
self
.
path
}
HTTP
/
1
.
1
\
r
\
n
"
.
encode
(
)
        
request
+
=
self
.
headers
.
serialize
(
)
        
return
request
dataclasses
.
dataclass
class
Response
:
    
"
"
"
    
WebSocket
handshake
response
.
    
Attributes
:
        
status_code
:
Response
code
.
        
reason_phrase
:
Response
reason
.
        
headers
:
Response
headers
.
        
body
:
Response
body
if
any
.
    
"
"
"
    
status_code
:
int
    
reason_phrase
:
str
    
headers
:
datastructures
.
Headers
    
body
:
Optional
[
bytes
]
=
None
    
_exception
:
Optional
[
Exception
]
=
None
    
property
    
def
exception
(
self
)
-
>
Optional
[
Exception
]
:
        
warnings
.
warn
(
            
"
Response
.
exception
is
deprecated
;
"
            
"
use
ClientConnection
.
handshake_exc
instead
"
            
DeprecationWarning
        
)
        
return
self
.
_exception
    
classmethod
    
def
parse
(
        
cls
        
read_line
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
        
read_exact
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
        
read_to_eof
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
    
)
-
>
Generator
[
None
None
Response
]
:
        
"
"
"
        
Parse
a
WebSocket
handshake
response
.
        
This
is
a
generator
-
based
coroutine
.
        
The
reason
phrase
and
headers
are
expected
to
contain
only
ASCII
        
characters
.
Other
characters
are
represented
with
surrogate
escapes
.
        
Args
:
            
read_line
:
generator
-
based
coroutine
that
reads
a
LF
-
terminated
                
line
or
raises
an
exception
if
there
isn
'
t
enough
data
.
            
read_exact
:
generator
-
based
coroutine
that
reads
the
requested
                
bytes
or
raises
an
exception
if
there
isn
'
t
enough
data
.
            
read_to_eof
:
generator
-
based
coroutine
that
reads
until
the
end
                
of
the
stream
.
        
Raises
:
            
EOFError
:
if
the
connection
is
closed
without
a
full
HTTP
response
.
            
SecurityError
:
if
the
response
exceeds
a
security
limit
.
            
LookupError
:
if
the
response
isn
'
t
well
formatted
.
            
ValueError
:
if
the
response
isn
'
t
well
formatted
.
        
"
"
"
        
try
:
            
status_line
=
yield
from
parse_line
(
read_line
)
        
except
EOFError
as
exc
:
            
raise
EOFError
(
"
connection
closed
while
reading
HTTP
status
line
"
)
from
exc
        
try
:
            
version
raw_status_code
raw_reason
=
status_line
.
split
(
b
"
"
2
)
        
except
ValueError
:
            
raise
ValueError
(
f
"
invalid
HTTP
status
line
:
{
d
(
status_line
)
}
"
)
from
None
        
if
version
!
=
b
"
HTTP
/
1
.
1
"
:
            
raise
ValueError
(
f
"
unsupported
HTTP
version
:
{
d
(
version
)
}
"
)
        
try
:
            
status_code
=
int
(
raw_status_code
)
        
except
ValueError
:
            
raise
ValueError
(
                
f
"
invalid
HTTP
status
code
:
{
d
(
raw_status_code
)
}
"
            
)
from
None
        
if
not
100
<
=
status_code
<
1000
:
            
raise
ValueError
(
f
"
unsupported
HTTP
status
code
:
{
d
(
raw_status_code
)
}
"
)
        
if
not
_value_re
.
fullmatch
(
raw_reason
)
:
            
raise
ValueError
(
f
"
invalid
HTTP
reason
phrase
:
{
d
(
raw_reason
)
}
"
)
        
reason
=
raw_reason
.
decode
(
)
        
headers
=
yield
from
parse_headers
(
read_line
)
        
if
"
Transfer
-
Encoding
"
in
headers
:
            
raise
NotImplementedError
(
"
transfer
codings
aren
'
t
supported
"
)
        
if
100
<
=
status_code
<
200
or
status_code
=
=
204
or
status_code
=
=
304
:
            
body
=
None
        
else
:
            
content_length
:
Optional
[
int
]
            
try
:
                
raw_content_length
=
headers
[
"
Content
-
Length
"
]
            
except
KeyError
:
                
content_length
=
None
            
else
:
                
content_length
=
int
(
raw_content_length
)
            
if
content_length
is
None
:
                
try
:
                    
body
=
yield
from
read_to_eof
(
MAX_BODY
)
                
except
RuntimeError
:
                    
raise
exceptions
.
SecurityError
(
                        
f
"
body
too
large
:
over
{
MAX_BODY
}
bytes
"
                    
)
            
elif
content_length
>
MAX_BODY
:
                
raise
exceptions
.
SecurityError
(
                    
f
"
body
too
large
:
{
content_length
}
bytes
"
                
)
            
else
:
                
body
=
yield
from
read_exact
(
content_length
)
        
return
cls
(
status_code
reason
headers
body
)
    
def
serialize
(
self
)
-
>
bytes
:
        
"
"
"
        
Serialize
a
WebSocket
handshake
response
.
        
"
"
"
        
response
=
f
"
HTTP
/
1
.
1
{
self
.
status_code
}
{
self
.
reason_phrase
}
\
r
\
n
"
.
encode
(
)
        
response
+
=
self
.
headers
.
serialize
(
)
        
if
self
.
body
is
not
None
:
            
response
+
=
self
.
body
        
return
response
def
parse_headers
(
    
read_line
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
)
-
>
Generator
[
None
None
datastructures
.
Headers
]
:
    
"
"
"
    
Parse
HTTP
headers
.
    
Non
-
ASCII
characters
are
represented
with
surrogate
escapes
.
    
Args
:
        
read_line
:
generator
-
based
coroutine
that
reads
a
LF
-
terminated
line
            
or
raises
an
exception
if
there
isn
'
t
enough
data
.
    
Raises
:
        
EOFError
:
if
the
connection
is
closed
without
complete
headers
.
        
SecurityError
:
if
the
request
exceeds
a
security
limit
.
        
ValueError
:
if
the
request
isn
'
t
well
formatted
.
    
"
"
"
    
headers
=
datastructures
.
Headers
(
)
    
for
_
in
range
(
MAX_HEADERS
+
1
)
:
        
try
:
            
line
=
yield
from
parse_line
(
read_line
)
        
except
EOFError
as
exc
:
            
raise
EOFError
(
"
connection
closed
while
reading
HTTP
headers
"
)
from
exc
        
if
line
=
=
b
"
"
:
            
break
        
try
:
            
raw_name
raw_value
=
line
.
split
(
b
"
:
"
1
)
        
except
ValueError
:
            
raise
ValueError
(
f
"
invalid
HTTP
header
line
:
{
d
(
line
)
}
"
)
from
None
        
if
not
_token_re
.
fullmatch
(
raw_name
)
:
            
raise
ValueError
(
f
"
invalid
HTTP
header
name
:
{
d
(
raw_name
)
}
"
)
        
raw_value
=
raw_value
.
strip
(
b
"
\
t
"
)
        
if
not
_value_re
.
fullmatch
(
raw_value
)
:
            
raise
ValueError
(
f
"
invalid
HTTP
header
value
:
{
d
(
raw_value
)
}
"
)
        
name
=
raw_name
.
decode
(
"
ascii
"
)
        
value
=
raw_value
.
decode
(
"
ascii
"
"
surrogateescape
"
)
        
headers
[
name
]
=
value
    
else
:
        
raise
exceptions
.
SecurityError
(
"
too
many
HTTP
headers
"
)
    
return
headers
def
parse_line
(
    
read_line
:
Callable
[
[
int
]
Generator
[
None
None
bytes
]
]
)
-
>
Generator
[
None
None
bytes
]
:
    
"
"
"
    
Parse
a
single
line
.
    
CRLF
is
stripped
from
the
return
value
.
    
Args
:
        
read_line
:
generator
-
based
coroutine
that
reads
a
LF
-
terminated
line
            
or
raises
an
exception
if
there
isn
'
t
enough
data
.
    
Raises
:
        
EOFError
:
if
the
connection
is
closed
without
a
CRLF
.
        
SecurityError
:
if
the
response
exceeds
a
security
limit
.
    
"
"
"
    
try
:
        
line
=
yield
from
read_line
(
MAX_LINE
)
    
except
RuntimeError
:
        
raise
exceptions
.
SecurityError
(
"
line
too
long
"
)
    
if
not
line
.
endswith
(
b
"
\
r
\
n
"
)
:
        
raise
EOFError
(
"
line
without
CRLF
"
)
    
return
line
[
:
-
2
]
