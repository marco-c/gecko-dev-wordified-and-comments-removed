from
__future__
import
absolute_import
from
abc
import
ABCMeta
abstractmethod
import
os
import
json
import
re
import
six
import
mozprocess
from
benchmark
import
Benchmark
from
logger
.
logger
import
RaptorLogger
from
perftest
import
Perftest
from
results
import
BrowsertimeResultsHandler
LOG
=
RaptorLogger
(
component
=
"
raptor
-
browsertime
"
)
DEFAULT_CHROMEVERSION
=
"
77
"
BROWSERTIME_PAGELOAD_OUTPUT_TIMEOUT
=
120
BROWSERTIME_BENCHMARK_OUTPUT_TIMEOUT
=
None
class
Browsertime
(
Perftest
)
:
    
"
"
"
Abstract
base
class
for
Browsertime
"
"
"
    
__metaclass__
=
ABCMeta
    
property
    
abstractmethod
    
def
browsertime_args
(
self
)
:
        
pass
    
def
__init__
(
self
app
binary
process_handler
=
None
*
*
kwargs
)
:
        
self
.
browsertime_failure
=
"
"
        
self
.
process_handler
=
process_handler
or
mozprocess
.
ProcessHandler
        
for
key
in
list
(
kwargs
)
:
            
if
key
.
startswith
(
"
browsertime_
"
)
:
                
value
=
kwargs
.
pop
(
key
)
                
setattr
(
self
key
value
)
        
def
klass
(
*
*
config
)
:
            
root_results_dir
=
os
.
path
.
join
(
                
os
.
environ
.
get
(
"
MOZ_UPLOAD_DIR
"
os
.
getcwd
(
)
)
"
browsertime
-
results
"
            
)
            
return
BrowsertimeResultsHandler
(
config
root_results_dir
=
root_results_dir
)
        
super
(
Browsertime
self
)
.
__init__
(
            
app
binary
results_handler_class
=
klass
*
*
kwargs
        
)
        
LOG
.
info
(
"
cwd
:
'
{
}
'
"
.
format
(
os
.
getcwd
(
)
)
)
        
self
.
config
[
"
browsertime
"
]
=
True
        
for
k
in
(
            
"
browsertime_node
"
            
"
browsertime_browsertimejs
"
            
"
browsertime_ffmpeg
"
            
"
browsertime_geckodriver
"
            
"
browsertime_chromedriver
"
        
)
:
            
try
:
                
if
not
self
.
browsertime_video
and
k
=
=
"
browsertime_ffmpeg
"
:
                    
continue
                
LOG
.
info
(
"
{
}
:
{
}
"
.
format
(
k
getattr
(
self
k
)
)
)
                
LOG
.
info
(
"
{
}
:
{
}
"
.
format
(
k
os
.
stat
(
getattr
(
self
k
)
)
)
)
            
except
Exception
as
e
:
                
LOG
.
info
(
"
{
}
:
{
}
"
.
format
(
k
e
)
)
    
def
build_browser_profile
(
self
)
:
        
super
(
Browsertime
self
)
.
build_browser_profile
(
)
        
self
.
remove_mozprofile_delimiters_from_profile
(
)
    
def
remove_mozprofile_delimiters_from_profile
(
self
)
:
        
LOG
.
info
(
"
Removing
mozprofile
delimiters
from
browser
profile
"
)
        
userjspath
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
user
.
js
"
)
        
try
:
            
with
open
(
userjspath
)
as
userjsfile
:
                
lines
=
userjsfile
.
readlines
(
)
            
lines
=
[
                
line
for
line
in
lines
                
if
not
line
.
startswith
(
"
#
MozRunner
"
)
and
line
.
strip
(
)
            
]
            
with
open
(
userjspath
"
w
"
)
as
userjsfile
:
                
userjsfile
.
writelines
(
lines
)
        
except
Exception
as
e
:
            
LOG
.
critical
(
"
Exception
{
}
while
removing
mozprofile
delimiters
"
.
format
(
e
)
)
    
def
set_browser_test_prefs
(
self
raw_prefs
)
:
        
LOG
.
info
(
"
setting
test
-
specific
Firefox
preferences
"
)
        
self
.
profile
.
set_preferences
(
json
.
loads
(
raw_prefs
)
)
        
self
.
remove_mozprofile_delimiters_from_profile
(
)
    
def
run_test_setup
(
self
test
)
:
        
super
(
Browsertime
self
)
.
run_test_setup
(
test
)
        
if
test
.
get
(
"
type
"
)
=
=
"
benchmark
"
:
            
self
.
benchmark
=
Benchmark
(
self
.
config
test
)
            
test
[
"
test_url
"
]
=
test
[
"
test_url
"
]
.
replace
(
"
<
host
>
"
self
.
benchmark
.
host
)
            
test
[
"
test_url
"
]
=
test
[
"
test_url
"
]
.
replace
(
"
<
port
>
"
self
.
benchmark
.
port
)
        
if
test
.
get
(
"
playback
"
)
is
not
None
and
self
.
playback
is
None
:
            
self
.
start_playback
(
test
)
        
self
.
driver_paths
=
[
]
        
if
self
.
browsertime_geckodriver
:
            
self
.
driver_paths
.
extend
(
                
[
"
-
-
firefox
.
geckodriverPath
"
self
.
browsertime_geckodriver
]
            
)
        
if
self
.
browsertime_chromedriver
and
self
.
config
[
"
app
"
]
in
[
"
chrome
"
"
chrome
-
m
"
]
:
            
if
(
                
not
self
.
config
.
get
(
"
run_local
"
None
)
                
or
"
{
}
"
in
self
.
browsertime_chromedriver
            
)
:
                
if
self
.
browser_version
:
                    
bvers
=
str
(
self
.
browser_version
)
                    
chromedriver_version
=
bvers
.
split
(
"
.
"
)
[
0
]
                
else
:
                    
chromedriver_version
=
DEFAULT_CHROMEVERSION
                
self
.
browsertime_chromedriver
=
self
.
browsertime_chromedriver
.
format
(
                    
chromedriver_version
                
)
                
if
not
os
.
path
.
exists
(
self
.
browsertime_chromedriver
)
:
                    
raise
Exception
(
                        
"
Cannot
find
the
chromedriver
for
the
chrome
version
"
                        
"
being
tested
:
%
s
"
%
self
.
browsertime_chromedriver
                    
)
            
self
.
driver_paths
.
extend
(
                
[
"
-
-
chrome
.
chromedriverPath
"
self
.
browsertime_chromedriver
]
            
)
        
LOG
.
info
(
"
test
:
{
}
"
.
format
(
test
)
)
    
def
run_test_teardown
(
self
test
)
:
        
super
(
Browsertime
self
)
.
run_test_teardown
(
test
)
        
if
self
.
playback
is
not
None
:
            
self
.
playback
.
stop
(
)
            
self
.
playback
=
None
    
def
check_for_crashes
(
self
)
:
        
super
(
Browsertime
self
)
.
check_for_crashes
(
)
    
def
clean_up
(
self
)
:
        
super
(
Browsertime
self
)
.
clean_up
(
)
    
def
_compose_cmd
(
self
test
timeout
)
:
        
if
test
.
get
(
"
type
"
"
"
)
=
=
"
scenario
"
:
            
browsertime_script
=
[
                
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
__file__
)
                    
"
.
.
"
                    
"
.
.
"
                    
"
browsertime
"
                    
"
browsertime_scenario
.
js
"
                
)
                
"
-
-
browsertime
.
scenario_time
"
test
.
get
(
"
scenario_time
"
60000
)
                
"
-
-
browsertime
.
background_app
"
test
.
get
(
"
background_app
"
"
false
"
)
            
]
        
else
:
            
browsertime_script
=
[
                
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
__file__
)
                    
"
.
.
"
                    
"
.
.
"
                    
"
browsertime
"
                    
"
browsertime_pageload
.
js
"
                
)
            
]
        
btime_args
=
self
.
browsertime_args
        
if
self
.
config
[
"
app
"
]
in
(
"
chrome
"
"
chromium
"
'
chrome
-
m
'
)
:
            
btime_args
.
extend
(
self
.
setup_chrome_args
(
test
)
)
        
browsertime_script
.
extend
(
btime_args
)
        
browsertime_script
.
extend
(
            
[
"
-
-
browsertime
.
page_cycles
"
str
(
test
.
get
(
"
page_cycles
"
1
)
)
]
        
)
        
browsertime_script
.
extend
(
[
"
-
-
browsertime
.
url
"
test
[
"
test_url
"
]
]
)
        
browsertime_script
.
extend
(
[
"
-
-
browsertime
.
page_cycle_delay
"
"
1000
"
]
)
        
browsertime_script
.
extend
(
            
[
"
-
-
browsertime
.
post_startup_delay
"
str
(
self
.
post_startup_delay
)
]
        
)
        
browsertime_options
=
[
            
"
-
-
firefox
.
profileTemplate
"
str
(
self
.
profile
.
profile
)
            
"
-
-
skipHar
"
            
"
-
-
viewPort
"
"
1366x695
"
            
"
-
-
pageLoadStrategy
"
"
none
"
            
"
-
-
firefox
.
disableBrowsertimeExtension
"
"
true
"
            
"
-
-
pageCompleteCheckStartWait
"
"
5000
"
            
"
-
-
pageCompleteCheckPollTimeout
"
"
1000
"
            
"
-
-
visualMetrics
"
"
false
"
            
"
-
-
timeouts
.
pageLoad
"
str
(
timeout
)
            
"
-
-
timeouts
.
script
"
str
(
timeout
*
int
(
test
.
get
(
"
page_cycles
"
1
)
)
)
            
"
-
-
resultDir
"
self
.
results_handler
.
result_dir_for_test
(
test
)
        
]
        
if
self
.
verbose
:
            
browsertime_options
.
append
(
"
-
vvv
"
)
        
if
self
.
browsertime_video
:
            
browsertime_options
.
extend
(
[
                
"
-
-
video
"
"
true
"
            
]
)
            
if
self
.
browsertime_no_ffwindowrecorder
:
                
browsertime_options
.
extend
(
[
                    
"
-
-
firefox
.
windowRecorder
"
"
false
"
                
]
)
                
LOG
.
info
(
"
Using
adb
screenrecord
for
mobile
or
ffmpeg
on
desktop
for
videos
"
)
            
else
:
                
browsertime_options
.
extend
(
[
                    
"
-
-
firefox
.
windowRecorder
"
"
true
"
                
]
)
                
LOG
.
info
(
"
Using
Firefox
Window
Recorder
for
videos
"
)
        
else
:
            
browsertime_options
.
extend
(
[
                
"
-
-
video
"
"
false
"
            
]
)
        
if
self
.
using_condprof
:
            
self
.
profile
.
profile
=
self
.
conditioned_profile_dir
        
if
self
.
config
[
"
gecko_profile
"
]
:
            
self
.
config
[
                
"
browsertime_result_dir
"
            
]
=
self
.
results_handler
.
result_dir_for_test
(
test
)
            
self
.
_init_gecko_profiling
(
test
)
            
browsertime_options
.
append
(
"
-
-
firefox
.
geckoProfiler
"
)
            
for
option
browser_time_option
in
(
                
(
"
gecko_profile_interval
"
"
-
-
firefox
.
geckoProfilerParams
.
interval
"
)
                
(
"
gecko_profile_entries
"
"
-
-
firefox
.
geckoProfilerParams
.
bufferSize
"
)
            
)
:
                
value
=
self
.
config
.
get
(
option
)
                
if
value
is
None
:
                    
value
=
test
.
get
(
option
)
                
if
value
is
not
None
:
                    
browsertime_options
.
extend
(
[
browser_time_option
str
(
value
)
]
)
        
return
(
            
[
self
.
browsertime_node
self
.
browsertime_browsertimejs
]
            
+
self
.
driver_paths
            
+
browsertime_script
            
+
            
browsertime_options
            
+
[
"
-
n
"
str
(
test
.
get
(
"
browser_cycles
"
1
)
)
]
        
)
    
def
_compute_process_timeout
(
self
test
timeout
)
:
        
bt_timeout
=
int
(
timeout
/
1000
)
*
int
(
test
.
get
(
"
page_cycles
"
1
)
)
        
bt_timeout
+
=
int
(
self
.
post_startup_delay
/
1000
)
        
bt_timeout
+
=
20
        
bt_timeout
=
bt_timeout
*
int
(
test
.
get
(
"
browser_cycles
"
1
)
)
        
if
self
.
config
[
"
gecko_profile
"
]
is
True
:
            
bt_timeout
+
=
5
*
60
        
return
bt_timeout
    
def
run_test
(
self
test
timeout
)
:
        
global
BROWSERTIME_PAGELOAD_OUTPUT_TIMEOUT
        
self
.
run_test_setup
(
test
)
        
cmd
=
self
.
_compose_cmd
(
test
timeout
)
        
if
test
.
get
(
"
type
"
"
"
)
=
=
"
benchmark
"
:
            
cmd
.
extend
(
                
[
                    
"
-
-
script
"
                    
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
__file__
)
                        
"
.
.
"
                        
"
.
.
"
                        
"
browsertime
"
                        
"
browsertime_benchmark
.
js
"
                    
)
                
]
            
)
        
if
test
.
get
(
"
type
"
"
"
)
=
=
"
scenario
"
:
            
BROWSERTIME_PAGELOAD_OUTPUT_TIMEOUT
=
timeout
        
LOG
.
info
(
"
timeout
(
s
)
:
{
}
"
.
format
(
timeout
)
)
        
LOG
.
info
(
"
browsertime
cwd
:
{
}
"
.
format
(
os
.
getcwd
(
)
)
)
        
LOG
.
info
(
"
browsertime
cmd
:
{
}
"
.
format
(
"
"
.
join
(
[
str
(
c
)
for
c
in
cmd
]
)
)
)
        
if
self
.
browsertime_video
:
            
LOG
.
info
(
"
browsertime_ffmpeg
:
{
}
"
.
format
(
self
.
browsertime_ffmpeg
)
)
        
env
=
dict
(
os
.
environ
)
        
if
self
.
browsertime_video
and
self
.
browsertime_ffmpeg
:
            
ffmpeg_dir
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
abspath
(
self
.
browsertime_ffmpeg
)
)
            
old_path
=
env
.
setdefault
(
"
PATH
"
"
"
)
            
new_path
=
os
.
pathsep
.
join
(
[
ffmpeg_dir
old_path
]
)
            
if
isinstance
(
new_path
six
.
text_type
)
:
                
new_path
=
new_path
.
encode
(
"
utf
-
8
"
"
strict
"
)
            
env
[
"
PATH
"
]
=
new_path
        
LOG
.
info
(
"
PATH
:
{
}
"
.
format
(
env
[
"
PATH
"
]
)
)
        
try
:
            
line_matcher
=
re
.
compile
(
r
"
.
*
(
\
[
.
*
\
]
)
\
s
+
(
[
a
-
zA
-
Z
]
+
)
:
\
s
+
(
.
*
)
"
)
            
def
_line_handler
(
line
)
:
                
"
"
"
This
function
acts
as
a
bridge
between
browsertime
                
and
raptor
.
It
reforms
the
lines
to
get
rid
of
information
                
that
is
not
needed
and
outputs
them
appropriately
based
                
on
the
level
that
is
found
.
(
Debug
and
info
all
go
to
info
)
.
                
For
errors
we
set
an
attribute
(
self
.
browsertime_failure
)
to
                
it
then
raise
a
generic
exception
.
When
we
return
we
check
                
if
self
.
browsertime_failure
and
raise
an
Exception
if
necessary
                
to
stop
Raptor
execution
(
preventing
the
results
processing
)
.
                
"
"
"
                
match
=
line_matcher
.
match
(
line
)
                
if
not
match
:
                    
LOG
.
info
(
line
)
                    
return
                
date
level
msg
=
match
.
groups
(
)
                
level
=
level
.
lower
(
)
                
if
"
error
"
in
level
:
                    
self
.
browsertime_failure
=
msg
                    
raise
Exception
(
"
Browsertime
failed
to
run
"
)
                
elif
"
warning
"
in
level
:
                    
LOG
.
warning
(
msg
)
                
else
:
                    
LOG
.
info
(
msg
)
            
proc
=
self
.
process_handler
(
cmd
processOutputLine
=
_line_handler
env
=
env
)
            
proc
.
run
(
                
timeout
=
self
.
_compute_process_timeout
(
test
timeout
)
                
outputTimeout
=
BROWSERTIME_BENCHMARK_OUTPUT_TIMEOUT
                
if
self
.
benchmark
                
else
BROWSERTIME_PAGELOAD_OUTPUT_TIMEOUT
            
)
            
proc
.
wait
(
)
            
if
self
.
browsertime_failure
:
                
raise
Exception
(
self
.
browsertime_failure
)
        
except
Exception
as
e
:
            
LOG
.
critical
(
str
(
e
)
)
            
raise
