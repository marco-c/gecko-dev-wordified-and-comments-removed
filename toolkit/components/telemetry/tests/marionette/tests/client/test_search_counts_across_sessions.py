import
textwrap
from
telemetry_harness
.
testcase
import
TelemetryTestCase
from
telemetry_harness
.
ping_filters
import
(
    
MAIN_ENVIRONMENT_CHANGE_PING
    
MAIN_SHUTDOWN_PING
)
class
TestSearchCounts
(
TelemetryTestCase
)
:
    
"
"
"
Test
for
SEARCH_COUNTS
across
sessions
.
"
"
"
    
def
get_current_search_engine
(
self
)
:
        
"
"
"
Retrieve
the
identifier
of
the
current
search
engine
.
"
"
"
        
script
=
"
"
"
\
        
let
searchService
=
Components
.
classes
[
                
"
mozilla
.
org
/
browser
/
search
-
service
;
1
"
]
            
.
getService
(
Components
.
interfaces
.
nsIBrowserSearchService
)
;
        
return
searchService
.
currentEngine
.
identifier
;
        
"
"
"
        
return
self
.
marionette
.
execute_script
(
textwrap
.
dedent
(
script
)
)
    
def
setUp
(
self
)
:
        
"
"
"
Set
up
the
test
case
and
store
the
identifier
of
the
current
        
search
engine
which
is
required
for
reading
SEARCH_COUNTS
from
        
keyed
histograms
in
pings
.
        
"
"
"
        
super
(
TestSearchCounts
self
)
.
setUp
(
)
        
self
.
search_engine
=
self
.
get_current_search_engine
(
)
    
def
search
(
self
text
)
:
        
"
"
"
Perform
a
search
via
the
browser
'
s
location
bar
.
"
"
"
        
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
            
self
.
browser
.
navbar
.
locationbar
.
load_url
(
text
)
    
def
search_in_new_tab
(
self
text
)
:
        
"
"
"
Open
a
new
tab
and
perform
a
search
via
the
browser
'
s
location
        
bar
then
close
the
new
tab
.
        
"
"
"
        
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
            
new_tab
=
self
.
browser
.
tabbar
.
open_tab
(
)
            
self
.
browser
.
tabbar
.
switch_to
(
new_tab
)
            
self
.
browser
.
navbar
.
locationbar
.
load_url
(
text
)
            
new_tab
.
close
(
)
    
def
restart_with_new_session
(
self
)
:
        
"
"
"
Restart
the
browser
with
the
same
profile
.
"
"
"
        
return
self
.
restart
(
clean
=
False
in_app
=
True
)
    
def
test_search_counts
(
self
)
:
        
"
"
"
Test
for
SEARCH_COUNTS
across
sessions
.
"
"
"
        
self
.
search_in_new_tab
(
"
mozilla
firefox
"
)
        
ping1
=
self
.
wait_for_ping
(
            
self
.
restart_with_new_session
MAIN_SHUTDOWN_PING
        
)
        
client_id
=
ping1
[
"
clientId
"
]
        
self
.
assertIsValidUUID
(
client_id
)
        
ping1_info
=
ping1
[
"
payload
"
]
[
"
info
"
]
        
self
.
assertEqual
(
ping1_info
[
"
reason
"
]
"
shutdown
"
)
        
s1_session_id
=
ping1_info
[
"
sessionId
"
]
        
self
.
assertNotEqual
(
s1_session_id
"
"
)
        
s1_s1_subsession_id
=
ping1_info
[
"
subsessionId
"
]
        
self
.
assertNotEqual
(
s1_s1_subsession_id
"
"
)
        
self
.
assertIsNone
(
ping1_info
[
"
previousSessionId
"
]
)
        
self
.
assertIsNone
(
ping1_info
[
"
previousSubsessionId
"
]
)
        
self
.
assertEqual
(
ping1_info
[
"
subsessionCounter
"
]
1
)
        
self
.
assertEqual
(
ping1_info
[
"
profileSubsessionCounter
"
]
1
)
        
scalars1
=
ping1
[
"
payload
"
]
[
"
processes
"
]
[
"
parent
"
]
[
"
scalars
"
]
        
self
.
assertEqual
(
            
scalars1
[
"
browser
.
engagement
.
tab_open_event_count
"
]
1
        
)
        
keyed_histograms1
=
ping1
[
"
payload
"
]
[
"
keyedHistograms
"
]
        
search_counts1
=
keyed_histograms1
[
"
SEARCH_COUNTS
"
]
[
            
"
{
}
.
urlbar
"
.
format
(
self
.
search_engine
)
        
]
        
self
.
assertEqual
(
            
search_counts1
            
{
                
u
"
range
"
:
[
1
2
]
                
u
"
bucket_count
"
:
3
                
u
"
histogram_type
"
:
4
                
u
"
values
"
:
{
u
"
1
"
:
0
u
"
0
"
:
1
}
                
u
"
sum
"
:
1
            
}
        
)
        
ping2
=
self
.
wait_for_ping
(
            
self
.
install_addon
MAIN_ENVIRONMENT_CHANGE_PING
        
)
        
self
.
assertEqual
(
ping2
[
"
clientId
"
]
client_id
)
        
ping2_info
=
ping2
[
"
payload
"
]
[
"
info
"
]
        
self
.
assertEqual
(
ping2_info
[
"
reason
"
]
"
environment
-
change
"
)
        
s2_session_id
=
ping2_info
[
"
sessionId
"
]
        
self
.
assertNotEqual
(
s2_session_id
s1_session_id
)
        
s2_s1_subsession_id
=
ping2_info
[
"
subsessionId
"
]
        
self
.
assertNotEqual
(
s2_s1_subsession_id
s1_s1_subsession_id
)
        
self
.
assertEqual
(
ping2_info
[
"
previousSessionId
"
]
s1_session_id
)
        
self
.
assertEqual
(
            
ping2_info
[
"
previousSubsessionId
"
]
s1_s1_subsession_id
        
)
        
self
.
assertEqual
(
ping2_info
[
"
subsessionCounter
"
]
1
)
        
self
.
assertEqual
(
ping2_info
[
"
profileSubsessionCounter
"
]
2
)
        
scalars2
=
ping2
[
"
payload
"
]
[
"
processes
"
]
[
"
parent
"
]
[
"
scalars
"
]
        
self
.
assertNotIn
(
"
browser
.
engagement
.
tab_open_event_count
"
scalars2
)
        
keyed_histograms2
=
ping2
[
"
payload
"
]
[
"
keyedHistograms
"
]
        
self
.
assertNotIn
(
"
SEARCH_COUNTS
"
keyed_histograms2
)
        
self
.
search
(
"
mozilla
telemetry
"
)
        
self
.
search
(
"
python
unittest
"
)
        
self
.
search
(
"
python
pytest
"
)
        
ping3
=
self
.
wait_for_ping
(
            
self
.
restart_with_new_session
MAIN_SHUTDOWN_PING
        
)
        
self
.
assertEqual
(
ping3
[
"
clientId
"
]
client_id
)
        
ping3_info
=
ping3
[
"
payload
"
]
[
"
info
"
]
        
self
.
assertEqual
(
ping3_info
[
"
reason
"
]
"
shutdown
"
)
        
self
.
assertEqual
(
ping3_info
[
"
sessionId
"
]
s2_session_id
)
        
s2_s2_subsession_id
=
ping3_info
[
"
subsessionId
"
]
        
self
.
assertNotEqual
(
s2_s2_subsession_id
s1_s1_subsession_id
)
        
self
.
assertNotEqual
(
s2_s2_subsession_id
s2_s1_subsession_id
)
        
self
.
assertEqual
(
ping3_info
[
"
previousSessionId
"
]
s1_session_id
)
        
self
.
assertEqual
(
            
ping3_info
[
"
previousSubsessionId
"
]
s2_s1_subsession_id
        
)
        
self
.
assertEqual
(
ping3_info
[
"
subsessionCounter
"
]
2
)
        
self
.
assertEqual
(
ping3_info
[
"
profileSubsessionCounter
"
]
3
)
        
scalars3
=
ping3
[
"
payload
"
]
[
"
processes
"
]
[
"
parent
"
]
[
"
scalars
"
]
        
self
.
assertNotIn
(
"
browser
.
engagement
.
tab_open_event_count
"
scalars3
)
        
keyed_histograms3
=
ping3
[
"
payload
"
]
[
"
keyedHistograms
"
]
        
search_counts3
=
keyed_histograms3
[
"
SEARCH_COUNTS
"
]
[
            
"
{
}
.
urlbar
"
.
format
(
self
.
search_engine
)
        
]
        
self
.
assertEqual
(
            
search_counts3
            
{
                
u
"
range
"
:
[
1
2
]
                
u
"
bucket_count
"
:
3
                
u
"
histogram_type
"
:
4
                
u
"
values
"
:
{
u
"
1
"
:
0
u
"
0
"
:
3
}
                
u
"
sum
"
:
3
            
}
        
)
