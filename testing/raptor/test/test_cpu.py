import
os
import
sys
from
unittest
import
mock
import
mozunit
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
raptor_dir
=
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
here
)
"
raptor
"
)
sys
.
path
.
insert
(
0
raptor_dir
)
import
cpu
from
webextension
import
WebExtensionAndroid
def
test_no_device
(
)
:
    
original_get
=
WebExtensionAndroid
.
get_browser_meta
    
WebExtensionAndroid
.
get_browser_meta
=
mock
.
MagicMock
(
)
    
WebExtensionAndroid
.
get_browser_meta
.
return_value
=
(
"
app
"
"
version
"
)
    
raptor
=
WebExtensionAndroid
(
        
"
geckoview
"
        
"
org
.
mozilla
.
org
.
mozilla
.
geckoview_example
"
        
cpu_test
=
True
    
)
    
WebExtensionAndroid
.
get_browser_meta
=
original_get
    
raptor
.
device
=
None
    
resp
=
cpu
.
start_android_cpu_profiler
(
raptor
)
    
assert
resp
is
None
def
test_usage_with_invalid_data_returns_zero
(
)
:
    
with
mock
.
patch
(
"
mozdevice
.
adb
.
ADBDevice
"
)
as
device
:
        
with
mock
.
patch
(
"
control_server
.
RaptorControlServer
"
)
as
control_server
:
            
device
.
shell_output
.
side_effect
=
[
"
8
.
0
.
0
"
"
geckoview
"
]
            
device
.
_verbose
=
True
            
control_server
.
cpu_test
=
True
            
control_server
.
device
=
device
            
original_get
=
WebExtensionAndroid
.
get_browser_meta
            
WebExtensionAndroid
.
get_browser_meta
=
mock
.
MagicMock
(
)
            
WebExtensionAndroid
.
get_browser_meta
.
return_value
=
(
"
app
"
"
version
"
)
            
raptor
=
WebExtensionAndroid
(
"
geckoview
"
"
org
.
mozilla
.
geckoview_example
"
)
            
WebExtensionAndroid
.
get_browser_meta
=
original_get
            
raptor
.
config
[
"
cpu_test
"
]
=
True
            
raptor
.
control_server
=
control_server
            
raptor
.
device
=
device
            
cpu_profiler
=
cpu
.
AndroidCPUProfiler
(
raptor
)
            
cpu_profiler
.
get_app_cpu_usage
(
)
            
avg_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_invalid_data_returns_zero
-
avg
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
avg
"
:
0
}
            
}
            
min_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_invalid_data_returns_zero
-
min
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
min
"
:
0
}
            
}
            
max_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_invalid_data_returns_zero
-
max
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
max
"
:
0
}
            
}
            
cpu_profiler
.
generate_android_cpu_profile
(
                
"
usage_with_invalid_data_returns_zero
"
            
)
            
control_server
.
submit_supporting_data
.
assert_has_calls
(
                
[
                    
mock
.
call
(
avg_cpuinfo_data
)
                    
mock
.
call
(
min_cpuinfo_data
)
                    
mock
.
call
(
max_cpuinfo_data
)
                
]
            
)
def
test_usage_with_output
(
)
:
    
with
mock
.
patch
(
"
mozdevice
.
adb
.
ADBDevice
"
)
as
device
:
        
with
mock
.
patch
(
"
control_server
.
RaptorControlServer
"
)
as
control_server
:
            
filepath
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
+
"
/
files
/
"
            
with
open
(
filepath
+
"
top
-
info
.
txt
"
"
r
"
)
as
f
:
                
test_data
=
f
.
read
(
)
            
device
.
shell_output
.
side_effect
=
[
"
8
.
0
.
0
"
test_data
]
            
device
.
_verbose
=
True
            
control_server
.
cpu_test
=
True
            
control_server
.
test_name
=
"
cpuunittest
"
            
control_server
.
device
=
device
            
control_server
.
app_name
=
"
org
.
mozilla
.
geckoview_example
"
            
original_get
=
WebExtensionAndroid
.
get_browser_meta
            
WebExtensionAndroid
.
get_browser_meta
=
mock
.
MagicMock
(
)
            
WebExtensionAndroid
.
get_browser_meta
.
return_value
=
(
"
app
"
"
version
"
)
            
raptor
=
WebExtensionAndroid
(
"
geckoview
"
"
org
.
mozilla
.
geckoview_example
"
)
            
WebExtensionAndroid
.
get_browser_meta
=
original_get
            
raptor
.
device
=
device
            
raptor
.
config
[
"
cpu_test
"
]
=
True
            
raptor
.
control_server
=
control_server
            
cpu_profiler
=
cpu
.
AndroidCPUProfiler
(
raptor
)
            
cpu_profiler
.
polls
.
append
(
cpu_profiler
.
get_app_cpu_usage
(
)
)
            
cpu_profiler
.
polls
.
append
(
0
)
            
avg_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_integer_cpu_info_output
-
avg
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
avg
"
:
93
.
7
/
2
}
            
}
            
min_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_integer_cpu_info_output
-
min
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
min
"
:
0
}
            
}
            
max_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_integer_cpu_info_output
-
max
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
max
"
:
93
.
7
}
            
}
            
cpu_profiler
.
generate_android_cpu_profile
(
                
"
usage_with_integer_cpu_info_output
"
            
)
            
control_server
.
submit_supporting_data
.
assert_has_calls
(
                
[
                    
mock
.
call
(
avg_cpuinfo_data
)
                    
mock
.
call
(
min_cpuinfo_data
)
                    
mock
.
call
(
max_cpuinfo_data
)
                
]
            
)
def
test_usage_with_fallback
(
)
:
    
with
mock
.
patch
(
"
mozdevice
.
adb
.
ADBDevice
"
)
as
device
:
        
with
mock
.
patch
(
"
control_server
.
RaptorControlServer
"
)
as
control_server
:
            
device
.
_verbose
=
True
            
shell_output
=
(
                
"
31093
u0_a196
10
-
10
8
%
S
"
                
+
"
66
1392100K
137012K
fg
org
.
mozilla
.
geckoview_example
"
            
)
            
device
.
shell_output
.
side_effect
=
[
"
7
.
0
.
0
"
shell_output
]
            
control_server
.
cpu_test
=
True
            
control_server
.
test_name
=
"
cpuunittest
"
            
control_server
.
device
=
device
            
control_server
.
app_name
=
"
org
.
mozilla
.
geckoview_example
"
            
original_get
=
WebExtensionAndroid
.
get_browser_meta
            
WebExtensionAndroid
.
get_browser_meta
=
mock
.
MagicMock
(
)
            
WebExtensionAndroid
.
get_browser_meta
.
return_value
=
(
"
app
"
"
version
"
)
            
raptor
=
WebExtensionAndroid
(
"
geckoview
"
"
org
.
mozilla
.
geckoview_example
"
)
            
WebExtensionAndroid
.
get_browser_meta
=
original_get
            
raptor
.
device
=
device
            
raptor
.
config
[
"
cpu_test
"
]
=
True
            
raptor
.
control_server
=
control_server
            
cpu_profiler
=
cpu
.
AndroidCPUProfiler
(
raptor
)
            
cpu_profiler
.
polls
.
append
(
cpu_profiler
.
get_app_cpu_usage
(
)
)
            
cpu_profiler
.
polls
.
append
(
0
)
            
avg_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_fallback
-
avg
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
avg
"
:
8
/
2
}
            
}
            
min_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_fallback
-
min
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
min
"
:
0
}
            
}
            
max_cpuinfo_data
=
{
                
"
type
"
:
"
cpu
"
                
"
test
"
:
"
usage_with_fallback
-
max
"
                
"
unit
"
:
"
%
"
                
"
values
"
:
{
"
max
"
:
8
}
            
}
            
cpu_profiler
.
generate_android_cpu_profile
(
"
usage_with_fallback
"
)
            
control_server
.
submit_supporting_data
.
assert_has_calls
(
                
[
                    
mock
.
call
(
avg_cpuinfo_data
)
                    
mock
.
call
(
min_cpuinfo_data
)
                    
mock
.
call
(
max_cpuinfo_data
)
                
]
            
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
