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
session_store_test_case
import
SessionStoreTestCase
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
SessionOutcomeTestCase
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
what
came
of
the
restore
    
decision
taken
during
that
startup
.
"
"
"
    
def
_quit_and_restore
(
self
app_args
=
None
)
:
        
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
            
if
app_args
:
                
self
.
marionette
.
instance
.
app_args
=
app_args
            
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
    
def
_read_outcome
(
self
)
:
        
self
.
wait_for_fog
(
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
startupSessionOutcome
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
An
outcome
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
The
outcome
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
[
"
outcome
"
]
class
TestSessionRestored
(
SessionOutcomeTestCase
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
test_restoring_a_session_reports_restored
(
self
)
:
        
self
.
_quit_and_restore
(
)
        
self
.
assertEqual
(
self
.
_read_outcome
(
)
"
restored
"
)
class
TestNoWindows
(
SessionOutcomeTestCase
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
test_a_session_with_only_closed_windows_reports_no_windows
(
self
)
:
        
closed_window_count
=
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
[
resolve
]
=
arguments
;
            
const
{
SessionStore
}
=
ChromeUtils
.
importESModule
(
                
"
moz
-
src
:
/
/
/
browser
/
components
/
sessionstore
/
SessionStore
.
sys
.
mjs
"
            
)
;
            
let
state
=
JSON
.
parse
(
SessionStore
.
getBrowserState
(
)
)
;
            
state
.
_closedWindows
=
state
.
windows
;
            
state
.
windows
=
[
]
;
            
IOUtils
.
writeJSON
(
                
PathUtils
.
join
(
PathUtils
.
profileDir
"
session
-
outcome
-
fixture
.
jsonlz4
"
)
                
state
                
{
compress
:
true
}
            
)
.
then
(
(
)
=
>
resolve
(
state
.
_closedWindows
.
length
)
)
;
            
"
"
"
        
)
        
self
.
marionette
.
quit
(
)
        
profile_dir
=
self
.
marionette
.
instance
.
profile
.
profile
        
os
.
replace
(
            
os
.
path
.
join
(
profile_dir
"
session
-
outcome
-
fixture
.
jsonlz4
"
)
            
os
.
path
.
join
(
profile_dir
"
sessionstore
.
jsonlz4
"
)
        
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
        
self
.
assertEqual
(
self
.
_read_outcome
(
)
"
no_windows
"
)
        
self
.
assertEqual
(
            
len
(
self
.
get_closed_windows
(
)
)
            
closed_window_count
            
"
The
closed
windows
in
the
saved
state
should
have
been
restored
.
"
        
)
class
TestNothing
(
SessionOutcomeTestCase
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
test_a_deferred_session_carrying_nothing_reports_nothing
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
persist_closed_tabs_between_sessions
"
:
False
        
}
)
        
self
.
_quit_and_restore
(
)
        
self
.
assertEqual
(
self
.
_read_outcome
(
)
"
nothing
"
)
class
TestDeferredToWindow
(
SessionOutcomeTestCase
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
test_a_private_first_window_holds_the_session_back
(
self
)
:
        
self
.
_quit_and_restore
(
app_args
=
[
"
-
private
-
window
"
]
)
        
self
.
assertEqual
(
self
.
_read_outcome
(
)
"
deferred_to_window
"
)
