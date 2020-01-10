from
__future__
import
absolute_import
import
os
import
sys
import
yaml
import
mozinfo
from
marionette_driver
.
errors
import
JavascriptException
ScriptTimeoutException
from
mozproxy
import
get_playback
AWSY_PATH
=
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
)
if
AWSY_PATH
not
in
sys
.
path
:
    
sys
.
path
.
append
(
AWSY_PATH
)
from
awsy
import
process_perf_data
webservers
from
awsy
.
awsy_test_case
import
AwsyTestCase
class
TestMemoryUsage
(
AwsyTestCase
)
:
    
"
"
"
Provides
a
test
that
collects
memory
usage
at
various
checkpoints
:
      
-
"
Start
"
-
Just
after
startup
      
-
"
StartSettled
"
-
After
an
additional
wait
time
      
-
"
TabsOpen
"
-
After
opening
all
provided
URLs
      
-
"
TabsOpenSettled
"
-
After
an
additional
wait
time
      
-
"
TabsOpenForceGC
"
-
After
forcibly
invoking
garbage
collection
      
-
"
TabsClosed
"
-
After
closing
all
tabs
      
-
"
TabsClosedSettled
"
-
After
an
additional
wait
time
      
-
"
TabsClosedForceGC
"
-
After
forcibly
invoking
garbage
collection
    
"
"
"
    
def
urls
(
self
)
:
        
return
self
.
_urls
    
def
perf_suites
(
self
)
:
        
return
process_perf_data
.
PERF_SUITES
    
def
perf_checkpoints
(
self
)
:
        
return
process_perf_data
.
CHECKPOINTS
    
def
perf_extra_opts
(
self
)
:
        
return
self
.
_extra_opts
    
def
setupTp5
(
self
)
:
        
urls
=
None
        
default_tp5n_manifest
=
os
.
path
.
join
(
self
.
_webroot_dir
'
page_load_test
'
'
tp5n
'
                                             
'
tp5n
.
manifest
'
)
        
tp5n_manifest
=
self
.
testvars
.
get
(
"
pageManifest
"
default_tp5n_manifest
)
        
with
open
(
tp5n_manifest
)
as
fp
:
            
urls
=
fp
.
readlines
(
)
        
urls
=
map
(
lambda
x
:
x
.
replace
(
'
localhost
'
'
localhost
:
{
}
'
)
urls
)
        
to_load
=
self
.
pages_to_load
(
)
        
if
not
to_load
:
            
to_load
=
len
(
urls
)
        
self
.
_webservers
=
webservers
.
WebServers
(
"
localhost
"
                                                 
8001
                                                 
self
.
_webroot_dir
                                                 
to_load
)
        
self
.
_webservers
.
start
(
)
        
for
url
server
in
zip
(
urls
self
.
_webservers
.
servers
)
:
            
self
.
_urls
.
append
(
url
.
strip
(
)
.
format
(
server
.
port
)
)
    
def
setupTp6
(
self
)
:
        
default_tp6_pages_manifest
=
os
.
path
.
join
(
AWSY_PATH
'
conf
'
'
tp6
-
pages
.
yml
'
)
        
tp6_pages_manifest
=
self
.
testvars
.
get
(
"
pageManifest
"
default_tp6_pages_manifest
)
        
urls
=
[
]
        
recordings
=
set
(
)
        
with
open
(
tp6_pages_manifest
)
as
f
:
            
d
=
yaml
.
safe_load
(
f
)
            
for
r
in
d
:
                
recordings
.
add
(
r
[
'
rec
'
]
)
                
url
=
r
[
'
url
'
]
                
if
isinstance
(
url
list
)
:
                    
urls
.
extend
(
url
)
                
else
:
                    
urls
.
append
(
url
)
        
self
.
_urls
=
urls
        
self
.
_extra_opts
=
[
"
tp6
"
]
        
tp6_pageset_manifest
=
os
.
path
.
join
(
AWSY_PATH
'
tp6
-
pageset
.
manifest
'
)
        
config
=
{
            
'
playback_tool
'
:
'
mitmproxy
'
            
'
playback_version
'
:
'
4
.
0
.
4
'
            
'
playback_pageset_manifest
'
:
tp6_pageset_manifest
            
'
platform
'
:
mozinfo
.
os
            
'
obj_path
'
:
self
.
_webroot_dir
            
'
binary
'
:
self
.
_binary
            
'
run_local
'
:
self
.
_run_local
            
'
app
'
:
'
firefox
'
            
'
host
'
:
'
127
.
0
.
0
.
1
'
            
'
ignore_mitmdump_exit_failure
'
:
True
        
}
        
self
.
_playback
=
get_playback
(
config
)
        
recording_arg
=
[
]
        
for
recording
in
recordings
:
            
recording_arg
.
append
(
os
.
path
.
join
(
self
.
_playback
.
mozproxy_dir
recording
)
)
        
self
.
_playback
.
config
[
'
playback_files
'
]
=
recording_arg
        
self
.
_playback
.
start
(
)
        
self
.
marionette
.
restart
(
clean
=
False
)
        
self
.
marionette
.
delete_session
(
)
        
caps
=
{
            
"
unhandledPromptBehavior
"
:
"
dismiss
"
        
}
        
self
.
marionette
.
start_session
(
caps
)
        
self
.
marionette
.
set_context
(
'
chrome
'
)
    
def
setUp
(
self
)
:
        
AwsyTestCase
.
setUp
(
self
)
        
self
.
logger
.
info
(
"
setting
up
"
)
        
self
.
_webroot_dir
=
self
.
testvars
[
"
webRootDir
"
]
        
self
.
_urls
=
[
]
        
self
.
_extra_opts
=
None
        
if
self
.
testvars
.
get
(
"
tp6
"
False
)
:
            
self
.
setupTp6
(
)
        
else
:
            
self
.
setupTp5
(
)
        
self
.
logger
.
info
(
"
areweslimyet
run
by
%
d
pages
%
d
iterations
"
                         
"
%
d
perTabPause
%
d
settleWaitTime
"
                         
%
(
self
.
_pages_to_load
self
.
_iterations
                            
self
.
_perTabPause
self
.
_settleWaitTime
)
)
        
self
.
logger
.
info
(
"
done
setting
up
!
"
)
    
def
tearDown
(
self
)
:
        
self
.
logger
.
info
(
"
tearing
down
!
"
)
        
self
.
logger
.
info
(
"
tearing
down
webservers
!
"
)
        
if
self
.
testvars
.
get
(
"
tp6
"
False
)
:
            
self
.
_playback
.
stop
(
)
        
else
:
            
self
.
_webservers
.
stop
(
)
        
AwsyTestCase
.
tearDown
(
self
)
        
self
.
logger
.
info
(
"
done
tearing
down
!
"
)
    
def
clear_preloaded_browser
(
self
)
:
        
"
"
"
        
Clears
out
the
preloaded
browser
.
        
Note
:
Does
nothing
on
older
builds
that
don
'
t
have
a
              
gBrowser
.
removePreloadedBrowser
method
.
        
"
"
"
        
self
.
logger
.
info
(
"
closing
preloaded
browser
"
)
        
script
=
"
"
"
            
if
(
window
.
NewTabPagePreloading
)
{
                
return
NewTabPagePreloading
.
removePreloadedBrowser
(
window
)
;
            
}
            
if
(
"
removePreloadedBrowser
"
in
gBrowser
)
{
                
return
gBrowser
.
removePreloadedBrowser
(
)
;
            
}
            
return
"
gBrowser
.
removePreloadedBrowser
not
available
"
;
            
"
"
"
        
try
:
            
result
=
self
.
marionette
.
execute_script
(
script
                                                    
script_timeout
=
180000
)
        
except
JavascriptException
as
e
:
            
self
.
logger
.
error
(
"
removePreloadedBrowser
(
)
JavaScript
error
:
%
s
"
%
e
)
        
except
ScriptTimeoutException
:
            
self
.
logger
.
error
(
"
removePreloadedBrowser
(
)
timed
out
"
)
        
except
Exception
:
            
self
.
logger
.
error
(
                
"
removePreloadedBrowser
(
)
Unexpected
error
:
%
s
"
%
sys
.
exc_info
(
)
[
0
]
)
        
else
:
            
if
result
:
                
self
.
logger
.
info
(
result
)
    
def
test_open_tabs
(
self
)
:
        
"
"
"
Marionette
test
entry
that
returns
an
array
of
checkoint
arrays
.
        
This
will
generate
a
set
of
checkpoints
for
each
iteration
requested
.
        
Upon
succesful
completion
the
results
will
be
stored
in
        
|
self
.
testvars
[
"
results
"
]
|
and
accessible
to
the
test
runner
via
the
        
|
testvars
|
object
it
passed
in
.
        
"
"
"
        
results
=
[
[
]
for
_
in
range
(
self
.
iterations
(
)
)
]
        
def
create_checkpoint
(
name
iteration
)
:
            
checkpoint
=
self
.
do_memory_report
(
name
iteration
)
            
self
.
assertIsNotNone
(
checkpoint
"
Checkpoint
was
recorded
"
)
            
results
[
iteration
]
.
append
(
checkpoint
)
        
create_checkpoint
(
"
Start
"
0
)
        
self
.
settle
(
)
        
create_checkpoint
(
"
StartSettled
"
0
)
        
for
itr
in
range
(
self
.
iterations
(
)
)
:
            
self
.
open_pages
(
)
            
create_checkpoint
(
"
TabsOpen
"
itr
)
            
self
.
settle
(
)
            
create_checkpoint
(
"
TabsOpenSettled
"
itr
)
            
self
.
assertTrue
(
self
.
do_full_gc
(
)
)
            
create_checkpoint
(
"
TabsOpenForceGC
"
itr
)
            
self
.
reset_state
(
)
            
with
self
.
marionette
.
using_context
(
'
content
'
)
:
                
self
.
logger
.
info
(
"
navigating
to
about
:
blank
"
)
                
self
.
marionette
.
navigate
(
"
about
:
blank
"
)
                
self
.
logger
.
info
(
"
navigated
to
about
:
blank
"
)
            
self
.
signal_user_active
(
)
            
create_checkpoint
(
"
TabsClosedExtraProcesses
"
itr
)
            
self
.
clear_preloaded_browser
(
)
            
create_checkpoint
(
"
TabsClosed
"
itr
)
            
self
.
settle
(
)
            
create_checkpoint
(
"
TabsClosedSettled
"
itr
)
            
self
.
assertTrue
(
self
.
do_full_gc
(
)
"
GC
ran
"
)
            
create_checkpoint
(
"
TabsClosedForceGC
"
itr
)
        
self
.
logger
.
info
(
"
setting
results
"
)
        
self
.
testvars
[
"
results
"
]
=
results
