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
RestoreCountsTestCase
(
SessionStoreTestCase
)
:
    
"
"
"
The
number_of_
*
counts
are
recorded
on
every
restore
attempt
including
    
attempts
that
end
up
restoring
nothing
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
_read_counts
(
self
)
:
        
wait_for_fog
(
self
.
marionette
)
        
Wait
(
self
.
marionette
timeout
=
40
)
.
until
(
            
lambda
_
:
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
numberOfTabsRestored
.
testGetValue
(
)
                  
!
=
null
;
                
"
"
"
            
)
            
message
=
"
The
restore
counts
should
be
recorded
.
"
        
)
        
return
self
.
marionette
.
execute_script
(
            
"
"
"
            
let
counts
=
{
}
;
            
for
(
let
name
of
[
              
"
numberOfTabsRestored
"
              
"
numberOfWindowsRestored
"
              
"
numberOfEagerTabsRestored
"
            
]
)
{
              
counts
[
name
]
=
Glean
.
sessionRestore
[
name
]
.
testGetValue
(
)
;
            
}
            
return
counts
;
            
"
"
"
        
)
class
TestCountsAfterRestore
(
RestoreCountsTestCase
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
test_counts_are_recorded_when_tabs_are_restored
(
self
)
:
        
self
.
_quit_and_restore
(
)
        
counts
=
self
.
_read_counts
(
)
        
for
name
value
in
counts
.
items
(
)
:
            
self
.
assertIsNotNone
(
value
f
"
{
name
}
should
be
recorded
.
"
)
        
self
.
assertGreater
(
            
counts
[
"
numberOfTabsRestored
"
]
[
"
sum
"
]
            
0
            
"
Tabs
were
restored
so
the
count
is
not
zero
.
"
        
)
class
TestCountsWhenNothingRestored
(
RestoreCountsTestCase
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
test_counts_are_recorded_when_no_window_is_restored
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
        
counts
=
self
.
_read_counts
(
)
        
for
name
value
in
counts
.
items
(
)
:
            
self
.
assertIsNotNone
(
                
value
f
"
{
name
}
should
be
recorded
even
with
nothing
restored
.
"
            
)
            
self
.
assertEqual
(
                
value
[
"
sum
"
]
0
f
"
{
name
}
should
report
zero
not
be
absent
.
"
            
)
