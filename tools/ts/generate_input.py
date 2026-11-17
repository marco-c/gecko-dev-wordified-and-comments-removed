import
sys
from
types
import
SimpleNamespace
SUBSTS
=
{
    
"
MOZ_UPDATE_CHANNEL
"
:
"
default
"
}
def
main
(
topsrcdir
topobjdir
*
args
)
:
    
sys
.
modules
[
"
buildconfig
"
]
=
SimpleNamespace
(
        
topsrcdir
=
topsrcdir
        
topobjdir
=
topobjdir
        
defines
=
{
}
        
substs
=
SUBSTS
        
get_dependencies
=
lambda
:
[
]
    
)
    
from
mozbuild
.
action
import
file_generate
    
return
file_generate
.
main
(
list
(
args
)
)
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
*
sys
.
argv
[
1
:
]
)
)
