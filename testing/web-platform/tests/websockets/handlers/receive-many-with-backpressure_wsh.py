import
time
def
web_socket_do_extra_handshake
(
request
)
:
    
request
.
ws_extension_processors
=
[
]
def
web_socket_transfer_data
(
request
)
:
    
while
True
:
        
time
.
sleep
(
0
.
1
)
        
line
=
request
.
ws_stream
.
receive_message
(
)
        
if
line
is
None
:
            
return
        
request
.
ws_stream
.
send_message
(
str
(
len
(
line
)
)
binary
=
False
)
