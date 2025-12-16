import
subprocess
import
sys
import
mozunit
from
buildconfig
import
topsrcdir
def
test_sites_compatible
(
tmpdir
:
str
)
:
    
result
=
subprocess
.
run
(
        
[
sys
.
executable
"
mach
"
"
generate
-
python
-
lockfiles
"
]
        
check
=
False
        
stdout
=
subprocess
.
PIPE
        
stderr
=
subprocess
.
STDOUT
        
cwd
=
topsrcdir
        
text
=
True
    
)
    
print
(
result
.
stdout
)
    
assert
result
.
returncode
=
=
0
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
