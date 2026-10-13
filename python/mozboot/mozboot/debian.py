import
subprocess
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
DebianBootstrapper
(
LinuxBootstrapper
BaseBootstrapper
)
:
    
def
__init__
(
self
distro
version
dist_id
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
distro
=
distro
        
self
.
version
=
version
        
self
.
dist_id
=
dist_id
    
def
install_packages
(
self
packages
)
:
        
try
:
            
if
int
(
self
.
version
)
<
11
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
        
except
ValueError
:
            
pass
        
self
.
apt_install
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
apt_update
(
)
    
def
_check_packages_installed
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
dpkg
-
query
"
"
-
W
"
"
-
f
=
{
db
:
Status
-
Status
}
\
n
"
]
        
command
.
extend
(
packages
)
        
result
=
subprocess
.
run
(
            
command
            
check
=
False
            
stdout
=
subprocess
.
PIPE
            
stderr
=
subprocess
.
DEVNULL
            
text
=
True
        
)
        
return
result
.
returncode
=
=
0
and
all
(
            
status
=
=
"
installed
"
for
status
in
result
.
stdout
.
split
(
)
        
)
    
def
apt_install
(
self
*
packages
)
:
        
if
self
.
_check_packages_installed
(
*
packages
)
:
            
return
        
command
=
[
"
apt
-
get
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
apt_update
(
self
)
:
        
command
=
[
"
apt
-
get
"
"
update
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
        
self
.
run_as_root
(
command
)
