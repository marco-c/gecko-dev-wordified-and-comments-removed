import
os
.
path
import
subprocess
import
sys
import
textwrap
from
contextlib
import
contextmanager
from
string
import
ascii_lowercase
import
py
.
path
from
_pytest
import
pytester
contextmanager
def
subst_path_windows
(
filename
)
:
    
for
c
in
ascii_lowercase
[
7
:
]
:
        
c
+
=
"
:
"
        
if
not
os
.
path
.
exists
(
c
)
:
            
drive
=
c
            
break
    
else
:
        
raise
AssertionError
(
"
Unable
to
find
suitable
drive
letter
for
subst
.
"
)
    
directory
=
filename
.
dirpath
(
)
    
basename
=
filename
.
basename
    
args
=
[
"
subst
"
drive
str
(
directory
)
]
    
subprocess
.
check_call
(
args
)
    
assert
os
.
path
.
exists
(
drive
)
    
try
:
        
filename
=
py
.
path
.
local
(
drive
)
/
basename
        
yield
filename
    
finally
:
        
args
=
[
"
subst
"
"
/
D
"
drive
]
        
subprocess
.
check_call
(
args
)
contextmanager
def
subst_path_linux
(
filename
)
:
    
directory
=
filename
.
dirpath
(
)
    
basename
=
filename
.
basename
    
target
=
directory
/
"
.
.
"
/
"
sub2
"
    
os
.
symlink
(
str
(
directory
)
str
(
target
)
target_is_directory
=
True
)
    
try
:
        
filename
=
target
/
basename
        
yield
filename
    
finally
:
        
pass
def
test_link_resolve
(
testdir
:
pytester
.
Testdir
)
-
>
None
:
    
"
"
"
See
:
https
:
/
/
github
.
com
/
pytest
-
dev
/
pytest
/
issues
/
5965
.
"
"
"
    
sub1
=
testdir
.
mkpydir
(
"
sub1
"
)
    
p
=
sub1
.
join
(
"
test_foo
.
py
"
)
    
p
.
write
(
        
textwrap
.
dedent
(
            
"
"
"
        
import
pytest
        
def
test_foo
(
)
:
            
raise
AssertionError
(
)
        
"
"
"
        
)
    
)
    
subst
=
subst_path_linux
    
if
sys
.
platform
=
=
"
win32
"
:
        
subst
=
subst_path_windows
    
with
subst
(
p
)
as
subst_p
:
        
result
=
testdir
.
runpytest
(
str
(
subst_p
)
"
-
v
"
)
        
stdout
=
result
.
stdout
.
str
(
)
        
assert
"
sub1
/
test_foo
.
py
"
not
in
stdout
        
expect
=
(
            
"
*
{
}
*
"
.
format
(
subst_p
)
if
sys
.
platform
=
=
"
win32
"
else
"
*
sub2
/
test_foo
.
py
*
"
        
)
        
result
.
stdout
.
fnmatch_lines
(
[
expect
]
)
