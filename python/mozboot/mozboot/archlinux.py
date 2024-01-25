import
subprocess
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
class
ArchlinuxBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
"
"
"
Archlinux
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
Archlinux
.
"
file
=
sys
.
stderr
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
pacman_install
(
*
packages
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
pacman_install
(
"
mercurial
"
)
    
def
pacman_install
(
self
*
packages
)
:
        
def
is_installed
(
package
)
:
            
pacman_query
=
subprocess
.
run
(
                
[
"
pacman
"
"
-
Q
"
package
]
                
stdout
=
subprocess
.
PIPE
                
stderr
=
subprocess
.
STDOUT
                
check
=
False
            
)
            
if
pacman_query
.
returncode
not
in
[
0
1
]
:
                
raise
Exception
(
                    
f
'
Failed
to
query
pacman
whether
"
{
package
}
"
is
installed
:
"
{
pacman_query
.
stdout
}
"
'
                
)
            
return
pacman_query
.
returncode
=
=
0
        
packages
=
[
p
for
p
in
packages
if
not
is_installed
(
p
)
]
        
if
not
packages
:
            
return
        
command
=
[
"
pacman
"
"
-
S
"
"
-
-
needed
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
noconfirm
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
