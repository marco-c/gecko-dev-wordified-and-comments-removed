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
    
results
=
[
]
    
fixed
=
0
    
if
platform
.
system
(
)
=
=
"
Windows
"
:
        
return
{
"
results
"
:
results
"
fixed
"
:
fixed
}
    
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
"
root
"
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
            
if
config
.
get
(
"
allow
-
shebang
"
)
:
                
with
open
(
f
"
r
+
"
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
                
fixed
+
=
1
                
continue
            
res
=
{
                
"
path
"
:
f
                
"
message
"
:
"
Execution
permissions
on
a
source
file
"
                
"
level
"
:
"
error
"
            
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
{
"
results
"
:
results
"
fixed
"
:
fixed
}
