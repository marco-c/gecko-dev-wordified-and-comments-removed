"
"
"
Implements
the
command
line
interface
.
"
"
"
from
__future__
import
absolute_import
from
__future__
import
unicode_literals
import
sys
from
os
import
path
import
argparse
from
commands
import
InitCommand
ExportCommand
ImportCommand
CommandError
from
env
import
IncompleteEnvironment
EnvironmentError
Environment
from
config
import
Config
from
utils
import
Writer
if
hasattr
(
argparse
'
__version__
'
)
and
argparse
.
__version__
<
'
1
.
1
'
:
    
raise
RuntimeError
(
'
Needs
at
least
argparse
1
.
1
to
function
you
are
using
:
%
s
'
%
argparse
.
__version__
)
__all__
=
(
'
main
'
'
run
'
)
COMMANDS
=
{
    
'
init
'
:
InitCommand
    
'
export
'
:
ExportCommand
    
'
import
'
:
ImportCommand
}
def
parse_args
(
argv
)
:
    
"
"
"
Builds
an
argument
parser
based
on
all
commands
and
configuration
    
values
that
we
support
.
    
"
"
"
    
parser
=
argparse
.
ArgumentParser
(
        
add_help
=
True
        
description
=
'
Convert
Android
string
resources
to
gettext
.
po
files
an
import
them
back
.
'
        
epilog
=
'
Written
by
:
Michael
Elsdoerfer
<
michael
elsdoerfer
.
com
>
'
    
)
    
parser
.
add_argument
(
'
-
-
version
'
action
=
'
version
'
version
=
"
moz1
"
)
    
base_parser
=
argparse
.
ArgumentParser
(
add_help
=
False
)
    
group
=
base_parser
.
add_mutually_exclusive_group
(
)
    
group
.
add_argument
(
'
-
-
verbose
'
'
-
v
'
action
=
'
store_true
'
help
=
'
be
extra
verbose
'
)
    
group
.
add_argument
(
'
-
-
quiet
'
'
-
q
'
action
=
'
store_true
'
help
=
'
be
extra
quiet
'
)
    
base_parser
.
add_argument
(
'
-
-
config
'
'
-
c
'
metavar
=
'
FILE
'
help
=
'
config
file
to
use
'
)
    
group
=
base_parser
.
add_argument_group
(
        
'
configuration
'
        
'
Those
can
also
be
specified
in
a
configuration
file
.
If
given
'
        
'
here
values
from
the
configuration
file
will
be
overwritten
.
'
    
)
    
Config
.
setup_arguments
(
group
)
    
subparsers
=
parser
.
add_subparsers
(
        
dest
=
"
command
"
title
=
'
commands
'
description
=
'
valid
commands
'
help
=
'
additional
help
'
    
)
    
for
name
cmdclass
in
list
(
COMMANDS
.
items
(
)
)
:
        
cmd_parser
=
subparsers
.
add_parser
(
name
parents
=
[
base_parser
]
add_help
=
True
)
        
group
=
cmd_parser
.
add_argument_group
(
'
command
arguments
'
)
        
cmdclass
.
setup_arg_parser
(
group
)
    
return
parser
.
parse_args
(
argv
[
1
:
]
)
def
read_config
(
in_file
)
:
    
"
"
"
Read
the
config
file
in
file
.
    
file
may
either
be
a
file
object
or
a
filename
.
    
The
config
file
currently
is
simply
a
file
with
command
line
options
    
each
option
on
a
separate
line
.
    
Just
for
reference
purposes
the
following
ticket
should
be
noted
    
which
intends
to
extend
argparse
with
support
for
configuration
files
:
        
http
:
/
/
code
.
google
.
com
/
p
/
argparse
/
issues
/
detail
?
id
=
35
    
Note
however
that
the
current
patch
doesn
'
t
seem
to
provide
an
easy
    
way
to
make
paths
in
the
config
relative
to
the
config
file
location
    
as
we
currently
need
.
    
"
"
"
    
if
hasattr
(
in_file
'
read
'
)
:
        
lines
=
in_file
.
readlines
(
)
        
if
hasattr
(
in_file
'
name
'
)
:
            
filename
=
in_file
.
name
        
else
:
            
filename
=
None
    
else
:
        
filename
=
in_file
        
f
=
open
(
in_file
'
rb
'
)
        
try
:
            
lines
=
f
.
readlines
(
)
        
finally
:
            
f
.
close
(
)
    
args
=
filter
(
lambda
x
:
bool
(
x
)
                  
[
i
.
strip
(
)
for
i
in
                   
"
"
.
join
(
filter
(
lambda
x
:
not
x
.
strip
(
)
.
startswith
(
'
#
'
)
                                   
lines
)
                            
)
.
split
(
"
"
)
]
)
    
parser
=
argparse
.
ArgumentParser
(
add_help
=
False
)
    
Config
.
setup_arguments
(
parser
)
    
config
unprocessed
=
parser
.
parse_known_args
(
args
)
    
if
unprocessed
:
        
raise
CommandError
(
"
unsupported
config
values
:
%
s
"
%
'
'
.
join
(
unprocessed
)
)
    
if
filename
:
        
Config
.
rebase_paths
(
config
path
.
dirname
(
filename
)
)
    
return
config
def
make_env_and_writer
(
argv
)
:
    
"
"
"
Given
the
command
line
arguments
in
argv
construct
an
    
environment
.
    
This
entails
everything
from
parsing
the
command
line
parsing
    
a
config
file
if
there
is
one
merging
the
two
etc
.
    
Returns
a
2
-
tuple
(
Environment
instance
Writer
instance
)
.
    
"
"
"
    
options
=
parse_args
(
argv
)
    
writer
=
Writer
(
)
    
if
options
.
verbose
:
        
writer
.
verbosity
=
3
    
elif
options
.
quiet
:
        
writer
.
verbosity
=
1
    
else
:
        
writer
.
verbosity
=
2
    
env
=
Environment
(
writer
)
    
config_file
=
None
    
if
options
.
config
:
        
config_file
=
options
.
config
        
env
.
config_file
=
config_file
    
elif
env
.
config_file
:
        
config_file
=
env
.
config_file
        
writer
.
action
(
'
info
'
"
Using
auto
-
detected
config
file
:
%
s
"
%
config_file
)
    
if
config_file
:
        
env
.
pop_from_config
(
read_config
(
config_file
)
)
    
env
.
pop_from_options
(
options
)
    
env
.
auto_paths
(
)
    
if
env
.
auto_gettext_dir
or
env
.
auto_resource_dir
:
        
writer
.
action
(
'
info
'
                      
"
Assuming
default
directory
structure
in
%
s
"
%
env
.
project_dir
)
    
try
:
        
env
.
init
(
)
    
except
IncompleteEnvironment
:
        
if
not
env
.
project_dir
:
            
if
not
env
.
config_file
:
                
raise
CommandError
(
'
You
need
to
run
this
from
inside
an
'
                                   
'
Android
project
directory
or
specify
the
source
and
'
                                   
'
target
directories
manually
either
as
command
line
'
                                   
'
options
or
through
a
configuration
file
'
)
            
else
:
                
raise
CommandError
(
'
Your
configuration
file
does
not
specify
'
                                   
'
the
source
and
target
directory
and
you
are
not
running
'
                                   
'
the
script
from
inside
an
Android
project
directory
.
'
)
    
except
EnvironmentError
as
e
:
        
raise
CommandError
(
e
)
    
writer
.
action
(
'
info
'
                  
"
Using
as
Android
resource
dir
:
%
s
"
%
env
.
resource_dir
)
    
writer
.
action
(
'
info
'
"
Using
as
gettext
dir
:
%
s
"
%
env
.
gettext_dir
)
    
return
env
writer
def
main
(
argv
)
:
    
"
"
"
The
program
.
    
Returns
an
error
code
or
None
.
    
"
"
"
    
try
:
        
env
writer
=
make_env_and_writer
(
argv
)
        
try
:
            
cmd
=
COMMANDS
[
env
.
options
.
command
]
(
env
writer
)
            
cmd
.
execute
(
)
        
finally
:
            
writer
.
finish
(
)
        
if
writer
.
erroneous
:
            
return
1
        
return
0
    
except
CommandError
as
e
:
        
print
(
'
Error
:
'
e
)
        
return
2
def
run
(
)
:
    
"
"
"
Simplified
interface
to
main
(
)
.
    
"
"
"
    
sys
.
exit
(
main
(
sys
.
argv
)
or
0
)
