from
mozboot
.
base
import
MERCURIAL_INSTALL_PROMPT
BaseBootstrapper
from
mozboot
.
linux_common
import
LinuxBootstrapper
class
OpenSUSEBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
"
"
"
openSUSE
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
openSUSE
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
        
packages
+
=
[
"
awk
"
]
        
self
.
zypper_install
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
        
self
.
zypper_update
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
system
packages
could
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
zypper_install
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
zypper_install
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
    
def
zypper
(
self
*
args
)
:
        
if
self
.
no_interactive
:
            
command
=
[
"
zypper
"
"
-
n
"
*
args
]
        
else
:
            
command
=
[
"
zypper
"
*
args
]
        
self
.
run_as_root
(
command
)
    
def
zypper_install
(
self
*
packages
)
:
        
self
.
zypper
(
"
install
"
*
packages
)
    
def
zypper_update
(
self
*
packages
)
:
        
self
.
zypper
(
"
update
"
*
packages
)
