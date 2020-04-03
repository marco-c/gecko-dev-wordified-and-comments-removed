from
argparse
import
ArgumentParser
SUPPRESS
import
os
import
mozlog
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
try
:
    
from
mozbuild
.
base
import
MozbuildObject
MachCommandConditions
as
conditions
    
build_obj
=
MozbuildObject
.
from_environment
(
cwd
=
here
)
except
ImportError
:
    
build_obj
=
None
    
conditions
=
None
SUPPORTED_APPS
=
(
"
generic
"
"
android
"
)
class
GenericGroup
:
    
"
"
"
Generic
options
    
"
"
"
    
name
=
"
Generic
"
    
args
=
[
        
[
            
[
"
tests
"
]
            
{
                
"
nargs
"
:
"
*
"
                
"
metavar
"
:
"
TEST
"
                
"
default
"
:
[
]
                
"
help
"
:
"
Test
to
run
.
Can
be
a
single
test
file
or
a
directory
of
tests
"
                
"
(
to
run
recursively
)
.
If
omitted
the
entire
suite
is
run
.
"
            
}
        
]
        
[
            
[
"
-
-
perfherder
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Output
data
in
the
perfherder
format
.
"
            
}
        
]
        
[
            
[
"
-
-
output
"
]
            
{
                
"
type
"
:
str
                
"
default
"
:
"
artifacts
"
                
"
help
"
:
"
Path
to
where
data
will
be
stored
defaults
to
a
top
-
level
"
                
"
artifacts
folder
.
"
            
}
        
]
        
[
            
[
"
-
-
prefix
"
]
            
{
                
"
type
"
:
str
                
"
default
"
:
"
"
                
"
help
"
:
"
Prefix
the
output
files
with
this
string
.
"
            
}
        
]
    
]
    
defaults
=
{
}
class
PerftestArgumentParser
(
ArgumentParser
)
:
    
"
"
"
%
(
prog
)
s
[
options
]
[
test
paths
]
"
"
"
    
def
__init__
(
self
app
=
None
*
*
kwargs
)
:
        
ArgumentParser
.
__init__
(
            
self
usage
=
self
.
__doc__
conflict_handler
=
"
resolve
"
*
*
kwargs
        
)
        
self
.
groups
=
[
GenericGroup
]
        
self
.
oldcwd
=
os
.
getcwd
(
)
        
self
.
app
=
app
        
if
not
self
.
app
and
build_obj
:
            
if
conditions
.
is_android
(
build_obj
)
:
                
self
.
app
=
"
android
"
        
if
not
self
.
app
:
            
self
.
app
=
"
generic
"
        
if
self
.
app
not
in
SUPPORTED_APPS
:
            
self
.
error
(
                
"
Unrecognized
app
'
{
}
'
!
Must
be
one
of
:
{
}
"
.
format
(
                    
self
.
app
"
"
.
join
(
SUPPORTED_APPS
)
                
)
            
)
        
defaults
=
{
}
        
for
klass
in
self
.
groups
:
            
defaults
.
update
(
klass
.
defaults
)
            
group
=
self
.
add_argument_group
(
klass
.
name
klass
.
__doc__
)
            
for
cli
kwargs
in
klass
.
args
:
                
if
"
default
"
in
kwargs
and
isinstance
(
kwargs
[
"
default
"
]
list
)
:
                    
kwargs
[
"
default
"
]
=
[
]
                
if
"
suppress
"
in
kwargs
:
                    
if
kwargs
[
"
suppress
"
]
:
                        
kwargs
[
"
help
"
]
=
SUPPRESS
                    
del
kwargs
[
"
suppress
"
]
                
group
.
add_argument
(
*
cli
*
*
kwargs
)
        
self
.
set_defaults
(
*
*
defaults
)
        
mozlog
.
commandline
.
add_logging_group
(
self
)
