"
"
"
Sets
up
the
isolate
daemon
environment
to
run
test
on
the
bots
.
"
"
"
import
os
import
tempfile
from
typing
import
Optional
from
contextlib
import
AbstractContextManager
from
common
import
get_ffx_isolate_dir
has_ffx_isolate_dir
\
                        
set_ffx_isolate_dir
is_daemon_running
\
                        
start_ffx_daemon
stop_ffx_daemon
from
ffx_integration
import
ScopedFfxConfig
from
modification_waiter
import
ModificationWaiter
class
IsolateDaemon
(
AbstractContextManager
)
:
    
"
"
"
Sets
up
the
environment
of
an
isolate
ffx
daemon
.
"
"
"
    
class
IsolateDir
(
AbstractContextManager
)
:
        
"
"
"
Sets
up
the
ffx
isolate
dir
to
a
temporary
folder
if
it
'
s
not
set
.
"
"
"
        
def
__init__
(
self
)
:
            
if
has_ffx_isolate_dir
(
)
:
                
self
.
_temp_dir
=
None
            
else
:
                
self
.
_temp_dir
=
tempfile
.
TemporaryDirectory
(
)
        
def
__enter__
(
self
)
:
            
if
self
.
_temp_dir
:
                
set_ffx_isolate_dir
(
self
.
_temp_dir
.
__enter__
(
)
)
            
return
self
        
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
            
if
self
.
_temp_dir
:
                
try
:
                    
self
.
_temp_dir
.
__exit__
(
exc_type
exc_value
traceback
)
                
except
OSError
:
                    
pass
            
return
False
    
class
RepoProcessDir
(
AbstractContextManager
)
:
        
"
"
"
Sets
up
a
temporary
folder
for
the
repository
server
process
dir
.
        
The
default
location
XDG_STATE_HOME
turns
out
to
be
in
the
        
a
binding
to
a
directory
on
the
host
machine
.
The
isolate
directory
is
        
a
docker
Volume
.
The
performance
of
the
isolate
dir
is
much
better
than
        
the
performance
of
using
the
volume
based
directory
especially
on
        
arm64
hosts
.
        
"
"
"
        
def
__init__
(
self
)
:
            
self
.
_process_dir_config
=
None
        
def
__enter__
(
self
)
:
            
self
.
_process_dir_config
=
ScopedFfxConfig
(
                    
'
repository
.
process_dir
'
                    
f
'
{
get_ffx_isolate_dir
(
)
}
/
repo_proc
'
)
            
self
.
_process_dir_config
.
__enter__
(
)
            
return
self
        
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
            
return
self
.
_process_dir_config
.
__exit__
(
exc_type
exc_value
                                                     
traceback
)
    
def
__init__
(
self
logs_dir
:
Optional
[
str
]
)
:
        
assert
not
has_ffx_isolate_dir
(
)
or
not
is_daemon_running
(
)
        
self
.
_inits
=
[
            
self
.
IsolateDir
(
)
            
self
.
RepoProcessDir
(
)
            
ModificationWaiter
(
logs_dir
)
            
ScopedFfxConfig
(
'
ffx
.
isolated
'
'
true
'
)
            
ScopedFfxConfig
(
'
daemon
.
autostart
'
'
false
'
)
            
ScopedFfxConfig
(
'
fastboot
.
flash
.
timeout_rate
'
'
1
'
)
            
ScopedFfxConfig
(
'
fastboot
.
reboot
.
reconnect_timeout
'
'
120
'
)
            
ScopedFfxConfig
(
'
fastboot
.
usb
.
disabled
'
'
true
'
)
            
ScopedFfxConfig
(
'
log
.
level
'
'
debug
'
)
        
]
        
if
logs_dir
:
            
self
.
_inits
.
append
(
ScopedFfxConfig
(
'
log
.
dir
'
logs_dir
)
)
    
def
__enter__
(
self
)
:
        
os
.
environ
[
'
FUCHSIA_ANALYTICS_DISABLED
'
]
=
'
1
'
        
stop_ffx_daemon
(
)
        
for
init
in
self
.
_inits
:
            
init
.
__enter__
(
)
        
start_ffx_daemon
(
)
        
return
self
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
        
for
init
in
self
.
_inits
:
            
init
.
__exit__
(
exc_type
exc_value
traceback
)
        
stop_ffx_daemon
(
)
