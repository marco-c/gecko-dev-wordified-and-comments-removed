from
__future__
import
print_function
import
argparse
import
collections
import
json
import
logging
import
os
import
pipes
import
posixpath
import
random
import
re
import
shlex
import
shutil
import
subprocess
import
sys
import
tempfile
import
textwrap
import
zipfile
import
adb_command_line
import
devil_chromium
from
devil
import
devil_env
from
devil
.
android
import
apk_helper
from
devil
.
android
import
device_errors
from
devil
.
android
import
device_utils
from
devil
.
android
import
flag_changer
from
devil
.
android
.
sdk
import
adb_wrapper
from
devil
.
android
.
sdk
import
build_tools
from
devil
.
android
.
sdk
import
intent
from
devil
.
android
.
sdk
import
version_codes
from
devil
.
utils
import
run_tests_helper
_DIR_SOURCE_ROOT
=
os
.
path
.
normpath
(
    
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
'
.
.
'
'
.
.
'
)
)
_JAVA_HOME
=
os
.
path
.
join
(
_DIR_SOURCE_ROOT
'
third_party
'
'
jdk
'
'
current
'
)
with
devil_env
.
SysPath
(
    
os
.
path
.
join
(
_DIR_SOURCE_ROOT
'
third_party
'
'
colorama
'
'
src
'
)
)
:
  
import
colorama
from
incremental_install
import
installer
from
pylib
import
constants
from
pylib
.
symbols
import
deobfuscator
from
pylib
.
utils
import
simpleperf
from
pylib
.
utils
import
app_bundle_utils
with
devil_env
.
SysPath
(
    
os
.
path
.
join
(
_DIR_SOURCE_ROOT
'
build
'
'
android
'
'
gyp
'
)
)
:
  
import
bundletool
BASE_MODULE
=
'
base
'
def
_Colorize
(
text
style
=
'
'
)
:
  
return
(
style
      
+
text
      
+
colorama
.
Style
.
RESET_ALL
)
def
_InstallApk
(
devices
apk
install_dict
)
:
  
def
install
(
device
)
:
    
if
install_dict
:
      
installer
.
Install
(
device
install_dict
apk
=
apk
permissions
=
[
]
)
    
else
:
      
device
.
Install
(
apk
permissions
=
[
]
allow_downgrade
=
True
reinstall
=
True
)
  
logging
.
info
(
'
Installing
%
sincremental
apk
.
'
'
'
if
install_dict
else
'
non
-
'
)
  
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
install
)
BundleGenerationInfo
=
collections
.
namedtuple
(
    
'
BundleGenerationInfo
'
    
'
bundle_path
bundle_apks_path
aapt2_path
keystore_path
keystore_password
'
    
'
keystore_alias
system_image_locales
'
)
def
_GenerateBundleApks
(
info
                        
output_path
=
None
                        
minimal
=
False
                        
minimal_sdk_version
=
None
                        
mode
=
None
                        
optimize_for
=
None
)
:
  
"
"
"
Generate
an
.
apks
archive
from
a
bundle
on
demand
.
  
Args
:
    
info
:
A
BundleGenerationInfo
instance
.
    
output_path
:
Path
of
output
.
apks
archive
.
    
minimal
:
Create
the
minimal
set
of
apks
possible
(
english
-
only
)
.
    
minimal_sdk_version
:
When
minimal
=
True
use
this
sdkVersion
.
    
mode
:
Build
mode
either
None
or
one
of
app_bundle_utils
.
BUILD_APKS_MODES
.
    
optimize_for
:
Override
split
config
either
None
or
one
of
      
app_bundle_utils
.
OPTIMIZE_FOR_OPTIONS
.
  
"
"
"
  
logging
.
info
(
'
Generating
.
apks
file
'
)
  
app_bundle_utils
.
GenerateBundleApks
(
      
info
.
bundle_path
      
output_path
or
info
.
bundle_apks_path
      
info
.
aapt2_path
      
info
.
keystore_path
      
info
.
keystore_password
      
info
.
keystore_alias
      
system_image_locales
=
info
.
system_image_locales
      
mode
=
mode
      
minimal
=
minimal
      
minimal_sdk_version
=
minimal_sdk_version
      
optimize_for
=
optimize_for
)
def
_InstallBundle
(
devices
apk_helper_instance
modules
fake_modules
)
:
  
def
Install
(
device
)
:
    
device
.
Install
(
        
apk_helper_instance
        
permissions
=
[
]
        
modules
=
modules
        
fake_modules
=
fake_modules
        
allow_downgrade
=
True
)
  
modules_set
=
set
(
modules
)
if
modules
else
set
(
)
  
fake_modules_set
=
set
(
fake_modules
)
if
fake_modules
else
set
(
)
  
if
BASE_MODULE
in
fake_modules_set
:
    
raise
Exception
(
'
\
'
-
f
{
}
\
'
is
disallowed
.
'
.
format
(
BASE_MODULE
)
)
  
if
fake_modules_set
and
BASE_MODULE
not
in
modules_set
:
    
raise
Exception
(
        
'
\
'
-
f
FAKE
\
'
must
be
accompanied
by
\
'
-
m
{
}
\
'
'
.
format
(
BASE_MODULE
)
)
  
logging
.
info
(
'
Installing
bundle
.
'
)
  
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
Install
)
def
_UninstallApk
(
devices
install_dict
package_name
)
:
  
def
uninstall
(
device
)
:
    
if
install_dict
:
      
installer
.
Uninstall
(
device
package_name
)
    
else
:
      
device
.
Uninstall
(
package_name
)
  
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
uninstall
)
def
_IsWebViewProvider
(
apk_helper_instance
)
:
  
meta_data
=
apk_helper_instance
.
GetAllMetadata
(
)
  
meta_data_keys
=
[
pair
[
0
]
for
pair
in
meta_data
]
  
return
'
com
.
android
.
webview
.
WebViewLibrary
'
in
meta_data_keys
def
_SetWebViewProvider
(
devices
package_name
)
:
  
def
switch_provider
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
      
logging
.
error
(
'
No
need
to
switch
provider
on
pre
-
Nougat
devices
(
%
s
)
'
                    
device
.
serial
)
    
else
:
      
device
.
SetWebViewImplementation
(
package_name
)
  
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
switch_provider
)
def
_NormalizeProcessName
(
debug_process_name
package_name
)
:
  
if
not
debug_process_name
:
    
debug_process_name
=
package_name
  
elif
debug_process_name
.
startswith
(
'
:
'
)
:
    
debug_process_name
=
package_name
+
debug_process_name
  
elif
'
.
'
not
in
debug_process_name
:
    
debug_process_name
=
package_name
+
'
:
'
+
debug_process_name
  
return
debug_process_name
def
_LaunchUrl
(
devices
package_name
argv
=
None
command_line_flags_file
=
None
               
url
=
None
apk
=
None
wait_for_java_debugger
=
False
               
debug_process_name
=
None
nokill
=
None
)
:
  
if
argv
and
command_line_flags_file
is
None
:
    
raise
Exception
(
'
This
apk
does
not
support
any
flags
.
'
)
  
if
url
:
    
if
not
apk
:
      
raise
Exception
(
'
Launching
with
URL
is
not
supported
when
using
'
                      
'
-
-
package
-
name
.
Use
-
-
apk
-
path
instead
.
'
)
    
view_activity
=
apk
.
GetViewActivityName
(
)
    
if
not
view_activity
:
      
raise
Exception
(
'
APK
does
not
support
launching
with
URLs
.
'
)
  
debug_process_name
=
_NormalizeProcessName
(
debug_process_name
package_name
)
  
def
launch
(
device
)
:
    
if
not
nokill
:
      
cmd
=
[
'
am
'
'
set
-
debug
-
app
'
'
-
-
persistent
'
debug_process_name
]
      
if
wait_for_java_debugger
:
        
cmd
[
-
1
:
-
1
]
=
[
'
-
w
'
]
      
device
.
RunShellCommand
(
cmd
check_return
=
False
)
      
if
command_line_flags_file
:
        
changer
=
flag_changer
.
FlagChanger
(
device
command_line_flags_file
)
        
flags
=
[
]
        
if
argv
:
          
adb_command_line
.
CheckBuildTypeSupportsFlags
(
device
                                                       
command_line_flags_file
)
          
flags
=
shlex
.
split
(
argv
)
        
try
:
          
changer
.
ReplaceFlags
(
flags
)
        
except
device_errors
.
AdbShellCommandFailedError
:
          
logging
.
exception
(
'
Failed
to
set
flags
'
)
    
if
url
is
None
:
      
cmd
=
[
          
'
am
'
'
start
'
'
-
p
'
package_name
'
-
c
'
          
'
android
.
intent
.
category
.
LAUNCHER
'
'
-
a
'
'
android
.
intent
.
action
.
MAIN
'
      
]
      
device
.
RunShellCommand
(
cmd
check_return
=
True
)
    
else
:
      
launch_intent
=
intent
.
Intent
(
action
=
'
android
.
intent
.
action
.
VIEW
'
                                    
activity
=
view_activity
data
=
url
                                    
package
=
package_name
)
      
device
.
StartActivity
(
launch_intent
)
  
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
launch
)
  
if
wait_for_java_debugger
:
    
print
(
'
Waiting
for
debugger
to
attach
to
process
:
'
+
          
_Colorize
(
debug_process_name
colorama
.
Fore
.
YELLOW
)
)
def
_ChangeFlags
(
devices
argv
command_line_flags_file
)
:
  
if
argv
is
None
:
    
_DisplayArgs
(
devices
command_line_flags_file
)
  
else
:
    
flags
=
shlex
.
split
(
argv
)
    
def
update
(
device
)
:
      
adb_command_line
.
CheckBuildTypeSupportsFlags
(
device
                                                   
command_line_flags_file
)
      
changer
=
flag_changer
.
FlagChanger
(
device
command_line_flags_file
)
      
changer
.
ReplaceFlags
(
flags
)
    
device_utils
.
DeviceUtils
.
parallel
(
devices
)
.
pMap
(
update
)
def
_TargetCpuToTargetArch
(
target_cpu
)
:
  
if
target_cpu
=
=
'
x64
'
:
    
return
'
x86_64
'
  
if
target_cpu
=
=
'
mipsel
'
:
    
return
'
mips
'
  
return
target_cpu
def
_RunGdb
(
device
package_name
debug_process_name
pid
output_directory
            
target_cpu
port
ide
verbose
)
:
  
if
not
pid
:
    
debug_process_name
=
_NormalizeProcessName
(
debug_process_name
package_name
)
    
pid
=
device
.
GetApplicationPids
(
debug_process_name
at_most_one
=
True
)
  
if
not
pid
:
    
raise
Exception
(
'
App
not
running
.
'
)
  
gdb_script_path
=
os
.
path
.
dirname
(
__file__
)
+
'
/
adb_gdb
'
  
cmd
=
[
      
gdb_script_path
      
'
-
-
package
-
name
=
%
s
'
%
package_name
      
'
-
-
output
-
directory
=
%
s
'
%
output_directory
      
'
-
-
adb
=
%
s
'
%
adb_wrapper
.
AdbWrapper
.
GetAdbPath
(
)
      
'
-
-
device
=
%
s
'
%
device
.
serial
      
'
-
-
pid
=
%
s
'
%
pid
      
'
-
-
port
=
%
d
'
%
port
  
]
  
if
ide
:
    
cmd
.
append
(
'
-
-
ide
'
)
  
if
verbose
:
    
cmd
.
append
(
'
-
-
verbose
'
)
  
if
target_cpu
:
    
cmd
.
append
(
'
-
-
target
-
arch
=
%
s
'
%
_TargetCpuToTargetArch
(
target_cpu
)
)
  
logging
.
warning
(
'
Running
:
%
s
'
'
'
.
join
(
pipes
.
quote
(
x
)
for
x
in
cmd
)
)
  
print
(
_Colorize
(
'
All
subsequent
output
is
from
adb_gdb
script
.
'
                  
colorama
.
Fore
.
YELLOW
)
)
  
os
.
execv
(
gdb_script_path
cmd
)
def
_PrintPerDeviceOutput
(
devices
results
single_line
=
False
)
:
  
for
d
result
in
zip
(
devices
results
)
:
    
if
not
single_line
and
d
is
not
devices
[
0
]
:
      
sys
.
stdout
.
write
(
'
\
n
'
)
    
sys
.
stdout
.
write
(
          
_Colorize
(
'
{
}
(
{
}
)
:
'
.
format
(
d
d
.
build_description
)
                    
colorama
.
Fore
.
YELLOW
)
)
    
sys
.
stdout
.
write
(
'
'
if
single_line
else
'
\
n
'
)
    
yield
result
def
_RunMemUsage
(
devices
package_name
query_app
=
False
)
:
  
cmd_args
=
[
'
dumpsys
'
'
meminfo
'
]
  
if
not
query_app
:
    
cmd_args
.
append
(
'
-
-
local
'
)
  
def
mem_usage_helper
(
d
)
:
    
ret
=
[
]
    
for
process
in
sorted
(
_GetPackageProcesses
(
d
package_name
)
)
:
      
meminfo
=
d
.
RunShellCommand
(
cmd_args
+
[
str
(
process
.
pid
)
]
)
      
ret
.
append
(
(
process
.
name
'
\
n
'
.
join
(
meminfo
)
)
)
    
return
ret
  
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
all_results
=
parallel_devices
.
pMap
(
mem_usage_helper
)
.
pGet
(
None
)
  
for
result
in
_PrintPerDeviceOutput
(
devices
all_results
)
:
    
if
not
result
:
      
print
(
'
No
processes
found
.
'
)
    
else
:
      
for
name
usage
in
sorted
(
result
)
:
        
print
(
_Colorize
(
'
=
=
=
=
Output
of
"
dumpsys
meminfo
%
s
"
=
=
=
=
'
%
name
                        
colorama
.
Fore
.
GREEN
)
)
        
print
(
usage
)
def
_DuHelper
(
device
path_spec
run_as
=
None
)
:
  
"
"
"
Runs
"
du
-
s
-
k
|
path_spec
|
"
on
|
device
|
and
returns
parsed
result
.
  
Args
:
    
device
:
A
DeviceUtils
instance
.
    
path_spec
:
The
list
of
paths
to
run
du
on
.
May
contain
shell
expansions
        
(
will
not
be
escaped
)
.
    
run_as
:
Package
name
to
run
as
or
None
to
run
as
shell
user
.
If
not
None
        
and
app
is
not
android
:
debuggable
(
run
-
as
fails
)
then
command
will
be
        
run
as
root
.
  
Returns
:
    
A
dict
of
path
-
>
size
in
KiB
containing
all
paths
in
|
path_spec
|
that
exist
    
on
device
.
Paths
that
do
not
exist
are
silently
ignored
.
  
"
"
"
  
cmd_str
=
'
du
-
s
-
k
'
+
path_spec
+
'
2
>
&
1
'
  
lines
=
device
.
RunShellCommand
(
cmd_str
run_as
=
run_as
shell
=
True
                                 
check_return
=
False
)
  
output
=
'
\
n
'
.
join
(
lines
)
  
if
output
.
startswith
(
'
run
-
as
:
'
)
:
    
lines
=
device
.
RunShellCommand
(
cmd_str
as_root
=
True
shell
=
True
                                   
check_return
=
False
)
  
ret
=
{
}
  
try
:
    
for
line
in
lines
:
      
if
line
.
startswith
(
'
du
:
'
)
:
        
continue
      
size
subpath
=
line
.
split
(
None
1
)
      
ret
[
subpath
]
=
int
(
size
)
    
return
ret
  
except
ValueError
:
    
logging
.
error
(
'
du
command
was
:
%
s
'
cmd_str
)
    
logging
.
error
(
'
Failed
to
parse
du
output
:
\
n
%
s
'
output
)
    
raise
def
_RunDiskUsage
(
devices
package_name
)
:
  
def
disk_usage_helper
(
d
)
:
    
package_output
=
'
\
n
'
.
join
(
d
.
RunShellCommand
(
        
[
'
dumpsys
'
'
package
'
package_name
]
check_return
=
True
)
)
    
if
not
package_output
or
'
Unable
to
find
package
:
'
in
package_output
:
      
return
None
    
package_output
=
re
.
sub
(
r
'
Hidden
system
packages
:
.
*
?
^
\
b
'
'
'
                            
package_output
flags
=
re
.
S
|
re
.
M
)
    
try
:
      
data_dir
=
re
.
search
(
r
'
dataDir
=
(
.
*
)
'
package_output
)
.
group
(
1
)
      
code_path
=
re
.
search
(
r
'
codePath
=
(
.
*
)
'
package_output
)
.
group
(
1
)
      
lib_path
=
re
.
search
(
r
'
(
?
:
legacyN
|
n
)
ativeLibrary
(
?
:
Dir
|
Path
)
=
(
.
*
)
'
                           
package_output
)
.
group
(
1
)
    
except
AttributeError
:
      
raise
Exception
(
'
Error
parsing
dumpsys
output
:
'
+
package_output
)
    
if
code_path
.
startswith
(
'
/
system
'
)
:
      
logging
.
warning
(
'
Measurement
of
system
image
apks
can
be
innacurate
'
)
    
compilation_filters
=
set
(
)
    
awful_wrapping
=
r
'
\
s
*
'
.
join
(
'
compilation_filter
=
'
)
    
for
m
in
re
.
finditer
(
awful_wrapping
+
r
'
(
[
\
s
\
S
]
+
?
)
[
\
]
]
'
package_output
)
:
      
compilation_filters
.
add
(
re
.
sub
(
r
'
\
s
+
'
'
'
m
.
group
(
1
)
)
)
    
for
m
in
re
.
finditer
(
r
'
\
[
status
=
(
.
+
?
)
\
]
'
package_output
)
:
      
compilation_filters
.
add
(
m
.
group
(
1
)
)
    
compilation_filter
=
'
'
.
join
(
sorted
(
compilation_filters
)
)
    
data_dir_sizes
=
_DuHelper
(
d
'
%
s
/
{
*
.
*
}
'
%
data_dir
run_as
=
package_name
)
    
code_cache_sizes
=
{
}
    
code_cache_dir
=
next
(
        
(
k
for
k
in
data_dir_sizes
if
k
.
endswith
(
'
/
code_cache
'
)
)
None
)
    
if
code_cache_dir
:
      
data_dir_sizes
.
pop
(
code_cache_dir
)
      
code_cache_sizes
=
_DuHelper
(
d
'
%
s
/
{
*
.
*
}
'
%
code_cache_dir
                                   
run_as
=
package_name
)
    
apk_path_spec
=
code_path
    
if
not
apk_path_spec
.
endswith
(
'
.
apk
'
)
:
      
apk_path_spec
+
=
'
/
*
.
apk
'
    
apk_sizes
=
_DuHelper
(
d
apk_path_spec
)
    
if
lib_path
.
endswith
(
'
/
lib
'
)
:
      
lib_sizes
=
_DuHelper
(
d
'
%
s
/
{
*
.
*
}
'
%
lib_path
)
    
else
:
      
lib_sizes
=
_DuHelper
(
d
lib_path
)
    
odex_paths
=
[
]
    
for
apk_path
in
apk_sizes
:
      
mangled_apk_path
=
apk_path
[
1
:
]
.
replace
(
'
/
'
'
'
)
      
apk_basename
=
posixpath
.
basename
(
apk_path
)
[
:
-
4
]
      
for
ext
in
(
'
dex
'
'
odex
'
'
vdex
'
'
art
'
)
:
        
for
arch
in
(
'
arm
'
'
arm64
'
'
x86
'
'
x86_64
'
'
mips
'
'
mips64
'
)
:
          
odex_paths
.
append
(
              
'
%
s
/
oat
/
%
s
/
%
s
.
%
s
'
%
(
code_path
arch
apk_basename
ext
)
)
          
for
suffix
in
(
'
'
'
2
'
'
3
'
'
4
'
'
5
'
)
:
            
odex_paths
.
append
(
'
/
data
/
dalvik
-
cache
/
%
s
/
%
s
classes
%
s
.
%
s
'
%
(
                
arch
mangled_apk_path
suffix
ext
)
)
            
if
arch
=
=
'
arm
'
:
              
odex_paths
.
append
(
'
/
data
/
dalvik
-
cache
/
%
s
classes
%
s
.
dex
'
%
(
                  
mangled_apk_path
suffix
)
)
    
odex_sizes
=
_DuHelper
(
d
'
'
.
join
(
pipes
.
quote
(
p
)
for
p
in
odex_paths
)
)
    
return
(
data_dir_sizes
code_cache_sizes
apk_sizes
lib_sizes
odex_sizes
            
compilation_filter
)
  
def
print_sizes
(
desc
sizes
)
:
    
print
(
'
%
s
:
%
d
KiB
'
%
(
desc
sum
(
sizes
.
values
(
)
)
)
)
    
for
path
size
in
sorted
(
sizes
.
items
(
)
)
:
      
print
(
'
%
s
:
%
s
KiB
'
%
(
path
size
)
)
  
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
all_results
=
parallel_devices
.
pMap
(
disk_usage_helper
)
.
pGet
(
None
)
  
for
result
in
_PrintPerDeviceOutput
(
devices
all_results
)
:
    
if
not
result
:
      
print
(
'
APK
is
not
installed
.
'
)
      
continue
    
(
data_dir_sizes
code_cache_sizes
apk_sizes
lib_sizes
odex_sizes
     
compilation_filter
)
=
result
    
total
=
sum
(
sum
(
sizes
.
values
(
)
)
for
sizes
in
result
[
:
-
1
]
)
    
print_sizes
(
'
Apk
'
apk_sizes
)
    
print_sizes
(
'
App
Data
(
non
-
code
cache
)
'
data_dir_sizes
)
    
print_sizes
(
'
App
Data
(
code
cache
)
'
code_cache_sizes
)
    
print_sizes
(
'
Native
Libs
'
lib_sizes
)
    
show_warning
=
compilation_filter
and
'
speed
'
not
in
compilation_filter
    
compilation_filter
=
compilation_filter
or
'
n
/
a
'
    
print_sizes
(
'
odex
(
compilation_filter
=
%
s
)
'
%
compilation_filter
odex_sizes
)
    
if
show_warning
:
      
logging
.
warning
(
'
For
a
more
realistic
odex
size
run
:
'
)
      
logging
.
warning
(
'
%
s
compile
-
dex
[
speed
|
speed
-
profile
]
'
sys
.
argv
[
0
]
)
    
print
(
'
Total
:
%
s
KiB
(
%
.
1f
MiB
)
'
%
(
total
total
/
1024
.
0
)
)
class
_LogcatProcessor
(
object
)
:
  
ParsedLine
=
collections
.
namedtuple
(
      
'
ParsedLine
'
      
[
'
date
'
'
invokation_time
'
'
pid
'
'
tid
'
'
priority
'
'
tag
'
'
message
'
]
)
  
class
NativeStackSymbolizer
(
object
)
:
    
"
"
"
Buffers
lines
from
native
stacks
and
symbolizes
them
when
done
.
"
"
"
    
_STACK_PATTERN
=
re
.
compile
(
r
'
\
s
*
#
\
d
+
\
s
+
(
?
:
pc
)
?
(
0x
)
?
[
0
-
9a
-
f
]
{
8
16
}
\
s
'
)
    
def
__init__
(
self
stack_script_context
print_func
)
:
      
self
.
_stack_script_context
=
stack_script_context
      
self
.
_print_func
=
print_func
      
self
.
_crash_lines_buffer
=
None
    
def
_FlushLines
(
self
)
:
      
"
"
"
Prints
queued
lines
after
sending
them
through
stack
.
py
.
"
"
"
      
crash_lines
=
self
.
_crash_lines_buffer
      
self
.
_crash_lines_buffer
=
None
      
with
tempfile
.
NamedTemporaryFile
(
mode
=
'
w
'
)
as
f
:
        
f
.
writelines
(
x
[
0
]
.
message
+
'
\
n
'
for
x
in
crash_lines
)
        
f
.
flush
(
)
        
proc
=
self
.
_stack_script_context
.
Popen
(
            
input_file
=
f
.
name
stdout
=
subprocess
.
PIPE
)
        
lines
=
proc
.
communicate
(
)
[
0
]
.
splitlines
(
)
      
for
i
line
in
enumerate
(
lines
)
:
        
parsed_line
dim
=
crash_lines
[
min
(
i
len
(
crash_lines
)
-
1
)
]
        
d
=
parsed_line
.
_asdict
(
)
        
d
[
'
message
'
]
=
line
        
parsed_line
=
_LogcatProcessor
.
ParsedLine
(
*
*
d
)
        
self
.
_print_func
(
parsed_line
dim
)
    
def
AddLine
(
self
parsed_line
dim
)
:
      
is_crash_line
=
parsed_line
.
tag
=
=
'
DEBUG
'
or
(
self
.
_STACK_PATTERN
.
match
(
          
parsed_line
.
message
)
)
      
if
is_crash_line
:
        
if
self
.
_crash_lines_buffer
is
None
:
          
self
.
_crash_lines_buffer
=
[
]
        
self
.
_crash_lines_buffer
.
append
(
(
parsed_line
dim
)
)
        
return
      
if
self
.
_crash_lines_buffer
is
not
None
:
        
self
.
_FlushLines
(
)
      
self
.
_print_func
(
parsed_line
dim
)
  
_ALLOWLISTED_TAGS
=
{
      
'
ActivityManager
'
      
'
ActivityTaskManager
'
      
'
AndroidRuntime
'
      
'
DEBUG
'
  
}
  
_DALVIK_IGNORE_PATTERN
=
re
.
compile
(
'
|
'
.
join
(
[
      
r
'
^
Added
shared
lib
'
      
r
'
^
Could
not
find
'
      
r
'
^
DexOpt
:
'
      
r
'
^
GC_
'
      
r
'
^
Late
-
enabling
CheckJNI
'
      
r
'
^
Link
of
class
'
      
r
'
^
No
JNI_OnLoad
found
in
'
      
r
'
^
Trying
to
load
lib
'
      
r
'
^
Unable
to
resolve
superclass
'
      
r
'
^
VFY
:
'
      
r
'
^
WAIT_
'
  
]
)
)
  
def
__init__
(
self
               
device
               
package_name
               
stack_script_context
               
deobfuscate
=
None
               
verbose
=
False
)
:
    
self
.
_device
=
device
    
self
.
_package_name
=
package_name
    
self
.
_verbose
=
verbose
    
self
.
_deobfuscator
=
deobfuscate
    
self
.
_native_stack_symbolizer
=
_LogcatProcessor
.
NativeStackSymbolizer
(
        
stack_script_context
self
.
_PrintParsedLine
)
    
self
.
_primary_pid
=
None
    
self
.
_my_pids
=
set
(
)
    
self
.
_seen_pids
=
set
(
)
    
self
.
_pid_pattern
=
re
.
compile
(
r
'
Start
proc
(
\
d
+
)
:
{
}
/
'
.
format
(
package_name
)
)
    
self
.
_start_pattern
=
re
.
compile
(
r
'
START
.
*
pkg
=
'
+
package_name
)
    
self
.
nonce
=
'
Chromium
apk_operations
.
py
nonce
=
{
}
'
.
format
(
random
.
random
(
)
)
    
self
.
_initial_buffered_lines
=
[
]
    
self
.
_UpdateMyPids
(
)
    
self
.
_found_initial_pid
=
self
.
_primary_pid
!
=
None
    
self
.
_user_defined_highlight
=
None
    
user_regex
=
os
.
environ
.
get
(
'
CHROMIUM_LOGCAT_HIGHLIGHT
'
)
    
if
user_regex
:
      
self
.
_user_defined_highlight
=
re
.
compile
(
user_regex
)
      
if
not
self
.
_user_defined_highlight
:
        
print
(
_Colorize
(
            
'
Rejecting
invalid
regular
expression
:
{
}
'
.
format
(
user_regex
)
            
colorama
.
Fore
.
RED
+
colorama
.
Style
.
BRIGHT
)
)
  
def
_UpdateMyPids
(
self
)
:
    
self
.
_primary_pid
=
None
    
for
process
in
_GetPackageProcesses
(
self
.
_device
self
.
_package_name
)
:
      
if
'
:
'
not
in
process
.
name
and
self
.
_primary_pid
is
None
:
        
self
.
_primary_pid
=
process
.
pid
      
self
.
_my_pids
.
add
(
process
.
pid
)
  
def
_GetPidStyle
(
self
pid
dim
=
False
)
:
    
if
pid
=
=
self
.
_primary_pid
:
      
return
colorama
.
Fore
.
WHITE
    
elif
pid
in
self
.
_my_pids
:
      
return
colorama
.
Fore
.
YELLOW
    
elif
dim
:
      
return
colorama
.
Style
.
DIM
    
return
'
'
  
def
_GetPriorityStyle
(
self
priority
dim
=
False
)
:
    
if
dim
:
      
return
'
'
    
style
=
colorama
.
Fore
.
BLACK
    
if
priority
=
=
'
E
'
or
priority
=
=
'
F
'
:
      
style
+
=
colorama
.
Back
.
RED
    
elif
priority
=
=
'
W
'
:
      
style
+
=
colorama
.
Back
.
YELLOW
    
elif
priority
=
=
'
I
'
:
      
style
+
=
colorama
.
Back
.
GREEN
    
elif
priority
=
=
'
D
'
:
      
style
+
=
colorama
.
Back
.
BLUE
    
return
style
  
def
_ParseLine
(
self
line
)
:
    
tokens
=
line
.
split
(
None
6
)
    
def
consume_token_or_default
(
default
)
:
      
return
tokens
.
pop
(
0
)
if
len
(
tokens
)
>
0
else
default
    
def
consume_integer_token_or_default
(
default
)
:
      
if
len
(
tokens
)
=
=
0
:
        
return
default
      
try
:
        
return
int
(
tokens
.
pop
(
0
)
)
      
except
ValueError
:
        
return
default
    
date
=
consume_token_or_default
(
'
'
)
    
invokation_time
=
consume_token_or_default
(
'
'
)
    
pid
=
consume_integer_token_or_default
(
-
1
)
    
tid
=
consume_integer_token_or_default
(
-
1
)
    
priority
=
consume_token_or_default
(
'
'
)
    
tag
=
consume_token_or_default
(
'
'
)
    
original_message
=
consume_token_or_default
(
'
'
)
    
if
tag
and
tag
[
-
1
]
=
=
'
:
'
:
      
tag
=
tag
[
:
-
1
]
    
elif
len
(
original_message
)
>
2
:
      
original_message
=
original_message
[
2
:
]
    
return
self
.
ParsedLine
(
        
date
invokation_time
pid
tid
priority
tag
original_message
)
  
def
_PrintParsedLine
(
self
parsed_line
dim
=
False
)
:
    
tid_style
=
colorama
.
Style
.
NORMAL
    
user_match
=
self
.
_user_defined_highlight
and
(
        
re
.
search
(
self
.
_user_defined_highlight
parsed_line
.
tag
)
        
or
re
.
search
(
self
.
_user_defined_highlight
parsed_line
.
message
)
)
    
if
not
dim
and
parsed_line
.
pid
=
=
parsed_line
.
tid
:
      
tid_style
=
colorama
.
Style
.
BRIGHT
    
pid_style
=
self
.
_GetPidStyle
(
parsed_line
.
pid
dim
)
    
msg_style
=
pid_style
if
not
user_match
else
(
colorama
.
Fore
.
GREEN
+
                                                  
colorama
.
Style
.
BRIGHT
)
    
pid_str
=
_Colorize
(
'
{
:
5
}
'
.
format
(
parsed_line
.
pid
)
pid_style
)
    
tid_str
=
_Colorize
(
'
{
:
5
}
'
.
format
(
parsed_line
.
tid
)
tid_style
)
    
tag
=
_Colorize
(
'
{
:
8
}
'
.
format
(
parsed_line
.
tag
)
                    
pid_style
+
(
'
'
if
dim
else
colorama
.
Style
.
BRIGHT
)
)
    
priority
=
_Colorize
(
parsed_line
.
priority
                         
self
.
_GetPriorityStyle
(
parsed_line
.
priority
)
)
    
messages
=
[
parsed_line
.
message
]
    
if
self
.
_deobfuscator
:
      
messages
=
self
.
_deobfuscator
.
TransformLines
(
messages
)
    
for
message
in
messages
:
      
message
=
_Colorize
(
message
msg_style
)
      
sys
.
stdout
.
write
(
'
{
}
{
}
{
}
{
}
{
}
{
}
:
{
}
\
n
'
.
format
(
          
parsed_line
.
date
parsed_line
.
invokation_time
pid_str
tid_str
          
priority
tag
message
)
)
  
def
_TriggerNonceFound
(
self
)
:
    
if
self
.
_primary_pid
:
      
for
args
in
self
.
_initial_buffered_lines
:
        
self
.
_native_stack_symbolizer
.
AddLine
(
*
args
)
    
self
.
_initial_buffered_lines
=
None
    
self
.
nonce
=
None
  
def
ProcessLine
(
self
line
)
:
    
if
not
line
or
line
.
startswith
(
'
-
-
-
-
-
-
'
)
:
      
return
    
if
self
.
nonce
and
self
.
nonce
in
line
:
      
self
.
_TriggerNonceFound
(
)
    
nonce_found
=
self
.
nonce
is
None
    
log
=
self
.
_ParseLine
(
line
)
    
if
log
.
pid
not
in
self
.
_seen_pids
:
      
self
.
_seen_pids
.
add
(
log
.
pid
)
      
if
nonce_found
:
        
self
.
_UpdateMyPids
(
)
    
if
not
nonce_found
:
      
if
self
.
_start_pattern
.
match
(
log
.
message
)
:
        
self
.
_initial_buffered_lines
=
[
]
      
if
not
self
.
_found_initial_pid
:
        
m
=
self
.
_pid_pattern
.
match
(
log
.
message
)
        
if
m
:
          
self
.
_primary_pid
=
m
.
group
(
1
)
          
self
.
_my_pids
.
clear
(
)
          
self
.
_my_pids
.
add
(
m
.
group
(
1
)
)
    
owned_pid
=
log
.
pid
in
self
.
_my_pids
    
if
owned_pid
and
not
self
.
_verbose
and
log
.
tag
=
=
'
dalvikvm
'
:
      
if
self
.
_DALVIK_IGNORE_PATTERN
.
match
(
log
.
message
)
:
        
return
    
if
owned_pid
or
self
.
_verbose
or
(
log
.
priority
=
=
'
F
'
or
                                      
log
.
tag
in
self
.
_ALLOWLISTED_TAGS
)
:
      
if
nonce_found
:
        
self
.
_native_stack_symbolizer
.
AddLine
(
log
not
owned_pid
)
      
else
:
        
self
.
_initial_buffered_lines
.
append
(
(
log
not
owned_pid
)
)
def
_RunLogcat
(
device
package_name
stack_script_context
deobfuscate
               
verbose
)
:
  
logcat_processor
=
_LogcatProcessor
(
      
device
package_name
stack_script_context
deobfuscate
verbose
)
  
device
.
RunShellCommand
(
[
'
log
'
logcat_processor
.
nonce
]
)
  
for
line
in
device
.
adb
.
Logcat
(
logcat_format
=
'
threadtime
'
)
:
    
try
:
      
logcat_processor
.
ProcessLine
(
line
)
    
except
:
      
sys
.
stderr
.
write
(
'
Failed
to
process
line
:
'
+
line
+
'
\
n
'
)
      
if
'
unexpected
EOF
'
in
line
:
        
sys
.
exit
(
1
)
      
raise
def
_GetPackageProcesses
(
device
package_name
)
:
  
return
[
      
p
for
p
in
device
.
ListProcesses
(
package_name
)
      
if
p
.
name
=
=
package_name
or
p
.
name
.
startswith
(
package_name
+
'
:
'
)
]
def
_RunPs
(
devices
package_name
)
:
  
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
all_processes
=
parallel_devices
.
pMap
(
      
lambda
d
:
_GetPackageProcesses
(
d
package_name
)
)
.
pGet
(
None
)
  
for
processes
in
_PrintPerDeviceOutput
(
devices
all_processes
)
:
    
if
not
processes
:
      
print
(
'
No
processes
found
.
'
)
    
else
:
      
proc_map
=
collections
.
defaultdict
(
list
)
      
for
p
in
processes
:
        
proc_map
[
p
.
name
]
.
append
(
str
(
p
.
pid
)
)
      
for
name
pids
in
sorted
(
proc_map
.
items
(
)
)
:
        
print
(
name
'
'
.
join
(
pids
)
)
def
_RunShell
(
devices
package_name
cmd
)
:
  
if
cmd
:
    
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
    
outputs
=
parallel_devices
.
RunShellCommand
(
        
cmd
run_as
=
package_name
)
.
pGet
(
None
)
    
for
output
in
_PrintPerDeviceOutput
(
devices
outputs
)
:
      
for
line
in
output
:
        
print
(
line
)
  
else
:
    
adb_path
=
adb_wrapper
.
AdbWrapper
.
GetAdbPath
(
)
    
cmd
=
[
adb_path
'
-
s
'
devices
[
0
]
.
serial
'
shell
'
]
    
if
devices
[
0
]
.
build_version_sdk
>
=
version_codes
.
NOUGAT
:
      
cmd
+
=
[
'
-
t
'
'
run
-
as
'
package_name
]
    
else
:
      
print
(
'
Upon
entering
the
shell
run
:
'
)
      
print
(
'
run
-
as
'
package_name
)
      
print
(
)
    
os
.
execv
(
adb_path
cmd
)
def
_RunCompileDex
(
devices
package_name
compilation_filter
)
:
  
cmd
=
[
'
cmd
'
'
package
'
'
compile
'
'
-
f
'
'
-
m
'
compilation_filter
         
package_name
]
  
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
outputs
=
parallel_devices
.
RunShellCommand
(
cmd
timeout
=
120
)
.
pGet
(
None
)
  
for
output
in
_PrintPerDeviceOutput
(
devices
outputs
)
:
    
for
line
in
output
:
      
print
(
line
)
def
_RunProfile
(
device
package_name
host_build_directory
pprof_out_path
                
process_specifier
thread_specifier
extra_args
)
:
  
simpleperf
.
PrepareDevice
(
device
)
  
device_simpleperf_path
=
simpleperf
.
InstallSimpleperf
(
device
package_name
)
  
with
tempfile
.
NamedTemporaryFile
(
)
as
fh
:
    
host_simpleperf_out_path
=
fh
.
name
    
with
simpleperf
.
RunSimpleperf
(
device
device_simpleperf_path
package_name
                                  
process_specifier
thread_specifier
                                  
extra_args
host_simpleperf_out_path
)
:
      
sys
.
stdout
.
write
(
'
Profiler
is
running
;
press
Enter
to
stop
.
.
.
'
)
      
sys
.
stdin
.
read
(
1
)
      
sys
.
stdout
.
write
(
'
Post
-
processing
data
.
.
.
'
)
      
sys
.
stdout
.
flush
(
)
    
simpleperf
.
ConvertSimpleperfToPprof
(
host_simpleperf_out_path
                                        
host_build_directory
pprof_out_path
)
    
print
(
textwrap
.
dedent
(
"
"
"
        
Profile
data
written
to
%
(
s
)
s
.
        
To
view
profile
as
a
call
graph
in
browser
:
          
pprof
-
web
%
(
s
)
s
        
To
print
the
hottest
methods
:
          
pprof
-
top
%
(
s
)
s
        
pprof
has
many
useful
customization
options
;
pprof
-
-
help
for
details
.
        
"
"
"
%
{
'
s
'
:
pprof_out_path
}
)
)
class
_StackScriptContext
(
object
)
:
  
"
"
"
Maintains
temporary
files
needed
by
stack
.
py
.
"
"
"
  
def
__init__
(
self
               
output_directory
               
apk_path
               
bundle_generation_info
               
quiet
=
False
)
:
    
self
.
_output_directory
=
output_directory
    
self
.
_apk_path
=
apk_path
    
self
.
_bundle_generation_info
=
bundle_generation_info
    
self
.
_staging_dir
=
None
    
self
.
_quiet
=
quiet
  
def
_CreateStaging
(
self
)
:
    
logging
.
debug
(
'
Creating
stack
staging
directory
'
)
    
self
.
_staging_dir
=
tempfile
.
mkdtemp
(
)
    
bundle_generation_info
=
self
.
_bundle_generation_info
    
if
bundle_generation_info
:
      
_GenerateBundleApks
(
bundle_generation_info
)
      
logging
.
debug
(
'
Extracting
.
apks
file
'
)
      
with
zipfile
.
ZipFile
(
bundle_generation_info
.
bundle_apks_path
'
r
'
)
as
z
:
        
files_to_extract
=
[
            
f
for
f
in
z
.
namelist
(
)
if
f
.
endswith
(
'
-
master
.
apk
'
)
        
]
        
z
.
extractall
(
self
.
_staging_dir
files_to_extract
)
    
elif
self
.
_apk_path
:
      
output
=
os
.
path
.
join
(
self
.
_staging_dir
os
.
path
.
basename
(
self
.
_apk_path
)
)
      
os
.
symlink
(
self
.
_apk_path
output
)
  
def
Close
(
self
)
:
    
if
self
.
_staging_dir
:
      
logging
.
debug
(
'
Clearing
stack
staging
directory
'
)
      
shutil
.
rmtree
(
self
.
_staging_dir
)
      
self
.
_staging_dir
=
None
  
def
Popen
(
self
input_file
=
None
*
*
kwargs
)
:
    
if
self
.
_staging_dir
is
None
:
      
self
.
_CreateStaging
(
)
    
stack_script
=
os
.
path
.
join
(
        
constants
.
host_paths
.
ANDROID_PLATFORM_DEVELOPMENT_SCRIPTS_PATH
        
'
stack
.
py
'
)
    
cmd
=
[
        
stack_script
'
-
-
output
-
directory
'
self
.
_output_directory
        
'
-
-
apks
-
directory
'
self
.
_staging_dir
    
]
    
if
self
.
_quiet
:
      
cmd
.
append
(
'
-
-
quiet
'
)
    
if
input_file
:
      
cmd
.
append
(
input_file
)
    
logging
.
info
(
'
Running
stack
.
py
'
)
    
return
subprocess
.
Popen
(
cmd
universal_newlines
=
True
*
*
kwargs
)
def
_GenerateAvailableDevicesMessage
(
devices
)
:
  
devices_obj
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
descriptions
=
devices_obj
.
pMap
(
lambda
d
:
d
.
build_description
)
.
pGet
(
None
)
  
msg
=
'
Available
devices
:
\
n
'
  
for
d
desc
in
zip
(
devices
descriptions
)
:
    
msg
+
=
'
%
s
(
%
s
)
\
n
'
%
(
d
desc
)
  
return
msg
def
_GenerateMissingAllFlagMessage
(
devices
)
:
  
return
(
'
More
than
one
device
available
.
Use
-
-
all
to
select
all
devices
'
+
          
'
or
use
-
-
device
to
select
a
device
by
serial
.
\
n
\
n
'
+
          
_GenerateAvailableDevicesMessage
(
devices
)
)
def
_DisplayArgs
(
devices
command_line_flags_file
)
:
  
def
flags_helper
(
d
)
:
    
changer
=
flag_changer
.
FlagChanger
(
d
command_line_flags_file
)
    
return
changer
.
GetCurrentFlags
(
)
  
parallel_devices
=
device_utils
.
DeviceUtils
.
parallel
(
devices
)
  
outputs
=
parallel_devices
.
pMap
(
flags_helper
)
.
pGet
(
None
)
  
print
(
'
Existing
flags
per
-
device
(
via
/
data
/
local
/
tmp
/
{
}
)
:
'
.
format
(
      
command_line_flags_file
)
)
  
for
flags
in
_PrintPerDeviceOutput
(
devices
outputs
single_line
=
True
)
:
    
quoted_flags
=
'
'
.
join
(
pipes
.
quote
(
f
)
for
f
in
flags
)
    
print
(
quoted_flags
or
'
No
flags
set
.
'
)
def
_DeviceCachePath
(
device
output_directory
)
:
  
file_name
=
'
device_cache_
%
s
.
json
'
%
device
.
serial
  
return
os
.
path
.
join
(
output_directory
file_name
)
def
_LoadDeviceCaches
(
devices
output_directory
)
:
  
if
not
output_directory
:
    
return
  
for
d
in
devices
:
    
cache_path
=
_DeviceCachePath
(
d
output_directory
)
    
if
os
.
path
.
exists
(
cache_path
)
:
      
logging
.
debug
(
'
Using
device
cache
:
%
s
'
cache_path
)
      
with
open
(
cache_path
)
as
f
:
        
d
.
LoadCacheData
(
f
.
read
(
)
)
      
os
.
unlink
(
cache_path
)
    
else
:
      
logging
.
debug
(
'
No
cache
present
for
device
:
%
s
'
d
)
def
_SaveDeviceCaches
(
devices
output_directory
)
:
  
if
not
output_directory
:
    
return
  
for
d
in
devices
:
    
cache_path
=
_DeviceCachePath
(
d
output_directory
)
    
with
open
(
cache_path
'
w
'
)
as
f
:
      
f
.
write
(
d
.
DumpCacheData
(
)
)
      
logging
.
info
(
'
Wrote
device
cache
:
%
s
'
cache_path
)
class
_Command
(
object
)
:
  
name
=
None
  
description
=
None
  
long_description
=
None
  
needs_package_name
=
False
  
needs_output_directory
=
False
  
needs_apk_helper
=
False
  
supports_incremental
=
False
  
accepts_command_line_flags
=
False
  
accepts_args
=
False
  
need_device_args
=
True
  
all_devices_by_default
=
False
  
calls_exec
=
False
  
supports_multiple_devices
=
True
  
def
__init__
(
self
from_wrapper_script
is_bundle
)
:
    
self
.
_parser
=
None
    
self
.
_from_wrapper_script
=
from_wrapper_script
    
self
.
args
=
None
    
self
.
apk_helper
=
None
    
self
.
additional_apk_helpers
=
None
    
self
.
install_dict
=
None
    
self
.
devices
=
None
    
self
.
is_bundle
=
is_bundle
    
self
.
bundle_generation_info
=
None
    
if
is_bundle
or
not
from_wrapper_script
:
      
self
.
supports_incremental
=
False
  
def
RegisterBundleGenerationInfo
(
self
bundle_generation_info
)
:
    
self
.
bundle_generation_info
=
bundle_generation_info
  
def
_RegisterExtraArgs
(
self
subp
)
:
    
pass
  
def
RegisterArgs
(
self
parser
)
:
    
subp
=
parser
.
add_parser
(
        
self
.
name
help
=
self
.
description
        
description
=
self
.
long_description
or
self
.
description
        
formatter_class
=
argparse
.
RawDescriptionHelpFormatter
)
    
self
.
_parser
=
subp
    
subp
.
set_defaults
(
command
=
self
)
    
if
self
.
need_device_args
:
      
subp
.
add_argument
(
'
-
-
all
'
                        
action
=
'
store_true
'
                        
default
=
self
.
all_devices_by_default
                        
help
=
'
Operate
on
all
connected
devices
.
'
)
      
subp
.
add_argument
(
'
-
d
'
                        
'
-
-
device
'
                        
action
=
'
append
'
                        
default
=
[
]
                        
dest
=
'
devices
'
                        
help
=
'
Target
device
for
script
to
work
on
.
Enter
'
                            
'
multiple
times
for
multiple
devices
.
'
)
    
subp
.
add_argument
(
'
-
v
'
                      
'
-
-
verbose
'
                      
action
=
'
count
'
                      
default
=
0
                      
dest
=
'
verbose_count
'
                      
help
=
'
Verbose
level
(
multiple
times
for
more
)
'
)
    
group
=
subp
.
add_argument_group
(
'
%
s
arguments
'
%
self
.
name
)
    
if
self
.
needs_package_name
:
      
if
not
self
.
is_bundle
:
        
group
.
add_argument
(
            
'
-
-
package
-
name
'
            
help
=
argparse
.
SUPPRESS
if
self
.
_from_wrapper_script
else
(
                
"
App
'
s
package
name
.
"
)
)
    
if
self
.
needs_apk_helper
or
self
.
needs_package_name
:
      
if
not
self
.
_from_wrapper_script
and
not
self
.
is_bundle
:
        
group
.
add_argument
(
            
'
-
-
apk
-
path
'
required
=
self
.
needs_apk_helper
help
=
'
Path
to
.
apk
'
)
    
if
self
.
supports_incremental
:
      
group
.
add_argument
(
'
-
-
incremental
'
                          
action
=
'
store_true
'
                          
default
=
False
                          
help
=
'
Always
install
an
incremental
apk
.
'
)
      
group
.
add_argument
(
'
-
-
non
-
incremental
'
                          
action
=
'
store_true
'
                          
default
=
False
                          
help
=
'
Always
install
a
non
-
incremental
apk
.
'
)
    
if
self
.
accepts_command_line_flags
:
      
group
.
add_argument
(
          
'
-
-
args
'
help
=
'
Command
-
line
flags
.
Use
=
to
assign
args
.
'
)
    
if
self
.
accepts_args
:
      
group
.
add_argument
(
          
'
-
-
args
'
help
=
'
Extra
arguments
.
Use
=
to
assign
args
'
)
    
if
not
self
.
_from_wrapper_script
and
self
.
accepts_command_line_flags
:
      
group
.
add_argument
(
          
'
-
-
command
-
line
-
flags
-
file
'
          
help
=
'
Name
of
the
command
-
line
flags
file
'
)
    
self
.
_RegisterExtraArgs
(
group
)
  
def
_CreateApkHelpers
(
self
args
incremental_apk_path
install_dict
)
:
    
"
"
"
Returns
true
iff
self
.
apk_helper
was
created
and
assigned
.
"
"
"
    
if
self
.
apk_helper
is
None
:
      
if
args
.
apk_path
:
        
self
.
apk_helper
=
apk_helper
.
ToHelper
(
args
.
apk_path
)
      
elif
incremental_apk_path
:
        
self
.
install_dict
=
install_dict
        
self
.
apk_helper
=
apk_helper
.
ToHelper
(
incremental_apk_path
)
      
elif
self
.
is_bundle
:
        
_GenerateBundleApks
(
self
.
bundle_generation_info
)
        
self
.
apk_helper
=
apk_helper
.
ToHelper
(
            
self
.
bundle_generation_info
.
bundle_apks_path
)
    
if
args
.
additional_apk_paths
and
self
.
additional_apk_helpers
is
None
:
      
self
.
additional_apk_helpers
=
[
          
apk_helper
.
ToHelper
(
apk_path
)
          
for
apk_path
in
args
.
additional_apk_paths
      
]
    
return
self
.
apk_helper
is
not
None
  
def
ProcessArgs
(
self
args
)
:
    
self
.
args
=
args
    
args
.
__dict__
.
setdefault
(
'
apk_path
'
None
)
    
args
.
__dict__
.
setdefault
(
'
incremental_json
'
None
)
    
incremental_apk_path
=
None
    
install_dict
=
None
    
if
args
.
incremental_json
and
not
(
self
.
supports_incremental
and
                                      
args
.
non_incremental
)
:
      
with
open
(
args
.
incremental_json
)
as
f
:
        
install_dict
=
json
.
load
(
f
)
        
incremental_apk_path
=
os
.
path
.
join
(
args
.
output_directory
                                            
install_dict
[
'
apk_path
'
]
)
        
if
not
os
.
path
.
exists
(
incremental_apk_path
)
:
          
incremental_apk_path
=
None
    
if
self
.
supports_incremental
:
      
if
args
.
incremental
and
args
.
non_incremental
:
        
self
.
_parser
.
error
(
'
Must
use
only
one
of
-
-
incremental
and
'
                           
'
-
-
non
-
incremental
'
)
      
elif
args
.
non_incremental
:
        
if
not
args
.
apk_path
:
          
self
.
_parser
.
error
(
'
Apk
has
not
been
built
.
'
)
      
elif
args
.
incremental
:
        
if
not
incremental_apk_path
:
          
self
.
_parser
.
error
(
'
Incremental
apk
has
not
been
built
.
'
)
        
args
.
apk_path
=
None
      
if
args
.
apk_path
and
incremental_apk_path
:
        
self
.
_parser
.
error
(
'
Both
incremental
and
non
-
incremental
apks
exist
.
'
                           
'
Select
using
-
-
incremental
or
-
-
non
-
incremental
'
)
    
if
self
.
needs_apk_helper
:
      
if
not
self
.
_CreateApkHelpers
(
args
incremental_apk_path
install_dict
)
:
        
self
.
_parser
.
error
(
'
App
is
not
built
.
'
)
    
if
self
.
needs_package_name
and
not
args
.
package_name
:
      
if
self
.
_CreateApkHelpers
(
args
incremental_apk_path
install_dict
)
:
        
args
.
package_name
=
self
.
apk_helper
.
GetPackageName
(
)
      
elif
self
.
_from_wrapper_script
:
        
self
.
_parser
.
error
(
'
App
is
not
built
.
'
)
      
else
:
        
self
.
_parser
.
error
(
'
One
of
-
-
package
-
name
or
-
-
apk
-
path
is
required
.
'
)
    
self
.
devices
=
[
]
    
if
self
.
need_device_args
:
      
abis
=
None
      
if
self
.
_CreateApkHelpers
(
args
incremental_apk_path
install_dict
)
:
        
abis
=
self
.
apk_helper
.
GetAbis
(
)
      
self
.
devices
=
device_utils
.
DeviceUtils
.
HealthyDevices
(
          
device_arg
=
args
.
devices
          
enable_device_files_cache
=
bool
(
args
.
output_directory
)
          
default_retries
=
0
          
abis
=
abis
)
      
_LoadDeviceCaches
(
self
.
devices
args
.
output_directory
)
      
try
:
        
if
len
(
self
.
devices
)
>
1
:
          
if
not
self
.
supports_multiple_devices
:
            
self
.
_parser
.
error
(
device_errors
.
MultipleDevicesError
(
self
.
devices
)
)
          
if
not
args
.
all
and
not
args
.
devices
:
            
self
.
_parser
.
error
(
_GenerateMissingAllFlagMessage
(
self
.
devices
)
)
        
if
self
.
calls_exec
:
          
_SaveDeviceCaches
(
self
.
devices
args
.
output_directory
)
      
except
:
        
_SaveDeviceCaches
(
self
.
devices
args
.
output_directory
)
        
raise
class
_DevicesCommand
(
_Command
)
:
  
name
=
'
devices
'
  
description
=
'
Describe
attached
devices
.
'
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
print
(
_GenerateAvailableDevicesMessage
(
self
.
devices
)
)
class
_PackageInfoCommand
(
_Command
)
:
  
name
=
'
package
-
info
'
  
description
=
'
Show
various
attributes
of
this
app
.
'
  
need_device_args
=
False
  
needs_package_name
=
True
  
needs_apk_helper
=
True
  
def
Run
(
self
)
:
    
print
(
'
Package
name
:
"
%
s
"
'
%
self
.
args
.
package_name
)
    
print
(
'
versionCode
:
%
s
'
%
self
.
apk_helper
.
GetVersionCode
(
)
)
    
print
(
'
versionName
:
"
%
s
"
'
%
self
.
apk_helper
.
GetVersionName
(
)
)
    
print
(
'
minSdkVersion
:
%
s
'
%
self
.
apk_helper
.
GetMinSdkVersion
(
)
)
    
print
(
'
targetSdkVersion
:
%
s
'
%
self
.
apk_helper
.
GetTargetSdkVersion
(
)
)
    
print
(
'
Supported
ABIs
:
%
r
'
%
self
.
apk_helper
.
GetAbis
(
)
)
class
_InstallCommand
(
_Command
)
:
  
name
=
'
install
'
  
description
=
'
Installs
the
APK
or
bundle
to
one
or
more
devices
.
'
  
needs_apk_helper
=
True
  
supports_incremental
=
True
  
default_modules
=
[
]
  
def
_RegisterExtraArgs
(
self
group
)
:
    
if
self
.
is_bundle
:
      
group
.
add_argument
(
          
'
-
m
'
          
'
-
-
module
'
          
action
=
'
append
'
          
default
=
self
.
default_modules
          
help
=
'
Module
to
install
.
Can
be
specified
multiple
times
.
'
)
      
group
.
add_argument
(
          
'
-
f
'
          
'
-
-
fake
'
          
action
=
'
append
'
          
default
=
[
]
          
help
=
'
Fake
bundle
module
install
.
Can
be
specified
multiple
times
.
'
          
'
Requires
\
'
-
m
{
0
}
\
'
to
be
given
and
\
'
-
f
{
0
}
\
'
is
illegal
.
'
.
format
(
              
BASE_MODULE
)
)
      
group
.
add_argument
(
'
-
-
no
-
module
'
                         
action
=
'
append
'
                         
choices
=
self
.
default_modules
                         
default
=
[
]
                         
help
=
'
Module
to
exclude
from
default
install
.
'
)
  
def
Run
(
self
)
:
    
if
self
.
additional_apk_helpers
:
      
for
additional_apk_helper
in
self
.
additional_apk_helpers
:
        
_InstallApk
(
self
.
devices
additional_apk_helper
None
)
    
if
self
.
is_bundle
:
      
modules
=
list
(
          
set
(
self
.
args
.
module
)
-
set
(
self
.
args
.
no_module
)
-
          
set
(
self
.
args
.
fake
)
)
      
_InstallBundle
(
self
.
devices
self
.
apk_helper
modules
self
.
args
.
fake
)
    
else
:
      
_InstallApk
(
self
.
devices
self
.
apk_helper
self
.
install_dict
)
class
_UninstallCommand
(
_Command
)
:
  
name
=
'
uninstall
'
  
description
=
'
Removes
the
APK
or
bundle
from
one
or
more
devices
.
'
  
needs_package_name
=
True
  
def
Run
(
self
)
:
    
_UninstallApk
(
self
.
devices
self
.
install_dict
self
.
args
.
package_name
)
class
_SetWebViewProviderCommand
(
_Command
)
:
  
name
=
'
set
-
webview
-
provider
'
  
description
=
(
"
Sets
the
device
'
s
WebView
provider
to
this
APK
'
s
"
                 
"
package
name
.
"
)
  
needs_package_name
=
True
  
needs_apk_helper
=
True
  
def
Run
(
self
)
:
    
if
not
_IsWebViewProvider
(
self
.
apk_helper
)
:
      
raise
Exception
(
'
This
package
does
not
have
a
WebViewLibrary
meta
-
data
'
                      
'
tag
.
Are
you
sure
it
contains
a
WebView
implementation
?
'
)
    
_SetWebViewProvider
(
self
.
devices
self
.
args
.
package_name
)
class
_LaunchCommand
(
_Command
)
:
  
name
=
'
launch
'
  
description
=
(
'
Sends
a
launch
intent
for
the
APK
or
bundle
after
first
'
                 
'
writing
the
command
-
line
flags
file
.
'
)
  
needs_package_name
=
True
  
accepts_command_line_flags
=
True
  
all_devices_by_default
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
'
-
w
'
'
-
-
wait
-
for
-
java
-
debugger
'
action
=
'
store_true
'
                       
help
=
'
Pause
execution
until
debugger
attaches
.
Applies
'
                            
'
only
to
the
main
process
.
To
have
renderers
wait
'
                            
'
use
-
-
args
=
"
-
-
renderer
-
wait
-
for
-
java
-
debugger
"
'
)
    
group
.
add_argument
(
'
-
-
debug
-
process
-
name
'
                       
help
=
'
Name
of
the
process
to
debug
.
'
                            
'
E
.
g
.
"
privileged_process0
"
or
"
foo
.
bar
:
baz
"
'
)
    
group
.
add_argument
(
'
-
-
nokill
'
action
=
'
store_true
'
                       
help
=
'
Do
not
set
the
debug
-
app
nor
set
command
-
line
'
                            
'
flags
.
Useful
to
load
a
URL
without
having
the
'
                             
'
app
restart
.
'
)
    
group
.
add_argument
(
'
url
'
nargs
=
'
?
'
help
=
'
A
URL
to
launch
with
.
'
)
  
def
Run
(
self
)
:
    
if
self
.
args
.
url
and
self
.
is_bundle
:
      
raise
Exception
(
'
Launching
with
URL
not
supported
for
bundles
yet
!
'
)
    
_LaunchUrl
(
self
.
devices
self
.
args
.
package_name
argv
=
self
.
args
.
args
               
command_line_flags_file
=
self
.
args
.
command_line_flags_file
               
url
=
self
.
args
.
url
apk
=
self
.
apk_helper
               
wait_for_java_debugger
=
self
.
args
.
wait_for_java_debugger
               
debug_process_name
=
self
.
args
.
debug_process_name
               
nokill
=
self
.
args
.
nokill
)
class
_StopCommand
(
_Command
)
:
  
name
=
'
stop
'
  
description
=
'
Force
-
stops
the
app
.
'
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
device_utils
.
DeviceUtils
.
parallel
(
self
.
devices
)
.
ForceStop
(
        
self
.
args
.
package_name
)
class
_ClearDataCommand
(
_Command
)
:
  
name
=
'
clear
-
data
'
  
descriptions
=
'
Clears
all
app
data
.
'
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
device_utils
.
DeviceUtils
.
parallel
(
self
.
devices
)
.
ClearApplicationState
(
        
self
.
args
.
package_name
)
class
_ArgvCommand
(
_Command
)
:
  
name
=
'
argv
'
  
description
=
'
Display
and
optionally
update
command
-
line
flags
file
.
'
  
needs_package_name
=
True
  
accepts_command_line_flags
=
True
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
_ChangeFlags
(
self
.
devices
self
.
args
.
args
                 
self
.
args
.
command_line_flags_file
)
class
_GdbCommand
(
_Command
)
:
  
name
=
'
gdb
'
  
description
=
'
Runs
/
/
build
/
android
/
adb_gdb
with
apk
-
specific
args
.
'
  
long_description
=
description
+
"
"
"
To
attach
to
a
process
other
than
the
APK
'
s
main
process
use
-
-
pid
=
1234
.
To
list
all
PIDs
use
the
"
ps
"
command
.
If
no
apk
process
is
currently
running
sends
a
launch
intent
.
"
"
"
  
needs_package_name
=
True
  
needs_output_directory
=
True
  
calls_exec
=
True
  
supports_multiple_devices
=
False
  
def
Run
(
self
)
:
    
_RunGdb
(
self
.
devices
[
0
]
self
.
args
.
package_name
            
self
.
args
.
debug_process_name
self
.
args
.
pid
            
self
.
args
.
output_directory
self
.
args
.
target_cpu
self
.
args
.
port
            
self
.
args
.
ide
bool
(
self
.
args
.
verbose_count
)
)
  
def
_RegisterExtraArgs
(
self
group
)
:
    
pid_group
=
group
.
add_mutually_exclusive_group
(
)
    
pid_group
.
add_argument
(
'
-
-
debug
-
process
-
name
'
                           
help
=
'
Name
of
the
process
to
attach
to
.
'
                                
'
E
.
g
.
"
privileged_process0
"
or
"
foo
.
bar
:
baz
"
'
)
    
pid_group
.
add_argument
(
'
-
-
pid
'
                           
help
=
'
The
process
ID
to
attach
to
.
Defaults
to
'
                                
'
the
main
process
for
the
package
.
'
)
    
group
.
add_argument
(
'
-
-
ide
'
action
=
'
store_true
'
                       
help
=
'
Rather
than
enter
a
gdb
prompt
set
up
the
'
                            
'
gdb
connection
and
wait
for
an
IDE
to
'
                            
'
connect
.
'
)
    
group
.
add_argument
(
'
-
-
port
'
type
=
int
default
=
5039
                       
help
=
'
Use
the
given
port
for
the
GDB
connection
'
)
class
_LogcatCommand
(
_Command
)
:
  
name
=
'
logcat
'
  
description
=
'
Runs
"
adb
logcat
"
with
filters
relevant
the
current
APK
.
'
  
long_description
=
description
+
"
"
"
"
Relevant
filters
"
means
:
  
*
Log
messages
from
processes
belonging
to
the
apk
  
*
Plus
log
messages
from
log
tags
:
ActivityManager
|
DEBUG
  
*
Plus
fatal
logs
from
any
process
  
*
Minus
spamy
dalvikvm
logs
(
for
pre
-
L
devices
)
.
Colors
:
  
*
Primary
process
is
white
  
*
Other
processes
(
gpu
renderer
)
are
yellow
  
*
Non
-
apk
processes
are
grey
  
*
UI
thread
has
a
bolded
Thread
-
ID
Java
stack
traces
are
detected
and
deobfuscated
(
for
release
builds
)
.
To
disable
filtering
(
but
keep
coloring
)
use
-
-
verbose
.
"
"
"
  
needs_package_name
=
True
  
supports_multiple_devices
=
False
  
def
Run
(
self
)
:
    
deobfuscate
=
None
    
if
self
.
args
.
proguard_mapping_path
and
not
self
.
args
.
no_deobfuscate
:
      
deobfuscate
=
deobfuscator
.
Deobfuscator
(
self
.
args
.
proguard_mapping_path
)
    
stack_script_context
=
_StackScriptContext
(
        
self
.
args
.
output_directory
        
self
.
args
.
apk_path
        
self
.
bundle_generation_info
        
quiet
=
True
)
    
try
:
      
_RunLogcat
(
self
.
devices
[
0
]
self
.
args
.
package_name
stack_script_context
                 
deobfuscate
bool
(
self
.
args
.
verbose_count
)
)
    
except
KeyboardInterrupt
:
      
pass
    
finally
:
      
stack_script_context
.
Close
(
)
      
if
deobfuscate
:
        
deobfuscate
.
Close
(
)
  
def
_RegisterExtraArgs
(
self
group
)
:
    
if
self
.
_from_wrapper_script
:
      
group
.
add_argument
(
'
-
-
no
-
deobfuscate
'
action
=
'
store_true
'
          
help
=
'
Disables
ProGuard
deobfuscation
of
logcat
.
'
)
    
else
:
      
group
.
set_defaults
(
no_deobfuscate
=
False
)
      
group
.
add_argument
(
'
-
-
proguard
-
mapping
-
path
'
          
help
=
'
Path
to
ProGuard
map
(
enables
deobfuscation
)
'
)
class
_PsCommand
(
_Command
)
:
  
name
=
'
ps
'
  
description
=
'
Show
PIDs
of
any
APK
processes
currently
running
.
'
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
_RunPs
(
self
.
devices
self
.
args
.
package_name
)
class
_DiskUsageCommand
(
_Command
)
:
  
name
=
'
disk
-
usage
'
  
description
=
'
Show
how
much
device
storage
is
being
consumed
by
the
app
.
'
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
Run
(
self
)
:
    
_RunDiskUsage
(
self
.
devices
self
.
args
.
package_name
)
class
_MemUsageCommand
(
_Command
)
:
  
name
=
'
mem
-
usage
'
  
description
=
'
Show
memory
usage
of
currently
running
APK
processes
.
'
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
'
-
-
query
-
app
'
action
=
'
store_true
'
        
help
=
'
Do
not
add
-
-
local
to
"
dumpsys
meminfo
"
.
This
will
output
'
             
'
additional
metrics
(
e
.
g
.
Context
count
)
but
also
cause
memory
'
             
'
to
be
used
in
order
to
gather
the
metrics
.
'
)
  
def
Run
(
self
)
:
    
_RunMemUsage
(
self
.
devices
self
.
args
.
package_name
                 
query_app
=
self
.
args
.
query_app
)
class
_ShellCommand
(
_Command
)
:
  
name
=
'
shell
'
  
description
=
(
'
Same
as
"
adb
shell
<
command
>
"
but
runs
as
the
apk
\
'
s
uid
'
                 
'
(
via
run
-
as
)
.
Useful
for
inspecting
the
app
\
'
s
data
'
                 
'
directory
.
'
)
  
needs_package_name
=
True
  
property
  
def
calls_exec
(
self
)
:
    
return
not
self
.
args
.
cmd
  
property
  
def
supports_multiple_devices
(
self
)
:
    
return
not
self
.
args
.
cmd
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
cmd
'
nargs
=
argparse
.
REMAINDER
help
=
'
Command
to
run
.
'
)
  
def
Run
(
self
)
:
    
_RunShell
(
self
.
devices
self
.
args
.
package_name
self
.
args
.
cmd
)
class
_CompileDexCommand
(
_Command
)
:
  
name
=
'
compile
-
dex
'
  
description
=
(
'
Applicable
only
for
Android
N
+
.
Forces
.
odex
files
to
be
'
                 
'
compiled
with
the
given
compilation
filter
.
To
see
existing
'
                 
'
filter
use
"
disk
-
usage
"
command
.
'
)
  
needs_package_name
=
True
  
all_devices_by_default
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
compilation_filter
'
        
choices
=
[
'
verify
'
'
quicken
'
'
space
-
profile
'
'
space
'
                 
'
speed
-
profile
'
'
speed
'
]
        
help
=
'
For
WebView
/
Monochrome
use
"
speed
"
.
For
other
apks
use
'
             
'
"
speed
-
profile
"
.
'
)
  
def
Run
(
self
)
:
    
_RunCompileDex
(
self
.
devices
self
.
args
.
package_name
                   
self
.
args
.
compilation_filter
)
class
_PrintCertsCommand
(
_Command
)
:
  
name
=
'
print
-
certs
'
  
description
=
'
Print
info
about
certificates
used
to
sign
this
APK
.
'
  
need_device_args
=
False
  
needs_apk_helper
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
-
-
full
-
cert
'
        
action
=
'
store_true
'
        
help
=
(
"
Print
the
certificate
'
s
full
signature
Base64
-
encoded
.
"
              
"
Useful
when
configuring
an
Android
image
'
s
"
              
"
config_webview_packages
.
xml
.
"
)
)
  
def
Run
(
self
)
:
    
keytool
=
os
.
path
.
join
(
_JAVA_HOME
'
bin
'
'
keytool
'
)
    
if
self
.
is_bundle
:
      
with
tempfile
.
NamedTemporaryFile
(
)
as
f
:
        
logging
.
warning
(
'
Bundles
are
not
signed
until
turned
into
.
apk
files
.
'
)
        
logging
.
warning
(
'
Showing
signing
info
based
on
associated
keystore
.
'
)
        
cmd
=
[
            
keytool
'
-
exportcert
'
'
-
keystore
'
            
self
.
bundle_generation_info
.
keystore_path
'
-
storepass
'
            
self
.
bundle_generation_info
.
keystore_password
'
-
alias
'
            
self
.
bundle_generation_info
.
keystore_alias
'
-
file
'
f
.
name
        
]
        
subprocess
.
check_output
(
cmd
stderr
=
subprocess
.
STDOUT
)
        
cmd
=
[
keytool
'
-
printcert
'
'
-
file
'
f
.
name
]
        
logging
.
warning
(
'
Running
:
%
s
'
'
'
.
join
(
cmd
)
)
        
subprocess
.
check_call
(
cmd
)
        
if
self
.
args
.
full_cert
:
          
full_output
=
subprocess
.
check_output
(
              
cmd
+
[
'
-
rfc
'
]
stderr
=
subprocess
.
STDOUT
)
    
else
:
      
cmd
=
[
          
build_tools
.
GetPath
(
'
apksigner
'
)
'
verify
'
'
-
-
print
-
certs
'
          
'
-
-
verbose
'
self
.
apk_helper
.
path
      
]
      
logging
.
warning
(
'
Running
:
%
s
'
'
'
.
join
(
cmd
)
)
      
env
=
os
.
environ
.
copy
(
)
      
env
[
'
PATH
'
]
=
os
.
path
.
pathsep
.
join
(
          
[
os
.
path
.
join
(
_JAVA_HOME
'
bin
'
)
           
env
.
get
(
'
PATH
'
)
]
)
      
stdout
=
subprocess
.
check_output
(
cmd
env
=
env
)
      
print
(
stdout
)
      
if
self
.
args
.
full_cert
:
        
if
'
v1
scheme
(
JAR
signing
)
:
true
'
not
in
stdout
:
          
raise
Exception
(
              
'
Cannot
print
full
certificate
because
apk
is
not
V1
signed
.
'
)
        
cmd
=
[
keytool
'
-
printcert
'
'
-
jarfile
'
self
.
apk_helper
.
path
'
-
rfc
'
]
        
full_output
=
subprocess
.
check_output
(
cmd
stderr
=
subprocess
.
STDOUT
)
    
if
self
.
args
.
full_cert
:
      
m
=
re
.
search
(
          
r
'
-
+
BEGIN
CERTIFICATE
-
+
(
[
\
r
\
n0
-
9A
-
Za
-
z
+
/
=
]
+
)
-
+
END
CERTIFICATE
-
+
'
          
full_output
re
.
MULTILINE
)
      
if
not
m
:
        
raise
Exception
(
'
Unable
to
parse
certificate
:
\
n
{
}
'
.
format
(
full_output
)
)
      
signature
=
re
.
sub
(
r
'
[
\
r
\
n
]
+
'
'
'
m
.
group
(
1
)
)
      
print
(
)
      
print
(
'
Full
Signature
:
'
)
      
print
(
signature
)
class
_ProfileCommand
(
_Command
)
:
  
name
=
'
profile
'
  
description
=
(
'
Run
the
simpleperf
sampling
CPU
profiler
on
the
currently
-
'
                 
'
running
APK
.
If
-
-
args
is
used
the
extra
arguments
will
be
'
                 
'
passed
on
to
simpleperf
;
otherwise
the
following
default
'
                 
'
arguments
are
used
:
-
g
-
f
1000
-
o
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
)
  
needs_package_name
=
True
  
needs_output_directory
=
True
  
supports_multiple_devices
=
False
  
accepts_args
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
-
-
profile
-
process
'
default
=
'
browser
'
        
help
=
(
'
Which
process
to
profile
.
This
may
be
a
process
name
or
pid
'
              
'
such
as
you
would
get
from
running
%
s
ps
;
or
'
              
'
it
can
be
one
of
(
browser
renderer
gpu
)
.
'
%
sys
.
argv
[
0
]
)
)
    
group
.
add_argument
(
        
'
-
-
profile
-
thread
'
default
=
None
        
help
=
(
'
(
Optional
)
Profile
only
a
single
thread
.
This
may
be
either
a
'
              
'
thread
ID
such
as
you
would
get
by
running
adb
shell
ps
-
t
'
              
'
(
pre
-
Oreo
)
or
adb
shell
ps
-
e
-
T
(
Oreo
and
later
)
;
or
it
may
'
              
'
be
one
of
(
io
compositor
main
render
)
in
which
case
'
              
'
-
-
profile
-
process
is
also
required
.
(
Note
that
"
render
"
thread
'
              
'
refers
to
a
thread
in
the
browser
process
that
manages
a
'
              
'
renderer
;
to
profile
the
main
thread
of
the
renderer
process
'
              
'
use
-
-
profile
-
thread
=
main
)
.
'
)
)
    
group
.
add_argument
(
'
-
-
profile
-
output
'
default
=
'
profile
.
pb
'
                       
help
=
'
Output
file
for
profiling
data
'
)
  
def
Run
(
self
)
:
    
extra_args
=
shlex
.
split
(
self
.
args
.
args
or
'
'
)
    
_RunProfile
(
self
.
devices
[
0
]
self
.
args
.
package_name
                
self
.
args
.
output_directory
self
.
args
.
profile_output
                
self
.
args
.
profile_process
self
.
args
.
profile_thread
                
extra_args
)
class
_RunCommand
(
_InstallCommand
_LaunchCommand
_LogcatCommand
)
:
  
name
=
'
run
'
  
description
=
'
Install
launch
and
show
logcat
(
when
targeting
one
device
)
.
'
  
all_devices_by_default
=
False
  
supports_multiple_devices
=
True
  
def
_RegisterExtraArgs
(
self
group
)
:
    
_InstallCommand
.
_RegisterExtraArgs
(
self
group
)
    
_LaunchCommand
.
_RegisterExtraArgs
(
self
group
)
    
_LogcatCommand
.
_RegisterExtraArgs
(
self
group
)
    
group
.
add_argument
(
'
-
-
no
-
logcat
'
action
=
'
store_true
'
                       
help
=
'
Install
and
launch
but
do
not
enter
logcat
.
'
)
  
def
Run
(
self
)
:
    
logging
.
warning
(
'
Installing
.
.
.
'
)
    
_InstallCommand
.
Run
(
self
)
    
logging
.
warning
(
'
Sending
launch
intent
.
.
.
'
)
    
_LaunchCommand
.
Run
(
self
)
    
if
len
(
self
.
devices
)
=
=
1
and
not
self
.
args
.
no_logcat
:
      
logging
.
warning
(
'
Entering
logcat
.
.
.
'
)
      
_LogcatCommand
.
Run
(
self
)
class
_BuildBundleApks
(
_Command
)
:
  
name
=
'
build
-
bundle
-
apks
'
  
description
=
(
'
Build
the
.
apks
archive
from
an
Android
app
bundle
and
'
                 
'
optionally
copy
it
to
a
specific
destination
.
'
)
  
need_device_args
=
False
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
-
-
output
-
apks
'
required
=
True
help
=
'
Destination
path
for
.
apks
file
.
'
)
    
group
.
add_argument
(
        
'
-
-
minimal
'
        
action
=
'
store_true
'
        
help
=
'
Build
.
apks
archive
that
targets
the
bundle
\
'
s
minSdkVersion
and
'
        
'
contains
only
english
splits
.
It
still
contains
optional
splits
.
'
)
    
group
.
add_argument
(
        
'
-
-
sdk
-
version
'
help
=
'
The
sdkVersion
to
build
the
.
apks
for
.
'
)
    
group
.
add_argument
(
        
'
-
-
build
-
mode
'
        
choices
=
app_bundle_utils
.
BUILD_APKS_MODES
        
help
=
'
Specify
which
type
of
APKs
archive
to
build
.
"
default
"
'
        
'
generates
regular
splits
"
universal
"
generates
an
archive
with
a
'
        
'
single
universal
APK
"
system
"
generates
an
archive
with
a
system
'
        
'
image
APK
while
"
system_compressed
"
generates
a
compressed
system
'
        
'
APK
with
an
additional
stub
APK
for
the
system
image
.
'
)
    
group
.
add_argument
(
        
'
-
-
optimize
-
for
'
        
choices
=
app_bundle_utils
.
OPTIMIZE_FOR_OPTIONS
        
help
=
'
Override
split
configuration
.
'
)
  
def
Run
(
self
)
:
    
_GenerateBundleApks
(
        
self
.
bundle_generation_info
        
output_path
=
self
.
args
.
output_apks
        
minimal
=
self
.
args
.
minimal
        
minimal_sdk_version
=
self
.
args
.
sdk_version
        
mode
=
self
.
args
.
build_mode
        
optimize_for
=
self
.
args
.
optimize_for
)
class
_ManifestCommand
(
_Command
)
:
  
name
=
'
dump
-
manifest
'
  
description
=
'
Dump
the
android
manifest
from
this
bundle
as
XML
to
stdout
.
'
  
need_device_args
=
False
  
def
Run
(
self
)
:
    
sys
.
stdout
.
write
(
        
bundletool
.
RunBundleTool
(
[
            
'
dump
'
'
manifest
'
'
-
-
bundle
'
            
self
.
bundle_generation_info
.
bundle_path
        
]
)
)
class
_StackCommand
(
_Command
)
:
  
name
=
'
stack
'
  
description
=
'
Decodes
an
Android
stack
.
'
  
need_device_args
=
False
  
def
_RegisterExtraArgs
(
self
group
)
:
    
group
.
add_argument
(
        
'
file
'
        
nargs
=
'
?
'
        
help
=
'
File
to
decode
.
If
not
specified
stdin
is
processed
.
'
)
  
def
Run
(
self
)
:
    
context
=
_StackScriptContext
(
self
.
args
.
output_directory
                                  
self
.
args
.
apk_path
                                  
self
.
bundle_generation_info
)
    
try
:
      
proc
=
context
.
Popen
(
input_file
=
self
.
args
.
file
)
      
if
proc
.
wait
(
)
:
        
raise
Exception
(
'
stack
script
returned
{
}
'
.
format
(
proc
.
returncode
)
)
    
finally
:
      
context
.
Close
(
)
_COMMANDS
=
[
    
_DevicesCommand
    
_PackageInfoCommand
    
_InstallCommand
    
_UninstallCommand
    
_SetWebViewProviderCommand
    
_LaunchCommand
    
_StopCommand
    
_ClearDataCommand
    
_ArgvCommand
    
_GdbCommand
    
_LogcatCommand
    
_PsCommand
    
_DiskUsageCommand
    
_MemUsageCommand
    
_ShellCommand
    
_CompileDexCommand
    
_PrintCertsCommand
    
_ProfileCommand
    
_RunCommand
    
_StackCommand
]
_BUNDLE_COMMANDS
=
[
    
_BuildBundleApks
    
_ManifestCommand
]
def
_ParseArgs
(
parser
from_wrapper_script
is_bundle
)
:
  
subparsers
=
parser
.
add_subparsers
(
)
  
command_list
=
_COMMANDS
+
(
_BUNDLE_COMMANDS
if
is_bundle
else
[
]
)
  
commands
=
[
clazz
(
from_wrapper_script
is_bundle
)
for
clazz
in
command_list
]
  
for
command
in
commands
:
    
if
from_wrapper_script
or
not
command
.
needs_output_directory
:
      
command
.
RegisterArgs
(
subparsers
)
  
argv
=
sys
.
argv
[
1
:
]
  
if
not
argv
:
    
argv
=
[
'
-
-
help
'
]
  
return
parser
.
parse_args
(
argv
)
def
_RunInternal
(
parser
                 
output_directory
=
None
                 
additional_apk_paths
=
None
                 
bundle_generation_info
=
None
)
:
  
colorama
.
init
(
)
  
parser
.
set_defaults
(
      
additional_apk_paths
=
additional_apk_paths
      
output_directory
=
output_directory
)
  
from_wrapper_script
=
bool
(
output_directory
)
  
args
=
_ParseArgs
(
parser
from_wrapper_script
bool
(
bundle_generation_info
)
)
  
run_tests_helper
.
SetLogLevel
(
args
.
verbose_count
)
  
if
bundle_generation_info
:
    
args
.
command
.
RegisterBundleGenerationInfo
(
bundle_generation_info
)
  
if
args
.
additional_apk_paths
:
    
for
path
in
additional_apk_paths
:
      
if
not
path
or
not
os
.
path
.
exists
(
path
)
:
        
raise
Exception
(
'
Invalid
additional
APK
path
"
{
}
"
'
.
format
(
path
)
)
  
args
.
command
.
ProcessArgs
(
args
)
  
args
.
command
.
Run
(
)
  
if
args
.
command
.
name
!
=
'
uninstall
'
:
    
_SaveDeviceCaches
(
args
.
command
.
devices
output_directory
)
def
Run
(
output_directory
apk_path
additional_apk_paths
incremental_json
        
command_line_flags_file
target_cpu
proguard_mapping_path
)
:
  
"
"
"
Entry
point
for
generated
wrapper
scripts
.
"
"
"
  
constants
.
SetOutputDirectory
(
output_directory
)
  
devil_chromium
.
Initialize
(
output_directory
=
output_directory
)
  
parser
=
argparse
.
ArgumentParser
(
)
  
exists_or_none
=
lambda
p
:
p
if
p
and
os
.
path
.
exists
(
p
)
else
None
  
parser
.
set_defaults
(
      
command_line_flags_file
=
command_line_flags_file
      
target_cpu
=
target_cpu
      
apk_path
=
exists_or_none
(
apk_path
)
      
incremental_json
=
exists_or_none
(
incremental_json
)
      
proguard_mapping_path
=
proguard_mapping_path
)
  
_RunInternal
(
      
parser
      
output_directory
=
output_directory
      
additional_apk_paths
=
additional_apk_paths
)
def
RunForBundle
(
output_directory
bundle_path
bundle_apks_path
                 
additional_apk_paths
aapt2_path
keystore_path
                 
keystore_password
keystore_alias
package_name
                 
command_line_flags_file
proguard_mapping_path
target_cpu
                 
system_image_locales
default_modules
)
:
  
"
"
"
Entry
point
for
generated
app
bundle
wrapper
scripts
.
  
Args
:
    
output_dir
:
Chromium
output
directory
path
.
    
bundle_path
:
Input
bundle
path
.
    
bundle_apks_path
:
Output
bundle
.
apks
archive
path
.
    
additional_apk_paths
:
Additional
APKs
to
install
prior
to
bundle
install
.
    
aapt2_path
:
Aapt2
tool
path
.
    
keystore_path
:
Keystore
file
path
.
    
keystore_password
:
Keystore
password
.
    
keystore_alias
:
Signing
key
name
alias
in
keystore
file
.
    
package_name
:
Application
'
s
package
name
.
    
command_line_flags_file
:
Optional
.
Name
of
an
on
-
device
file
that
will
be
      
used
to
store
command
-
line
flags
for
this
bundle
.
    
proguard_mapping_path
:
Input
path
to
the
Proguard
mapping
file
used
to
      
deobfuscate
Java
stack
traces
.
    
target_cpu
:
Chromium
target
CPU
name
used
by
the
'
gdb
'
command
.
    
system_image_locales
:
List
of
Chromium
locales
that
should
be
included
in
      
system
image
APKs
.
    
default_modules
:
List
of
modules
that
are
installed
in
addition
to
those
      
given
by
the
'
-
m
'
switch
.
  
"
"
"
  
constants
.
SetOutputDirectory
(
output_directory
)
  
devil_chromium
.
Initialize
(
output_directory
=
output_directory
)
  
bundle_generation_info
=
BundleGenerationInfo
(
      
bundle_path
=
bundle_path
      
bundle_apks_path
=
bundle_apks_path
      
aapt2_path
=
aapt2_path
      
keystore_path
=
keystore_path
      
keystore_password
=
keystore_password
      
keystore_alias
=
keystore_alias
      
system_image_locales
=
system_image_locales
)
  
_InstallCommand
.
default_modules
=
default_modules
  
parser
=
argparse
.
ArgumentParser
(
)
  
parser
.
set_defaults
(
      
package_name
=
package_name
      
command_line_flags_file
=
command_line_flags_file
      
proguard_mapping_path
=
proguard_mapping_path
      
target_cpu
=
target_cpu
)
  
_RunInternal
(
      
parser
      
output_directory
=
output_directory
      
additional_apk_paths
=
additional_apk_paths
      
bundle_generation_info
=
bundle_generation_info
)
def
main
(
)
:
  
devil_chromium
.
Initialize
(
)
  
_RunInternal
(
argparse
.
ArgumentParser
(
)
)
if
__name__
=
=
'
__main__
'
:
  
main
(
)
