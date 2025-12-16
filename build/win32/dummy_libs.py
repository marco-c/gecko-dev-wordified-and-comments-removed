import
os
import
subprocess
from
buildconfig
import
substs
def
main
(
output
*
other_libs
)
:
    
output
.
close
(
)
    
os
.
unlink
(
output
.
name
)
    
libs
=
[
output
.
name
]
    
parent
=
os
.
path
.
dirname
(
output
.
name
)
    
libs
.
extend
(
os
.
path
.
join
(
parent
l
)
for
l
in
other_libs
)
    
for
lib
in
libs
:
        
result
=
subprocess
.
run
(
            
[
substs
[
"
AR
"
]
]
+
[
f
.
replace
(
"
"
lib
)
for
f
in
substs
[
"
AR_FLAGS
"
]
]
            
check
=
False
        
)
        
if
result
.
returncode
!
=
0
:
            
return
result
.
returncode
    
return
0
