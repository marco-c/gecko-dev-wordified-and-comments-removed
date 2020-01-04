"
"
"
A
generic
means
of
running
an
URL
based
browser
test
   
follows
the
following
steps
     
-
creates
a
profile
     
-
tests
the
profile
     
-
gets
metrics
for
the
current
test
environment
     
-
loads
the
url
     
-
collects
info
on
any
counters
while
test
runs
     
-
waits
for
a
'
dump
'
from
the
browser
"
"
"
import
os
import
sys
import
platform
import
results
import
subprocess
import
utils
import
mozcrash
import
talosconfig
import
shutil
import
mozfile
from
mozlog
import
get_proxy_logger
from
talos
.
utils
import
TalosCrash
TalosRegression
from
talos
.
talos_process
import
run_browser
from
talos
.
ffsetup
import
FFSetup
from
talos
.
cmanager
import
CounterManagement
LOG
=
get_proxy_logger
(
)
class
TTest
(
object
)
:
    
platform_type
=
utils
.
PLATFORM_TYPE
    
def
check_for_crashes
(
self
browser_config
minidump_dir
test_name
)
:
        
found
=
mozcrash
.
check_for_crashes
(
minidump_dir
                                           
browser_config
[
'
symbols_path
'
]
                                           
test_name
=
test_name
)
        
mozfile
.
remove
(
minidump_dir
)
        
if
found
:
            
raise
TalosCrash
(
"
Found
crashes
after
test
run
terminating
test
"
)
    
def
runTest
(
self
browser_config
test_config
)
:
        
"
"
"
            
Runs
an
url
based
test
on
the
browser
as
specified
in
the
            
browser_config
dictionary
        
Args
:
            
browser_config
:
Dictionary
of
configuration
options
for
the
                             
browser
(
paths
prefs
etc
)
            
test_config
:
Dictionary
of
configuration
for
the
given
                             
test
(
url
cycles
counters
etc
)
        
"
"
"
        
LOG
.
debug
(
"
operating
with
platform_type
:
%
s
"
%
self
.
platform_type
)
        
with
FFSetup
(
browser_config
test_config
)
as
setup
:
            
return
self
.
_runTest
(
browser_config
test_config
setup
)
    
def
_runTest
(
self
browser_config
test_config
setup
)
:
        
minidump_dir
=
os
.
path
.
join
(
setup
.
profile_dir
'
minidumps
'
)
        
counters
=
test_config
.
get
(
self
.
platform_type
+
'
counters
'
[
]
)
        
resolution
=
test_config
[
'
resolution
'
]
        
here
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
realpath
(
__file__
)
)
        
if
test_config
[
'
mainthread
'
]
:
            
mainthread_io
=
os
.
path
.
join
(
here
"
mainthread_io
.
log
"
)
            
setup
.
env
[
'
MOZ_MAIN_THREAD_IO_LOG
'
]
=
mainthread_io
        
test_config
[
'
url
'
]
=
utils
.
interpolate
(
            
test_config
[
'
url
'
]
            
profile
=
setup
.
profile_dir
            
firefox
=
browser_config
[
'
browser_path
'
]
        
)
        
global_counters
=
{
}
        
if
browser_config
.
get
(
'
xperf_path
'
)
:
            
for
c
in
test_config
.
get
(
'
xperf_counters
'
[
]
)
:
                
global_counters
[
c
]
=
[
]
        
if
test_config
[
'
shutdown
'
]
:
            
global_counters
[
'
shutdown
'
]
=
[
]
        
if
test_config
.
get
(
'
responsiveness
'
)
and
\
           
platform
.
system
(
)
!
=
"
Darwin
"
:
            
setup
.
env
[
'
MOZ_INSTRUMENT_EVENT_LOOP
'
]
=
'
1
'
            
setup
.
env
[
'
MOZ_INSTRUMENT_EVENT_LOOP_THRESHOLD
'
]
=
'
20
'
            
setup
.
env
[
'
MOZ_INSTRUMENT_EVENT_LOOP_INTERVAL
'
]
=
'
10
'
            
global_counters
[
'
responsiveness
'
]
=
[
]
        
test_results
=
results
.
TestResults
(
            
test_config
            
global_counters
        
)
        
for
i
in
range
(
test_config
[
'
cycles
'
]
)
:
            
LOG
.
info
(
"
Running
cycle
%
d
/
%
d
for
%
s
test
.
.
.
"
                     
%
(
i
+
1
test_config
[
'
cycles
'
]
test_config
[
'
name
'
]
)
)
            
mozfile
.
remove
(
browser_config
[
'
error_filename
'
]
)
            
if
test_config
.
get
(
'
reinstall
'
'
'
)
:
                
for
keep
in
test_config
[
'
reinstall
'
]
:
                    
origin
=
os
.
path
.
join
(
test_config
[
'
profile_path
'
]
                                          
keep
)
                    
dest
=
os
.
path
.
join
(
setup
.
profile_dir
keep
)
                    
LOG
.
debug
(
"
Reinstalling
%
s
on
top
of
%
s
"
                              
%
(
origin
dest
)
)
                    
shutil
.
copy
(
origin
dest
)
            
timeout
=
test_config
.
get
(
'
timeout
'
7200
)
            
if
setup
.
sps_profile
:
                
timeout
+
=
5
*
60
            
command_args
=
utils
.
GenerateBrowserCommandLine
(
                
browser_config
[
"
browser_path
"
]
                
browser_config
[
"
extra_args
"
]
                
setup
.
profile_dir
                
test_config
[
'
url
'
]
                
profiling_info
=
(
setup
.
sps_profile
.
profiling_info
                                
if
setup
.
sps_profile
else
None
)
            
)
            
mainthread_error_count
=
0
            
if
test_config
[
'
setup
'
]
:
                
talosconfig
.
generateTalosConfig
(
command_args
                                                
browser_config
                                                
test_config
)
                
subprocess
.
call
(
                    
[
'
python
'
]
+
test_config
[
'
setup
'
]
.
split
(
)
                
)
            
counter_management
=
None
            
if
counters
:
                
counter_management
=
CounterManagement
(
                    
browser_config
[
'
process
'
]
                    
counters
                    
resolution
                
)
            
try
:
                
pcontext
=
run_browser
(
                    
command_args
                    
minidump_dir
                    
timeout
=
timeout
                    
env
=
setup
.
env
                    
on_started
=
(
counter_management
.
start
                                
if
counter_management
else
None
)
                
)
            
finally
:
                
if
counter_management
:
                    
counter_management
.
stop
(
)
            
if
test_config
[
'
mainthread
'
]
:
                
rawlog
=
os
.
path
.
join
(
here
"
mainthread_io
.
log
"
)
                
if
os
.
path
.
exists
(
rawlog
)
:
                    
processedlog
=
\
                        
os
.
path
.
join
(
here
'
mainthread_io
.
json
'
)
                    
xre_path
=
\
                        
os
.
path
.
dirname
(
browser_config
[
'
browser_path
'
]
)
                    
mtio_py
=
os
.
path
.
join
(
here
'
mainthreadio
.
py
'
)
                    
command
=
[
'
python
'
mtio_py
rawlog
                               
processedlog
xre_path
]
                    
mtio
=
subprocess
.
Popen
(
command
                                            
env
=
os
.
environ
.
copy
(
)
                                            
stdout
=
subprocess
.
PIPE
)
                    
output
stderr
=
mtio
.
communicate
(
)
                    
for
line
in
output
.
split
(
'
\
n
'
)
:
                        
if
line
.
strip
(
)
=
=
"
"
:
                            
continue
                        
print
line
                        
mainthread_error_count
+
=
1
                    
mozfile
.
remove
(
rawlog
)
            
if
test_config
[
'
cleanup
'
]
:
                
talosconfig
.
generateTalosConfig
(
command_args
                                                
browser_config
                                                
test_config
                                                
pid
=
pcontext
.
pid
)
                
subprocess
.
call
(
                    
[
sys
.
executable
]
+
test_config
[
'
cleanup
'
]
.
split
(
)
                
)
            
for
fname
in
(
'
sessionstore
.
js
'
'
.
parentlock
'
                          
'
sessionstore
.
bak
'
)
:
                
mozfile
.
remove
(
os
.
path
.
join
(
setup
.
profile_dir
fname
)
)
            
if
os
.
path
.
exists
(
browser_config
[
'
error_filename
'
]
)
or
\
               
mainthread_error_count
>
0
:
                
raise
TalosRegression
(
                    
"
Talos
has
found
a
regression
if
you
have
questions
"
                    
"
ask
for
help
in
irc
on
#
perf
"
                
)
            
test_results
.
add
(
                
'
\
n
'
.
join
(
pcontext
.
output
)
                
counter_results
=
(
counter_management
.
results
(
)
                                 
if
counter_management
                                 
else
None
)
            
)
            
if
setup
.
sps_profile
:
                
setup
.
sps_profile
.
symbolicate
(
i
)
            
self
.
check_for_crashes
(
browser_config
minidump_dir
                                   
test_config
[
'
name
'
]
)
        
test_results
.
all_counter_results
.
extend
(
            
[
{
key
:
value
}
for
key
value
in
global_counters
.
items
(
)
]
        
)
        
for
c
in
test_results
.
all_counter_results
:
            
for
key
value
in
c
.
items
(
)
:
                
LOG
.
debug
(
"
COUNTER
%
r
:
%
s
"
%
(
key
value
)
)
        
return
test_results
