import
os
import
sys
import
tempfile
from
subprocess
import
call
from
shutil
import
rmtree
import
logging
import
unittest
import
mozunit
def
banner
(
)
:
    
"
"
"
    
Display
interpreter
and
system
info
for
the
test
env
    
"
"
"
    
print
'
*
'
*
75
    
cmd
=
os
.
path
.
basename
(
__file__
)
    
print
"
%
s
:
python
version
is
%
s
"
%
(
cmd
sys
.
version
)
    
print
'
*
'
*
75
def
myopts
(
vals
)
:
    
"
"
"
    
Storage
for
extra
command
line
args
passed
.
    
Returns
:
    
hash
-
argparse
:
:
Namespace
object
values
    
"
"
"
    
if
not
hasattr
(
myopts
'
vals
'
)
:
        
if
'
argparse
'
in
sys
.
modules
:
            
tmp
=
{
}
        
else
:
            
tmp
=
{
'
debug
'
:
False
'
verbose
'
:
False
}
        
for
k
in
dir
(
vals
)
:
            
if
k
[
0
:
1
]
=
=
'
_
'
:
                
continue
            
tmp
[
k
]
=
getattr
(
vals
k
)
        
myopts
.
vals
=
tmp
    
return
myopts
.
vals
def
path2posix
(
src
)
:
    
"
"
"
    
Normalize
directory
path
syntax
    
Keyword
arguments
:
    
src
-
path
to
normalize
    
Returns
:
    
scalar
-
a
file
path
with
drive
separators
and
windows
slashes
removed
    
Todo
:
    
move
to
{
build
config
tools
toolkit
}
/
python
for
use
in
a
library
    
"
"
"
    
drive
=
'
'
    
winpath
=
src
.
find
(
'
:
'
)
    
if
-
1
!
=
winpath
and
10
>
winpath
:
        
(
drive
tail
)
=
src
.
split
(
'
:
'
1
)
    
if
drive
:
        
todo
=
[
'
'
drive
.
rstrip
(
'
:
'
)
.
lstrip
(
'
/
'
)
.
lstrip
(
'
\
\
'
)
]
        
todo
.
extend
(
tail
.
lstrip
(
'
/
'
)
.
lstrip
(
'
\
\
'
)
.
split
(
'
\
\
'
)
)
    
else
:
        
todo
=
src
.
split
(
'
\
\
'
)
    
dst
=
'
/
'
.
join
(
todo
)
    
return
dst
def
checkMkdir
(
work
debug
=
False
)
:
    
"
"
"
    
Verify
arg
permutations
for
directory
mutex
creation
.
    
Keyword
arguments
:
    
None
    
Returns
:
    
Exception
on
error
    
Note
:
    
Exception
(
)
rather
than
self
.
assertTrue
(
)
is
used
in
this
test
    
function
to
enable
scatch
cleanup
on
test
exit
/
failure
conditions
.
    
Not
guaranteed
by
python
closures
on
early
exit
.
    
"
"
"
    
logging
.
debug
(
"
Testing
:
checkMkdir
"
)
    
skipposix
=
sys
.
platform
=
=
"
win32
"
    
if
skipposix
:
        
path
=
os
.
path
.
abspath
(
__file__
)
        
dirname_fun
=
os
.
path
.
dirname
    
else
:
        
path
=
path2posix
(
os
.
path
.
abspath
(
__file__
)
)
        
import
posixpath
        
dirname_fun
=
posixpath
.
dirname
    
src
=
dirname_fun
(
path
)
    
root
=
reduce
(
lambda
x
_
:
dirname_fun
(
x
)
xrange
(
5
)
path
)
    
rootP
=
path2posix
(
root
)
    
srcP
=
path2posix
(
src
)
    
workP
=
path2posix
(
work
)
    
paths
=
[
        
"
mkdir_bycall
"
        
"
mkdir_bydep
"
        
"
mkdir_bygen
"
    
]
    
cmd
=
{
'
make
'
:
'
make
'
}
    
shell0
=
os
.
environ
.
get
(
'
MAKE
'
)
    
if
shell0
:
        
shell
=
os
.
path
.
splitext
(
shell0
)
[
0
]
        
if
-
1
!
=
shell
.
find
(
'
make
'
)
:
            
print
"
MAKE
COMMAND
FOUND
:
%
s
"
%
(
shell0
)
            
cmd
[
'
make
'
]
=
shell0
if
skipposix
else
path2posix
(
shell0
)
    
args
=
[
]
    
args
.
append
(
'
%
s
'
%
(
cmd
[
'
make
'
]
)
)
    
args
.
append
(
'
-
C
%
s
'
%
(
work
if
skipposix
else
workP
)
)
    
args
.
append
(
"
-
f
%
s
/
testor
.
tmpl
"
%
(
src
if
skipposix
else
srcP
)
)
    
args
.
append
(
'
topsrcdir
=
%
s
'
%
(
root
if
skipposix
else
rootP
)
)
    
args
.
append
(
'
deps_mkdir_bycall
=
%
s
'
%
paths
[
0
]
)
    
args
.
append
(
'
deps_mkdir_bydep
=
%
s
'
%
paths
[
1
]
)
    
args
.
append
(
'
deps_mkdir_bygen
=
%
s
'
%
paths
[
2
]
)
    
args
.
append
(
'
checkup
'
)
    
if
debug
:
        
pass
    
if
False
:
        
args
.
append
(
'
>
/
dev
/
null
'
)
    
cmd
=
'
%
s
'
%
(
'
'
.
join
(
args
)
)
    
logging
.
debug
(
"
Running
:
%
s
"
%
(
cmd
)
)
    
rc
=
call
(
cmd
shell
=
True
)
    
if
rc
:
        
raise
Exception
(
"
make
failed
(
?
=
%
s
)
:
cmd
=
%
s
"
%
(
rc
cmd
)
)
    
for
i
in
paths
:
        
path
=
os
.
path
.
join
(
work
i
)
        
logging
.
debug
(
"
Did
testing
mkdir
(
%
s
)
succeed
?
"
%
(
path
)
)
        
if
not
os
.
path
.
exists
(
path
)
:
            
raise
Exception
(
"
Test
path
%
s
does
not
exist
"
%
(
path
)
)
def
parseargs
(
)
:
    
"
"
"
    
Support
additional
command
line
arguments
for
testing
    
Returns
:
    
hash
-
arguments
of
interested
parsed
from
the
command
line
    
"
"
"
    
opts
=
None
    
try
:
        
import
argparse2
        
parser
=
argparse
.
ArgumentParser
(
)
        
parser
.
add_argument
(
'
-
-
debug
'
                            
action
=
"
store_true
"
                            
default
=
False
                            
help
=
'
Enable
debug
mode
'
)
        
parser
.
add_argument
(
'
-
-
verbose
'
                            
action
=
"
store_true
"
                            
default
=
False
                            
help
=
'
Enable
verbose
mode
'
)
        
parser
.
add_argument
(
'
unittest_args
'
                            
nargs
=
'
*
'
                            
)
        
opts
=
parser
.
parse_args
(
)
    
except
ImportError
:
        
pass
    
return
opts
class
TestMakeLogic
(
unittest
.
TestCase
)
:
    
"
"
"
    
Test
suite
used
to
validate
makefile
library
rules
and
macros
    
"
"
"
    
def
setUp
(
self
)
:
        
opts
=
myopts
(
None
)
        
self
.
debug
=
opts
[
'
debug
'
]
        
self
.
verbose
=
opts
[
'
verbose
'
]
        
if
self
.
debug
:
            
logging
.
basicConfig
(
level
=
logging
.
DEBUG
)
        
if
self
.
verbose
:
            
print
            
print
"
ENVIRONMENT
DUMP
:
"
            
print
'
=
'
*
75
            
for
k
v
in
os
.
environ
.
items
(
)
:
                
print
"
env
{
%
s
}
=
>
%
s
"
%
(
k
v
)
            
print
    
def
test_path2posix
(
self
)
:
        
todo
=
{
            
'
/
dev
/
null
'
:
'
/
dev
/
null
'
            
'
A
:
\
\
a
\
\
b
\
\
c
'
:
'
/
A
/
a
/
b
/
c
'
            
'
B
:
/
x
/
y
'
:
'
/
B
/
x
/
y
'
            
'
C
:
/
x
\
\
y
/
z
'
:
'
/
C
/
x
/
y
/
z
'
            
'
/
/
FOO
/
bar
/
tans
'
:
'
/
/
FOO
/
bar
/
tans
'
            
'
/
/
X
\
\
a
/
b
\
\
c
/
d
'
:
'
/
/
X
/
a
/
b
/
c
/
d
'
            
'
\
\
c
:
mozilla
\
\
sandbox
'
:
'
/
c
/
mozilla
/
sandbox
'
        
}
        
for
val
exp
in
todo
.
items
(
)
:
            
found
=
path2posix
(
val
)
            
tst
=
"
posix2path
(
%
s
)
:
%
s
!
=
%
s
)
"
%
(
val
exp
found
)
            
self
.
assertEqual
(
exp
found
"
%
s
:
invalid
path
detected
"
%
(
tst
)
)
    
def
test_mkdir
(
self
)
:
        
"
"
"
        
Verify
directory
creation
rules
and
macros
        
"
"
"
        
failed
=
True
        
try
:
            
work
=
tempfile
.
mkdtemp
(
)
            
checkMkdir
(
work
self
.
debug
)
            
failed
=
False
        
finally
:
            
if
os
.
path
.
exists
(
work
)
:
                
rmtree
(
work
)
        
self
.
assertFalse
(
failed
"
Unit
test
failure
detected
"
)
if
__name__
=
=
'
__main__
'
:
    
banner
(
)
    
opts
=
parseargs
(
)
    
myopts
(
opts
)
    
if
opts
:
        
if
hasattr
(
opts
'
unittest_args
'
)
:
            
sys
.
argv
[
1
:
]
=
opts
.
unittest_args
        
else
:
            
sys
.
argv
[
1
:
]
=
[
]
    
mozunit
.
main
(
)
