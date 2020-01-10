from
__future__
import
absolute_import
print_function
unicode_literals
from
taskgraph
.
transforms
.
base
import
TransformSequence
transforms
=
TransformSequence
(
)
transforms
.
add
def
use_toolchains
(
config
jobs
)
:
    
"
"
"
Transform
toolchains
definitions
into
the
corresponding
fetch
    
definitions
.
    
"
"
"
    
for
job
in
jobs
:
        
toolchains
=
job
.
pop
(
'
toolchains
'
None
)
        
if
toolchains
:
            
job
.
setdefault
(
'
fetches
'
{
}
)
\
               
.
setdefault
(
'
toolchain
'
[
]
)
\
               
.
extend
(
toolchains
)
        
yield
job
