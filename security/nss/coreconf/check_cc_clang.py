import
os
import
subprocess
import
sys
def
main
(
)
:
    
if
sys
.
platform
=
=
'
win32
'
:
        
print
(
0
)
    
else
:
        
cc
=
os
.
environ
.
get
(
'
CC
'
'
cc
'
)
        
try
:
            
cc_is_clang
=
'
clang
'
in
subprocess
.
check_output
(
              
[
cc
'
-
-
version
'
]
universal_newlines
=
True
)
        
except
OSError
:
            
cc_is_clang
=
False
        
print
(
int
(
cc_is_clang
)
)
if
__name__
=
=
'
__main__
'
:
    
main
(
)
