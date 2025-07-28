"
"
"
Deploys
packages
and
runs
an
FFX
command
on
a
Fuchsia
target
.
"
"
"
import
argparse
import
logging
import
os
import
pkg_repo
import
shlex
import
sys
import
tempfile
import
time
from
common_args
import
AddCommonArgs
AddTargetSpecificArgs
\
                        
ConfigureLogging
GetDeploymentTargetForArgs
def
main
(
)
:
  
parser
=
argparse
.
ArgumentParser
(
)
  
logging
.
getLogger
(
)
.
setLevel
(
logging
.
INFO
)
  
parser
.
add_argument
(
'
-
-
command
'
                      
required
=
True
                      
help
=
'
FFX
command
to
run
.
Runtime
arguments
are
handled
'
                      
'
using
the
%
%
args
%
%
placeholder
.
'
)
  
parser
.
add_argument
(
'
child_args
'
                      
nargs
=
'
*
'
                      
help
=
'
Arguments
for
the
command
.
'
)
  
AddCommonArgs
(
parser
)
  
AddTargetSpecificArgs
(
parser
)
  
args
=
parser
.
parse_args
(
)
  
ffx_args
=
shlex
.
split
(
args
.
command
)
  
try
:
    
args_index
=
ffx_args
.
index
(
'
%
args
%
'
)
    
ffx_args
[
args_index
:
args_index
+
1
]
=
args
.
child_args
  
except
ValueError
:
    
pass
  
with
GetDeploymentTargetForArgs
(
args
)
as
target
:
    
target
.
Start
(
)
    
target
.
StartSystemLog
(
args
.
package
)
    
with
target
.
GetPkgRepo
(
)
as
pkg_repo
:
      
target
.
InstallPackage
(
args
.
package
)
      
process
=
target
.
RunFFXCommand
(
ffx_args
)
      
logging
.
info
(
'
Command
is
now
running
.
Press
CTRL
-
C
to
exit
.
'
)
      
try
:
        
while
True
:
          
time
.
sleep
(
1
)
      
except
KeyboardInterrupt
:
        
pass
  
return
0
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
)
)
