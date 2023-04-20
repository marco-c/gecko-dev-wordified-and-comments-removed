from
__future__
import
absolute_import
print_function
unicode_literals
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
install_packages
(
self
packages
)
:
        
self
.
package_install
(
*
packages
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
