from
__future__
import
annotations
import
argparse
import
asyncio
import
os
import
signal
import
sys
import
threading
from
typing
import
Any
Set
from
.
exceptions
import
ConnectionClosed
from
.
frames
import
Close
from
.
legacy
.
client
import
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
exit_from_event_loop_thread
(
    
loop
:
asyncio
.
AbstractEventLoop
    
stop
:
asyncio
.
Future
[
None
]
)
-
>
None
:
    
loop
.
stop
(
)
    
if
not
stop
.
done
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
async
def
run_client
(
    
uri
:
str
    
loop
:
asyncio
.
AbstractEventLoop
    
inputs
:
asyncio
.
Queue
[
str
]
    
stop
:
asyncio
.
Future
[
None
]
)
-
>
None
:
    
try
:
        
websocket
=
await
connect
(
uri
)
    
except
Exception
as
exc
:
        
print_over_input
(
f
"
Failed
to
connect
to
{
uri
}
:
{
exc
}
.
"
)
        
exit_from_event_loop_thread
(
loop
stop
)
        
return
    
else
:
        
print_during_input
(
f
"
Connected
to
{
uri
}
.
"
)
    
try
:
        
while
True
:
            
incoming
:
asyncio
.
Future
[
Any
]
=
asyncio
.
create_task
(
websocket
.
recv
(
)
)
            
outgoing
:
asyncio
.
Future
[
Any
]
=
asyncio
.
create_task
(
inputs
.
get
(
)
)
            
done
:
Set
[
asyncio
.
Future
[
Any
]
]
            
pending
:
Set
[
asyncio
.
Future
[
Any
]
]
            
done
pending
=
await
asyncio
.
wait
(
                
[
incoming
outgoing
stop
]
return_when
=
asyncio
.
FIRST_COMPLETED
            
)
            
if
incoming
in
pending
:
                
incoming
.
cancel
(
)
            
if
outgoing
in
pending
:
                
outgoing
.
cancel
(
)
            
if
incoming
in
done
:
                
try
:
                    
message
=
incoming
.
result
(
)
                
except
ConnectionClosed
:
                    
break
                
else
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
outgoing
in
done
:
                
message
=
outgoing
.
result
(
)
                
await
websocket
.
send
(
message
)
            
if
stop
in
done
:
                
break
    
finally
:
        
await
websocket
.
close
(
)
        
assert
websocket
.
close_code
is
not
None
and
websocket
.
close_reason
is
not
None
        
close_status
=
Close
(
websocket
.
close_code
websocket
.
close_reason
)
        
print_over_input
(
f
"
Connection
closed
:
{
close_status
}
.
"
)
        
exit_from_event_loop_thread
(
loop
stop
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
        
import
readline
    
except
ImportError
:
        
pass
    
loop
=
asyncio
.
new_event_loop
(
)
    
async
def
queue_factory
(
)
-
>
asyncio
.
Queue
[
str
]
:
        
return
asyncio
.
Queue
(
)
    
inputs
:
asyncio
.
Queue
[
str
]
=
loop
.
run_until_complete
(
queue_factory
(
)
)
    
stop
:
asyncio
.
Future
[
None
]
=
loop
.
create_future
(
)
    
loop
.
create_task
(
run_client
(
args
.
uri
loop
inputs
stop
)
)
    
thread
=
threading
.
Thread
(
target
=
loop
.
run_forever
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
            
loop
.
call_soon_threadsafe
(
inputs
.
put_nowait
message
)
    
except
(
KeyboardInterrupt
EOFError
)
:
        
loop
.
call_soon_threadsafe
(
stop
.
set_result
None
)
    
thread
.
join
(
)
    
loop
.
close
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
