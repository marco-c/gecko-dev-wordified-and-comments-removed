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
video
"
self
.
browsertime_video
and
"
true
"
or
"
false
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
vvv
"
            
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
not
self
.
no_condprof
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
cmd
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
            
proc
=
self
.
process_handler
(
cmd
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
2
*
60
            
)
            
proc
.
wait
(
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
Error
while
attempting
to
run
browsertime
:
%
s
"
%
str
(
e
)
)
            
raise
