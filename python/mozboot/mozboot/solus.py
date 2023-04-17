from
__future__
import
absolute_import
print_function
unicode_literals
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
from
mozboot
.
linux_common
import
LinuxBootstrapper
if
sys
.
version_info
<
(
3
)
:
    
input
=
raw_input
class
SolusBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
"
"
"
Solus
experimental
bootstrapper
.
"
"
"
    
SYSTEM_PACKAGES
=
[
"
nodejs
"
"
unzip
"
"
zip
"
]
    
SYSTEM_COMPONENTS
=
[
"
system
.
devel
"
]
    
BROWSER_PACKAGES
=
[
        
"
alsa
-
lib
"
        
"
dbus
"
        
"
libgtk
-
3
"
        
"
libevent
"
        
"
libvpx
"
        
"
libxt
"
        
"
nasm
"
        
"
libstartup
-
notification
"
        
"
gst
-
plugins
-
base
"
        
"
gst
-
plugins
-
good
"
        
"
pulseaudio
"
        
"
xorg
-
server
-
xvfb
"
    
]
    
MOBILE_ANDROID_COMMON_PACKAGES
=
[
        
"
openjdk
-
8
"
        
"
ncurses
-
32bit
"
        
"
readline
-
32bit
"
        
"
zlib
-
32bit
"
    
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
        
print
(
"
Using
an
experimental
bootstrapper
for
Solus
.
"
)
        
BaseBootstrapper
.
__init__
(
self
*
*
kwargs
)
    
def
install_system_packages
(
self
)
:
        
self
.
package_install
(
*
self
.
SYSTEM_PACKAGES
)
        
self
.
component_install
(
*
self
.
SYSTEM_COMPONENTS
)
    
def
install_browser_packages
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
package_install
(
*
self
.
BROWSER_PACKAGES
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
install_browser_packages
(
mozconfig_builder
artifact_mode
=
True
)
    
def
ensure_nasm_packages
(
self
state_dir
checkout_root
)
:
        
pass
    
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
        
try
:
            
self
.
package_install
(
*
self
.
MOBILE_ANDROID_COMMON_PACKAGES
)
        
except
Exception
as
e
:
            
print
(
"
Failed
to
install
all
packages
!
"
)
            
raise
e
        
self
.
ensure_java
(
mozconfig_builder
)
        
super
(
)
.
install_mobile_android_packages
(
            
mozconfig_builder
artifact_mode
=
artifact_mode
        
)
    
def
_update_package_manager
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
package_install
(
"
mercurial
"
)
    
def
package_install
(
self
*
packages
)
:
        
command
=
[
"
eopkg
"
"
install
"
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
"
-
-
yes
-
all
"
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
component_install
(
self
*
components
)
:
        
command
=
[
"
eopkg
"
"
install
"
"
-
c
"
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
"
-
-
yes
-
all
"
)
        
command
.
extend
(
components
)
        
self
.
run_as_root
(
command
)
    
def
run
(
self
command
env
=
None
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
env
=
env
)
