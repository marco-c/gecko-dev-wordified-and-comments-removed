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
mozfile
import
which
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
"
.
"
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
            
"
gmake
"
            
"
gtar
"
            
"
pkgconf
"
            
"
py
%
s
%
s
-
sqlite3
"
%
sys
.
version_info
[
0
:
2
]
            
"
rust
"
            
"
watchman
"
            
"
zip
"
        
]
        
self
.
browser_packages
=
[
            
"
dbus
-
glib
"
            
"
gtk3
"
            
"
libXt
"
            
"
mesa
-
dri
"
            
"
nasm
"
            
"
pulseaudio
"
            
"
v4l_compat
"
        
]
        
if
not
which
(
"
as
"
)
:
            
self
.
packages
.
append
(
"
binutils
"
)
        
if
not
which
(
"
unzip
"
)
:
            
self
.
packages
.
append
(
"
unzip
"
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
"
pkg
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
y
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
mozconfig_builder
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
ensure_clang_static_analysis_package
(
self
)
:
        
pass
    
def
ensure_stylo_packages
(
self
)
:
        
self
.
pkg_install
(
"
rust
-
cbindgen
"
)
    
def
ensure_nasm_packages
(
self
)
:
        
pass
    
def
ensure_node_packages
(
self
)
:
        
self
.
pkg_install
(
"
npm
"
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
"
mercurial
"
)
