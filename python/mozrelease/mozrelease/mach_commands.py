#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
print_function
unicode_literals
import
sys
import
logging
from
mach
.
decorators
import
(
    
CommandArgument
    
CommandProvider
    
Command
    
SubCommand
)
from
mozbuild
.
base
import
MachCommandBase
from
mozilla_version
.
gecko
import
GeckoVersion
CommandProvider
class
MachCommands
(
MachCommandBase
)
:
    
Command
(
'
release
'
category
=
"
release
"
             
description
=
"
Task
that
are
part
of
the
release
process
.
"
)
    
def
release
(
self
)
:
        
"
"
"
        
The
release
subcommands
all
relate
to
the
release
process
.
        
"
"
"
    
SubCommand
(
'
release
'
'
buglist
'
                
description
=
"
Generate
list
of
bugs
since
the
last
release
.
"
)
    
CommandArgument
(
'
-
-
version
'
                     
required
=
True
                     
type
=
GeckoVersion
.
parse
                     
help
=
"
The
version
being
built
.
"
)
    
CommandArgument
(
'
-
-
product
'
                     
required
=
True
                     
help
=
"
The
product
being
built
.
"
)
    
CommandArgument
(
'
-
-
revision
'
                     
required
=
True
                     
help
=
"
The
revision
being
built
.
"
)
    
def
buglist
(
self
version
product
revision
)
:
        
self
.
setup_logging
(
)
        
from
mozrelease
.
buglist_creator
import
create_bugs_url
        
print
(
create_bugs_url
(
            
product
=
product
            
current_version
=
version
            
current_revision
=
revision
        
)
)
    
def
setup_logging
(
self
quiet
=
False
verbose
=
True
)
:
        
"
"
"
        
Set
up
Python
logging
for
all
loggers
sending
results
to
stderr
(
so
        
that
command
output
can
be
redirected
easily
)
and
adding
the
typical
        
mach
timestamp
.
        
"
"
"
        
old
=
self
.
log_manager
.
replace_terminal_handler
(
None
)
        
if
not
quiet
:
            
level
=
logging
.
DEBUG
if
verbose
else
logging
.
INFO
            
self
.
log_manager
.
add_terminal_logging
(
                
fh
=
sys
.
stderr
level
=
level
                
write_interval
=
old
.
formatter
.
write_interval
                
write_times
=
old
.
formatter
.
write_times
)
        
self
.
log_manager
.
enable_unstructured
(
)
