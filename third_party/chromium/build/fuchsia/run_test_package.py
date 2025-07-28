"
"
"
Contains
a
helper
function
for
deploying
and
executing
a
packaged
executable
on
a
Target
.
"
"
"
from
__future__
import
print_function
import
common
import
hashlib
import
logging
import
multiprocessing
import
os
import
re
import
select
import
subprocess
import
sys
import
threading
import
time
import
uuid
from
exit_on_sig_term
import
ExitOnSigTerm
from
symbolizer
import
BuildIdsPaths
RunSymbolizer
FAR
=
common
.
GetHostToolPathFromPlatform
(
'
far
'
)
_JOIN_TIMEOUT_SECS
=
5
def
_AttachKernelLogReader
(
target
)
:
  
"
"
"
Attaches
a
kernel
log
reader
as
a
long
-
running
SSH
task
.
"
"
"
  
logging
.
info
(
'
Attaching
kernel
logger
.
'
)
  
return
target
.
RunCommandPiped
(
[
'
log_listener
'
                                 
'
-
-
since_now
'
                                 
'
-
-
hide_metadata
'
                                 
'
-
-
tag
'
                                 
'
klog
'
                                
]
                                
stdin
=
open
(
os
.
devnull
'
r
'
)
                                
stdout
=
subprocess
.
PIPE
                                
stderr
=
subprocess
.
STDOUT
)
class
MergedInputStream
(
object
)
:
  
"
"
"
Merges
a
number
of
input
streams
into
a
UTF
-
8
encoded
UNIX
pipe
on
a
  
dedicated
thread
.
Terminates
when
the
file
descriptor
of
the
primary
stream
  
(
the
first
in
the
sequence
)
is
closed
.
"
"
"
  
def
__init__
(
self
streams
)
:
    
assert
len
(
streams
)
>
0
    
self
.
_streams
=
streams
    
self
.
_output_stream
=
None
    
self
.
_thread
=
None
  
def
Start
(
self
)
:
    
"
"
"
Returns
a
pipe
to
the
merged
output
stream
.
"
"
"
    
read_pipe
write_pipe
=
os
.
pipe
(
)
    
self
.
_output_stream
=
os
.
fdopen
(
write_pipe
'
wb
'
0
)
    
self
.
_thread
=
threading
.
Thread
(
target
=
self
.
_Run
)
    
self
.
_thread
.
start
(
)
    
return
os
.
fdopen
(
read_pipe
'
r
'
)
  
def
_Run
(
self
)
:
    
streams_by_fd
=
{
}
    
primary_fd
=
self
.
_streams
[
0
]
.
fileno
(
)
    
for
s
in
self
.
_streams
:
      
streams_by_fd
[
s
.
fileno
(
)
]
=
s
    
flush
=
False
    
while
primary_fd
:
      
rlist
_
xlist
=
select
.
select
(
streams_by_fd
[
]
streams_by_fd
)
      
if
len
(
rlist
)
=
=
0
and
flush
:
        
break
      
for
fileno
in
xlist
:
        
del
streams_by_fd
[
fileno
]
        
if
fileno
=
=
primary_fd
:
          
primary_fd
=
None
      
for
fileno
in
rlist
:
        
line
=
streams_by_fd
[
fileno
]
.
readline
(
)
        
if
line
:
          
self
.
_output_stream
.
write
(
line
)
        
else
:
          
del
streams_by_fd
[
fileno
]
          
if
fileno
=
=
primary_fd
:
            
primary_fd
=
None
    
while
streams_by_fd
:
      
rlist
_
_
=
select
.
select
(
streams_by_fd
[
]
[
]
0
)
      
if
not
rlist
:
        
break
      
for
fileno
in
rlist
:
        
line
=
streams_by_fd
[
fileno
]
.
readline
(
)
        
if
line
:
          
self
.
_output_stream
.
write
(
line
)
        
else
:
          
del
streams_by_fd
[
fileno
]
def
_GetComponentUri
(
package_name
package_component_version
)
:
  
suffix
=
'
cm
'
if
package_component_version
=
=
'
2
'
else
'
cmx
'
  
return
'
fuchsia
-
pkg
:
/
/
fuchsia
.
com
/
%
s
#
meta
/
%
s
.
%
s
'
%
(
package_name
                                                      
package_name
suffix
)
class
RunTestPackageArgs
:
  
"
"
"
RunTestPackage
(
)
configuration
arguments
structure
.
  
code_coverage
:
If
set
the
test
package
will
be
run
via
'
runtests
'
and
the
                 
output
will
be
saved
to
/
tmp
folder
on
the
device
.
  
test_realm_label
:
Specifies
the
realm
name
that
run
-
test
-
component
should
use
.
      
This
must
be
specified
if
a
filter
file
is
to
be
set
or
a
results
summary
      
file
fetched
after
the
test
suite
has
run
.
  
use_run_test_component
:
If
True
then
the
test
package
will
be
run
hermetically
                          
via
'
run
-
test
-
component
'
rather
than
using
'
run
'
.
  
output_directory
:
If
set
the
output
directory
for
CFv2
tests
that
use
                    
custom
artifacts
;
see
fxb
/
75690
.
  
"
"
"
  
def
__init__
(
self
)
:
    
self
.
code_coverage
=
False
    
self
.
test_realm_label
=
None
    
self
.
use_run_test_component
=
False
    
self
.
output_directory
=
None
  
staticmethod
  
def
FromCommonArgs
(
args
)
:
    
run_test_package_args
=
RunTestPackageArgs
(
)
    
run_test_package_args
.
code_coverage
=
args
.
code_coverage
    
return
run_test_package_args
def
_DrainStreamToStdout
(
stream
quit_event
)
:
  
"
"
"
Outputs
the
contents
of
|
stream
|
until
|
quit_event
|
is
set
.
"
"
"
  
while
not
quit_event
.
is_set
(
)
:
    
rlist
_
_
=
select
.
select
(
[
stream
]
[
]
[
]
0
.
1
)
    
if
rlist
:
      
line
=
rlist
[
0
]
.
readline
(
)
      
if
not
line
:
        
return
      
print
(
line
.
rstrip
(
)
)
def
_SymbolizeStream
(
input_fd
ids_txt_files
)
:
  
"
"
"
Returns
a
Popen
object
for
a
symbolizer
process
invocation
.
  
input_fd
:
The
data
to
symbolize
.
  
ids_txt_files
:
A
list
of
ids
.
txt
files
which
contain
symbol
data
.
"
"
"
  
return
RunSymbolizer
(
input_fd
subprocess
.
PIPE
ids_txt_files
)
def
RunTestPackage
(
target
ffx_session
package_paths
package_name
                   
package_component_version
package_args
args
)
:
  
"
"
"
Installs
the
Fuchsia
package
at
|
package_path
|
on
the
target
  
executes
it
with
|
package_args
|
and
symbolizes
its
output
.
  
target
:
The
deployment
Target
object
that
will
run
the
package
.
  
ffx_session
:
An
FfxSession
object
if
the
test
is
to
be
run
via
ffx
or
None
.
  
package_paths
:
The
paths
to
the
.
far
packages
to
be
installed
.
  
package_name
:
The
name
of
the
primary
package
to
run
.
  
package_component_version
:
The
component
version
of
the
primary
package
to
    
run
(
"
1
"
or
"
2
"
)
.
  
package_args
:
The
arguments
which
will
be
passed
to
the
Fuchsia
process
.
  
args
:
RunTestPackageArgs
instance
configuring
how
the
package
will
be
run
.
  
Returns
the
exit
code
of
the
remote
package
process
.
"
"
"
  
kernel_logger
=
_AttachKernelLogReader
(
target
)
  
try
:
    
log_output_quit_event
=
multiprocessing
.
Event
(
)
    
log_output_thread
=
threading
.
Thread
(
target
=
lambda
:
_DrainStreamToStdout
(
        
kernel_logger
.
stdout
log_output_quit_event
)
)
    
log_output_thread
.
daemon
=
True
    
log_output_thread
.
start
(
)
    
with
ExitOnSigTerm
(
)
target
.
GetPkgRepo
(
)
:
      
on_target
=
True
      
start_time
=
time
.
time
(
)
      
target
.
InstallPackage
(
package_paths
)
      
logging
.
info
(
'
Test
installed
in
{
:
.
2f
}
seconds
.
'
.
format
(
time
.
time
(
)
-
                                                              
start_time
)
)
      
log_output_quit_event
.
set
(
)
      
log_output_thread
.
join
(
timeout
=
_JOIN_TIMEOUT_SECS
)
      
logging
.
info
(
'
Running
application
.
'
)
      
component_uri
=
_GetComponentUri
(
package_name
package_component_version
)
      
process
=
None
      
if
ffx_session
:
        
process
=
ffx_session
.
test_run
(
target
.
GetFfxTarget
(
)
component_uri
                                       
package_args
)
      
elif
args
.
code_coverage
:
        
command
=
[
'
runtests
'
'
-
o
'
'
/
tmp
'
component_uri
]
        
if
args
.
test_realm_label
:
          
command
+
=
[
'
-
-
realm
-
label
'
args
.
test_realm_label
]
        
command
+
=
[
'
-
-
'
]
        
command
.
extend
(
package_args
)
      
elif
args
.
use_run_test_component
:
        
command
=
[
'
run
-
test
-
component
'
]
        
if
args
.
test_realm_label
:
          
command
+
=
[
'
-
-
realm
-
label
=
%
s
'
%
args
.
test_realm_label
]
        
command
.
append
(
component_uri
)
        
command
.
append
(
'
-
-
'
)
        
command
.
extend
(
package_args
)
      
else
:
        
command
=
[
'
run
'
component_uri
]
        
command
.
extend
(
package_args
)
      
if
process
is
None
:
        
process
=
target
.
RunCommandPiped
(
command
                                         
stdin
=
open
(
os
.
devnull
'
r
'
)
                                         
stdout
=
subprocess
.
PIPE
                                         
stderr
=
subprocess
.
STDOUT
)
      
ids_txt_paths
=
BuildIdsPaths
(
package_paths
)
      
with
_SymbolizeStream
(
process
.
stdout
ids_txt_paths
)
as
\
              
symbolized_stdout
\
           
_SymbolizeStream
(
kernel_logger
.
stdout
ids_txt_paths
)
as
\
               
symbolized_klog
:
        
output_stream
=
MergedInputStream
(
[
symbolized_stdout
.
stdout
                                           
symbolized_klog
.
stdout
]
)
.
Start
(
)
        
for
next_line
in
output_stream
:
          
print
(
next_line
.
rstrip
(
)
)
        
symbolized_stdout
.
wait
(
)
        
symbolized_klog
.
kill
(
)
      
process
.
wait
(
)
      
if
process
.
returncode
=
=
0
:
        
logging
.
info
(
'
Process
exited
normally
with
status
code
0
.
'
)
      
else
:
        
logging
.
warning
(
'
Process
exited
with
status
code
%
d
.
'
%
                        
process
.
returncode
)
  
finally
:
    
logging
.
info
(
'
Terminating
kernel
log
reader
.
'
)
    
log_output_quit_event
.
set
(
)
    
log_output_thread
.
join
(
)
    
kernel_logger
.
kill
(
)
  
return
process
.
returncode
