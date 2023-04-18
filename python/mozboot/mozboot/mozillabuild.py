from
__future__
import
absolute_import
print_function
unicode_literals
import
ctypes
import
os
import
platform
import
sys
import
subprocess
from
mozboot
.
base
import
BaseBootstrapper
def
is_aarch64_host
(
)
:
    
from
ctypes
import
wintypes
    
kernel32
=
ctypes
.
windll
.
kernel32
    
IMAGE_FILE_MACHINE_UNKNOWN
=
0
    
IMAGE_FILE_MACHINE_ARM64
=
0xAA64
    
try
:
        
iswow64process2
=
kernel32
.
IsWow64Process2
    
except
Exception
:
        
return
False
    
currentProcess
=
kernel32
.
GetCurrentProcess
(
)
    
processMachine
=
wintypes
.
USHORT
(
IMAGE_FILE_MACHINE_UNKNOWN
)
    
nativeMachine
=
wintypes
.
USHORT
(
IMAGE_FILE_MACHINE_UNKNOWN
)
    
gotValue
=
iswow64process2
(
        
currentProcess
ctypes
.
byref
(
processMachine
)
ctypes
.
byref
(
nativeMachine
)
    
)
    
if
not
gotValue
:
        
return
False
    
return
nativeMachine
.
value
=
=
IMAGE_FILE_MACHINE_ARM64
def
get_is_windefender_disabled
(
)
:
    
import
winreg
    
try
:
        
with
winreg
.
OpenKeyEx
(
            
winreg
.
HKEY_LOCAL_MACHINE
r
"
SOFTWARE
\
Microsoft
\
Windows
Defender
"
        
)
as
windefender_key
:
            
is_antivirus_disabled
_
=
winreg
.
QueryValueEx
(
                
windefender_key
"
DisableAntiSpyware
"
            
)
            
return
bool
(
is_antivirus_disabled
)
    
except
FileNotFoundError
:
        
return
True
def
get_windefender_exclusion_paths
(
)
:
    
import
winreg
    
paths
=
[
]
    
try
:
        
with
winreg
.
OpenKeyEx
(
            
winreg
.
HKEY_LOCAL_MACHINE
            
r
"
SOFTWARE
\
Microsoft
\
Windows
Defender
\
Exclusions
\
Paths
"
        
)
as
exclusions_key
:
            
_
values_count
__
=
winreg
.
QueryInfoKey
(
exclusions_key
)
            
for
i
in
range
(
0
values_count
)
:
                
path
_
__
=
winreg
.
EnumValue
(
exclusions_key
i
)
                
paths
.
append
(
path
)
    
except
FileNotFoundError
:
        
pass
    
return
paths
def
is_windefender_affecting_srcdir
(
srcdir
)
:
    
if
get_is_windefender_disabled
(
)
:
        
return
False
    
srcdir
=
os
.
path
.
normcase
(
os
.
path
.
abspath
(
srcdir
)
)
    
try
:
        
exclusion_paths
=
get_windefender_exclusion_paths
(
)
    
except
OSError
as
e
:
        
if
e
.
winerror
=
=
5
:
            
return
        
raise
    
for
exclusion_path
in
exclusion_paths
:
        
exclusion_path
=
os
.
path
.
normcase
(
os
.
path
.
abspath
(
exclusion_path
)
)
        
try
:
            
if
os
.
path
.
commonpath
(
[
exclusion_path
srcdir
]
)
=
=
exclusion_path
:
                
return
False
        
except
ValueError
:
            
pass
    
return
True
class
MozillaBuildBootstrapper
(
BaseBootstrapper
)
:
    
"
"
"
Bootstrapper
for
MozillaBuild
to
install
rustup
.
"
"
"
    
def
__init__
(
self
no_interactive
=
False
no_system_changes
=
False
)
:
        
BaseBootstrapper
.
__init__
(
            
self
no_interactive
=
no_interactive
no_system_changes
=
no_system_changes
        
)
    
def
validate_environment
(
self
)
:
        
if
self
.
application
.
startswith
(
"
mobile_android
"
)
:
            
print
(
                
"
WARNING
!
!
!
Building
Firefox
for
Android
on
Windows
is
not
"
                
"
fully
supported
.
See
https
:
/
/
bugzilla
.
mozilla
.
org
/
show_bug
.
"
                
"
cgi
?
id
=
1169873
for
details
.
"
                
file
=
sys
.
stderr
            
)
        
if
is_windefender_affecting_srcdir
(
self
.
srcdir
)
:
            
print
(
                
"
Warning
:
the
Firefox
checkout
directory
is
currently
not
in
the
"
                
"
Windows
Defender
exclusion
list
.
This
can
cause
the
build
process
"
                
"
to
be
dramatically
slowed
or
broken
.
To
resolve
this
follow
the
"
                
"
directions
here
:
"
                
"
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
setup
/
windows_build
.
html
"
                
"
#
antivirus
-
performance
"
                
file
=
sys
.
stderr
            
)
    
def
install_system_packages
(
self
)
:
        
pass
    
def
upgrade_mercurial
(
self
current
)
:
        
self
.
pip_install
(
"
mercurial
"
"
-
-
only
-
binary
"
"
mercurial
"
)
    
def
install_browser_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
install_browser_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
_os_arch
(
self
)
:
        
os_arch
=
platform
.
machine
(
)
        
if
os_arch
=
=
"
AMD64
"
:
            
return
"
x86_64
"
        
return
os_arch
    
def
install_mobile_android_packages
(
self
mozconfig_builder
artifact_mode
=
False
)
:
        
from
mozboot
import
android
        
os_arch
=
self
.
_os_arch
(
)
        
android
.
ensure_android
(
            
"
windows
"
            
os_arch
            
artifact_mode
=
artifact_mode
            
no_interactive
=
self
.
no_interactive
        
)
        
android
.
ensure_android
(
            
"
windows
"
            
os_arch
            
system_images_only
=
True
            
artifact_mode
=
artifact_mode
            
no_interactive
=
self
.
no_interactive
            
avd_manifest_path
=
android
.
AVD_MANIFEST_X86_64
        
)
        
android
.
ensure_android
(
            
"
windows
"
            
os_arch
            
system_images_only
=
True
            
artifact_mode
=
artifact_mode
            
no_interactive
=
self
.
no_interactive
            
avd_manifest_path
=
android
.
AVD_MANIFEST_ARM
        
)
    
def
ensure_mobile_android_packages
(
self
)
:
        
from
mozboot
import
android
        
android
.
ensure_java
(
"
windows
"
self
.
_os_arch
(
)
)
        
self
.
install_toolchain_artifact
(
android
.
WINDOWS_X86_64_ANDROID_AVD
)
        
self
.
install_toolchain_artifact
(
android
.
WINDOWS_ARM_ANDROID_AVD
)
    
def
install_mobile_android_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
self
.
install_mobile_android_packages
(
mozconfig_builder
artifact_mode
=
True
)
    
def
generate_mobile_android_mozconfig
(
self
artifact_mode
=
False
)
:
        
from
mozboot
import
android
        
return
android
.
generate_mozconfig
(
"
windows
"
artifact_mode
=
artifact_mode
)
    
def
generate_mobile_android_artifact_mode_mozconfig
(
self
)
:
        
return
self
.
generate_mobile_android_mozconfig
(
artifact_mode
=
True
)
    
def
ensure_clang_static_analysis_package
(
self
)
:
        
from
mozboot
import
static_analysis
        
self
.
install_toolchain_static_analysis
(
static_analysis
.
WINDOWS_CLANG_TIDY
)
    
def
ensure_sccache_packages
(
self
)
:
        
from
mozboot
import
sccache
        
self
.
install_toolchain_artifact
(
"
sccache
"
)
        
self
.
install_toolchain_artifact
(
sccache
.
RUSTC_DIST_TOOLCHAIN
no_unpack
=
True
)
        
self
.
install_toolchain_artifact
(
sccache
.
CLANG_DIST_TOOLCHAIN
no_unpack
=
True
)
    
def
ensure_stylo_packages
(
self
)
:
        
if
is_aarch64_host
(
)
:
            
raise
Exception
(
                
"
You
should
not
be
performing
desktop
builds
on
an
"
                
"
AArch64
device
.
If
you
want
to
do
artifact
builds
"
                
"
instead
please
choose
the
appropriate
artifact
build
"
                
"
option
when
beginning
bootstrap
.
"
            
)
        
self
.
install_toolchain_artifact
(
"
clang
"
)
        
self
.
install_toolchain_artifact
(
"
cbindgen
"
)
    
def
ensure_nasm_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
nasm
"
)
    
def
ensure_node_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
node
"
)
    
def
ensure_fix_stacks_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
fix
-
stacks
"
)
    
def
ensure_minidump_stackwalk_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
minidump_stackwalk
"
)
    
def
_update_package_manager
(
self
)
:
        
pass
    
def
run
(
self
command
)
:
        
subprocess
.
check_call
(
command
stdin
=
sys
.
stdin
)
    
def
pip_install
(
self
*
packages
)
:
        
pip_dir
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
[
"
MOZILLABUILD
"
]
"
python
"
"
Scripts
"
"
pip
.
exe
"
        
)
        
command
=
[
pip_dir
"
install
"
"
-
-
upgrade
"
]
        
command
.
extend
(
packages
)
        
self
.
run
(
command
)
