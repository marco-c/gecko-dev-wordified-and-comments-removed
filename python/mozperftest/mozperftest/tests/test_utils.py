import
sys
import
mozunit
from
mozperftest
.
utils
import
host_platform
silence
def
test_silence
(
)
:
    
with
silence
(
)
:
        
print
(
"
HIDDEN
"
)
def
test_host_platform
(
)
:
    
plat
=
host_platform
(
)
    
if
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
        
assert
plat
=
=
"
darwin
"
    
else
:
        
if
sys
.
maxsize
>
2
*
*
32
:
            
assert
"
64
"
in
plat
        
else
:
            
assert
"
64
"
not
in
plat
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
