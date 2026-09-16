def
session_established
(
session
)
:
    
stream_id
=
session
.
create_bidirectional_stream
(
)
    
data
=
b
'
X
'
*
5000
    
session
.
send_stream_data
(
stream_id
data
end_stream
=
True
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
    
pass
def
datagram_received
(
session
data
:
bytes
)
:
    
session
.
send_datagram
(
data
)
