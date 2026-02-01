import
os
import
sys
from
unittest
.
mock
import
patch
from
mach
.
requirements
import
MachEnvRequirements
PthSpecifier
from
mach
.
site
import
CommandSiteManager
MachSiteManager
def
main
(
)
:
    
topsrcdir
=
os
.
environ
[
"
TOPSRCDIR
"
]
    
command_site
=
os
.
environ
[
"
COMMAND_SITE
"
]
    
mach_site_requirements
=
os
.
environ
[
"
MACH_SITE_PTH_REQUIREMENTS
"
]
    
command_site_requirements
=
os
.
environ
[
"
COMMAND_SITE_PTH_REQUIREMENTS
"
]
    
work_dir
=
os
.
environ
[
"
WORK_DIR
"
]
    
def
resolve_requirements
(
topsrcdir
site_name
)
:
        
req
=
MachEnvRequirements
(
)
        
if
site_name
=
=
"
mach
"
:
            
req
.
pth_requirements
=
[
                
PthSpecifier
(
path
)
for
path
in
mach_site_requirements
.
split
(
os
.
pathsep
)
            
]
        
else
:
            
req
.
pth_requirements
=
[
PthSpecifier
(
command_site_requirements
)
]
        
return
req
    
with
patch
(
"
mach
.
site
.
resolve_requirements
"
resolve_requirements
)
:
        
initial_sys_path
=
sys
.
path
.
copy
(
)
        
mach_site
=
MachSiteManager
.
from_environment
(
            
topsrcdir
            
lambda
:
work_dir
        
)
        
mach_site
.
activate
(
)
        
mach_sys_path
=
sys
.
path
.
copy
(
)
        
command_site
=
CommandSiteManager
.
from_environment
(
            
topsrcdir
lambda
:
work_dir
command_site
work_dir
        
)
        
command_site
.
activate
(
)
        
command_sys_path
=
sys
.
path
.
copy
(
)
    
print
(
[
        
initial_sys_path
        
mach_sys_path
        
command_sys_path
    
]
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
