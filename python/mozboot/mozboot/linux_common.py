class
StyloInstall
(
object
)
:
    
def
__init__
(
self
*
*
kwargs
)
:
        
pass
    
def
ensure_stylo_packages
(
self
state_dir
)
:
        
import
stylo
        
self
.
install_tooltool_clang_package
(
state_dir
*
*
stylo
.
LINUX
)
