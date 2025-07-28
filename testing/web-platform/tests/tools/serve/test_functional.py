try
:
    
from
importlib
import
reload
except
ImportError
:
    
pass
import
json
import
os
import
queue
import
tempfile
import
threading
import
pytest
from
.
import
serve
from
wptserve
import
logger
class
ServerProcSpy
(
serve
.
ServerProc
)
:
    
instances
=
None
    
def
start
(
self
*
args
*
*
kwargs
)
:
        
result
=
super
(
)
.
start
(
*
args
*
*
kwargs
)
        
if
ServerProcSpy
.
instances
is
not
None
:
            
ServerProcSpy
.
instances
.
put
(
self
)
        
return
result
serve
.
ServerProc
=
ServerProcSpy
pytest
.
fixture
(
)
def
server_subprocesses
(
)
:
    
ServerProcSpy
.
instances
=
queue
.
Queue
(
)
    
yield
ServerProcSpy
.
instances
    
ServerProcSpy
.
instances
=
None
pytest
.
fixture
(
)
def
tempfile_name
(
)
:
    
fd
name
=
tempfile
.
mkstemp
(
)
    
yield
name
    
os
.
close
(
fd
)
    
os
.
remove
(
name
)
def
test_subprocess_exit
(
server_subprocesses
tempfile_name
)
:
    
timeout
=
30
    
def
target
(
)
:
        
config
=
{
            
"
browser_host
"
:
"
localhost
"
            
"
alternate_hosts
"
:
{
"
alt
"
:
"
127
.
0
.
0
.
1
"
}
            
"
check_subdomains
"
:
False
        
}
        
with
open
(
tempfile_name
"
w
"
)
as
handle
:
            
json
.
dump
(
config
handle
)
        
reload
(
logger
)
        
serve
.
run
(
config_path
=
tempfile_name
)
    
thread
=
threading
.
Thread
(
target
=
target
)
    
thread
.
start
(
)
    
server_subprocesses
.
get
(
True
timeout
)
    
subprocess
=
server_subprocesses
.
get
(
True
timeout
)
    
subprocess
.
request_shutdown
(
)
    
subprocess
.
wait
(
)
    
thread
.
join
(
timeout
)
    
assert
not
thread
.
is_alive
(
)
