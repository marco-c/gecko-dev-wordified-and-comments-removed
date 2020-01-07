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
from
__future__
import
absolute_import
print_function
import
json
import
os
import
platform
import
shutil
import
subprocess
import
sys
import
mozcrash
import
mozfile
import
results
import
talosconfig
import
utils
from
mozlog
import
get_proxy_logger
from
talos
.
cmanager
import
CounterManagement
from
talos
.
ffsetup
import
FFSetup
from
talos
.
talos_process
import
run_browser
from
talos
.
utils
import
TalosCrash
TalosError
TalosRegression
run_in_debug_mode
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
'
Found
crashes
after
test
run
terminating
test
'
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
    
staticmethod
    
def
_get_counter_prefix
(
)
:
        
if
platform
.
system
(
)
=
=
'
Linux
'
:
            
return
'
linux
'
        
elif
platform
.
system
(
)
in
(
'
Windows
'
'
Microsoft
'
)
:
            
if
'
6
.
1
'
in
platform
.
version
(
)
:
                
return
'
w7
'
            
elif
'
6
.
2
'
in
platform
.
version
(
)
:
                
return
'
w8
'
            
elif
'
6
.
3
'
in
platform
.
version
(
)
:
                
return
'
w8
'
            
elif
'
10
.
0
'
in
platform
.
version
(
)
:
                
return
'
w8
'
            
else
:
                
raise
TalosError
(
'
unsupported
windows
version
'
)
        
elif
platform
.
system
(
)
=
=
'
Darwin
'
:
            
return
'
mac
'
    
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
'
%
s_counters
'
%
self
.
_get_counter_prefix
(
)
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
'
mainthread_io
.
log
'
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
        
setup
.
env
[
'
STYLO_FORCE_ENABLED
'
]
=
'
1
'
        
if
browser_config
.
get
(
'
stylothreads
'
0
)
>
0
:
            
setup
.
env
[
'
STYLO_THREADS
'
]
=
str
(
browser_config
[
'
stylothreads
'
]
)
        
if
test_config
.
get
(
'
url
'
None
)
is
not
None
:
            
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
'
Darwin
'
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
        
setup
.
env
[
'
JSGC_DISABLE_POISONING
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
MOZ_DISABLE_NONLOCAL_CONNECTIONS
'
]
=
'
1
'
        
if
browser_config
.
get
(
'
mitmproxy
'
False
)
:
            
LOG
.
info
(
'
Using
mitmproxy
so
setting
MOZ_DISABLE_NONLOCAL_CONNECTIONS
to
0
'
)
            
setup
.
env
[
'
MOZ_DISABLE_NONLOCAL_CONNECTIONS
'
]
=
'
0
'
        
test_results
=
results
.
TestResults
(
            
test_config
            
global_counters
            
browser_config
.
get
(
'
framework
'
)
        
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
'
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
'
                     
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
'
Reinstalling
%
s
on
top
of
%
s
'
                              
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
gecko_profile
:
                
timeout
+
=
5
*
60
                
setup
.
env
[
"
TPPROFILINGINFO
"
]
=
json
.
dumps
(
setup
.
gecko_profile
.
profiling_info
)
            
command_args
=
utils
.
GenerateBrowserCommandLine
(
                
browser_config
[
'
browser_path
'
]
                
browser_config
[
'
extra_args
'
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
gecko_profile
.
profiling_info
                                
if
setup
.
gecko_profile
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
                    
debug
=
browser_config
[
'
debug
'
]
                    
debugger
=
browser_config
[
'
debugger
'
]
                    
debugger_args
=
browser_config
[
'
debugger_args
'
]
                
)
            
except
Exception
:
                
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
                
raise
            
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
'
mainthread_io
.
log
'
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
'
'
:
                            
continue
                        
print
(
line
)
                        
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
                    
'
Talos
has
found
a
regression
if
you
have
questions
'
                    
'
ask
for
help
in
irc
on
#
perf
'
                
)
            
if
not
run_in_debug_mode
(
browser_config
)
:
                
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
gecko_profile
:
                
setup
.
gecko_profile
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
'
COUNTER
%
r
:
%
s
'
%
(
key
value
)
)
        
if
browser_config
.
get
(
'
code_coverage
'
False
)
:
            
setup
.
collect_or_clean_ccov
(
)
        
return
test_results
