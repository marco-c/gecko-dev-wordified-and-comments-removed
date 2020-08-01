import
asyncio
import
errno
import
signal
from
pexpect
import
EOF
asyncio
.
coroutine
def
expect_async
(
expecter
timeout
=
None
)
:
    
idx
=
expecter
.
existing_data
(
)
    
if
idx
is
not
None
:
        
return
idx
    
if
not
expecter
.
spawn
.
async_pw_transport
:
        
pw
=
PatternWaiter
(
)
        
pw
.
set_expecter
(
expecter
)
        
transport
pw
=
yield
from
asyncio
.
get_event_loop
(
)
\
            
.
connect_read_pipe
(
lambda
:
pw
expecter
.
spawn
)
        
expecter
.
spawn
.
async_pw_transport
=
pw
transport
    
else
:
        
pw
transport
=
expecter
.
spawn
.
async_pw_transport
        
pw
.
set_expecter
(
expecter
)
        
transport
.
resume_reading
(
)
    
try
:
        
return
(
yield
from
asyncio
.
wait_for
(
pw
.
fut
timeout
)
)
    
except
asyncio
.
TimeoutError
as
e
:
        
transport
.
pause_reading
(
)
        
return
expecter
.
timeout
(
e
)
asyncio
.
coroutine
def
repl_run_command_async
(
repl
cmdlines
timeout
=
-
1
)
:
    
res
=
[
]
    
repl
.
child
.
sendline
(
cmdlines
[
0
]
)
    
for
line
in
cmdlines
[
1
:
]
:
        
yield
from
repl
.
_expect_prompt
(
timeout
=
timeout
async_
=
True
)
        
res
.
append
(
repl
.
child
.
before
)
        
repl
.
child
.
sendline
(
line
)
    
prompt_idx
=
yield
from
repl
.
_expect_prompt
(
timeout
=
timeout
async_
=
True
)
    
if
prompt_idx
=
=
1
:
        
repl
.
child
.
kill
(
signal
.
SIGINT
)
        
yield
from
repl
.
_expect_prompt
(
timeout
=
1
async_
=
True
)
        
raise
ValueError
(
"
Continuation
prompt
found
-
input
was
incomplete
:
"
)
    
return
u
'
'
.
join
(
res
+
[
repl
.
child
.
before
]
)
class
PatternWaiter
(
asyncio
.
Protocol
)
:
    
transport
=
None
    
def
set_expecter
(
self
expecter
)
:
        
self
.
expecter
=
expecter
        
self
.
fut
=
asyncio
.
Future
(
)
    
def
found
(
self
result
)
:
        
if
not
self
.
fut
.
done
(
)
:
            
self
.
fut
.
set_result
(
result
)
            
self
.
transport
.
pause_reading
(
)
    
def
error
(
self
exc
)
:
        
if
not
self
.
fut
.
done
(
)
:
            
self
.
fut
.
set_exception
(
exc
)
            
self
.
transport
.
pause_reading
(
)
    
def
connection_made
(
self
transport
)
:
        
self
.
transport
=
transport
    
def
data_received
(
self
data
)
:
        
spawn
=
self
.
expecter
.
spawn
        
s
=
spawn
.
_decoder
.
decode
(
data
)
        
spawn
.
_log
(
s
'
read
'
)
        
if
self
.
fut
.
done
(
)
:
            
spawn
.
_before
.
write
(
s
)
            
spawn
.
_buffer
.
write
(
s
)
            
return
        
try
:
            
index
=
self
.
expecter
.
new_data
(
s
)
            
if
index
is
not
None
:
                
self
.
found
(
index
)
        
except
Exception
as
e
:
            
self
.
expecter
.
errored
(
)
            
self
.
error
(
e
)
    
def
eof_received
(
self
)
:
        
try
:
            
self
.
expecter
.
spawn
.
flag_eof
=
True
            
index
=
self
.
expecter
.
eof
(
)
        
except
EOF
as
e
:
            
self
.
error
(
e
)
        
else
:
            
self
.
found
(
index
)
    
def
connection_lost
(
self
exc
)
:
        
if
isinstance
(
exc
OSError
)
and
exc
.
errno
=
=
errno
.
EIO
:
            
self
.
eof_received
(
)
        
elif
exc
is
not
None
:
            
self
.
error
(
exc
)
