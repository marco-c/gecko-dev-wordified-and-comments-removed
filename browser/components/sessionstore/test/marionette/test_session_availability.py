import
os
import
sys
sys
.
path
.
append
(
os
.
path
.
dirname
(
__file__
)
)
from
marionette_driver
import
Wait
from
session_store_test_case
import
SessionStoreTestCase
def
wait_for_fog
(
marionette
)
:
    
Wait
(
marionette
timeout
=
60
)
.
until
(
        
lambda
_
:
marionette
.
execute_script
(
            
"
"
"
            
return
Services
.
fog
.
initialized
;
            
"
"
"
        
)
        
message
=
"
FOG
should
be
initialized
before
reading
Glean
metrics
.
"
    
)
def
inline
(
title
)
:
    
return
f
"
data
:
text
/
html
;
charset
=
utf
-
8
<
html
>
<
head
>
<
title
>
{
title
}
<
/
title
>
<
/
head
>
<
body
>
<
/
body
>
<
/
html
>
"
def
as_bool
(
value
)
:
    
return
value
if
isinstance
(
value
bool
)
else
value
=
=
"
true
"
TEST_WINDOWS
=
set
(
[
    
(
        
inline
(
"
Page
1
"
)
        
inline
(
"
Page
2
"
)
    
)
]
)
class
SessionAvailabilityTestCase
(
SessionStoreTestCase
)
:
    
"
"
"
Restart
the
browser
for
real
then
read
back
the
telemetry
that
startup
    
recorded
about
what
it
found
to
restore
from
.
"
"
"
    
def
_quit_and_restore
(
self
)
:
        
self
.
marionette
.
quit
(
)
        
self
.
marionette
.
start_session
(
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
    
def
_read_availability_telemetry
(
self
)
:
        
"
"
"
Read
the
session_restore
.
startup_session_availability
event
that
the
        
startup
we
just
completed
recorded
and
return
its
extra
keys
.
"
"
"
        
wait_for_fog
(
self
.
marionette
)
        
events
=
self
.
marionette
.
execute_script
(
            
"
"
"
            
return
Glean
.
sessionRestore
.
startupSessionAvailability
.
testGetValue
(
)
;
            
"
"
"
        
)
        
self
.
assertIsNotNone
(
            
events
"
Session
availability
should
be
recorded
on
startup
.
"
        
)
        
self
.
assertEqual
(
            
len
(
events
)
1
"
Session
availability
should
be
recorded
once
per
startup
.
"
        
)
        
return
events
[
0
]
[
"
extra
"
]
class
TestSessionAvailableAndWanted
(
SessionAvailabilityTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
            
startup_page
=
3
            
include_private
=
False
            
restore_on_demand
=
False
            
test_windows
=
TEST_WINDOWS
        
)
    
def
test_previous_session_is_available
(
self
)
:
        
self
.
_quit_and_restore
(
)
        
telemetry
=
self
.
_read_availability_telemetry
(
)
        
self
.
assertEqual
(
            
telemetry
[
"
origin
"
]
            
"
clean
"
            
"
A
clean
shutdown
leaves
a
session
in
the
clean
file
.
"
        
)
        
self
.
assertEqual
(
telemetry
[
"
format
"
]
"
jsonlz4
"
)
        
self
.
assertEqual
(
telemetry
[
"
clean
"
]
"
present
"
"
The
clean
file
was
found
.
"
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
startup_page_is_resume
"
]
)
            
"
The
user
asked
for
the
previous
session
to
be
restored
.
"
        
)
class
TestOneOffResume
(
SessionAvailabilityTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
            
startup_page
=
1
            
include_private
=
False
            
restore_on_demand
=
False
            
test_windows
=
TEST_WINDOWS
        
)
    
def
test_one_off_resume_is_recorded_before_it_is_cleared
(
self
)
:
        
self
.
marionette
.
set_prefs
(
{
            
"
browser
.
sessionstore
.
resume_session_once
"
:
True
        
}
)
        
self
.
_quit_and_restore
(
)
        
telemetry
=
self
.
_read_availability_telemetry
(
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
resume_session_once
"
]
)
            
"
A
pending
one
-
off
resume
is
recorded
before
SessionStore
clears
it
.
"
        
)
        
self
.
assertFalse
(
            
as_bool
(
telemetry
[
"
startup_page_is_resume
"
]
)
            
"
The
standing
preference
is
reported
separately
from
the
one
-
off
.
"
        
)
class
TestResumeArmedForOsRestart
(
SessionAvailabilityTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
            
startup_page
=
1
            
include_private
=
False
            
restore_on_demand
=
False
            
test_windows
=
TEST_WINDOWS
        
)
    
def
test_one_off_resume_armed_for_an_os_restart_is_recorded
(
self
)
:
        
self
.
marionette
.
set_prefs
(
{
            
"
browser
.
sessionstore
.
resume_session_once
"
:
True
            
"
browser
.
sessionstore
.
resuming_after_os_restart
"
:
True
        
}
)
        
self
.
_quit_and_restore
(
)
        
telemetry
=
self
.
_read_availability_telemetry
(
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
resuming_after_os_restart
"
]
)
            
"
A
resume
armed
for
an
OS
restart
is
reported
.
"
        
)
        
self
.
assertFalse
(
            
as_bool
(
telemetry
[
"
restarted_by_os
"
]
)
            
"
The
OS
did
not
in
fact
restart
us
which
is
what
clears
the
pref
.
"
        
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
resume_session_once
"
]
)
            
"
The
pending
one
-
off
resume
is
recorded
as
it
was
found
at
startup
.
"
        
)
    
def
test_one_off_resume_is_recorded_when_the_os_did_restart_us
(
self
)
:
        
self
.
marionette
.
set_prefs
(
{
            
"
browser
.
sessionstore
.
resume_session_once
"
:
True
            
"
browser
.
sessionstore
.
resuming_after_os_restart
"
:
True
        
}
)
        
self
.
marionette
.
quit
(
)
        
saved_args
=
self
.
marionette
.
instance
.
app_args
        
try
:
            
self
.
marionette
.
instance
.
app_args
=
[
"
-
os
-
restarted
"
]
            
self
.
marionette
.
start_session
(
)
            
self
.
marionette
.
set_context
(
"
chrome
"
)
        
finally
:
            
self
.
marionette
.
instance
.
app_args
=
saved_args
        
telemetry
=
self
.
_read_availability_telemetry
(
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
restarted_by_os
"
]
)
            
"
The
OS
started
the
browser
so
the
armed
resume
stands
.
"
        
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
resuming_after_os_restart
"
]
)
            
"
A
resume
armed
for
an
OS
restart
is
reported
.
"
        
)
        
self
.
assertTrue
(
            
as_bool
(
telemetry
[
"
resume_session_once
"
]
)
            
"
The
pending
one
-
off
resume
is
recorded
as
it
was
found
at
startup
.
"
        
)
