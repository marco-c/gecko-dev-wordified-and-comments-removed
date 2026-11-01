"
"
"
Provisioning
of
the
"
server
"
Firefox
used
by
the
DevTools
backward
compatibility
tests
.
Each
recipe
here
produces
a
running
Firefox
with
an
open
DevTools
server
socket
reachable
from
the
client
as
a
plain
about
:
debugging
network
location
.
The
client
side
of
the
tests
never
needs
to
know
which
recipe
was
used
.
"
"
"
from
__future__
import
annotations
import
os
import
signal
import
socket
import
subprocess
import
sys
import
time
from
dataclasses
import
dataclass
field
from
marionette_driver
.
marionette
import
Marionette
SERVER_PREFS
=
{
    
"
devtools
.
debugger
.
remote
-
enabled
"
:
True
    
"
devtools
.
debugger
.
prompt
-
connection
"
:
False
    
"
devtools
.
chrome
.
enabled
"
:
True
}
DESCRIBE_SCRIPT
=
"
"
"
  
const
{
AppConstants
}
=
ChromeUtils
.
importESModule
(
    
"
resource
:
/
/
gre
/
modules
/
AppConstants
.
sys
.
mjs
"
  
)
;
  
const
bundle
=
Services
.
strings
.
createBundle
(
    
"
chrome
:
/
/
branding
/
locale
/
brand
.
properties
"
  
)
;
  
return
{
    
brandName
:
bundle
.
GetStringFromName
(
"
brandFullName
"
)
    
version
:
Services
.
appinfo
.
version
    
channel
:
AppConstants
.
MOZ_UPDATE_CHANNEL
  
}
;
"
"
"
def
find_free_port
(
)
-
>
int
:
    
with
socket
.
socket
(
socket
.
AF_INET
socket
.
SOCK_STREAM
)
as
sock
:
        
sock
.
bind
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
)
        
return
sock
.
getsockname
(
)
[
1
]
def
wait_for_port
(
port
:
int
timeout
:
float
=
60
)
-
>
None
:
    
deadline
=
time
.
monotonic
(
)
+
timeout
    
while
time
.
monotonic
(
)
<
deadline
:
        
try
:
            
with
socket
.
create_connection
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
port
)
timeout
=
1
)
:
                
return
        
except
OSError
:
            
time
.
sleep
(
0
.
25
)
    
raise
RuntimeError
(
f
"
DevTools
server
did
not
start
listening
on
port
{
port
}
"
)
class
DesktopServer
:
    
"
"
"
A
second
desktop
Firefox
acting
as
the
DevTools
server
.
    
Runs
with
a
dedicated
temporary
profile
and
is
driven
over
Marionette
so
    
the
harness
can
perform
server
-
side
page
actions
(
open
a
tab
click
in
the
    
page
install
an
extension
)
that
the
client
cannot
perform
itself
.
    
:
param
binary
:
path
to
the
Firefox
binary
to
run
as
the
server
.
    
:
param
gecko_log
:
path
of
the
log
file
for
the
server
instance
.
    
:
param
headless
:
whether
to
run
the
server
without
a
visible
window
.
    
"
"
"
    
def
__init__
(
        
self
        
binary
:
str
        
gecko_log
:
str
|
None
=
None
        
headless
:
bool
=
True
    
)
-
>
None
:
        
self
.
binary
=
binary
        
self
.
gecko_log
=
gecko_log
        
self
.
headless
=
headless
        
self
.
port
=
None
        
self
.
marionette
=
None
    
def
start
(
self
)
-
>
None
:
        
self
.
port
=
find_free_port
(
)
        
self
.
marionette
=
Marionette
(
            
bin
=
self
.
binary
            
app_args
=
[
"
-
-
start
-
debugger
-
server
"
str
(
self
.
port
)
]
            
prefs
=
SERVER_PREFS
            
gecko_log
=
self
.
gecko_log
            
headless
=
self
.
headless
        
)
        
self
.
marionette
.
start_session
(
)
        
wait_for_port
(
self
.
port
)
    
def
stop
(
self
)
-
>
None
:
        
if
self
.
marionette
:
            
self
.
marionette
.
cleanup
(
)
            
self
.
marionette
=
None
    
property
    
def
host
(
self
)
-
>
str
:
        
return
f
"
localhost
:
{
self
.
port
}
"
    
def
describe
(
self
)
-
>
dict
[
str
str
]
:
        
with
self
.
marionette
.
using_context
(
"
chrome
"
)
:
            
return
self
.
marionette
.
execute_script
(
DESCRIBE_SCRIPT
)
    
def
__enter__
(
self
)
-
>
DesktopServer
:
        
self
.
start
(
)
        
return
self
    
def
__exit__
(
self
*
args
)
-
>
None
:
        
self
.
stop
(
)
XPCSHELL_MANIFEST
=
os
.
path
.
join
(
    
os
.
path
.
dirname
(
os
.
path
.
realpath
(
__file__
)
)
"
fixtures
"
"
xpcshell
"
"
xpcshell
.
toml
"
)
XPCSHELL_EXIT_TIMEOUT
=
10
dataclass
class
XpcshellHarness
:
    
"
"
"
Location
of
the
xpcshell
test
harness
.
    
:
param
script
:
path
to
runxpcshelltests
.
py
.
    
:
param
binary
:
path
to
the
xpcshell
binary
.
    
:
param
extra_args
:
additional
arguments
for
runxpcshelltests
.
py
for
paths
        
it
cannot
guess
by
itself
.
    
"
"
"
    
script
:
str
    
binary
:
str
    
extra_args
:
list
[
str
]
=
field
(
default_factory
=
list
)
class
XpcshellServer
:
    
"
"
"
An
xpcshell
test
run
with
-
-
jsdebugger
acting
as
the
DevTools
server
.
    
The
xpcshell
harness
opens
a
DevTools
server
socket
and
waits
for
a
client
    
to
connect
.
The
test
then
pauses
on
its
first
line
so
the
process
only
    
exits
once
the
client
resumes
it
.
    
start
(
)
does
not
wait
for
the
socket
to
be
open
:
connecting
to
check
it
    
would
be
seen
as
a
debugger
connecting
then
leaving
and
the
test
would
run
    
without
pausing
.
The
client
retries
until
the
connection
succeeds
instead
.
    
:
param
harness
:
the
xpcshell
harness
to
use
.
    
:
param
log_path
:
path
of
the
file
receiving
the
harness
output
.
    
"
"
"
    
def
__init__
(
self
harness
:
XpcshellHarness
log_path
:
str
)
-
>
None
:
        
self
.
harness
=
harness
        
self
.
log_path
=
log_path
        
self
.
port
=
None
        
self
.
_process
=
None
        
self
.
_log_file
=
None
    
def
start
(
self
)
-
>
None
:
        
self
.
stop
(
)
        
self
.
port
=
find_free_port
(
)
        
self
.
_log_file
=
open
(
self
.
log_path
"
w
"
)
        
self
.
_process
=
subprocess
.
Popen
(
            
[
                
sys
.
executable
                
self
.
harness
.
script
                
"
-
-
xpcshell
"
                
self
.
harness
.
binary
                
"
-
-
manifest
"
                
XPCSHELL_MANIFEST
                
"
-
-
jsdebugger
"
                
"
-
-
jsdebugger
-
port
"
                
str
(
self
.
port
)
                
"
-
-
no
-
logfiles
"
                
"
-
-
log
-
mach
"
                
"
-
"
            
]
            
+
self
.
harness
.
extra_args
            
stdout
=
self
.
_log_file
            
stderr
=
subprocess
.
STDOUT
            
start_new_session
=
True
        
)
    
def
wait
(
self
)
-
>
int
:
        
try
:
            
return
self
.
_process
.
wait
(
timeout
=
XPCSHELL_EXIT_TIMEOUT
)
        
finally
:
            
self
.
stop
(
)
    
def
stop
(
self
)
-
>
None
:
        
if
self
.
_process
:
            
if
self
.
_process
.
poll
(
)
is
None
:
                
if
os
.
name
=
=
"
posix
"
:
                    
os
.
killpg
(
self
.
_process
.
pid
signal
.
SIGKILL
)
                
else
:
                    
self
.
_process
.
kill
(
)
                
self
.
_process
.
wait
(
)
            
self
.
_process
=
None
        
if
self
.
_log_file
:
            
self
.
_log_file
.
close
(
)
            
self
.
_log_file
=
None
    
property
    
def
host
(
self
)
-
>
str
:
        
return
f
"
localhost
:
{
self
.
port
}
"
