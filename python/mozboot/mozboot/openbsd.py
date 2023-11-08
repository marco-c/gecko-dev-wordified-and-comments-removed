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
"
gmake
"
"
gtar
"
"
rust
"
"
unzip
"
]
        
self
.
browser_packages
=
[
            
"
llvm
"
            
"
cbindgen
"
            
"
nasm
"
            
"
node
"
            
"
gtk
+
3
"
            
"
pulseaudio
"
        
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
"
pkg_add
"
"
-
z
"
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
mozconfig_builder
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
"
pkg_add
"
"
-
z
"
]
+
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
