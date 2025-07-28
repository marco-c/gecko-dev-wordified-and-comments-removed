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
class
AerynOsBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
"
"
"
AerynOs
experimental
bootstrapper
.
"
"
"
    
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
AerynOs
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
        
packages
=
[
p
for
p
in
packages
if
p
!
=
"
watchman
"
]
        
self
.
package_install
(
*
packages
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
moss
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
