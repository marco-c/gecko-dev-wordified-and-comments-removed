from
__future__
import
absolute_import
from
mozboot
.
base
import
BaseBootstrapper
class
OpenBSDBootstrapper
(
BaseBootstrapper
)
:
    
def
__init__
(
self
version
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
packages
=
[
            
'
mercurial
'
            
'
autoconf
-
2
.
13
'
            
'
gmake
'
            
'
gtar
'
            
'
node
'
            
'
rust
'
            
'
wget
'
            
'
unzip
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
llvm
'
            
'
yasm
'
            
'
gconf2
'
            
'
gtk
+
2
'
            
'
gtk
+
3
'
            
'
dbus
-
glib
'
            
'
pulseaudio
'
        
]
    
def
install_system_packages
(
self
)
:
        
self
.
run_as_root
(
[
'
pkg_add
'
'
-
z
'
]
+
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
run_as_root
(
[
'
pkg_add
'
'
-
z
'
]
+
self
.
browser_packages
)
    
def
ensure_stylo_packages
(
self
state_dir
checkout_root
)
:
        
pass
