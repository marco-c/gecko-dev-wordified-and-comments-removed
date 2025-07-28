import
json
import
logging
import
multiprocessing
import
os
import
subprocess
import
sys
import
tempfile
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
      
if
shards
>
1
:
        
jar_arg
.
extend
(
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
group_test_list
[
index
]
)
]
)
      
elif
self
.
_test_instance
.
test_filter
:
        
jar_arg
.
extend
(
[
'
-
gtest
-
filter
'
self
.
_test_instance
.
test_filter
]
)
      
if
self
.
_test_instance
.
package_filter
:
        
jar_arg
.
extend
(
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
)
      
if
self
.
_test_instance
.
runner_filter
:
        
jar_arg
.
extend
(
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
)
    
return
jar_args_list
  
def
_CreateJvmArgsList
(
self
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
resourcesMode
=
binary
'
    
]
    
if
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
:
      
jvm_args
+
=
[
'
-
Drobolectric
.
logging
=
stdout
'
]
    
if
self
.
_test_instance
.
debug_socket
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
      
if
self
.
_test_instance
.
coverage_on_the_fly
:
        
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
)
    
return
jvm_args
  
def
RunTests
(
self
results
)
:
    
wrapper_path
=
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
test_filter
        
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
wrapper_path
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
wrapper_path
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
      
procs
=
[
]
      
temp_files
=
[
]
      
for
index
cmd
in
enumerate
(
cmd_list
)
:
        
if
index
=
=
0
:
          
sys
.
stdout
.
write
(
'
\
nShard
0
output
:
\
n
'
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
sys
.
stdout
                  
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
      
PrintProcessesStdout
(
procs
temp_files
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
'
%
resource_apk
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
PrintProcessesStdout
(
procs
temp_files
)
:
  
"
"
"
Prints
the
files
that
the
processes
wrote
stdout
to
.
  
Waits
for
processes
to
finish
then
writes
the
files
to
stdout
.
  
Args
:
    
procs
:
A
list
of
subprocesses
.
    
temp_files
:
A
list
of
temporaryFile
objects
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
  
processes_running
=
True
  
while
processes_running
:
    
if
all
(
p
.
poll
(
)
is
not
None
for
p
in
procs
)
:
      
processes_running
=
False
    
else
:
      
time
.
sleep
(
.
25
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
  
for
i
f
in
enumerate
(
temp_files
)
:
    
f
.
seek
(
0
)
    
sys
.
stdout
.
write
(
'
\
nShard
%
d
output
:
\
n
'
%
(
i
+
1
)
)
    
sys
.
stdout
.
write
(
f
.
read
(
)
.
decode
(
'
utf
-
8
'
)
)
    
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
        
sys
.
stdout
.
write
(
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
)
    
sys
.
stdout
.
write
(
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
\
n
'
)
    
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
