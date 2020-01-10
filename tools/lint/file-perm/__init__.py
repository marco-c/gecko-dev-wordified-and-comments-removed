import
os
import
platform
from
mozlint
import
result
from
mozlint
.
pathutils
import
expand_exclusions
results
=
[
]
def
lint
(
paths
config
fix
=
None
*
*
lintargs
)
:
    
if
platform
.
system
(
)
=
=
'
Windows
'
:
        
return
results
    
files
=
list
(
expand_exclusions
(
paths
config
lintargs
[
'
root
'
]
)
)
    
for
f
in
files
:
        
if
os
.
access
(
f
os
.
X_OK
)
:
            
with
open
(
f
'
r
+
'
)
as
content
:
                
line
=
content
.
readline
(
)
                
if
line
.
startswith
(
"
#
!
"
)
:
                    
continue
            
if
fix
:
                
os
.
chmod
(
f
0o644
)
                
continue
            
res
=
{
'
path
'
:
f
                   
'
message
'
:
"
Execution
permissions
on
a
source
file
"
                   
'
level
'
:
'
error
'
                   
}
            
results
.
append
(
result
.
from_config
(
config
*
*
res
)
)
    
return
results
