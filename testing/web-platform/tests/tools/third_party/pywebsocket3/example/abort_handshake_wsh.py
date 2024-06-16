from
__future__
import
absolute_import
from
pywebsocket3
import
handshake
def
web_socket_do_extra_handshake
(
request
)
:
    
raise
handshake
.
AbortedByUserException
(
        
"
Aborted
in
web_socket_do_extra_handshake
"
)
def
web_socket_transfer_data
(
request
)
:
    
pass
