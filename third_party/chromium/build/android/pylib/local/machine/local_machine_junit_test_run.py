import
json
import
logging
import
multiprocessing
import
os
import
queue
import
re
import
subprocess
import
sys
import
tempfile
import
threading
import
time
import
zipfile
from
six
.
moves
import
range
from
devil
.
utils
import
cmd_helper
from
py_utils
import
tempfile_ext
from
pylib
import
constants
from
pylib
.
base
import
base_test_result
from
pylib
.
base
import
test_run
from
pylib
.
constants
import
host_paths
from
pylib
.
results
import
json_results
_EXCLUDED_CLASSES_PREFIXES
=
(
'
android
'
'
junit
'
'
org
/
bouncycastle
/
util
'
                              
'
org
/
hamcrest
'
'
org
/
junit
'
'
org
/
mockito
'
)
_EXCLUDED_SUITES
=
{
    
'
password_check_junit_tests
'
    
'
touch_to_fill_junit_tests
'
}
_MIN_CLASSES_PER_SHARD
=
8
_SHARD_TIMEOUT
=
30
*
60
_LOGCAT_RE
=
re
.
compile
(
r
'
[
A
-
Z
]
/
[
\
w
\
d_
-
]
+
:
'
)
class
LocalMachineJunitTestRun
(
test_run
.
TestRun
)
:
  
def
TestPackage
(
self
)
:
    
return
self
.
_test_instance
.
suite
  
def
SetUp
(
self
)
:
    
pass
  
def
_GetFilterArgs
(
self
shard_test_filter
=
None
)
:
    
ret
=
[
]
    
if
shard_test_filter
:
      
ret
+
=
[
'
-
gtest
-
filter
'
'
:
'
.
join
(
shard_test_filter
)
]
    
for
test_filter
in
self
.
_test_instance
.
test_filters
:
      
ret
+
=
[
'
-
gtest
-
filter
'
test_filter
]
    
if
self
.
_test_instance
.
package_filter
:
      
ret
+
=
[
'
-
package
-
filter
'
self
.
_test_instance
.
package_filter
]
    
if
self
.
_test_instance
.
runner_filter
:
      
ret
+
=
[
'
-
runner
-
filter
'
self
.
_test_instance
.
runner_filter
]
    
return
ret
  
def
_CreateJarArgsList
(
self
json_result_file_paths
group_test_list
shards
)
:
    
jar_args_list
=
[
[
'
-
json
-
results
-
file
'
result_file
]
                     
for
result_file
in
json_result_file_paths
]
    
for
index
jar_arg
in
enumerate
(
jar_args_list
)
:
      
shard_test_filter
=
group_test_list
[
index
]
if
shards
>
1
else
None
      
jar_arg
+
=
self
.
_GetFilterArgs
(
shard_test_filter
)
    
return
jar_args_list
  
def
_CreateJvmArgsList
(
self
for_listing
=
False
)
:
    
jvm_args
=
[
        
'
-
Drobolectric
.
dependency
.
dir
=
%
s
'
%
        
self
.
_test_instance
.
robolectric_runtime_deps_dir
        
'
-
Ddir
.
source
.
root
=
%
s
'
%
constants
.
DIR_SOURCE_ROOT
        
'
-
Drobolectric
.
offline
=
true
'
        
'
-
Drobolectric
.
resourcesMode
=
binary
'
        
'
-
Drobolectric
.
logging
=
stdout
'
        
'
-
Djava
.
library
.
path
=
%
s
'
%
self
.
_test_instance
.
native_libs_dir
    
]
    
if
self
.
_test_instance
.
debug_socket
and
not
for_listing
:
      
jvm_args
+
=
[
          
'
-
agentlib
:
jdwp
=
transport
=
dt_socket
'
          
'
server
=
y
suspend
=
y
address
=
%
s
'
%
self
.
_test_instance
.
debug_socket
      
]
    
if
self
.
_test_instance
.
coverage_dir
and
not
for_listing
:
      
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
_test_instance
.
coverage_dir
)
:
        
os
.
makedirs
(
self
.
_test_instance
.
coverage_dir
)
      
elif
not
os
.
path
.
isdir
(
self
.
_test_instance
.
coverage_dir
)
:
        
raise
Exception
(
'
-
-
coverage
-
dir
takes
a
directory
not
file
path
.
'
)
      
jacoco_coverage_file
=
os
.
path
.
join
(
self
.
_test_instance
.
coverage_dir
                                          
'
%
s
.
exec
'
%
self
.
_test_instance
.
suite
)
      
if
self
.
_test_instance
.
coverage_on_the_fly
:
        
jacoco_agent_path
=
os
.
path
.
join
(
host_paths
.
DIR_SOURCE_ROOT
                                         
'
third_party
'
'
jacoco
'
'
lib
'
                                         
'
jacocoagent
.
jar
'
)
        
jacoco_args
=
'
-
javaagent
:
{
}
=
destfile
=
{
}
inclnolocationclasses
=
false
'
        
jvm_args
.
append
(
            
jacoco_args
.
format
(
jacoco_agent_path
jacoco_coverage_file
)
)
      
else
:
        
jvm_args
.
append
(
'
-
Djacoco
-
agent
.
destfile
=
%
s
'
%
jacoco_coverage_file
)
    
return
jvm_args
  
property
  
def
_wrapper_path
(
self
)
:
    
return
os
.
path
.
join
(
constants
.
GetOutDirectory
(
)
'
bin
'
'
helper
'
                        
self
.
_test_instance
.
suite
)
  
def
GetTestsForListing
(
self
)
:
    
with
tempfile_ext
.
NamedTemporaryDirectory
(
)
as
temp_dir
:
      
cmd
=
[
self
.
_wrapper_path
'
-
-
list
-
tests
'
]
+
self
.
_GetFilterArgs
(
)
      
jvm_args
=
self
.
_CreateJvmArgsList
(
for_listing
=
True
)
      
if
jvm_args
:
        
cmd
+
=
[
'
-
-
jvm
-
args
'
'
"
%
s
"
'
%
'
'
.
join
(
jvm_args
)
]
      
AddPropertiesJar
(
[
cmd
]
temp_dir
self
.
_test_instance
.
resource_apk
)
      
lines
=
subprocess
.
check_output
(
cmd
encoding
=
'
utf8
'
)
.
splitlines
(
)
    
PREFIX
=
'
#
TEST
#
'
    
prefix_len
=
len
(
PREFIX
)
    
return
sorted
(
l
[
prefix_len
:
]
for
l
in
lines
if
l
.
startswith
(
PREFIX
)
)
  
def
RunTests
(
self
results
raw_logs_fh
=
None
)
:
    
if
(
self
.
_test_instance
.
shards
=
=
1
        
or
self
.
_test_instance
.
has_literal_filters
or
        
self
.
_test_instance
.
suite
in
_EXCLUDED_SUITES
)
:
      
test_classes
=
[
]
      
shards
=
1
    
else
:
      
test_classes
=
_GetTestClasses
(
self
.
_wrapper_path
)
      
shards
=
ChooseNumOfShards
(
test_classes
self
.
_test_instance
.
shards
)
    
logging
.
info
(
'
Running
tests
on
%
d
shard
(
s
)
.
'
shards
)
    
group_test_list
=
GroupTestsForShard
(
shards
test_classes
)
    
with
tempfile_ext
.
NamedTemporaryDirectory
(
)
as
temp_dir
:
      
cmd_list
=
[
[
self
.
_wrapper_path
]
for
_
in
range
(
shards
)
]
      
json_result_file_paths
=
[
          
os
.
path
.
join
(
temp_dir
'
results
%
d
.
json
'
%
i
)
for
i
in
range
(
shards
)
      
]
      
jar_args_list
=
self
.
_CreateJarArgsList
(
json_result_file_paths
                                              
group_test_list
shards
)
      
if
jar_args_list
:
        
for
i
in
range
(
shards
)
:
          
cmd_list
[
i
]
.
extend
(
              
[
'
-
-
jar
-
args
'
'
"
%
s
"
'
%
'
'
.
join
(
jar_args_list
[
i
]
)
]
)
      
jvm_args
=
self
.
_CreateJvmArgsList
(
)
      
if
jvm_args
:
        
for
cmd
in
cmd_list
:
          
cmd
.
extend
(
[
'
-
-
jvm
-
args
'
'
"
%
s
"
'
%
'
'
.
join
(
jvm_args
)
]
)
      
AddPropertiesJar
(
cmd_list
temp_dir
self
.
_test_instance
.
resource_apk
)
      
show_logcat
=
logging
.
getLogger
(
)
.
isEnabledFor
(
logging
.
INFO
)
      
num_omitted_lines
=
0
      
for
line
in
_RunCommandsAndSerializeOutput
(
cmd_list
)
:
        
if
raw_logs_fh
:
          
raw_logs_fh
.
write
(
line
)
        
if
show_logcat
or
not
_LOGCAT_RE
.
match
(
line
)
:
          
sys
.
stdout
.
write
(
line
)
        
else
:
          
num_omitted_lines
+
=
1
      
if
num_omitted_lines
>
0
:
        
logging
.
critical
(
'
%
d
log
lines
omitted
.
'
num_omitted_lines
)
      
sys
.
stdout
.
flush
(
)
      
if
raw_logs_fh
:
        
raw_logs_fh
.
flush
(
)
      
results_list
=
[
]
      
try
:
        
for
json_file_path
in
json_result_file_paths
:
          
with
open
(
json_file_path
'
r
'
)
as
f
:
            
results_list
+
=
json_results
.
ParseResultsFromJson
(
                
json
.
loads
(
f
.
read
(
)
)
)
      
except
IOError
:
        
results_list
=
[
            
base_test_result
.
BaseTestResult
(
'
Test
Runner
Failure
'
                                            
base_test_result
.
ResultType
.
UNKNOWN
)
        
]
      
test_run_results
=
base_test_result
.
TestRunResults
(
)
      
test_run_results
.
AddResults
(
results_list
)
      
results
.
append
(
test_run_results
)
  
def
TearDown
(
self
)
:
    
pass
def
AddPropertiesJar
(
cmd_list
temp_dir
resource_apk
)
:
  
properties_jar_path
=
os
.
path
.
join
(
temp_dir
'
properties
.
jar
'
)
  
with
zipfile
.
ZipFile
(
properties_jar_path
'
w
'
)
as
z
:
    
z
.
writestr
(
'
com
/
android
/
tools
/
test_config
.
properties
'
               
'
android_resource_apk
=
%
s
\
n
'
%
resource_apk
)
    
props
=
[
        
'
application
=
android
.
app
.
Application
'
        
'
sdk
=
28
'
        
(
'
shadows
=
org
.
chromium
.
testing
.
local
.
'
         
'
CustomShadowApplicationPackageManager
'
)
    
]
    
z
.
writestr
(
'
robolectric
.
properties
'
'
\
n
'
.
join
(
props
)
)
  
for
cmd
in
cmd_list
:
    
cmd
.
extend
(
[
'
-
-
classpath
'
properties_jar_path
]
)
def
ChooseNumOfShards
(
test_classes
shards
)
:
  
if
shards
=
=
1
:
    
return
1
  
if
shards
>
(
len
(
test_classes
)
/
/
_MIN_CLASSES_PER_SHARD
)
or
shards
<
1
:
    
shards
=
max
(
1
(
len
(
test_classes
)
/
/
_MIN_CLASSES_PER_SHARD
)
)
  
shards
=
max
(
1
min
(
shards
multiprocessing
.
cpu_count
(
)
/
/
2
)
)
  
shards
=
min
(
len
(
test_classes
)
shards
)
  
return
shards
def
GroupTestsForShard
(
num_of_shards
test_classes
)
:
  
"
"
"
Groups
tests
that
will
be
ran
on
each
shard
.
  
Args
:
    
num_of_shards
:
number
of
shards
to
split
tests
between
.
    
test_classes
:
A
list
of
test_class
files
in
the
jar
.
  
Return
:
    
Returns
a
dictionary
containing
a
list
of
test
classes
.
  
"
"
"
  
test_dict
=
{
i
:
[
]
for
i
in
range
(
num_of_shards
)
}
  
for
count
test_cls
in
enumerate
(
test_classes
)
:
    
test_cls
=
test_cls
.
replace
(
'
.
class
'
'
*
'
)
    
test_cls
=
test_cls
.
replace
(
'
/
'
'
.
'
)
    
test_dict
[
count
%
num_of_shards
]
.
append
(
test_cls
)
  
return
test_dict
def
_RunCommandsAndSerializeOutput
(
cmd_list
)
:
  
"
"
"
Runs
multiple
commands
in
parallel
and
yields
serialized
output
lines
.
  
Args
:
    
cmd_list
:
List
of
commands
.
  
Returns
:
N
/
A
  
Raises
:
    
TimeoutError
:
If
timeout
is
exceeded
.
  
"
"
"
  
num_shards
=
len
(
cmd_list
)
  
assert
num_shards
>
0
  
procs
=
[
]
  
temp_files
=
[
]
  
for
i
cmd
in
enumerate
(
cmd_list
)
:
    
if
i
=
=
0
:
      
temp_files
.
append
(
None
)
      
procs
.
append
(
          
cmd_helper
.
Popen
(
              
cmd
              
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
)
    
else
:
      
temp_file
=
tempfile
.
TemporaryFile
(
mode
=
'
w
+
t
'
encoding
=
'
utf
-
8
'
)
      
temp_files
.
append
(
temp_file
)
      
procs
.
append
(
cmd_helper
.
Popen
(
          
cmd
          
stdout
=
temp_file
          
stderr
=
temp_file
      
)
)
  
timeout_time
=
time
.
time
(
)
+
_SHARD_TIMEOUT
  
timed_out
=
False
  
yield
'
\
n
'
  
yield
'
Shard
0
output
:
\
n
'
  
def
pump_stream_to_queue
(
f
q
)
:
    
try
:
      
for
line
in
iter
(
f
.
readline
'
'
)
:
        
q
.
put
(
line
)
    
except
ValueError
:
      
pass
  
shard_0_q
=
queue
.
Queue
(
)
  
shard_0_pump
=
threading
.
Thread
(
target
=
pump_stream_to_queue
                                  
args
=
(
procs
[
0
]
.
stdout
shard_0_q
)
)
  
shard_0_pump
.
start
(
)
  
shard_to_check
=
0
  
while
shard_to_check
<
num_shards
:
    
if
shard_0_pump
.
is_alive
(
)
:
      
while
not
shard_0_q
.
empty
(
)
:
        
yield
shard_0_q
.
get_nowait
(
)
    
if
procs
[
shard_to_check
]
.
poll
(
)
is
not
None
:
      
shard_to_check
+
=
1
    
else
:
      
time
.
sleep
(
.
1
)
    
if
time
.
time
(
)
>
timeout_time
:
      
timed_out
=
True
      
break
  
if
shard_0_pump
.
is_alive
(
)
:
    
procs
[
0
]
.
stdout
.
close
(
)
  
shard_0_pump
.
join
(
)
  
while
not
shard_0_q
.
empty
(
)
:
    
yield
shard_0_q
.
get_nowait
(
)
  
for
i
in
range
(
1
num_shards
)
:
    
f
=
temp_files
[
i
]
    
yield
'
\
n
'
    
yield
'
Shard
%
d
output
:
\
n
'
%
i
    
f
.
seek
(
0
)
    
for
line
in
f
.
readlines
(
)
:
      
yield
line
    
f
.
close
(
)
  
if
timed_out
:
    
for
i
p
in
enumerate
(
procs
)
:
      
if
p
.
poll
(
)
is
None
:
        
p
.
kill
(
)
        
yield
'
Index
of
timed
out
shard
:
%
d
\
n
'
%
i
    
yield
'
Output
in
shards
may
be
cutoff
due
to
timeout
.
\
n
'
    
yield
'
\
n
'
    
raise
cmd_helper
.
TimeoutError
(
'
Junit
shards
timed
out
.
'
)
def
_GetTestClasses
(
file_path
)
:
  
test_jar_paths
=
subprocess
.
check_output
(
[
file_path
                                            
'
-
-
print
-
classpath
'
]
)
.
decode
(
)
  
test_jar_paths
=
test_jar_paths
.
split
(
'
:
'
)
  
test_classes
=
[
]
  
for
test_jar_path
in
test_jar_paths
:
    
if
'
third_party
/
robolectric
/
'
in
test_jar_path
:
      
continue
    
test_classes
+
=
_GetTestClassesFromJar
(
test_jar_path
)
  
logging
.
info
(
'
Found
%
d
test
classes
in
class_path
jars
.
'
len
(
test_classes
)
)
  
return
test_classes
def
_GetTestClassesFromJar
(
test_jar_path
)
:
  
"
"
"
Returns
a
list
of
test
classes
from
a
jar
.
  
Test
files
end
in
Test
this
is
enforced
:
  
/
/
tools
/
android
/
errorprone_plugin
/
src
/
org
/
chromium
/
tools
/
errorprone
  
/
plugin
/
TestClassNameCheck
.
java
  
Args
:
    
test_jar_path
:
Path
to
the
jar
.
  
Return
:
    
Returns
a
list
of
test
classes
that
were
in
the
jar
.
  
"
"
"
  
class_list
=
[
]
  
with
zipfile
.
ZipFile
(
test_jar_path
'
r
'
)
as
zip_f
:
    
for
test_class
in
zip_f
.
namelist
(
)
:
      
if
test_class
.
startswith
(
_EXCLUDED_CLASSES_PREFIXES
)
:
        
continue
      
if
test_class
.
endswith
(
'
Test
.
class
'
)
and
'
'
not
in
test_class
:
        
class_list
.
append
(
test_class
)
  
return
class_list
