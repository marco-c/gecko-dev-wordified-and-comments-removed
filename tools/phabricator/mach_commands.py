from
__future__
import
absolute_import
unicode_literals
import
mozfile
from
mach
.
decorators
import
Command
CommandArgument
from
mach
.
site
import
MozSiteMetadata
Command
(
    
"
install
-
moz
-
phab
"
    
category
=
"
misc
"
    
description
=
"
Install
patch
submission
tool
.
"
)
CommandArgument
(
    
"
-
-
force
"
    
"
-
f
"
    
action
=
"
store_true
"
    
help
=
"
Force
installation
even
if
already
installed
.
"
)
def
install_moz_phab
(
command_context
force
=
False
)
:
    
import
logging
    
import
os
    
import
re
    
import
subprocess
    
import
sys
    
existing
=
mozfile
.
which
(
"
moz
-
phab
"
)
    
if
existing
and
not
force
:
        
command_context
.
log
(
            
logging
.
ERROR
            
"
already_installed
"
            
{
}
            
"
moz
-
phab
is
already
installed
in
%
s
.
"
%
existing
        
)
        
sys
.
exit
(
1
)
    
active_metadata
=
MozSiteMetadata
.
from_runtime
(
)
    
original_python
=
active_metadata
.
original_python
.
python_path
    
is_external_python_virtualenv
=
(
        
subprocess
.
check_output
(
            
[
                
original_python
                
"
-
c
"
                
"
import
sys
;
print
(
sys
.
prefix
!
=
sys
.
base_prefix
)
"
            
]
        
)
.
strip
(
)
        
=
=
b
"
True
"
    
)
    
has_pip
=
subprocess
.
run
(
[
original_python
"
-
c
"
"
import
pip
"
]
)
.
returncode
=
=
0
    
if
not
has_pip
:
        
command_context
.
log
(
            
logging
.
ERROR
            
"
pip_not_installed
"
            
{
}
            
"
Python
3
'
s
pip
is
not
installed
.
Try
installing
it
with
your
system
"
            
"
package
manager
.
"
        
)
        
sys
.
exit
(
1
)
    
command
=
[
original_python
"
-
m
"
"
pip
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
MozPhab
"
]
    
if
(
        
sys
.
platform
.
startswith
(
"
linux
"
)
        
or
sys
.
platform
.
startswith
(
"
openbsd
"
)
        
or
sys
.
platform
.
startswith
(
"
dragonfly
"
)
        
or
sys
.
platform
.
startswith
(
"
freebsd
"
)
    
)
:
        
platform_prefers_user_install
=
True
    
elif
sys
.
platform
.
startswith
(
"
darwin
"
)
:
        
platform_prefers_user_install
=
False
    
elif
sys
.
platform
.
startswith
(
"
win32
"
)
or
sys
.
platform
.
startswith
(
"
msys
"
)
:
        
platform_prefers_user_install
=
False
    
else
:
        
command_context
.
log
(
            
logging
.
WARNING
            
"
unsupported_platform
"
            
{
}
            
"
Unsupported
platform
(
%
s
)
assuming
per
-
user
installation
is
"
            
"
preferred
.
"
%
sys
.
platform
        
)
        
platform_prefers_user_install
=
True
    
if
platform_prefers_user_install
and
not
is_external_python_virtualenv
:
        
command
.
append
(
"
-
-
user
"
)
    
command_context
.
log
(
logging
.
INFO
"
run
"
{
}
"
Installing
moz
-
phab
"
)
    
subprocess
.
run
(
command
)
    
info
=
subprocess
.
check_output
(
        
[
original_python
"
-
m
"
"
pip
"
"
show
"
"
-
f
"
"
MozPhab
"
]
        
universal_newlines
=
True
    
)
    
mozphab_package_location
=
re
.
compile
(
r
"
Location
:
(
.
*
)
"
)
.
search
(
info
)
.
group
(
1
)
    
potential_cli_paths
=
re
.
compile
(
        
r
"
(
[
^
\
s
]
*
moz
-
phab
(
?
:
\
.
exe
)
?
)
"
re
.
MULTILINE
    
)
.
findall
(
info
)
    
if
len
(
potential_cli_paths
)
!
=
1
:
        
command_context
.
log
(
            
logging
.
WARNING
            
"
no_mozphab_console_script
"
            
{
}
            
"
Could
not
find
the
CLI
script
for
moz
-
phab
.
Skipping
install
-
certificate
step
.
"
        
)
        
sys
.
exit
(
1
)
    
console_script
=
os
.
path
.
realpath
(
        
os
.
path
.
join
(
mozphab_package_location
potential_cli_paths
[
0
]
)
    
)
    
subprocess
.
run
(
[
console_script
"
install
-
certificate
"
]
)
