import
os
import
sys
from
ctypes
import
(
    
byref
sizeof
windll
Structure
WinError
    
c_size_t
c_char
c_void_p
)
from
ctypes
.
wintypes
import
DWORD
LONG
from
.
_core
import
SHELL_NAMES
ERROR_NO_MORE_FILES
=
18
ERROR_INSUFFICIENT_BUFFER
=
122
INVALID_HANDLE_VALUE
=
c_void_p
(
-
1
)
.
value
if
sys
.
version_info
[
0
]
<
3
:
    
string_types
=
(
str
unicode
)
else
:
    
string_types
=
(
str
)
class
PROCESSENTRY32
(
Structure
)
:
    
_fields_
=
[
        
(
'
dwSize
'
DWORD
)
        
(
'
cntUsage
'
DWORD
)
        
(
'
th32ProcessID
'
DWORD
)
        
(
'
th32DefaultHeapID
'
c_size_t
)
        
(
'
th32ModuleID
'
DWORD
)
        
(
'
cntThreads
'
DWORD
)
        
(
'
th32ParentProcessID
'
DWORD
)
        
(
'
pcPriClassBase
'
LONG
)
        
(
'
dwFlags
'
DWORD
)
        
(
'
szExeFile
'
c_char
*
260
)
    
]
def
_iter_process
(
)
:
    
"
"
"
Iterate
through
processes
yielding
process
ID
and
properties
of
each
.
    
Example
usage
:
:
        
>
>
>
for
pid
info
in
_iter_process
(
)
:
        
.
.
.
print
(
pid
'
-
>
'
info
)
        
1509
-
>
{
'
parent_pid
'
:
1201
'
executable
'
:
'
python
.
exe
'
}
    
"
"
"
    
h_process
=
windll
.
kernel32
.
CreateToolhelp32Snapshot
(
        
2
        
0
    
)
    
if
h_process
=
=
INVALID_HANDLE_VALUE
:
        
raise
WinError
(
)
    
pe
=
PROCESSENTRY32
(
)
    
pe
.
dwSize
=
sizeof
(
PROCESSENTRY32
)
    
success
=
windll
.
kernel32
.
Process32First
(
h_process
byref
(
pe
)
)
    
while
True
:
        
if
not
success
:
            
errcode
=
windll
.
kernel32
.
GetLastError
(
)
            
if
errcode
=
=
ERROR_NO_MORE_FILES
:
                
return
            
elif
errcode
=
=
ERROR_INSUFFICIENT_BUFFER
:
                
continue
            
raise
WinError
(
)
        
executable
=
pe
.
szExeFile
        
if
isinstance
(
executable
bytes
)
:
            
executable
=
executable
.
decode
(
'
mbcs
'
'
replace
'
)
        
info
=
{
'
executable
'
:
executable
}
        
if
pe
.
th32ParentProcessID
:
            
info
[
'
parent_pid
'
]
=
pe
.
th32ParentProcessID
        
yield
pe
.
th32ProcessID
info
        
success
=
windll
.
kernel32
.
Process32Next
(
h_process
byref
(
pe
)
)
def
_get_executable
(
process_dict
)
:
    
try
:
        
executable
=
process_dict
.
get
(
'
executable
'
)
    
except
(
AttributeError
TypeError
)
:
        
return
None
    
if
isinstance
(
executable
string_types
)
:
        
executable
=
executable
.
lower
(
)
.
rsplit
(
'
.
'
1
)
[
0
]
    
return
executable
def
get_shell
(
pid
=
None
max_depth
=
6
)
:
    
"
"
"
Get
the
shell
that
the
supplied
pid
or
os
.
getpid
(
)
is
running
in
.
    
"
"
"
    
if
not
pid
:
        
pid
=
os
.
getpid
(
)
    
processes
=
dict
(
_iter_process
(
)
)
    
def
check_parent
(
pid
lvl
=
0
)
:
        
ppid
=
processes
[
pid
]
.
get
(
'
parent_pid
'
)
        
shell_name
=
_get_executable
(
processes
.
get
(
ppid
)
)
        
if
shell_name
in
SHELL_NAMES
:
            
return
(
shell_name
processes
[
ppid
]
[
'
executable
'
]
)
        
if
lvl
>
=
max_depth
:
            
return
None
        
return
check_parent
(
ppid
lvl
=
lvl
+
1
)
    
shell_name
=
_get_executable
(
processes
.
get
(
pid
)
)
    
if
shell_name
in
SHELL_NAMES
:
        
return
(
shell_name
processes
[
pid
]
[
'
executable
'
]
)
    
try
:
        
return
check_parent
(
pid
)
    
except
KeyError
:
        
return
None
