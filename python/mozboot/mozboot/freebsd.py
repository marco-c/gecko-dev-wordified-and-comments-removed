from
mozboot
.
base
import
BaseBootstrapper
class
FreeBSDBootstrapper
(
BaseBootstrapper
)
:
    
def
__init__
(
self
version
flavor
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
version
=
int
(
version
.
split
(
'
.
'
)
[
0
]
)
        
self
.
flavor
=
flavor
.
lower
(
)
        
self
.
packages
=
[
            
'
autoconf213
'
            
'
gmake
'
            
'
gtar
'
            
'
mercurial
'
            
'
pkgconf
'
            
'
watchman
'
            
'
zip
'
        
]
        
self
.
browser_packages
=
[
            
'
dbus
-
glib
'
            
'
gconf2
'
            
'
gtk2
'
            
'
gtk3
'
            
'
libGL
'
            
'
pulseaudio
'
            
'
v4l_compat
'
            
'
yasm
'
        
]
        
if
not
self
.
which
(
'
unzip
'
)
:
            
self
.
packages
.
append
(
'
unzip
'
)
        
if
self
.
flavor
=
=
'
freebsd
'
and
self
.
version
<
11
:
            
self
.
browser_packages
.
append
(
'
gcc
'
)
    
def
pkg_install
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
pkg
'
'
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
install_system_packages
(
self
)
:
        
self
.
pkg_install
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
pkg_install
(
*
self
.
browser_packages
)
    
def
upgrade_mercurial
(
self
current
)
:
        
self
.
pkg_install
(
'
mercurial
'
)
