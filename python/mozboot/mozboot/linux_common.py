from
__future__
import
absolute_import
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
checkout_root
)
:
        
from
mozboot
import
stylo
        
self
.
install_toolchain_artifact
(
state_dir
checkout_root
stylo
.
LINUX
)
class
NodeInstall
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
ensure_node_packages
(
self
state_dir
checkout_root
)
:
        
from
mozboot
import
node
        
self
.
install_toolchain_artifact
(
state_dir
checkout_root
node
.
LINUX
)
