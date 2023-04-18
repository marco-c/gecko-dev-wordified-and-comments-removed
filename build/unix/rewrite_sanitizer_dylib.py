from
argparse
import
ArgumentParser
import
os
from
pathlib
import
Path
import
re
import
shutil
import
subprocess
import
sys
from
buildconfig
import
substs
"
"
"
Scans
the
given
directories
for
binaries
referencing
the
AddressSanitizer
runtime
library
copies
it
to
the
main
directory
and
rewrites
binaries
to
not
reference
it
with
absolute
paths
but
with
executable_path
instead
.
"
"
"
DYLIB_NAME_PATTERN
=
re
.
compile
(
r
"
libclang_rt
\
.
(
a
|
ub
)
san_osx_dynamic
\
.
dylib
"
)
def
resolve_rpath
(
filename
)
:
    
otoolOut
=
subprocess
.
check_output
(
[
substs
[
"
OTOOL
"
]
"
-
l
"
filename
]
text
=
True
)
    
currentCmd
=
None
    
for
line
in
otoolOut
.
splitlines
(
)
:
        
cmdMatch
=
re
.
match
(
r
"
^
\
s
+
cmd
(
[
A
-
Z_
]
+
)
"
line
)
        
if
cmdMatch
is
not
None
:
            
currentCmd
=
cmdMatch
.
group
(
1
)
            
continue
        
if
currentCmd
=
=
"
LC_RPATH
"
:
            
pathMatch
=
re
.
match
(
r
"
^
\
s
+
path
(
.
*
)
\
(
offset
\
d
+
\
)
"
line
)
            
if
pathMatch
is
not
None
:
                
path
=
pathMatch
.
group
(
1
)
                
if
Path
(
path
)
.
is_dir
(
)
:
                    
return
path
    
print
(
f
"
rpath
could
not
be
resolved
from
{
filename
}
"
file
=
sys
.
stderr
)
    
sys
.
exit
(
1
)
def
scan_directory
(
path
)
:
    
dylibsCopied
=
set
(
)
    
dylibsRequired
=
set
(
)
    
if
not
path
.
is_dir
(
)
:
        
print
(
f
"
Input
path
{
path
}
is
not
a
folder
"
file
=
sys
.
stderr
)
        
sys
.
exit
(
1
)
    
for
file
in
path
.
rglob
(
"
*
"
)
:
        
if
not
file
.
is_file
(
)
:
            
continue
        
if
not
(
file
.
suffix
=
=
"
.
dylib
"
or
os
.
access
(
str
(
file
)
os
.
X_OK
)
)
:
            
continue
        
try
:
            
otoolOut
=
subprocess
.
check_output
(
                
[
substs
[
"
OTOOL
"
]
"
-
L
"
str
(
file
)
]
text
=
True
            
)
        
except
Exception
:
            
continue
        
for
line
in
otoolOut
.
splitlines
(
)
:
            
match
=
DYLIB_NAME_PATTERN
.
search
(
line
)
            
if
match
is
not
None
:
                
dylibName
=
match
.
group
(
0
)
                
absDylibPath
=
line
.
split
(
)
[
0
]
                
if
absDylibPath
.
startswith
(
"
executable_path
/
"
)
:
                    
continue
                
dylibsRequired
.
add
(
dylibName
)
                
if
dylibName
not
in
dylibsCopied
:
                    
if
absDylibPath
.
startswith
(
"
rpath
/
"
)
:
                        
rpath
=
resolve_rpath
(
str
(
file
)
)
                        
copyDylibPath
=
absDylibPath
.
replace
(
"
rpath
"
rpath
)
                    
else
:
                        
copyDylibPath
=
absDylibPath
                    
if
Path
(
copyDylibPath
)
.
is_file
(
)
:
                        
shutil
.
copy
(
copyDylibPath
str
(
path
)
)
                        
subprocess
.
check_call
(
                            
[
                                
substs
[
"
INSTALL_NAME_TOOL
"
]
                                
"
-
id
"
                                
f
"
executable_path
/
{
dylibName
}
"
                                
str
(
path
/
dylibName
)
                            
]
                        
)
                        
dylibsCopied
.
add
(
dylibName
)
                    
else
:
                        
print
(
                            
f
"
dylib
path
in
{
file
}
was
not
found
at
:
{
copyDylibPath
}
"
                            
file
=
sys
.
stderr
                        
)
                
if
file
.
parent
=
=
path
:
                    
relpath
=
"
"
                
else
:
                    
relpath
=
f
"
{
os
.
path
.
relpath
(
str
(
path
)
str
(
file
.
parent
)
)
}
/
"
                
subprocess
.
check_call
(
                    
[
                        
substs
[
"
INSTALL_NAME_TOOL
"
]
                        
"
-
change
"
                        
absDylibPath
                        
f
"
executable_path
/
{
relpath
}
{
dylibName
}
"
                        
str
(
file
)
                    
]
                
)
                
break
    
dylibsMissing
=
dylibsRequired
-
dylibsCopied
    
if
dylibsMissing
:
        
for
dylibName
in
dylibsMissing
:
            
print
(
f
"
{
dylibName
}
could
not
be
found
"
file
=
sys
.
stderr
)
        
sys
.
exit
(
1
)
def
parse_args
(
argv
=
None
)
:
    
parser
=
ArgumentParser
(
)
    
parser
.
add_argument
(
"
paths
"
metavar
=
"
path
"
type
=
Path
nargs
=
"
+
"
)
    
return
parser
.
parse_args
(
argv
)
if
__name__
=
=
"
__main__
"
:
    
args
=
parse_args
(
)
    
for
d
in
args
.
paths
:
        
scan_directory
(
d
)
