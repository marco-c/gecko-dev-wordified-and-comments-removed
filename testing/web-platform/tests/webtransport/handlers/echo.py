streams_dict
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
    
if
session
.
stream_is_unidirectional
(
stream_id
)
:
        
if
(
session
.
session_id
stream_id
)
not
in
streams_dict
.
keys
(
)
:
            
new_stream_id
=
session
.
create_unidirectional_stream
(
)
            
streams_dict
[
(
session
.
session_id
stream_id
)
]
=
new_stream_id
        
session
.
send_stream_data
(
streams_dict
[
(
session
.
session_id
stream_id
)
]
                                 
data
                                 
end_stream
=
stream_ended
)
        
if
(
stream_ended
)
:
          
del
streams_dict
[
(
session
.
session_id
stream_id
)
]
        
return
    
session
.
send_stream_data
(
stream_id
data
end_stream
=
stream_ended
)
def
session_closed
(
session
close_info
abruptly
)
:
    
keys_to_delete
=
[
key
for
key
in
streams_dict
if
key
[
0
]
=
=
session
.
session_id
]
    
for
key
in
keys_to_delete
:
        
del
streams_dict
[
key
]
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
