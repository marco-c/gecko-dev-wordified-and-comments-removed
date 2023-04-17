from
__future__
import
absolute_import
unicode_literals
import
os
import
sys
from
mach
.
decorators
import
(
    
CommandArgument
    
CommandProvider
    
Command
)
from
mozbuild
.
base
import
MachCommandBase
from
mozbuild
.
util
import
mkdir
def
get_test_parser
(
)
:
    
import
runtests
    
return
runtests
.
get_parser
CommandProvider
class
WebIDLProvider
(
MachCommandBase
)
:
    
Command
(
        
"
webidl
-
example
"
        
category
=
"
misc
"
        
description
=
"
Generate
example
files
for
a
WebIDL
interface
.
"
    
)
    
CommandArgument
(
        
"
interface
"
nargs
=
"
+
"
help
=
"
Interface
(
s
)
whose
examples
to
generate
.
"
    
)
    
def
webidl_example
(
self
command_context
interface
)
:
        
from
mozwebidlcodegen
import
BuildSystemWebIDL
        
manager
=
command_context
.
_spawn
(
BuildSystemWebIDL
)
.
manager
        
for
i
in
interface
:
            
manager
.
generate_example_files
(
i
)
    
Command
(
        
"
webidl
-
parser
-
test
"
        
category
=
"
testing
"
        
parser
=
get_test_parser
        
description
=
"
Run
WebIDL
tests
(
Interface
Browser
parser
)
.
"
    
)
    
def
webidl_test
(
self
command_context
*
*
kwargs
)
:
        
sys
.
path
.
insert
(
            
0
os
.
path
.
join
(
command_context
.
topsrcdir
"
other
-
licenses
"
"
ply
"
)
        
)
        
mkdir
(
command_context
.
topobjdir
)
        
os
.
chdir
(
command_context
.
topobjdir
)
        
if
kwargs
[
"
verbose
"
]
is
None
:
            
kwargs
[
"
verbose
"
]
=
False
        
sys
.
path
.
insert
(
0
command_context
.
topobjdir
)
        
import
runtests
        
return
runtests
.
run_tests
(
kwargs
[
"
tests
"
]
verbose
=
kwargs
[
"
verbose
"
]
)
