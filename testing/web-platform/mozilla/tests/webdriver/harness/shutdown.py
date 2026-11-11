import
os
import
signal
import
subprocess
import
pytest
from
tests
.
support
.
sync
import
Poll
IS_WINDOWS
=
os
.
name
=
=
"
nt
"
if
IS_WINDOWS
:
    
SIGNALS
=
[
signal
.
CTRL_BREAK_EVENT
]
else
:
    
SIGNALS
=
[
signal
.
SIGINT
signal
.
SIGTERM
]
pytest
.
mark
.
parametrize
(
"
signal
"
SIGNALS
)
def
test_firefox_quits_on_signal
(
configuration
geckodriver
is_process_alive
signal
)
:
    
popen_kwargs
=
{
}
    
if
IS_WINDOWS
:
        
popen_kwargs
[
"
creationflags
"
]
=
subprocess
.
CREATE_NEW_PROCESS_GROUP
    
driver
=
geckodriver
(
        
config
=
configuration
        
popen_kwargs
=
popen_kwargs
    
)
    
driver
.
new_session
(
)
    
firefox_pid
=
driver
.
session
.
capabilities
[
"
moz
:
processID
"
]
    
driver
.
proc
.
send_signal
(
signal
)
    
wait
=
Poll
(
        
driver
.
session
        
timeout
=
75
        
message
=
"
Firefox
process
still
running
after
geckodriver
was
terminated
"
    
)
    
wait
.
until
(
lambda
session
:
not
is_process_alive
(
firefox_pid
)
)
