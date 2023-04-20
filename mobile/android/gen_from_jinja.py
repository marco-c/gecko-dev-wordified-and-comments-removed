from
__future__
import
absolute_import
print_function
import
os
from
jinja2
import
Environment
FileSystemLoader
StrictUndefined
def
main
(
output_fd
input_filename
*
args
)
:
    
(
path
leaf
)
=
os
.
path
.
split
(
input_filename
)
    
env
=
Environment
(
        
loader
=
FileSystemLoader
(
path
encoding
=
"
utf
-
8
"
)
        
autoescape
=
True
        
undefined
=
StrictUndefined
    
)
    
tpl
=
env
.
get_template
(
leaf
)
    
context
=
dict
(
)
    
for
arg
in
args
:
        
(
k
v
)
=
arg
.
split
(
"
=
"
1
)
        
context
[
k
]
=
v
    
tpl
.
stream
(
context
)
.
dump
(
output_fd
encoding
=
"
utf
-
8
"
)
