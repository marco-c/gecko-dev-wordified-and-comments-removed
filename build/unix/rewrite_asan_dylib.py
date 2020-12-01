from
__future__
import
absolute_import
print_function
unicode_literals
import
re
import
sys
import
os
import
subprocess
import
shutil
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
DYLIB_NAME
=
"
libclang_rt
.
asan_osx_dynamic
.
dylib
"
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
universal_newlines
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
os
.
path
.
isdir
(
path
)
:
                    
return
path
    
sys
.
stderr
.
write
(
"
rpath
could
not
be
resolved
from
%
s
\
n
"
%
filename
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
    
dylibCopied
=
False
    
for
root
subdirs
files
in
os
.
walk
(
path
)
:
        
for
filename
in
files
:
            
filename
=
os
.
path
.
join
(
root
filename
)
            
if
not
(
filename
.
endswith
(
"
.
dylib
"
)
or
os
.
access
(
filename
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
filename
]
universal_newlines
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
                
if
DYLIB_NAME
in
line
:
                    
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
                    
if
not
dylibCopied
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
filename
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
os
.
path
.
isfile
(
copyDylibPath
)
:
                            
shutil
.
copy
(
copyDylibPath
path
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
                                    
"
executable_path
/
"
+
DYLIB_NAME
                                    
os
.
path
.
join
(
path
DYLIB_NAME
)
                                
]
                            
)
                            
dylibCopied
=
True
                        
else
:
                            
sys
.
stderr
.
write
(
                                
"
dylib
path
in
%
s
was
not
found
at
:
%
s
\
n
"
                                
%
(
filename
copyDylibPath
)
                            
)
                    
relpath
=
"
"
if
path
=
=
root
else
os
.
path
.
relpath
(
path
root
)
+
"
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
                            
"
executable_path
/
"
+
relpath
+
DYLIB_NAME
                            
filename
                        
]
                    
)
                    
break
    
if
not
dylibCopied
:
        
sys
.
stderr
.
write
(
"
%
s
could
not
be
found
\
n
"
%
DYLIB_NAME
)
        
sys
.
exit
(
1
)
if
__name__
=
=
"
__main__
"
:
    
for
d
in
sys
.
argv
[
1
:
]
:
        
scan_directory
(
d
)
