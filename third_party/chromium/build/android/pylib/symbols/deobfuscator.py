import
logging
import
os
import
subprocess
import
threading
import
time
import
uuid
from
devil
.
utils
import
reraiser_thread
from
pylib
import
constants
_MINIUMUM_TIMEOUT
=
3
.
0
_PER_LINE_TIMEOUT
=
.
002
_PROCESS_START_TIMEOUT
=
10
.
0
_MAX_RESTARTS
=
10
class
Deobfuscator
:
  
def
__init__
(
self
mapping_path
)
:
    
script_path
=
os
.
path
.
join
(
constants
.
DIR_SOURCE_ROOT
'
build
'
'
android
'
                               
'
stacktrace
'
'
java_deobfuscate
.
py
'
)
    
cmd
=
[
script_path
mapping_path
]
    
self
.
_lock
=
threading
.
Lock
(
)
    
self
.
_close_lock
=
threading
.
Lock
(
)
    
self
.
_closed_called
=
False
    
self
.
_proc
=
None
    
self
.
_proc_start_time
=
time
.
time
(
)
    
self
.
_proc
=
subprocess
.
Popen
(
cmd
                                  
bufsize
=
1
                                  
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
                                  
universal_newlines
=
True
                                  
close_fds
=
True
)
  
def
IsClosed
(
self
)
:
    
return
self
.
_closed_called
or
self
.
_proc
.
returncode
is
not
None
  
def
IsBusy
(
self
)
:
    
return
self
.
_lock
.
locked
(
)
  
def
IsReady
(
self
)
:
    
return
not
self
.
IsClosed
(
)
and
not
self
.
IsBusy
(
)
  
def
TransformLines
(
self
lines
)
:
    
"
"
"
Deobfuscates
obfuscated
names
found
in
the
given
lines
.
    
If
anything
goes
wrong
(
process
crashes
timeout
etc
)
returns
|
lines
|
.
    
Args
:
      
lines
:
A
list
of
strings
without
trailing
newlines
.
    
Returns
:
      
A
list
of
strings
without
trailing
newlines
.
    
"
"
"
    
if
not
lines
:
      
return
[
]
    
eof_line
=
uuid
.
uuid4
(
)
.
hex
    
out_lines
=
[
]
    
def
deobfuscate_reader
(
)
:
      
while
True
:
        
line
=
self
.
_proc
.
stdout
.
readline
(
)
        
if
not
line
:
          
break
        
line
=
line
[
:
-
1
]
        
if
line
=
=
eof_line
:
          
break
        
out_lines
.
append
(
line
)
    
if
self
.
IsBusy
(
)
:
      
logging
.
warning
(
'
deobfuscator
:
Having
to
wait
for
Java
deobfuscation
.
'
)
    
with
self
.
_lock
:
      
if
self
.
IsClosed
(
)
:
        
if
not
self
.
_closed_called
:
          
logging
.
warning
(
'
deobfuscator
:
Process
exited
with
code
=
%
d
.
'
                          
self
.
_proc
.
returncode
)
          
self
.
Close
(
)
        
return
lines
      
reader_thread
=
reraiser_thread
.
ReraiserThread
(
deobfuscate_reader
)
      
reader_thread
.
start
(
)
      
try
:
        
self
.
_proc
.
stdin
.
write
(
'
\
n
'
.
join
(
lines
)
)
        
self
.
_proc
.
stdin
.
write
(
'
\
n
{
}
\
n
'
.
format
(
eof_line
)
)
        
self
.
_proc
.
stdin
.
flush
(
)
        
time_since_proc_start
=
time
.
time
(
)
-
self
.
_proc_start_time
        
timeout
=
(
max
(
0
_PROCESS_START_TIMEOUT
-
time_since_proc_start
)
+
                   
max
(
_MINIUMUM_TIMEOUT
len
(
lines
)
*
_PER_LINE_TIMEOUT
)
)
        
reader_thread
.
join
(
timeout
)
        
if
self
.
IsClosed
(
)
:
          
logging
.
warning
(
              
'
deobfuscator
:
Close
(
)
called
by
another
thread
during
join
(
)
.
'
)
          
return
lines
        
if
reader_thread
.
is_alive
(
)
:
          
logging
.
error
(
'
deobfuscator
:
Timed
out
.
'
)
          
self
.
Close
(
)
          
return
lines
        
return
out_lines
      
except
IOError
:
        
logging
.
exception
(
'
deobfuscator
:
Exception
during
java_deobfuscate
'
)
        
self
.
Close
(
)
        
return
lines
  
def
Close
(
self
)
:
    
with
self
.
_close_lock
:
      
needs_closing
=
not
self
.
IsClosed
(
)
      
self
.
_closed_called
=
True
    
if
needs_closing
:
      
self
.
_proc
.
stdin
.
close
(
)
      
self
.
_proc
.
kill
(
)
      
self
.
_proc
.
wait
(
)
  
def
__del__
(
self
)
:
    
if
not
self
.
_closed_called
and
self
.
_proc
:
      
logging
.
error
(
'
deobfuscator
:
Forgot
to
Close
(
)
'
)
      
self
.
Close
(
)
class
DeobfuscatorPool
:
  
def
__init__
(
self
mapping_path
pool_size
=
4
)
:
    
self
.
_mapping_path
=
mapping_path
    
self
.
_pool
=
[
Deobfuscator
(
mapping_path
)
for
_
in
range
(
pool_size
)
]
    
self
.
_lock
=
threading
.
Lock
(
)
    
self
.
_num_restarts
=
0
  
def
TransformLines
(
self
lines
)
:
    
with
self
.
_lock
:
      
assert
self
.
_pool
'
TransformLines
(
)
called
on
a
closed
DeobfuscatorPool
.
'
      
if
self
.
_num_restarts
=
=
_MAX_RESTARTS
:
        
raise
Exception
(
'
Deobfuscation
seems
broken
.
'
)
      
for
i
d
in
enumerate
(
self
.
_pool
)
:
        
if
d
.
IsClosed
(
)
:
          
logging
.
warning
(
'
deobfuscator
:
Restarting
closed
instance
.
'
)
          
self
.
_pool
[
i
]
=
Deobfuscator
(
self
.
_mapping_path
)
          
self
.
_num_restarts
+
=
1
          
if
self
.
_num_restarts
=
=
_MAX_RESTARTS
:
            
logging
.
warning
(
'
deobfuscator
:
MAX_RESTARTS
reached
.
'
)
      
selected
=
next
(
(
x
for
x
in
self
.
_pool
if
x
.
IsReady
(
)
)
self
.
_pool
[
0
]
)
      
self
.
_pool
.
remove
(
selected
)
      
self
.
_pool
.
append
(
selected
)
    
return
selected
.
TransformLines
(
lines
)
  
def
Close
(
self
)
:
    
with
self
.
_lock
:
      
for
d
in
self
.
_pool
:
        
d
.
Close
(
)
      
self
.
_pool
=
None
