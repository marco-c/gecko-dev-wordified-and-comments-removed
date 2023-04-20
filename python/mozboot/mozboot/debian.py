from
__future__
import
absolute_import
print_function
unicode_literals
from
mozboot
.
base
import
BaseBootstrapper
MERCURIAL_INSTALL_PROMPT
from
mozboot
.
linux_common
import
LinuxBootstrapper
import
sys
class
DebianBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
COMMON_PACKAGES
=
[
        
"
build
-
essential
"
        
"
libpython3
-
dev
"
        
"
m4
"
        
"
unzip
"
        
"
uuid
"
    
]
    
BROWSER_COMMON_PACKAGES
=
[
        
"
libasound2
-
dev
"
        
"
libcurl4
-
openssl
-
dev
"
        
"
libdbus
-
1
-
dev
"
        
"
libdbus
-
glib
-
1
-
dev
"
        
"
libdrm
-
dev
"
        
"
libgtk
-
3
-
dev
"
        
"
libpulse
-
dev
"
        
"
libx11
-
xcb
-
dev
"
        
"
libxt
-
dev
"
        
"
xvfb
"
    
]
    
MOBILE_ANDROID_COMMON_PACKAGES
=
[
        
"
libncurses5
"
    
]
    
def
__init__
(
self
distro
version
dist_id
codename
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
distro
        
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
codename
=
codename
        
self
.
packages
=
list
(
self
.
COMMON_PACKAGES
)
        
try
:
            
version_number
=
int
(
version
)
        
except
ValueError
:
            
version_number
=
None
        
if
(
version_number
and
(
version_number
>
=
11
)
)
or
version
=
=
"
unstable
"
:
            
self
.
packages
+
=
[
"
watchman
"
]
    
def
suggest_install_distutils
(
self
)
:
        
print
(
            
"
HINT
:
Try
installing
distutils
with
"
            
"
apt
-
get
install
python3
-
distutils
.
"
            
file
=
sys
.
stderr
        
)
    
def
suggest_install_pip3
(
self
)
:
        
print
(
            
"
HINT
:
Try
installing
pip3
with
apt
-
get
install
python3
-
pip
.
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
        
self
.
apt_install
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
artifact_mode
=
False
)
:
        
self
.
apt_install
(
*
self
.
BROWSER_COMMON_PACKAGES
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
install_mobile_android_packages
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
apt_install
(
*
self
.
MOBILE_ANDROID_COMMON_PACKAGES
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
        
self
.
apt_update
(
)
    
def
upgrade_mercurial
(
self
current
)
:
        
"
"
"
Install
Mercurial
from
pip
because
Debian
packages
typically
lag
.
"
"
"
        
if
self
.
no_interactive
:
            
self
.
apt_install
(
"
mercurial
"
)
            
return
        
res
=
self
.
prompt_int
(
MERCURIAL_INSTALL_PROMPT
1
3
)
        
if
res
=
=
2
:
            
self
.
apt_install
(
"
mercurial
"
)
            
return
False
        
if
res
=
=
3
:
            
print
(
"
Not
installing
Mercurial
.
"
)
            
return
False
        
assert
res
=
=
1
        
self
.
run_as_root
(
[
"
pip3
"
"
install
"
"
-
-
upgrade
"
"
Mercurial
"
]
)
