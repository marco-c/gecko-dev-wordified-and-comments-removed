import
argparse
import
importlib
.
util
import
os
import
sys
import
traceback
import
buildconfig
from
mozbuild
.
logging
import
serialize_root_logger
from
mozbuild
.
makeutil
import
Makefile
from
mozbuild
.
pythonutil
import
iter_modules_in_path
from
mozbuild
.
util
import
FileAvoidWrite
def
main
(
argv
)
:
    
serialize_root_logger
(
)
    
parser
=
argparse
.
ArgumentParser
(
        
"
Generate
a
file
from
a
Python
script
"
add_help
=
False
    
)
    
parser
.
add_argument
(
        
"
-
-
locale
"
metavar
=
"
locale
"
type
=
str
help
=
"
The
locale
in
use
.
"
    
)
    
parser
.
add_argument
(
        
"
python_script
"
        
metavar
=
"
python
-
script
"
        
type
=
str
        
help
=
"
The
Python
script
to
run
"
    
)
    
parser
.
add_argument
(
        
"
method_name
"
        
metavar
=
"
method
-
name
"
        
type
=
str
        
help
=
"
The
method
of
the
script
to
invoke
"
    
)
    
parser
.
add_argument
(
        
"
output_file
"
        
metavar
=
"
output
-
file
"
        
type
=
str
        
help
=
"
The
file
to
generate
"
    
)
    
parser
.
add_argument
(
        
"
dep_file
"
        
metavar
=
"
dep
-
file
"
        
type
=
str
        
help
=
"
File
to
write
any
additional
make
dependencies
to
"
    
)
    
parser
.
add_argument
(
        
"
dep_target
"
        
metavar
=
"
dep
-
target
"
        
type
=
str
        
help
=
"
Make
target
to
use
in
the
dependencies
file
"
    
)
    
parser
.
add_argument
(
        
"
additional_arguments
"
        
metavar
=
"
arg
"
        
nargs
=
argparse
.
REMAINDER
        
help
=
"
Additional
arguments
to
the
script
'
s
main
(
)
method
"
    
)
    
args
=
parser
.
parse_args
(
argv
)
    
kwargs
=
{
}
    
if
args
.
locale
:
        
kwargs
[
"
locale
"
]
=
args
.
locale
    
script
=
args
.
python_script
    
sys
.
path
.
append
(
os
.
path
.
dirname
(
script
)
)
    
spec
=
importlib
.
util
.
spec_from_file_location
(
"
script
"
script
)
    
module
=
importlib
.
util
.
module_from_spec
(
spec
)
    
spec
.
loader
.
exec_module
(
module
)
    
method
=
args
.
method_name
    
if
not
hasattr
(
module
method
)
:
        
print
(
            
f
'
Error
:
script
"
{
script
}
"
is
missing
a
{
method
}
method
'
            
file
=
sys
.
stderr
        
)
        
return
1
    
ret
=
1
    
try
:
        
with
FileAvoidWrite
(
args
.
output_file
readmode
=
"
rb
"
)
as
output
:
            
try
:
                
ret
=
module
.
__dict__
[
method
]
(
                    
output
*
args
.
additional_arguments
*
*
kwargs
                
)
            
except
Exception
:
                
output
.
avoid_writing_to_file
(
)
                
raise
            
if
isinstance
(
ret
set
)
:
                
deps
=
ret
                
ret
=
None
            
else
:
                
deps
=
set
(
)
            
if
not
ret
:
                
deps
|
=
set
(
                    
s
                    
for
s
in
iter_modules_in_path
(
                        
buildconfig
.
topsrcdir
buildconfig
.
topobjdir
                    
)
                
)
                
deps
|
=
set
(
buildconfig
.
get_dependencies
(
)
)
                
mk
=
Makefile
(
)
                
mk
.
create_rule
(
[
args
.
dep_target
]
)
.
add_dependencies
(
deps
)
                
with
FileAvoidWrite
(
args
.
dep_file
)
as
dep_file
:
                    
mk
.
dump
(
dep_file
)
            
else
:
                
output
.
avoid_writing_to_file
(
)
    
except
OSError
as
e
:
        
print
(
f
'
Error
opening
file
"
{
e
.
filename
}
"
'
file
=
sys
.
stderr
)
        
traceback
.
print_exc
(
)
        
return
1
    
return
ret
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
sys
.
argv
[
1
:
]
)
)
