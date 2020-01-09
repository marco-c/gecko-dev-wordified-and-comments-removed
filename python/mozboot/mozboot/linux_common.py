from
__future__
import
absolute_import
print_function
import
os
def
is_non_x86_64
(
)
:
    
return
os
.
uname
(
)
[
4
]
!
=
'
x86_64
'
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
        
if
is_non_x86_64
(
)
:
            
print
(
'
Cannot
install
bindgen
clang
and
cbindgen
packages
from
taskcluster
.
\
n
'
                  
'
Please
install
these
packages
manually
.
'
)
            
return
        
self
.
install_toolchain_artifact
(
state_dir
checkout_root
stylo
.
LINUX_CLANG
)
        
self
.
install_toolchain_artifact
(
state_dir
checkout_root
stylo
.
LINUX_CBINDGEN
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
        
if
is_non_x86_64
(
)
:
            
print
(
'
Cannot
install
node
package
from
taskcluster
.
\
n
'
                  
'
Please
install
this
package
manually
.
'
)
            
return
        
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
class
ClangStaticAnalysisInstall
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
ensure_clang_static_analysis_package
(
self
checkout_root
)
:
        
if
is_non_x86_64
(
)
:
            
print
(
'
Cannot
install
static
analysis
tools
from
taskcluster
.
\
n
'
                  
'
Please
install
these
tools
manually
.
'
)
            
return
        
from
mozboot
import
static_analysis
        
self
.
install_toolchain_static_analysis
(
            
state_dir
checkout_root
static_analysis
.
LINUX_CLANG_TIDY
)
