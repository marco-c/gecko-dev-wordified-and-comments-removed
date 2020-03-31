from
__future__
import
absolute_import
unicode_literals
from
mach
.
decorators
import
CommandProvider
Command
CommandArgument
from
mozbuild
.
base
import
MachCommandBase
CommandProvider
class
PhabricatorCommandProvider
(
MachCommandBase
)
:
    
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
self
force
=
False
)
:
        
import
logging
        
import
shutil
        
import
subprocess
        
import
sys
        
existing
=
shutil
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
            
self
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
        
if
not
shutil
.
which
(
"
pip3
"
)
:
            
self
.
log
(
                
logging
.
ERROR
                
"
pip3_not_installed
"
                
{
}
                
"
pip3
is
not
installed
.
Try
running
mach
bootstrap
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
            
pass
        
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
            
pass
        
else
:
            
self
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
.
"
                
%
sys
.
platform
            
)
            
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
        
self
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
