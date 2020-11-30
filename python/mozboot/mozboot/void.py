from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
subprocess
import
sys
from
mozboot
.
base
import
BaseBootstrapper
from
mozboot
.
linux_common
import
LinuxBootstrapper
class
VoidBootstrapper
(
        
LinuxBootstrapper
        
BaseBootstrapper
)
:
    
PACKAGES
=
[
        
'
autoconf213
'
        
'
clang
'
        
'
make
'
        
'
mercurial
'
        
'
nodejs
'
        
'
unzip
'
        
'
zip
'
    
]
    
BROWSER_PACKAGES
=
[
        
'
dbus
-
devel
'
        
'
dbus
-
glib
-
devel
'
        
'
gtk
+
3
-
devel
'
        
'
pulseaudio
'
        
'
pulseaudio
-
devel
'
        
'
libcurl
-
devel
'
        
'
libxcb
-
devel
'
        
'
libXt
-
devel
'
        
'
yasm
'
    
]
    
MOBILE_ANDROID_PACKAGES
=
[
        
'
openjdk8
'
        
'
wget
'
    
]
    
def
__init__
(
self
version
dist_id
*
*
kwargs
)
:
        
BaseBootstrapper
.
__init__
(
self
*
*
kwargs
)
        
self
.
distro
=
"
void
"
        
self
.
version
=
version
        
self
.
dist_id
=
dist_id
        
self
.
packages
=
self
.
PACKAGES
        
self
.
browser_packages
=
self
.
BROWSER_PACKAGES
        
self
.
mobile_android_packages
=
self
.
MOBILE_ANDROID_PACKAGES
    
def
run_as_root
(
self
command
)
:
        
if
os
.
geteuid
(
)
!
=
0
:
            
command
=
[
'
su
'
'
root
'
'
-
c
'
'
'
.
join
(
command
)
]
        
print
(
'
Executing
as
root
:
'
subprocess
.
list2cmdline
(
command
)
)
        
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
xbps_install
(
self
*
packages
)
:
        
command
=
[
'
xbps
-
install
'
]
        
if
self
.
no_interactive
:
            
command
.
append
(
'
-
y
'
)
        
command
.
extend
(
packages
)
        
self
.
run_as_root
(
command
)
    
def
xbps_update
(
self
)
:
        
command
=
[
'
xbps
-
install
'
'
-
Su
'
]
        
if
self
.
no_interactive
:
            
command
.
append
(
'
-
y
'
)
        
self
.
run_as_root
(
command
)
    
def
install_system_packages
(
self
)
:
        
self
.
xbps_install
(
*
self
.
packages
)
    
def
install_browser_packages
(
self
mozconfig_builder
)
:
        
self
.
ensure_browser_packages
(
)
    
def
install_browser_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
self
.
ensure_browser_packages
(
artifact_mode
=
True
)
    
def
install_mobile_android_packages
(
self
mozconfig_builder
)
:
        
self
.
ensure_mobile_android_packages
(
mozconfig_builder
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
ensure_mobile_android_packages
(
mozconfig_builder
artifact_mode
=
True
)
    
def
ensure_browser_packages
(
self
artifact_mode
=
False
)
:
        
self
.
xbps_install
(
*
self
.
browser_packages
)
    
def
ensure_mobile_android_packages
(
self
mozconfig_builder
artifact_mode
=
False
)
:
        
self
.
xbps_install
(
*
self
.
mobile_android_packages
)
        
self
.
ensure_java
(
mozconfig_builder
)
        
from
mozboot
import
android
        
android
.
ensure_android
(
'
linux
'
artifact_mode
=
artifact_mode
                               
no_interactive
=
self
.
no_interactive
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
'
linux
'
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
_update_package_manager
(
self
)
:
        
self
.
xbps_update
(
)
