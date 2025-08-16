import
sys
import
time
def
sleep_for_a_little_bit
(
)
:
    
time
.
sleep
(
0
.
2
)
def
spawn_child_and_exit
(
is_breakaway_job
)
:
    
"
"
"
    
Spawns
and
exits
child
processes
to
allow
tests
to
verify
that
they
detect
    
specifically
the
exit
of
this
(
parent
)
process
.
    
The
expected
sequence
of
outputs
is
as
follows
:
    
1
.
parent_start
    
2
.
first_child_start_and_exit
    
3
.
parent_after_first_child_exit
    
4
.
spawned_child_start
    
5
.
Listening
at
http
:
/
/
127
.
0
.
0
.
1
:
12345
-
with
12345
being
random
port
    
6
.
child_received_http_request
-
DELETE
request
from
test
.
    
7
.
data_from_child
:
kill_parent
    
8
.
parent_exit
       
(
now
the
parent
has
exit
)
       
(
child_process_still_alive_1
response
sent
to
request
from
step
6
)
       
(
wait
for
new
request
from
client
to
request
child
to
exit
)
       
(
child_process_still_alive_2
response
sent
to
that
new
request
)
    
9
.
spawned_child_exit
    
"
"
"
    
import
subprocess
    
print
(
"
1
.
parent_start
"
flush
=
True
)
    
subprocess
.
run
(
        
[
sys
.
executable
"
-
c
"
"
print
(
'
2
.
first_child_start_and_exit
'
)
"
]
        
stdout
=
sys
.
stdout
        
stderr
=
sys
.
stderr
    
)
    
sleep_for_a_little_bit
(
)
    
print
(
"
3
.
parent_after_first_child_exit
"
flush
=
True
)
    
creationflags
=
0
    
if
is_breakaway_job
:
        
creationflags
=
subprocess
.
CREATE_BREAKAWAY_FROM_JOB
    
child_proc
=
subprocess
.
Popen
(
        
[
sys
.
executable
"
-
u
"
__file__
"
spawned_child
"
]
        
creationflags
=
creationflags
        
stdin
=
subprocess
.
PIPE
        
stdout
=
subprocess
.
PIPE
        
stderr
=
sys
.
stdout
    
)
    
data_from_child
=
child_proc
.
stdout
.
readline
(
)
.
decode
(
)
.
rstrip
(
)
    
print
(
f
"
7
.
data_from_child
:
{
data_from_child
}
"
flush
=
True
)
    
print
(
"
8
.
parent_exit
"
flush
=
True
)
    
sleep_for_a_little_bit
(
)
    
sys
.
exit
(
0
)
def
spawned_child
(
)
:
    
import
http
.
server
    
import
socketserver
    
def
print_to_parent_stdout
(
msg
)
:
        
print
(
msg
flush
=
True
file
=
sys
.
stderr
)
    
print_to_parent_stdout
(
"
4
.
spawned_child_start
"
)
    
class
RequestHandler
(
http
.
server
.
BaseHTTPRequestHandler
)
:
        
def
log_message
(
self
*
args
)
:
            
pass
        
def
do_DELETE
(
self
)
:
            
print_to_parent_stdout
(
"
6
.
child_received_http_request
"
)
            
self
.
send_response
(
200
)
            
self
.
send_header
(
"
Connection
"
"
close
"
)
            
self
.
end_headers
(
)
            
sleep_for_a_little_bit
(
)
            
print
(
"
kill_parent
"
flush
=
True
)
            
res
=
sys
.
stdin
.
read
(
1
)
            
if
len
(
res
)
:
                
print_to_parent_stdout
(
"
spawned_child_UNEXPECTED_STDIN
"
)
            
self
.
wfile
.
write
(
b
"
child_process_still_alive_1
"
)
        
def
do_GET
(
self
)
:
            
self
.
send_response
(
200
)
            
self
.
send_header
(
"
Connection
"
"
close
"
)
            
self
.
end_headers
(
)
            
self
.
wfile
.
write
(
b
"
child_process_still_alive_2
"
)
    
with
socketserver
.
TCPServer
(
(
"
127
.
0
.
0
.
1
"
0
)
RequestHandler
)
as
server
:
        
host
port
=
server
.
server_address
[
:
2
]
        
print_to_parent_stdout
(
f
"
5
.
Listening
at
http
:
/
/
{
host
}
:
{
port
}
"
)
        
server
.
handle_request
(
)
        
server
.
handle_request
(
)
    
print_to_parent_stdout
(
"
9
.
spawned_child_exit
"
)
    
sys
.
exit
(
0
)
cmd
=
sys
.
argv
[
1
]
if
cmd
=
=
"
spawn_child_and_exit
"
:
    
spawn_child_and_exit
(
is_breakaway_job
=
False
)
elif
cmd
=
=
"
spawn_child_in_breakaway_job_and_exit
"
:
    
spawn_child_and_exit
(
is_breakaway_job
=
True
)
elif
cmd
=
=
"
spawned_child
"
:
    
spawned_child
(
)
else
:
    
raise
Exception
(
f
"
Unknown
command
:
{
cmd
}
"
)
