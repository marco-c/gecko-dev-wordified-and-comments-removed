from
__future__
import
absolute_import
print_function
import
json
import
os
import
mozinfo
import
sys
from
collections
import
namedtuple
from
distutils
.
spawn
import
find_executable
from
subprocess
import
check_output
__all__
=
[
'
get_debugger_info
'
           
'
get_default_debugger_name
'
           
'
DebuggerSearch
'
           
'
get_default_valgrind_args
'
           
'
DebuggerInfo
'
]
'
'
'
Map
of
debugging
programs
to
information
about
them
like
default
arguments
and
whether
or
not
they
are
interactive
.
To
add
support
for
a
new
debugger
simply
add
the
relative
entry
in
_DEBUGGER_INFO
and
optionally
update
the
_DEBUGGER_PRIORITIES
.
'
'
'
_DEBUGGER_INFO
=
{
    
'
gdb
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
q
'
'
-
-
args
'
]
    
}
    
'
cgdb
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
q
'
'
-
-
args
'
]
    
}
    
'
rust
-
gdb
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
q
'
'
-
-
args
'
]
    
}
    
'
lldb
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
-
'
]
        
'
requiresEscapedArgs
'
:
True
    
}
    
'
devenv
.
exe
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
debugexe
'
]
    
}
    
'
wdexpress
.
exe
'
:
{
        
'
interactive
'
:
True
        
'
args
'
:
[
'
-
debugexe
'
]
    
}
    
'
windbg
.
exe
'
:
{
        
'
interactive
'
:
True
    
}
}
_DEBUGGER_PRIORITIES
=
{
    
'
win
'
:
[
'
devenv
.
exe
'
'
wdexpress
.
exe
'
]
    
'
linux
'
:
[
'
gdb
'
'
cgdb
'
'
lldb
'
]
    
'
mac
'
:
[
'
lldb
'
'
gdb
'
]
    
'
android
'
:
[
'
gdb
'
]
    
'
unknown
'
:
[
'
gdb
'
]
}
DebuggerInfo
=
namedtuple
(
    
'
DebuggerInfo
'
    
[
'
path
'
'
interactive
'
'
args
'
'
requiresEscapedArgs
'
]
)
def
_windbg_installation_paths
(
)
:
    
programFilesSuffixes
=
[
'
'
'
(
x86
)
'
]
    
programFiles
=
"
C
:
/
Program
Files
"
    
windowsKitsVersions
=
[
'
10
'
'
8
.
1
'
'
8
'
]
    
for
suffix
in
programFilesSuffixes
:
        
windowsKitsPrefix
=
os
.
path
.
join
(
programFiles
+
suffix
                                         
'
Windows
Kits
'
)
        
for
version
in
windowsKitsVersions
:
            
yield
os
.
path
.
join
(
windowsKitsPrefix
version
                               
'
Debuggers
'
'
x64
'
'
windbg
.
exe
'
)
def
_vswhere_path
(
)
:
    
try
:
        
import
buildconfig
        
path
=
os
.
path
.
join
(
buildconfig
.
topsrcdir
'
build
'
'
win32
'
'
vswhere
.
exe
'
)
        
if
os
.
path
.
isfile
(
path
)
:
            
return
path
    
except
ImportError
:
        
pass
    
return
'
vswhere
.
exe
'
def
get_debugger_path
(
debugger
)
:
    
'
'
'
    
Get
the
full
path
of
the
debugger
.
    
:
param
debugger
:
The
name
of
the
debugger
.
    
'
'
'
    
if
mozinfo
.
os
=
=
'
mac
'
and
debugger
=
=
'
lldb
'
:
        
try
:
            
path
=
check_output
(
[
'
xcrun
'
'
-
-
find
'
'
lldb
'
]
)
.
strip
(
)
            
if
path
:
                
return
path
        
except
Exception
:
            
pass
    
if
mozinfo
.
os
=
=
'
win
'
and
debugger
=
=
'
devenv
.
exe
'
:
        
try
:
            
encoding
=
'
mbcs
'
if
sys
.
platform
=
=
'
win32
'
else
'
utf
-
8
'
            
vswhere
=
_vswhere_path
(
)
            
vsinfo
=
check_output
(
[
vswhere
'
-
format
'
'
json
'
'
-
latest
'
]
)
            
vsinfo
=
json
.
loads
(
vsinfo
.
decode
(
encoding
'
replace
'
)
)
            
return
os
.
path
.
join
(
vsinfo
[
0
]
[
'
installationPath
'
]
'
Common7
'
'
IDE
'
'
devenv
.
exe
'
)
        
except
Exception
:
            
pass
    
return
find_executable
(
debugger
)
def
get_debugger_info
(
debugger
debuggerArgs
=
None
debuggerInteractive
=
False
)
:
    
'
'
'
    
Get
the
information
about
the
requested
debugger
.
    
Returns
a
dictionary
containing
the
|
path
|
of
the
debugger
executable
    
if
it
will
run
in
|
interactive
|
mode
its
arguments
and
whether
it
needs
    
to
escape
arguments
it
passes
to
the
debugged
program
(
|
requiresEscapedArgs
|
)
.
    
If
the
debugger
cannot
be
found
in
the
system
returns
|
None
|
.
    
:
param
debugger
:
The
name
of
the
debugger
.
    
:
param
debuggerArgs
:
If
specified
it
'
s
the
arguments
to
pass
to
the
debugger
    
as
a
string
.
Any
debugger
-
specific
separator
arguments
are
appended
after
these
    
arguments
.
    
:
param
debuggerInteractive
:
If
specified
forces
the
debugger
to
be
interactive
.
    
'
'
'
    
debuggerPath
=
None
    
if
debugger
:
        
if
(
os
.
name
=
=
'
nt
'
                
and
not
debugger
.
lower
(
)
.
endswith
(
'
.
exe
'
)
)
:
            
debugger
+
=
'
.
exe
'
        
debuggerPath
=
get_debugger_path
(
debugger
)
    
if
not
debuggerPath
:
        
if
debugger
=
=
'
windbg
.
exe
'
:
            
for
candidate
in
_windbg_installation_paths
(
)
:
                
if
os
.
path
.
exists
(
candidate
)
:
                    
debuggerPath
=
candidate
                    
break
        
else
:
            
if
os
.
path
.
exists
(
debugger
)
:
                
debuggerPath
=
debugger
    
if
not
debuggerPath
:
        
print
(
'
Error
:
Could
not
find
debugger
%
s
.
'
%
debugger
)
        
print
(
'
Is
it
installed
?
Is
it
in
your
PATH
?
'
)
        
return
None
    
debuggerName
=
os
.
path
.
basename
(
debuggerPath
)
.
lower
(
)
    
def
get_debugger_info
(
type
default
)
:
        
if
debuggerName
in
_DEBUGGER_INFO
and
type
in
_DEBUGGER_INFO
[
debuggerName
]
:
            
return
_DEBUGGER_INFO
[
debuggerName
]
[
type
]
        
return
default
    
debugger_arguments
=
[
]
    
if
debuggerArgs
:
        
debugger_arguments
+
=
debuggerArgs
.
split
(
)
    
debugger_arguments
+
=
get_debugger_info
(
'
args
'
[
]
)
    
debugger_interactive
=
get_debugger_info
(
'
interactive
'
False
)
    
if
debuggerInteractive
:
        
debugger_interactive
=
debuggerInteractive
    
d
=
DebuggerInfo
(
        
debuggerPath
        
debugger_interactive
        
debugger_arguments
        
get_debugger_info
(
'
requiresEscapedArgs
'
False
)
    
)
    
return
d
class
DebuggerSearch
:
    
OnlyFirst
=
1
    
KeepLooking
=
2
def
get_default_debugger_name
(
search
=
DebuggerSearch
.
OnlyFirst
)
:
    
'
'
'
    
Get
the
debugger
name
for
the
default
debugger
on
current
platform
.
    
:
param
search
:
If
specified
stops
looking
for
the
debugger
if
the
     
default
one
is
not
found
(
|
DebuggerSearch
.
OnlyFirst
|
)
or
keeps
     
looking
for
other
compatible
debuggers
(
|
DebuggerSearch
.
KeepLooking
|
)
.
    
'
'
'
    
mozinfo
.
find_and_update_from_json
(
)
    
os
=
mozinfo
.
info
[
'
os
'
]
    
debuggerPriorities
=
_DEBUGGER_PRIORITIES
[
os
if
os
in
_DEBUGGER_PRIORITIES
else
'
unknown
'
]
    
for
debuggerName
in
debuggerPriorities
:
        
debuggerPath
=
get_debugger_path
(
debuggerName
)
        
if
debuggerPath
:
            
return
debuggerName
        
elif
not
search
=
=
DebuggerSearch
.
KeepLooking
:
            
return
None
    
return
None
def
get_default_valgrind_args
(
)
:
    
return
(
[
'
-
-
fair
-
sched
=
yes
'
             
'
-
-
smc
-
check
=
all
-
non
-
file
'
             
'
-
-
vex
-
iropt
-
register
-
updates
=
allregs
-
at
-
mem
-
access
'
             
'
-
-
trace
-
children
=
yes
'
             
'
-
-
child
-
silent
-
after
-
fork
=
yes
'
             
(
'
-
-
trace
-
children
-
skip
=
'
              
+
'
/
usr
/
bin
/
hg
/
bin
/
rm
*
/
bin
/
certutil
*
/
bin
/
pk12util
'
              
+
'
*
/
bin
/
ssltunnel
*
/
bin
/
uname
*
/
bin
/
which
*
/
bin
/
ps
'
              
+
'
*
/
bin
/
grep
*
/
bin
/
java
*
/
bin
/
lsb_release
'
)
             
]
            
+
get_default_valgrind_tool_specific_args
(
)
)
def
get_default_valgrind_tool_specific_args
(
)
:
    
return
[
'
-
-
partial
-
loads
-
ok
=
yes
'
            
'
-
-
leak
-
check
=
summary
'
            
'
-
-
show
-
possibly
-
lost
=
no
'
            
'
-
-
show
-
mismatched
-
frees
=
no
'
            
]
