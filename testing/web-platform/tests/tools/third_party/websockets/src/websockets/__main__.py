from
__future__
import
annotations
import
argparse
import
os
import
signal
import
sys
import
threading
try
:
    
import
readline
except
ImportError
:
    
pass
from
.
sync
.
client
import
ClientConnection
connect
from
.
version
import
version
as
websockets_version
if
sys
.
platform
=
=
"
win32
"
:
    
def
win_enable_vt100
(
)
-
>
None
:
        
"
"
"
        
Enable
VT
-
100
for
console
output
on
Windows
.
        
See
also
https
:
/
/
bugs
.
python
.
org
/
issue29059
.
        
"
"
"
        
import
ctypes
        
STD_OUTPUT_HANDLE
=
ctypes
.
c_uint
(
-
11
)
        
INVALID_HANDLE_VALUE
=
ctypes
.
c_uint
(
-
1
)
        
ENABLE_VIRTUAL_TERMINAL_PROCESSING
=
0x004
        
handle
=
ctypes
.
windll
.
kernel32
.
GetStdHandle
(
STD_OUTPUT_HANDLE
)
        
if
handle
=
=
INVALID_HANDLE_VALUE
:
            
raise
RuntimeError
(
"
unable
to
obtain
stdout
handle
"
)
        
cur_mode
=
ctypes
.
c_uint
(
)
        
if
ctypes
.
windll
.
kernel32
.
GetConsoleMode
(
handle
ctypes
.
byref
(
cur_mode
)
)
=
=
0
:
            
raise
RuntimeError
(
"
unable
to
query
current
console
mode
"
)
        
py_int_mode
=
int
.
from_bytes
(
cur_mode
sys
.
byteorder
)
        
new_mode
=
ctypes
.
c_uint
(
py_int_mode
|
ENABLE_VIRTUAL_TERMINAL_PROCESSING
)
        
if
ctypes
.
windll
.
kernel32
.
SetConsoleMode
(
handle
new_mode
)
=
=
0
:
            
raise
RuntimeError
(
"
unable
to
set
console
mode
"
)
def
print_during_input
(
string
:
str
)
-
>
None
:
    
sys
.
stdout
.
write
(
        
"
\
N
{
ESC
}
7
"
        
"
\
N
{
LINE
FEED
}
"
        
"
\
N
{
ESC
}
[
A
"
        
"
\
N
{
ESC
}
[
L
"
        
f
"
{
string
}
\
N
{
LINE
FEED
}
"
        
"
\
N
{
ESC
}
8
"
        
"
\
N
{
ESC
}
[
B
"
    
)
    
sys
.
stdout
.
flush
(
)
def
print_over_input
(
string
:
str
)
-
>
None
:
    
sys
.
stdout
.
write
(
        
"
\
N
{
CARRIAGE
RETURN
}
"
        
"
\
N
{
ESC
}
[
K
"
        
f
"
{
string
}
\
N
{
LINE
FEED
}
"
    
)
    
sys
.
stdout
.
flush
(
)
def
print_incoming_messages
(
websocket
:
ClientConnection
stop
:
threading
.
Event
)
-
>
None
:
    
for
message
in
websocket
:
        
if
isinstance
(
message
str
)
:
            
print_during_input
(
"
<
"
+
message
)
        
else
:
            
print_during_input
(
"
<
(
binary
)
"
+
message
.
hex
(
)
)
    
if
not
stop
.
is_set
(
)
:
        
if
sys
.
platform
=
=
"
win32
"
:
            
ctrl_c
=
signal
.
CTRL_C_EVENT
        
else
:
            
ctrl_c
=
signal
.
SIGINT
        
os
.
kill
(
os
.
getpid
(
)
ctrl_c
)
def
main
(
)
-
>
None
:
    
parser
=
argparse
.
ArgumentParser
(
        
prog
=
"
python
-
m
websockets
"
        
description
=
"
Interactive
WebSocket
client
.
"
        
add_help
=
False
    
)
    
group
=
parser
.
add_mutually_exclusive_group
(
)
    
group
.
add_argument
(
"
-
-
version
"
action
=
"
store_true
"
)
    
group
.
add_argument
(
"
uri
"
metavar
=
"
<
uri
>
"
nargs
=
"
?
"
)
    
args
=
parser
.
parse_args
(
)
    
if
args
.
version
:
        
print
(
f
"
websockets
{
websockets_version
}
"
)
        
return
    
if
args
.
uri
is
None
:
        
parser
.
error
(
"
the
following
arguments
are
required
:
<
uri
>
"
)
    
if
sys
.
platform
=
=
"
win32
"
:
        
try
:
            
win_enable_vt100
(
)
        
except
RuntimeError
as
exc
:
            
sys
.
stderr
.
write
(
                
f
"
Unable
to
set
terminal
to
VT100
mode
.
This
is
only
"
                
f
"
supported
since
Win10
anniversary
update
.
Expect
"
                
f
"
weird
symbols
on
the
terminal
.
\
nError
:
{
exc
}
\
n
"
            
)
            
sys
.
stderr
.
flush
(
)
    
try
:
        
websocket
=
connect
(
args
.
uri
)
    
except
Exception
as
exc
:
        
print
(
f
"
Failed
to
connect
to
{
args
.
uri
}
:
{
exc
}
.
"
)
        
sys
.
exit
(
1
)
    
else
:
        
print
(
f
"
Connected
to
{
args
.
uri
}
.
"
)
    
stop
=
threading
.
Event
(
)
    
thread
=
threading
.
Thread
(
target
=
print_incoming_messages
args
=
(
websocket
stop
)
)
    
thread
.
start
(
)
    
try
:
        
while
True
:
            
message
=
input
(
"
>
"
)
            
websocket
.
send
(
message
)
    
except
(
KeyboardInterrupt
EOFError
)
:
        
stop
.
set
(
)
        
websocket
.
close
(
)
        
print_over_input
(
"
Connection
closed
.
"
)
    
thread
.
join
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
    
main
(
)
