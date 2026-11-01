MAX_DATAGRAMS
=
10000
def
datagram_received
(
session
data
:
bytes
)
:
    
try
:
        
count
=
int
(
data
)
    
except
ValueError
:
        
return
    
count
=
max
(
0
min
(
count
MAX_DATAGRAMS
)
)
    
for
i
in
range
(
count
)
:
        
session
.
send_datagram
(
str
(
i
)
.
encode
(
)
)
