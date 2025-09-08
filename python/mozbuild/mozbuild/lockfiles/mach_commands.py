from
mach
.
decorators
import
Command
CommandArgument
Command
(
    
"
generate
-
python
-
lockfiles
"
    
category
=
"
misc
"
    
description
=
"
Vendor
third
-
party
dependencies
into
the
source
repository
.
"
    
virtualenv_name
=
"
uv
"
)
CommandArgument
(
    
"
-
-
sites
"
    
dest
=
"
sites
"
    
nargs
=
"
+
"
    
default
=
[
]
    
help
=
"
List
of
site
names
to
generate
lockfiles
for
.
If
this
is
not
specified
lockfiles
for
all
sites
will
be
generated
.
"
)
CommandArgument
(
    
"
-
-
keep
-
lockfiles
"
    
action
=
"
store_true
"
    
dest
=
"
keep_lockfiles
"
    
default
=
False
    
help
=
"
Do
not
delete
generated
lockfiles
on
command
exit
.
"
)
def
generate_python_lockfiles
(
command_context
sites
keep_lockfiles
)
:
    
from
mozbuild
.
lockfiles
.
generate_python_lockfiles
import
GeneratePythonLockfiles
    
command
=
command_context
.
_spawn
(
GeneratePythonLockfiles
)
    
return
command
.
run
(
keep_lockfiles
=
keep_lockfiles
sites
=
sites
)
