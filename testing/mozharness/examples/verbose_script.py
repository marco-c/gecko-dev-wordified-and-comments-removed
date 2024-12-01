"
"
"
verbose_script
.
py
Contrast
to
silent_script
.
py
.
"
"
"
import
os
import
sys
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
sys
.
path
[
0
]
)
)
from
mozharness
.
base
.
script
import
BaseScript
class
VerboseExample
(
BaseScript
)
:
    
def
__init__
(
self
require_config_file
=
False
)
:
        
super
(
VerboseExample
self
)
.
__init__
(
            
all_actions
=
[
                
"
verbosity
"
            
]
            
require_config_file
=
require_config_file
            
config
=
{
"
tarball_name
"
:
"
bar
.
tar
.
xz
"
}
        
)
    
def
verbosity
(
self
)
:
        
tarball_name
=
self
.
config
[
"
tarball_name
"
]
        
self
.
download_file
(
            
"
http
:
/
/
people
.
mozilla
.
org
/
~
asasaki
/
foo
.
tar
.
xz
"
file_name
=
tarball_name
        
)
        
self
.
run_command
(
            
[
"
tar
"
"
xJvf
"
tarball_name
]
        
)
        
self
.
rmtree
(
"
x
/
ship2
"
)
        
self
.
rmtree
(
tarball_name
)
        
self
.
run_command
(
            
[
"
tar
"
"
cJvf
"
tarball_name
"
x
"
]
        
)
        
self
.
rmtree
(
"
x
"
)
        
if
self
.
run_command
(
            
[
"
scp
"
tarball_name
"
people
.
mozilla
.
org
:
public_html
/
foo2
.
tar
.
xz
"
]
        
)
:
            
self
.
error
(
                
"
There
'
s
been
a
problem
with
the
scp
.
We
'
re
going
to
proceed
anyway
.
"
            
)
        
self
.
rmtree
(
tarball_name
)
if
__name__
=
=
"
__main__
"
:
    
verbose_example
=
VerboseExample
(
)
    
verbose_example
.
run_and_exit
(
)
