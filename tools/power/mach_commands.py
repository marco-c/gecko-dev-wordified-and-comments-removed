from
__future__
import
print_function
absolute_import
from
distutils
.
version
import
StrictVersion
from
mach
.
decorators
import
(
    
Command
    
CommandArgument
    
CommandProvider
)
from
mozbuild
.
base
import
MachCommandBase
def
is_osx_10_10_or_greater
(
cls
)
:
    
import
platform
    
release
=
platform
.
mac_ver
(
)
[
0
]
    
return
release
and
StrictVersion
(
release
)
>
=
StrictVersion
(
'
10
.
10
'
)
CommandProvider
class
MachCommands
(
MachCommandBase
)
:
    
'
'
'
    
Get
system
power
consumption
and
related
measurements
.
    
'
'
'
    
def
__init__
(
self
context
)
:
        
MachCommandBase
.
__init__
(
self
context
)
    
Command
(
'
power
'
category
=
'
misc
'
             
conditions
=
[
is_osx_10_10_or_greater
]
             
description
=
'
Get
system
power
consumption
and
related
measurements
for
'
             
'
all
running
browsers
.
Available
only
on
Mac
OS
X
10
.
10
and
above
.
'
             
'
Requires
root
access
.
'
)
    
CommandArgument
(
'
-
i
'
'
-
-
interval
'
type
=
int
default
=
30000
                     
help
=
'
The
sample
period
measured
in
milliseconds
.
Defaults
to
30000
.
'
)
    
def
power
(
self
interval
)
:
        
import
os
        
import
re
        
import
subprocess
        
rapl
=
os
.
path
.
join
(
self
.
topobjdir
'
dist
'
'
bin
'
'
rapl
'
)
        
interval
=
str
(
interval
)
        
try
:
            
subprocess
.
check_call
(
[
'
sudo
'
'
true
'
]
)
        
except
Exception
:
            
print
(
'
\
nsudo
failed
;
aborting
'
)
            
return
1
        
subprocess
.
Popen
(
[
rapl
'
-
n
'
'
1
'
'
-
i
'
interval
]
)
        
lines
=
subprocess
.
check_output
(
[
'
sudo
'
'
powermetrics
'
                                         
'
-
-
samplers
'
'
tasks
'
                                         
'
-
-
show
-
process
-
coalition
'
                                         
'
-
-
show
-
process
-
gpu
'
                                         
'
-
n
'
'
1
'
                                         
'
-
i
'
interval
]
                                        
universal_newlines
=
True
)
        
print
(
)
        
for
line
in
lines
.
splitlines
(
)
:
            
if
re
.
search
(
r
'
(
^
Name
|
firefox
|
plugin
-
container
|
Safari
\
b
|
WebKit
|
Chrome
|
Terminal
|
WindowServer
|
kernel
)
'
line
)
:
                
print
(
line
)
        
return
0
