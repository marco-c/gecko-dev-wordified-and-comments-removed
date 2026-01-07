import
sys
import
buildconfig
from
mozbuild
.
preprocessor
import
Preprocessor
def
main
(
output
input_file
*
defines
)
:
    
pp
=
Preprocessor
(
)
    
pp
.
context
.
update
(
        
{
            
"
FFI_EXEC_TRAMPOLINE_TABLE
"
:
"
0
"
            
"
HAVE_LONG_DOUBLE
"
:
"
0
"
            
"
TARGET
"
:
buildconfig
.
substs
[
"
FFI_TARGET
"
]
            
"
VERSION
"
:
"
"
        
}
    
)
    
for
d
in
defines
:
        
pp
.
context
.
update
(
{
d
:
"
1
"
}
)
    
pp
.
do_filter
(
"
substitution
"
)
    
pp
.
setMarker
(
None
)
    
pp
.
out
=
output
    
pp
.
do_include
(
input_file
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
*
sys
.
agv
[
1
:
]
)
