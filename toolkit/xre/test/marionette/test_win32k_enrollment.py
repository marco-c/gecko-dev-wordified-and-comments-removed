from
__future__
import
absolute_import
print_function
from
marionette_harness
import
MarionetteTestCase
from
contextlib
import
contextmanager
class
ExperimentStatus
:
    
UNENROLLED
=
0
    
ENROLLED_CONTROL
=
1
    
ENROLLED_TREATMENT
=
2
    
DISQUALIFIED
=
3
class
ContentWin32kLockdownState
:
    
LockdownEnabled
=
1
    
MissingWebRender
=
2
    
OperatingSystemNotSupported
=
3
    
PrefNotSet
=
4
    
MissingRemoteWebGL
=
5
    
MissingNonNativeTheming
=
6
    
DisabledByEnvVar
=
7
    
DisabledBySafeMode
=
8
    
DisabledByE10S
=
9
    
DisabledByUserPref
=
10
    
EnabledByUserPref
=
11
    
DisabledByControlGroup
=
12
    
EnabledByTreatmentGroup
=
13
    
DisabledByDefault
=
14
    
EnabledByDefault
=
15
class
Prefs
:
    
ENROLLMENT_STATUS
=
"
security
.
sandbox
.
content
.
win32k
-
experiment
.
enrollmentStatus
"
    
STARTUP_ENROLLMENT_STATUS
=
(
        
"
security
.
sandbox
.
content
.
win32k
-
experiment
.
startupEnrollmentStatus
"
    
)
    
WIN32K
=
"
security
.
sandbox
.
content
.
win32k
-
disable
"
    
WEBGL
=
"
webgl
.
out
-
of
-
process
"
ENV_DISABLE_WIN32K
=
"
MOZ_ENABLE_WIN32K
"
ENV_DISABLE_E10S
=
"
MOZ_FORCE_DISABLE_E10S
"
class
TestWin32kAutostart
(
MarionetteTestCase
)
:
    
SANDBOX_NAME
=
"
win32k
-
autostart
"
    
def
execute_script
(
self
code
*
args
*
*
kwargs
)
:
        
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
)
:
            
return
self
.
marionette
.
execute_script
(
                
code
new_sandbox
=
False
sandbox
=
self
.
SANDBOX_NAME
*
args
*
*
kwargs
            
)
    
def
get_win32k_status
(
self
)
:
        
return
self
.
execute_script
(
            
r
"
"
"
          
let
win
=
Services
.
wm
.
getMostRecentWindow
(
"
navigator
:
browser
"
)
;
          
let
ses
=
"
security
.
sandbox
.
content
.
win32k
-
experiment
.
startupEnrollmentStatus
"
;
          
return
{
            
win32kSessionStatus
:
Services
.
appinfo
.
win32kSessionStatus
            
win32kStatus
:
Services
.
appinfo
.
win32kLiveStatusTestingOnly
            
win32kExperimentStatus
:
Services
.
appinfo
.
win32kExperimentStatus
            
win32kPref
:
Services
.
prefs
.
getBoolPref
(
"
security
.
sandbox
.
content
.
win32k
-
disable
"
)
            
win32kStartupEnrollmentStatusPref
:
Services
.
prefs
.
getIntPref
(
ses
)
          
}
;
        
"
"
"
        
)
    
def
check_win32k_status
(
        
self
status
sessionStatus
experimentStatus
pref
enrollmentStatusPref
    
)
:
        
expected
=
{
            
"
win32kSessionStatus
"
:
sessionStatus
            
"
win32kStatus
"
:
status
            
"
win32kExperimentStatus
"
:
experimentStatus
            
"
win32kPref
"
:
pref
            
"
win32kStartupEnrollmentStatusPref
"
:
enrollmentStatusPref
        
}
        
status
=
self
.
get_win32k_status
(
)
        
for
prop
value
in
expected
.
items
(
)
:
            
self
.
assertEqual
(
                
status
[
prop
]
                
value
                
"
%
s
should
have
the
value
%
r
but
has
%
r
"
                
%
(
prop
value
status
[
prop
]
)
            
)
    
def
set_env
(
self
env
value
)
:
        
self
.
execute_script
(
            
"
env
.
set
(
arguments
[
0
]
arguments
[
1
]
)
;
"
script_args
=
(
env
value
)
        
)
    
def
get_env
(
self
env
)
:
        
return
self
.
execute_script
(
"
return
env
.
get
(
arguments
[
0
]
)
;
"
script_args
=
(
env
)
)
    
def
set_enrollment_status
(
self
status
)
:
        
self
.
marionette
.
set_pref
(
Prefs
.
ENROLLMENT_STATUS
status
default_branch
=
True
)
        
updated_status
=
self
.
marionette
.
get_pref
(
Prefs
.
ENROLLMENT_STATUS
)
        
self
.
assertTrue
(
            
status
=
=
updated_status
or
updated_status
=
=
ExperimentStatus
.
DISQUALIFIED
        
)
        
startup_status
=
self
.
marionette
.
get_pref
(
Prefs
.
STARTUP_ENROLLMENT_STATUS
)
        
self
.
assertEqual
(
            
startup_status
            
updated_status
            
"
Startup
enrollment
status
(
%
r
)
should
match
"
            
"
session
status
(
%
r
)
"
%
(
startup_status
updated_status
)
        
)
    
def
restart
(
self
prefs
=
None
env
=
None
)
:
        
if
prefs
:
            
self
.
marionette
.
set_prefs
(
prefs
)
        
if
env
:
            
for
name
value
in
env
.
items
(
)
:
                
self
.
set_env
(
name
value
)
        
self
.
marionette
.
restart
(
in_app
=
True
clean
=
False
)
        
self
.
setUpSession
(
)
        
if
prefs
:
            
for
key
val
in
prefs
.
items
(
)
:
                
if
val
is
not
None
:
                    
self
.
assertEqual
(
self
.
marionette
.
get_pref
(
key
)
val
)
        
if
env
:
            
for
key
val
in
env
.
items
(
)
:
                
self
.
assertEqual
(
self
.
get_env
(
key
)
val
or
"
"
)
    
def
setUpSession
(
self
)
:
        
self
.
marionette
.
set_context
(
self
.
marionette
.
CONTEXT_CHROME
)
        
self
.
execute_script
(
            
r
"
"
"
          
/
/
We
'
re
running
in
a
function
in
a
sandbox
that
inherits
from
an
          
/
/
X
-
ray
wrapped
window
.
Anything
we
want
to
be
globally
available
          
/
/
needs
to
be
defined
on
that
window
.
          
window
.
env
=
Cc
[
"
mozilla
.
org
/
process
/
environment
;
1
"
]
                    
.
getService
(
Ci
.
nsIEnvironment
)
;
        
"
"
"
        
)
    
contextmanager
    
def
full_restart
(
self
)
:
        
profile
=
self
.
marionette
.
instance
.
profile
        
try
:
            
self
.
marionette
.
quit
(
in_app
=
True
clean
=
False
)
            
yield
profile
        
finally
:
            
self
.
marionette
.
start_session
(
)
            
self
.
setUpSession
(
)
    
def
setUp
(
self
)
:
        
super
(
TestWin32kAutostart
self
)
.
setUp
(
)
        
self
.
win32kRequired
=
None
        
if
Prefs
.
WIN32K
in
self
.
marionette
.
instance
.
required_prefs
:
            
self
.
win32kRequired
=
self
.
marionette
.
instance
.
required_prefs
[
Prefs
.
WIN32K
]
            
del
self
.
marionette
.
instance
.
required_prefs
[
Prefs
.
WIN32K
]
            
self
.
marionette
.
restart
(
clean
=
True
)
        
self
.
setUpSession
(
)
        
prefJS
=
'
return
Services
.
prefs
.
getBoolPref
(
"
security
.
sandbox
.
content
.
win32k
-
disable
"
)
;
'
        
self
.
default_is
=
self
.
execute_script
(
prefJS
)
        
if
self
.
default_is
is
False
:
            
self
.
check_win32k_status
(
                
status
=
ContentWin32kLockdownState
.
DisabledByDefault
                
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
                
experimentStatus
=
ExperimentStatus
.
UNENROLLED
                
pref
=
False
                
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
            
)
        
else
:
            
self
.
check_win32k_status
(
                
status
=
ContentWin32kLockdownState
.
EnabledByDefault
                
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
                
experimentStatus
=
ExperimentStatus
.
UNENROLLED
                
pref
=
True
                
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
            
)
    
def
tearDown
(
self
)
:
        
if
self
.
win32kRequired
is
not
None
:
            
self
.
marionette
.
instance
.
required_prefs
[
Prefs
.
WIN32K
]
=
self
.
win32kRequired
        
self
.
marionette
.
restart
(
clean
=
True
)
        
super
(
TestWin32kAutostart
self
)
.
tearDown
(
)
    
def
test_1
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_2
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_3
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_4
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_5
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_6
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_7
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_8
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_9
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_10
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_11
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_12
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_13
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_14
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_15
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_16
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_17
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_18
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_19
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_20
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_21
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_22
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_23
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_24
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_25
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_26
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_27
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_28
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_29
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_30
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_31
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_32
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_33
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_34
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_35
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_36
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByControlGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_CONTROL
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
    
def
test_37
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_38
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_39
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_40
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_41
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_42
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_43
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByUserPref
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_44
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_45
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
app_version
=
self
.
execute_script
(
"
return
Services
.
appinfo
.
version
"
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_E10S
:
app_version
}
)
        
self
.
set_env
(
ENV_DISABLE_E10S
"
null
"
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByE10S
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByE10S
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_46
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByDefault
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
env
=
{
ENV_DISABLE_WIN32K
:
"
1
"
}
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByEnvVar
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
set_env
(
ENV_DISABLE_WIN32K
"
"
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByTreatmentGroup
            
experimentStatus
=
ExperimentStatus
.
ENROLLED_TREATMENT
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
    
def
test_47
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_48
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_49
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_50
(
self
)
:
        
if
self
.
default_is
is
not
False
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
DisabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_51
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_CONTROL
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_CONTROL
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_52
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
set_enrollment_status
(
ExperimentStatus
.
ENROLLED_TREATMENT
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
ENROLLED_TREATMENT
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
DISQUALIFIED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
DISQUALIFIED
        
)
    
def
test_53
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
True
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
    
def
test_54
(
self
)
:
        
if
self
.
default_is
is
not
True
:
            
return
        
self
.
marionette
.
set_pref
(
Prefs
.
WEBGL
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
EnabledByDefault
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
restart
(
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
True
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
        
self
.
marionette
.
set_pref
(
Prefs
.
WIN32K
False
)
        
self
.
check_win32k_status
(
            
status
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
sessionStatus
=
ContentWin32kLockdownState
.
MissingRemoteWebGL
            
experimentStatus
=
ExperimentStatus
.
UNENROLLED
            
pref
=
False
            
enrollmentStatusPref
=
ExperimentStatus
.
UNENROLLED
        
)
