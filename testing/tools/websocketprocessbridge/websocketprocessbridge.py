from
__future__
import
absolute_import
print_function
from
twisted
.
internet
import
protocol
reactor
from
twisted
.
internet
.
task
import
LoopingCall
from
autobahn
.
twisted
.
websocket
import
WebSocketServerProtocol
WebSocketServerFactory
import
psutil
import
argparse
import
six
import
sys
import
os
commands
=
{
    
"
iceserver
"
:
[
sys
.
executable
"
-
u
"
os
.
path
.
join
(
"
iceserver
"
"
iceserver
.
py
"
)
]
}
class
ProcessSide
(
protocol
.
ProcessProtocol
)
:
    
"
"
"
Handles
the
spawned
process
(
I
/
O
process
termination
)
"
"
"
    
def
__init__
(
self
socketSide
)
:
        
self
.
socketSide
=
socketSide
    
def
outReceived
(
self
data
)
:
        
data
=
six
.
ensure_str
(
data
)
        
if
self
.
socketSide
:
            
lines
=
data
.
splitlines
(
)
            
for
line
in
lines
:
                
self
.
socketSide
.
sendMessage
(
line
.
encode
(
"
utf8
"
)
False
)
    
def
errReceived
(
self
data
)
:
        
self
.
outReceived
(
data
)
    
def
processEnded
(
self
reason
)
:
        
if
self
.
socketSide
:
            
self
.
outReceived
(
reason
.
getTraceback
(
)
)
            
self
.
socketSide
.
processGone
(
)
    
def
socketGone
(
self
)
:
        
self
.
socketSide
=
None
        
self
.
transport
.
loseConnection
(
)
        
self
.
transport
.
signalProcess
(
"
KILL
"
)
class
SocketSide
(
WebSocketServerProtocol
)
:
    
"
"
"
    
Handles
the
websocket
(
I
/
O
closed
connection
)
and
spawning
the
process
    
"
"
"
    
def
__init__
(
self
)
:
        
super
(
SocketSide
self
)
.
__init__
(
)
        
self
.
processSide
=
None
    
def
onConnect
(
self
request
)
:
        
return
None
    
def
onOpen
(
self
)
:
        
return
None
    
def
onMessage
(
self
payload
isBinary
)
:
        
if
not
self
.
processSide
:
            
self
.
processSide
=
ProcessSide
(
self
)
            
data
=
six
.
ensure_str
(
payload
)
            
try
:
                
reactor
.
spawnProcess
(
                    
self
.
processSide
commands
[
data
]
[
0
]
commands
[
data
]
env
=
os
.
environ
                
)
            
except
BaseException
as
e
:
                
print
(
e
.
str
(
)
)
                
self
.
sendMessage
(
e
.
str
(
)
)
                
self
.
processGone
(
)
    
def
onClose
(
self
wasClean
code
reason
)
:
        
if
self
.
processSide
:
            
self
.
processSide
.
socketGone
(
)
    
def
processGone
(
self
)
:
        
self
.
processSide
=
None
        
self
.
transport
.
loseConnection
(
)
parent_process
=
psutil
.
Process
(
os
.
getpid
(
)
)
.
parent
(
)
def
check_parent
(
)
:
    
"
"
"
Checks
if
parent
process
is
still
alive
and
exits
if
not
"
"
"
    
if
not
parent_process
.
is_running
(
)
:
        
print
(
"
websocket
/
process
bridge
exiting
because
parent
process
is
gone
"
)
        
reactor
.
stop
(
)
if
__name__
=
=
"
__main__
"
:
    
parser
=
argparse
.
ArgumentParser
(
description
=
"
Starts
websocket
/
process
bridge
.
"
)
    
parser
.
add_argument
(
        
"
-
-
port
"
        
type
=
str
        
dest
=
"
port
"
        
default
=
"
8191
"
        
help
=
"
Port
for
websocket
/
process
bridge
.
Default
8191
.
"
    
)
    
args
=
parser
.
parse_args
(
)
    
parent_checker
=
LoopingCall
(
check_parent
)
    
parent_checker
.
start
(
1
)
    
bridgeFactory
=
WebSocketServerFactory
(
)
    
bridgeFactory
.
protocol
=
SocketSide
    
reactor
.
listenTCP
(
int
(
args
.
port
)
bridgeFactory
)
    
print
(
"
websocket
/
process
bridge
listening
on
port
%
s
"
%
args
.
port
)
    
reactor
.
run
(
)
