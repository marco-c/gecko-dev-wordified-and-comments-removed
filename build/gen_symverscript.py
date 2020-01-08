import
sys
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
version
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
        
'
VERSION
'
:
version
    
}
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
'
__main__
'
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
