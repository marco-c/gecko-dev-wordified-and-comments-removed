import
contextlib
import
os
import
shutil
import
subprocess
import
sys
import
tempfile
from
devil
import
devil_env
from
devil
.
android
import
device_signal
from
devil
.
android
.
sdk
import
version_codes
from
pylib
import
constants
def
_ProcessType
(
proc
)
:
  
_
_
suffix
=
proc
.
name
.
partition
(
'
:
'
)
  
if
not
suffix
:
    
return
'
browser
'
  
if
suffix
.
startswith
(
'
sandboxed_process
'
)
:
    
return
'
renderer
'
  
if
suffix
.
startswith
(
'
privileged_process
'
)
:
    
return
'
gpu
'
  
return
None
def
_GetSpecifiedPID
(
device
package_name
process_specifier
)
:
  
if
process_specifier
is
None
:
    
return
None
  
try
:
    
pid
=
int
(
process_specifier
)
    
return
pid
  
except
ValueError
:
    
pass
  
full_process_name
=
process_specifier
  
if
process_specifier
.
startswith
(
'
:
'
)
:
    
full_process_name
=
package_name
+
process_specifier
  
elif
'
:
'
not
in
process_specifier
:
    
full_process_name
=
'
%
s
:
%
s
'
%
(
package_name
process_specifier
)
  
matching_processes
=
device
.
ListProcesses
(
full_process_name
)
  
if
len
(
matching_processes
)
=
=
1
:
    
return
matching_processes
[
0
]
.
pid
  
if
len
(
matching_processes
)
>
1
:
    
raise
RuntimeError
(
'
Found
%
d
processes
with
name
"
%
s
"
.
'
%
(
        
len
(
matching_processes
)
process_specifier
)
)
  
package_processes
=
device
.
ListProcesses
(
package_name
)
  
matching_processes
=
[
p
for
p
in
package_processes
if
(
      
_ProcessType
(
p
)
=
=
process_specifier
)
]
  
if
process_specifier
=
=
'
renderer
'
and
len
(
matching_processes
)
>
1
:
    
raise
RuntimeError
(
'
Found
%
d
renderer
processes
;
please
re
-
run
with
only
'
                       
'
one
open
tab
.
'
%
len
(
matching_processes
)
)
  
if
len
(
matching_processes
)
!
=
1
:
    
raise
RuntimeError
(
'
Found
%
d
processes
of
type
"
%
s
"
.
'
%
(
        
len
(
matching_processes
)
process_specifier
)
)
  
return
matching_processes
[
0
]
.
pid
def
_ThreadsForProcess
(
device
pid
)
:
  
if
device
.
build_version_sdk
>
=
version_codes
.
OREO
:
    
pid_regex
=
(
        
r
'
^
[
[
:
graph
:
]
]
\
{
1
\
}
[
[
:
blank
:
]
]
\
{
1
\
}
%
d
[
[
:
blank
:
]
]
\
{
1
\
}
'
%
pid
)
    
ps_cmd
=
"
ps
-
T
-
e
|
grep
'
%
s
'
"
%
pid_regex
    
ps_output_lines
=
device
.
RunShellCommand
(
        
ps_cmd
shell
=
True
check_return
=
True
)
  
else
:
    
ps_cmd
=
[
'
ps
'
'
-
p
'
str
(
pid
)
'
-
t
'
]
    
ps_output_lines
=
device
.
RunShellCommand
(
ps_cmd
check_return
=
True
)
  
result
=
[
]
  
for
l
in
ps_output_lines
:
    
fields
=
l
.
split
(
)
    
if
fields
[
2
]
=
=
str
(
pid
)
:
      
continue
    
result
.
append
(
(
int
(
fields
[
2
]
)
fields
[
-
1
]
)
)
  
return
result
def
_ThreadType
(
thread_name
)
:
  
if
not
thread_name
:
    
return
'
unknown
'
  
if
(
thread_name
.
startswith
(
'
Chrome_ChildIO
'
)
or
      
thread_name
.
startswith
(
'
Chrome_IO
'
)
)
:
    
return
'
io
'
  
if
thread_name
.
startswith
(
'
Compositor
'
)
:
    
return
'
compositor
'
  
if
(
thread_name
.
startswith
(
'
ChildProcessMai
'
)
or
      
thread_name
.
startswith
(
'
CrGpuMain
'
)
or
      
thread_name
.
startswith
(
'
CrRendererMain
'
)
)
:
    
return
'
main
'
  
if
thread_name
.
startswith
(
'
RenderThread
'
)
:
    
return
'
render
'
  
raise
ValueError
(
'
got
no
matching
thread_name
'
)
def
_GetSpecifiedTID
(
device
pid
thread_specifier
)
:
  
if
thread_specifier
is
None
:
    
return
None
  
try
:
    
tid
=
int
(
thread_specifier
)
    
return
tid
  
except
ValueError
:
    
pass
  
if
pid
is
not
None
:
    
matching_threads
=
[
t
for
t
in
_ThreadsForProcess
(
device
pid
)
if
(
        
_ThreadType
(
t
[
1
]
)
=
=
thread_specifier
)
]
    
if
len
(
matching_threads
)
!
=
1
:
      
raise
RuntimeError
(
'
Found
%
d
threads
of
type
"
%
s
"
.
'
%
(
          
len
(
matching_threads
)
thread_specifier
)
)
    
return
matching_threads
[
0
]
[
0
]
  
return
None
def
PrepareDevice
(
device
)
:
  
if
device
.
build_version_sdk
<
version_codes
.
NOUGAT
:
    
raise
RuntimeError
(
'
Simpleperf
profiling
is
only
supported
on
Android
N
'
                       
'
and
later
.
'
)
  
device
.
SetProp
(
'
security
.
perf_harden
'
'
0
'
)
def
InstallSimpleperf
(
device
package_name
)
:
  
package_arch
=
device
.
GetPackageArchitecture
(
package_name
)
or
'
armeabi
-
v7a
'
  
host_simpleperf_path
=
devil_env
.
config
.
LocalPath
(
'
simpleperf
'
package_arch
)
  
if
not
host_simpleperf_path
:
    
raise
Exception
(
'
Could
not
get
path
to
simpleperf
executable
on
host
.
'
)
  
device_simpleperf_path
=
'
/
'
.
join
(
      
(
'
/
data
/
local
/
tmp
/
profilers
'
package_arch
'
simpleperf
'
)
)
  
device
.
PushChangedFiles
(
[
(
host_simpleperf_path
device_simpleperf_path
)
]
)
  
return
device_simpleperf_path
contextlib
.
contextmanager
def
RunSimpleperf
(
device
device_simpleperf_path
package_name
                  
process_specifier
thread_specifier
profiler_args
                  
host_out_path
)
:
  
pid
=
_GetSpecifiedPID
(
device
package_name
process_specifier
)
  
tid
=
_GetSpecifiedTID
(
device
pid
thread_specifier
)
  
if
pid
is
None
and
tid
is
None
:
    
raise
RuntimeError
(
'
Could
not
find
specified
process
/
thread
running
on
'
                       
'
device
.
Make
sure
the
apk
is
already
running
before
'
                       
'
attempting
to
profile
.
'
)
  
profiler_args
=
list
(
profiler_args
)
  
if
profiler_args
and
profiler_args
[
0
]
=
=
'
record
'
:
    
profiler_args
.
pop
(
0
)
  
if
'
-
-
call
-
graph
'
not
in
profiler_args
and
'
-
g
'
not
in
profiler_args
:
    
profiler_args
.
append
(
'
-
g
'
)
  
if
'
-
f
'
not
in
profiler_args
:
    
profiler_args
.
extend
(
(
'
-
f
'
'
1000
'
)
)
  
device_out_path
=
'
/
data
/
local
/
tmp
/
perf
.
data
'
  
if
'
-
o
'
in
profiler_args
:
    
device_out_path
=
profiler_args
[
profiler_args
.
index
(
'
-
o
'
)
+
1
]
  
else
:
    
profiler_args
.
extend
(
(
'
-
o
'
device_out_path
)
)
  
if
tid
:
    
profiler_args
.
extend
(
(
'
-
t
'
str
(
tid
)
)
)
  
else
:
    
profiler_args
.
extend
(
(
'
-
p
'
str
(
pid
)
)
)
  
adb_shell_simpleperf_process
=
device
.
adb
.
StartShell
(
      
[
device_simpleperf_path
'
record
'
]
+
profiler_args
)
  
completed
=
False
  
try
:
    
yield
    
completed
=
True
  
finally
:
    
device
.
KillAll
(
'
simpleperf
'
signum
=
device_signal
.
SIGINT
blocking
=
True
                   
quiet
=
True
)
    
if
completed
:
      
adb_shell_simpleperf_process
.
wait
(
)
      
device
.
PullFile
(
device_out_path
host_out_path
)
def
ConvertSimpleperfToPprof
(
simpleperf_out_path
build_directory
                             
pprof_out_path
)
:
  
unstripped_lib_dir
=
os
.
path
.
join
(
build_directory
'
lib
.
unstripped
'
)
  
unstripped_libs
=
set
(
      
f
for
f
in
os
.
listdir
(
unstripped_lib_dir
)
if
f
.
endswith
(
'
.
so
'
)
)
  
script_dir
=
devil_env
.
config
.
LocalPath
(
'
simpleperf_scripts
'
)
  
report_path
=
os
.
path
.
join
(
script_dir
'
report
.
py
'
)
  
report_cmd
=
[
sys
.
executable
report_path
'
-
i
'
simpleperf_out_path
]
  
device_lib_path
=
None
  
output
=
subprocess
.
check_output
(
report_cmd
stderr
=
subprocess
.
STDOUT
)
  
if
isinstance
(
output
bytes
)
:
    
output
=
output
.
decode
(
)
  
for
line
in
output
.
splitlines
(
)
:
    
fields
=
line
.
split
(
)
    
if
len
(
fields
)
<
5
:
      
continue
    
shlib_path
=
fields
[
4
]
    
shlib_dirname
shlib_basename
=
shlib_path
.
rpartition
(
'
/
'
)
[
:
:
2
]
    
if
shlib_basename
in
unstripped_libs
:
      
device_lib_path
=
shlib_dirname
      
break
  
if
not
device_lib_path
:
    
raise
RuntimeError
(
'
No
chrome
-
related
symbols
in
profiling
data
in
%
s
.
'
                       
'
Either
the
process
was
idle
for
the
entire
profiling
'
                       
'
period
or
something
went
very
wrong
(
and
you
should
'
                       
'
file
a
bug
at
crbug
.
com
/
new
with
component
'
                       
'
Speed
>
Tracing
and
assign
it
to
szager
chromium
.
org
)
.
'
                       
%
simpleperf_out_path
)
  
processing_dir
=
tempfile
.
mkdtemp
(
)
  
try
:
    
processing_lib_dir
=
os
.
path
.
join
(
        
processing_dir
'
binary_cache
'
device_lib_path
.
lstrip
(
'
/
'
)
)
    
os
.
makedirs
(
processing_lib_dir
)
    
for
lib
in
unstripped_libs
:
      
unstripped_lib_path
=
os
.
path
.
join
(
unstripped_lib_dir
lib
)
      
processing_lib_path
=
os
.
path
.
join
(
processing_lib_dir
lib
)
      
os
.
symlink
(
unstripped_lib_path
processing_lib_path
)
    
pprof_converter_script
=
os
.
path
.
join
(
        
script_dir
'
pprof_proto_generator
.
py
'
)
    
pprof_converter_cmd
=
[
        
sys
.
executable
pprof_converter_script
'
-
i
'
simpleperf_out_path
'
-
o
'
        
os
.
path
.
abspath
(
pprof_out_path
)
'
-
-
ndk_path
'
        
constants
.
ANDROID_NDK_ROOT
    
]
    
subprocess
.
check_output
(
pprof_converter_cmd
stderr
=
subprocess
.
STDOUT
                            
cwd
=
processing_dir
)
  
finally
:
    
shutil
.
rmtree
(
processing_dir
ignore_errors
=
True
)
