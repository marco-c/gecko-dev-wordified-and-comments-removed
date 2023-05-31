import
socket
from
typing
import
AnyStr
Dict
List
TypeVar
from
.
logger
import
get_logger
KT
=
TypeVar
(
'
KT
'
)
VT
=
TypeVar
(
'
VT
'
)
def
isomorphic_decode
(
s
:
AnyStr
)
-
>
str
:
    
"
"
"
Decodes
a
binary
string
into
a
text
string
using
iso
-
8859
-
1
.
    
Returns
str
.
The
function
is
a
no
-
op
if
the
argument
already
has
a
text
    
type
.
iso
-
8859
-
1
is
chosen
because
it
is
an
8
-
bit
encoding
whose
code
    
points
range
from
0x0
to
0xFF
and
the
values
are
the
same
as
the
binary
    
representations
so
any
binary
string
can
be
decoded
into
and
encoded
from
    
iso
-
8859
-
1
without
any
errors
or
data
loss
.
Python
3
also
uses
iso
-
8859
-
1
    
(
or
latin
-
1
)
extensively
in
http
:
    
https
:
/
/
github
.
com
/
python
/
cpython
/
blob
/
273fc220b25933e443c82af6888eb1871d032fb8
/
Lib
/
http
/
client
.
py
#
L213
    
"
"
"
    
if
isinstance
(
s
str
)
:
        
return
s
    
if
isinstance
(
s
bytes
)
:
        
return
s
.
decode
(
"
iso
-
8859
-
1
"
)
    
raise
TypeError
(
"
Unexpected
value
(
expecting
string
-
like
)
:
%
r
"
%
s
)
def
isomorphic_encode
(
s
:
AnyStr
)
-
>
bytes
:
    
"
"
"
Encodes
a
text
-
type
string
into
binary
data
using
iso
-
8859
-
1
.
    
Returns
bytes
.
The
function
is
a
no
-
op
if
the
argument
already
has
a
    
binary
type
.
This
is
the
counterpart
of
isomorphic_decode
.
    
"
"
"
    
if
isinstance
(
s
bytes
)
:
        
return
s
    
if
isinstance
(
s
str
)
:
        
return
s
.
encode
(
"
iso
-
8859
-
1
"
)
    
raise
TypeError
(
"
Unexpected
value
(
expecting
string
-
like
)
:
%
r
"
%
s
)
def
invert_dict
(
dict
:
Dict
[
KT
List
[
VT
]
]
)
-
>
Dict
[
VT
KT
]
:
    
rv
=
{
}
    
for
key
values
in
dict
.
items
(
)
:
        
for
value
in
values
:
            
if
value
in
rv
:
                
raise
ValueError
            
rv
[
value
]
=
key
    
return
rv
class
HTTPException
(
Exception
)
:
    
def
__init__
(
self
code
:
int
message
:
str
=
"
"
)
:
        
self
.
code
=
code
        
self
.
message
=
message
def
_open_socket
(
host
:
str
port
:
int
)
-
>
socket
.
socket
:
    
sock
=
socket
.
socket
(
socket
.
AF_INET
socket
.
SOCK_STREAM
)
    
if
port
!
=
0
:
        
sock
.
setsockopt
(
socket
.
SOL_SOCKET
socket
.
SO_REUSEADDR
1
)
    
sock
.
bind
(
(
host
port
)
)
    
sock
.
listen
(
5
)
    
return
sock
def
is_bad_port
(
port
:
int
)
-
>
bool
:
    
"
"
"
    
Bad
port
as
per
https
:
/
/
fetch
.
spec
.
whatwg
.
org
/
#
port
-
blocking
    
"
"
"
    
return
port
in
[
        
1
        
7
        
9
        
11
        
13
        
15
        
17
        
19
        
20
        
21
        
22
        
23
        
25
        
37
        
42
        
43
        
53
        
69
        
77
        
79
        
87
        
95
        
101
        
102
        
103
        
104
        
109
        
110
        
111
        
113
        
115
        
117
        
119
        
123
        
135
        
137
        
139
        
143
        
161
        
179
        
389
        
427
        
465
        
512
        
513
        
514
        
515
        
526
        
530
        
531
        
532
        
540
        
548
        
554
        
556
        
563
        
587
        
601
        
636
        
989
        
999
        
993
        
995
        
1719
        
1720
        
1723
        
2049
        
3659
        
4045
        
5060
        
5061
        
6000
        
6566
        
6665
        
6666
        
6667
        
6668
        
6669
        
6697
        
10080
    
]
def
get_port
(
host
:
str
=
'
'
)
-
>
int
:
    
host
=
host
or
'
127
.
0
.
0
.
1
'
    
port
=
0
    
while
True
:
        
free_socket
=
_open_socket
(
host
0
)
        
port
=
free_socket
.
getsockname
(
)
[
1
]
        
free_socket
.
close
(
)
        
if
not
is_bad_port
(
port
)
:
            
break
    
return
port
def
http2_compatible
(
)
-
>
bool
:
    
import
ssl
    
if
not
ssl
.
OPENSSL_VERSION
.
startswith
(
"
OpenSSL
"
)
:
        
logger
=
get_logger
(
)
        
logger
.
warning
(
            
'
Skipping
HTTP
/
2
.
0
compatibility
check
as
system
is
not
using
'
            
'
OpenSSL
(
found
:
%
s
)
'
%
ssl
.
OPENSSL_VERSION
)
        
return
True
    
ssl_v
=
ssl
.
OPENSSL_VERSION_INFO
    
return
(
ssl_v
[
0
]
>
1
or
            
(
ssl_v
[
0
]
=
=
1
and
             
(
ssl_v
[
1
]
=
=
1
or
              
(
ssl_v
[
1
]
=
=
0
and
ssl_v
[
2
]
>
=
2
)
)
)
)
def
get_error_cause
(
exc
:
BaseException
)
-
>
BaseException
:
    
"
"
"
Get
the
parent
cause
/
context
from
an
exception
"
"
"
    
if
exc
.
__cause__
is
not
None
:
        
return
exc
.
__cause__
    
if
exc
.
__context__
is
not
None
:
        
return
exc
.
__context__
    
return
exc
