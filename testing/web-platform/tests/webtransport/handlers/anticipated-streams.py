import
json
buffered_data
=
{
}
def
session_established
(
session
)
:
    
session
.
create_bidirectional_stream
(
)
def
stream_data_received
(
session
                         
stream_id
:
int
                         
data
:
bytes
                         
stream_ended
:
bool
)
:
    
key
=
(
session
.
session_id
stream_id
)
    
if
key
not
in
buffered_data
:
        
buffered_data
[
key
]
=
b
'
'
    
buffered_data
[
key
]
+
=
data
    
if
not
stream_ended
:
        
return
    
full_data
=
buffered_data
[
key
]
    
del
buffered_data
[
key
]
    
try
:
        
request
=
json
.
loads
(
full_data
.
decode
(
'
utf
-
8
'
)
)
        
num_uni
=
request
.
get
(
'
uni
'
0
)
        
num_bidi
=
request
.
get
(
'
bidi
'
0
)
    
except
(
json
.
JSONDecodeError
UnicodeDecodeError
)
as
e
:
        
response
=
json
.
dumps
(
{
'
error
'
:
f
'
Invalid
JSON
:
{
str
(
e
)
}
'
}
)
        
session
.
send_stream_data
(
stream_id
response
.
encode
(
'
utf
-
8
'
)
end_stream
=
True
)
        
return
    
quic_conn
=
session
.
_http
.
_quic
    
bidi_max_streams
=
quic_conn
.
_remote_max_streams_bidi
    
uni_max_streams
=
quic_conn
.
_remote_max_streams_uni
    
response
=
json
.
dumps
(
{
        
'
uni_created
'
:
uni_max_streams
        
'
bidi_created
'
:
bidi_max_streams
        
'
uni_requested
'
:
num_uni
        
'
bidi_requested
'
:
num_bidi
    
}
)
    
session
.
send_stream_data
(
stream_id
response
.
encode
(
'
utf
-
8
'
)
end_stream
=
True
)
