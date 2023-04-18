import
os
import
time
import
pytest
from
mozprofile
import
Profile
from
mozrunner
import
FirefoxRunner
class
Browser
:
    
def
__init__
(
self
firefox_options
extra_prefs
)
:
        
self
.
extra_prefs
=
extra_prefs
        
self
.
remote_agent_port
=
None
        
profile_arg
profile_folder
=
firefox_options
[
"
args
"
]
        
self
.
profile
=
Profile
.
clone
(
profile_folder
)
        
if
self
.
extra_prefs
:
            
self
.
profile
.
set_preferences
(
self
.
extra_prefs
)
        
binary
=
firefox_options
[
"
binary
"
]
        
cmdargs
=
[
"
-
-
remote
-
debugging
-
port
"
"
-
no
-
remote
"
]
        
self
.
runner
=
FirefoxRunner
(
            
binary
=
binary
profile
=
self
.
profile
cmdargs
=
cmdargs
        
)
    
def
start
(
self
)
:
        
self
.
runner
.
start
(
)
        
port_file
=
os
.
path
.
join
(
self
.
profile
.
profile
"
WebDriverBiDiActivePort
"
)
        
while
not
os
.
path
.
exists
(
port_file
)
:
            
time
.
sleep
(
0
.
1
)
        
self
.
remote_agent_port
=
open
(
port_file
)
.
read
(
)
    
def
quit
(
self
)
:
        
if
self
.
runner
:
            
self
.
runner
.
stop
(
)
            
self
.
runner
.
cleanup
(
)
            
self
.
profile
.
cleanup
(
)
pytest
.
fixture
(
scope
=
"
module
"
)
def
browser
(
full_configuration
)
:
    
"
"
"
Start
a
Firefox
instance
without
using
geckodriver
.
    
geckodriver
will
automatically
set
the
remote
.
origins
.
allowed
and
    
remote
.
hosts
.
allowed
preferences
we
want
to
test
in
websocket_upgrade
.
py
    
Starting
Firefox
without
geckodriver
allows
to
set
those
preferences
as
    
needed
.
The
fixture
method
returns
the
port
that
should
be
used
to
connect
    
to
WebDriverBiDi
.
    
"
"
"
    
current_browser
=
None
    
def
_browser
(
extra_prefs
=
{
}
)
:
        
nonlocal
current_browser
        
if
current_browser
and
current_browser
.
extra_prefs
=
=
extra_prefs
:
            
return
current_browser
        
if
current_browser
:
            
current_browser
.
quit
(
)
        
firefox_options
=
full_configuration
[
"
capabilities
"
]
[
"
moz
:
firefoxOptions
"
]
        
current_browser
=
Browser
(
firefox_options
extra_prefs
)
        
current_browser
.
start
(
)
        
return
current_browser
    
yield
_browser
    
current_browser
.
quit
(
)
    
current_browser
=
None
