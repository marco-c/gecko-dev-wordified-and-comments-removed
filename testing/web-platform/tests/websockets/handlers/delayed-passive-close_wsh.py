from
pywebsocket3
import
common
import
time
def
web_socket_do_extra_handshake
(
request
)
:
    
pass
def
web_socket_transfer_data
(
request
)
:
    
request
.
ws_stream
.
receive_message
(
)
def
web_socket_passive_closing_handshake
(
request
)
:
    
code
reason
=
request
.
ws_close_code
request
.
ws_close_reason
    
if
code
=
=
common
.
STATUS_NO_STATUS_RECEIVED
:
        
code
=
None
    
time
.
sleep
(
1
)
    
return
code
reason
