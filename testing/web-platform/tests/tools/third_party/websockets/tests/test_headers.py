import
unittest
from
websockets
.
exceptions
import
InvalidHeaderFormat
InvalidHeaderValue
from
websockets
.
headers
import
*
class
HeadersTests
(
unittest
.
TestCase
)
:
    
def
test_parse_connection
(
self
)
:
        
for
header
parsed
in
[
            
(
"
Upgrade
"
[
"
Upgrade
"
]
)
            
(
"
keep
-
alive
Upgrade
"
[
"
keep
-
alive
"
"
Upgrade
"
]
)
            
(
"
\
t
Upgrade
"
[
"
Upgrade
"
]
)
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
self
.
assertEqual
(
parse_connection
(
header
)
parsed
)
    
def
test_parse_connection_invalid_header_format
(
self
)
:
        
for
header
in
[
"
?
?
?
"
"
keep
-
alive
;
Upgrade
"
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderFormat
)
:
                    
parse_connection
(
header
)
    
def
test_parse_upgrade
(
self
)
:
        
for
header
parsed
in
[
            
(
"
websocket
"
[
"
websocket
"
]
)
            
(
"
http
/
3
.
0
websocket
"
[
"
http
/
3
.
0
"
"
websocket
"
]
)
            
(
"
WebSocket
\
t
"
[
"
WebSocket
"
]
)
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
self
.
assertEqual
(
parse_upgrade
(
header
)
parsed
)
    
def
test_parse_upgrade_invalid_header_format
(
self
)
:
        
for
header
in
[
"
?
?
?
"
"
websocket
2
"
"
http
/
3
.
0
;
websocket
"
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderFormat
)
:
                    
parse_upgrade
(
header
)
    
def
test_parse_extension
(
self
)
:
        
for
header
parsed
in
[
            
(
"
foo
"
[
(
"
foo
"
[
]
)
]
)
            
(
"
foo
bar
"
[
(
"
foo
"
[
]
)
(
"
bar
"
[
]
)
]
)
            
(
                
'
foo
;
name
;
token
=
token
;
quoted
-
string
=
"
quoted
-
string
"
'
                
"
bar
;
quux
;
quuux
"
                
[
                    
(
                        
"
foo
"
                        
[
                            
(
"
name
"
None
)
                            
(
"
token
"
"
token
"
)
                            
(
"
quoted
-
string
"
"
quoted
-
string
"
)
                        
]
                    
)
                    
(
"
bar
"
[
(
"
quux
"
None
)
(
"
quuux
"
None
)
]
)
                
]
            
)
            
(
                
"
\
t
foo
;
bar
=
42
baz
"
                
[
(
"
foo
"
[
(
"
bar
"
"
42
"
)
]
)
(
"
baz
"
[
]
)
]
            
)
            
(
"
permessage
-
deflate
"
[
(
"
permessage
-
deflate
"
[
]
)
]
)
            
(
                
"
permessage
-
deflate
;
client_max_window_bits
"
                
[
(
"
permessage
-
deflate
"
[
(
"
client_max_window_bits
"
None
)
]
)
]
            
)
            
(
                
"
permessage
-
deflate
;
server_max_window_bits
=
10
"
                
[
(
"
permessage
-
deflate
"
[
(
"
server_max_window_bits
"
"
10
"
)
]
)
]
            
)
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
self
.
assertEqual
(
parse_extension
(
header
)
parsed
)
                
unparsed
=
build_extension
(
parsed
)
                
self
.
assertEqual
(
parse_extension
(
unparsed
)
parsed
)
    
def
test_parse_extension_invalid_header_format
(
self
)
:
        
for
header
in
[
            
"
"
            
"
\
t
"
            
"
foo
;
"
            
"
foo
;
bar
;
"
            
"
foo
;
bar
=
"
            
'
foo
;
bar
=
"
baz
'
            
"
foo
bar
baz
=
quux
;
quuux
"
            
'
foo
;
bar
=
"
"
'
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderFormat
)
:
                    
parse_extension
(
header
)
    
def
test_parse_subprotocol
(
self
)
:
        
for
header
parsed
in
[
            
(
"
foo
"
[
"
foo
"
]
)
            
(
"
foo
bar
"
[
"
foo
"
"
bar
"
]
)
            
(
"
\
t
foo
bar
baz
"
[
"
foo
"
"
bar
"
"
baz
"
]
)
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
self
.
assertEqual
(
parse_subprotocol
(
header
)
parsed
)
                
unparsed
=
build_subprotocol
(
parsed
)
                
self
.
assertEqual
(
parse_subprotocol
(
unparsed
)
parsed
)
    
def
test_parse_subprotocol_invalid_header
(
self
)
:
        
for
header
in
[
            
"
"
            
"
\
t
"
            
"
foo
;
bar
"
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderFormat
)
:
                    
parse_subprotocol
(
header
)
    
def
test_build_www_authenticate_basic
(
self
)
:
        
self
.
assertEqual
(
            
build_www_authenticate_basic
(
"
foo
"
)
'
Basic
realm
=
"
foo
"
charset
=
"
UTF
-
8
"
'
        
)
    
def
test_build_www_authenticate_basic_invalid_realm
(
self
)
:
        
with
self
.
assertRaises
(
ValueError
)
:
            
build_www_authenticate_basic
(
"
\
u0007
"
)
    
def
test_build_authorization_basic
(
self
)
:
        
self
.
assertEqual
(
            
build_authorization_basic
(
"
Aladdin
"
"
open
sesame
"
)
            
"
Basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
"
        
)
    
def
test_build_authorization_basic_utf8
(
self
)
:
        
self
.
assertEqual
(
            
build_authorization_basic
(
"
test
"
"
123
"
)
"
Basic
dGVzdDoxMjPCow
=
=
"
        
)
    
def
test_parse_authorization_basic
(
self
)
:
        
for
header
parsed
in
[
            
(
"
Basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
"
(
"
Aladdin
"
"
open
sesame
"
)
)
            
(
"
Basic
dGVzdDoxMjPCow
=
=
"
(
"
test
"
"
123
"
)
)
            
(
"
Basic
YWxhZGRpbjpvcGVuOnNlc2FtZQ
=
=
"
(
"
aladdin
"
"
open
:
sesame
"
)
)
            
(
"
basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
"
(
"
Aladdin
"
"
open
sesame
"
)
)
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
self
.
assertEqual
(
parse_authorization_basic
(
header
)
parsed
)
    
def
test_parse_authorization_basic_invalid_header_format
(
self
)
:
        
for
header
in
[
            
"
/
/
Basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
"
            
"
Basic
\
tQWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
"
            
"
Basic
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
"
            
"
Basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
=
=
/
/
"
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderFormat
)
:
                    
parse_authorization_basic
(
header
)
    
def
test_parse_authorization_basic_invalid_header_value
(
self
)
:
        
for
header
in
[
            
"
Digest
.
.
.
"
            
"
Basic
QWxhZGRpbjpvcGVuIHNlc2FtZQ
"
            
"
Basic
QWxhZGNlc2FtZQ
=
=
"
        
]
:
            
with
self
.
subTest
(
header
=
header
)
:
                
with
self
.
assertRaises
(
InvalidHeaderValue
)
:
                    
parse_authorization_basic
(
header
)
