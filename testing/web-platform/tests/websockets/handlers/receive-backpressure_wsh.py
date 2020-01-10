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
    
time
.
sleep
(
2
)
;
    
request
.
ws_stream
.
receive_message
(
)
