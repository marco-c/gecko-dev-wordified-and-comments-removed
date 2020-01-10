"
"
"
A
fake
ADB
binary
"
"
"
from
__future__
import
absolute_import
import
os
import
SocketServer
import
sys
HOST
=
'
127
.
0
.
0
.
1
'
PORT
=
5037
class
ADBRequestHandler
(
SocketServer
.
BaseRequestHandler
)
:
    
def
sendData
(
self
data
)
:
        
header
=
'
OKAY
%
04x
'
%
len
(
data
)
        
all_data
=
header
+
data
        
total_length
=
len
(
all_data
)
        
sent_length
=
0
        
while
sent_length
<
total_length
:
            
sent
=
self
.
request
.
send
(
all_data
[
sent_length
:
]
)
            
sent_length
=
sent_length
+
sent
    
def
handle
(
self
)
:
        
while
True
:
            
data
=
self
.
request
.
recv
(
4096
)
            
if
'
host
:
kill
'
in
data
:
                
self
.
sendData
(
'
'
)
                
os
.
_exit
(
0
)
                
break
            
elif
'
host
:
version
'
in
data
:
                
self
.
sendData
(
'
001F
'
)
                
self
.
request
.
close
(
)
                
break
            
elif
'
host
:
track
-
devices
'
in
data
:
                
self
.
sendData
(
'
1234567890
\
tdevice
'
)
                
break
class
ADBServer
(
SocketServer
.
TCPServer
)
:
    
def
__init__
(
self
server_address
)
:
        
SocketServer
.
TCPServer
.
__init__
(
self
\
                                        
server_address
\
                                        
ADBRequestHandler
\
                                        
bind_and_activate
=
False
)
if
len
(
sys
.
argv
)
=
=
2
and
sys
.
argv
[
1
]
=
=
'
start
-
server
'
:
    
if
os
.
fork
(
)
>
0
:
        
sys
.
exit
(
0
)
    
os
.
setsid
(
)
    
if
os
.
fork
(
)
>
0
:
        
sys
.
exit
(
0
)
    
server
=
ADBServer
(
(
HOST
PORT
)
)
    
server
.
allow_reuse_address
=
True
    
server
.
server_bind
(
)
    
server
.
server_activate
(
)
    
server
.
serve_forever
(
)
