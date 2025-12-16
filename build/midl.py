import
functools
import
os
import
shutil
import
subprocess
import
sys
import
buildconfig
def
relativize
(
path
base
=
None
)
:
    
if
path
.
startswith
(
"
/
"
)
:
        
return
os
.
path
.
relpath
(
path
base
)
    
if
os
.
path
.
isabs
(
path
)
or
path
.
startswith
(
"
-
"
)
:
        
return
path
    
return
os
.
path
.
relpath
(
path
base
)
functools
.
cache
def
files_in
(
path
)
:
    
return
{
p
.
lower
(
)
:
os
.
path
.
join
(
path
p
)
for
p
in
os
.
listdir
(
path
)
}
def
search_path
(
paths
path
)
:
    
for
p
in
paths
:
        
f
=
os
.
path
.
join
(
p
path
)
        
if
os
.
path
.
isfile
(
f
)
:
            
return
f
        
maybe_match
=
files_in
(
p
)
.
get
(
path
.
lower
(
)
)
        
if
maybe_match
:
            
return
maybe_match
    
raise
RuntimeError
(
f
"
Cannot
find
{
path
}
"
)
def
filter_preprocessor
(
cmd
)
:
    
for
arg
in
cmd
:
        
if
not
arg
.
startswith
(
(
"
-
std
=
"
"
-
std
:
"
)
)
:
            
yield
arg
def
preprocess
(
base
input
flags
)
:
    
import
argparse
    
import
re
    
from
collections
import
deque
    
IMPORT_RE
=
re
.
compile
(
r
'
import
\
s
*
"
(
[
^
"
]
+
)
"
;
'
)
    
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
"
-
I
"
action
=
"
append
"
)
    
parser
.
add_argument
(
"
-
D
"
action
=
"
append
"
)
    
parser
.
add_argument
(
"
-
acf
"
)
    
args
remainder
=
parser
.
parse_known_args
(
flags
)
    
preprocessor
=
(
        
list
(
filter_preprocessor
(
buildconfig
.
substs
[
"
CXXCPP
"
]
)
)
        
+
[
"
-
D__midl
=
801
"
]
        
+
[
f
"
-
D
{
d
}
"
for
d
in
args
.
D
or
(
)
]
        
+
[
f
"
-
I
{
i
}
"
for
i
in
args
.
I
or
(
)
]
    
)
    
includes
=
[
"
.
"
]
+
buildconfig
.
substs
[
"
INCLUDE
"
]
.
split
(
"
;
"
)
+
(
args
.
I
or
[
]
)
    
seen
=
set
(
)
    
queue
=
deque
(
[
input
]
)
    
if
args
.
acf
:
        
queue
.
append
(
args
.
acf
)
    
output
=
os
.
path
.
join
(
base
os
.
path
.
basename
(
input
)
)
    
while
True
:
        
try
:
            
input
=
queue
.
popleft
(
)
        
except
IndexError
:
            
break
        
if
os
.
path
.
basename
(
input
)
in
seen
:
            
continue
        
seen
.
add
(
os
.
path
.
basename
(
input
)
)
        
input
=
search_path
(
includes
input
)
        
if
input
.
lower
(
)
.
endswith
(
"
.
idl
"
)
:
            
try
:
                
acf
=
search_path
(
                    
[
os
.
path
.
dirname
(
input
)
]
os
.
path
.
basename
(
input
)
[
:
-
4
]
+
"
.
acf
"
                
)
                
if
acf
:
                    
queue
.
append
(
acf
)
            
except
RuntimeError
:
                
pass
        
command
=
preprocessor
+
[
input
]
        
preprocessed
=
os
.
path
.
join
(
base
os
.
path
.
basename
(
input
)
)
        
subprocess
.
run
(
command
stdout
=
open
(
preprocessed
"
wb
"
)
check
=
True
)
        
with
open
(
preprocessed
)
as
fh
:
            
for
line
in
fh
:
                
if
not
line
.
startswith
(
"
import
"
)
:
                    
continue
                
m
=
IMPORT_RE
.
match
(
line
)
                
if
not
m
:
                    
continue
                
imp
=
m
.
group
(
1
)
                
queue
.
append
(
imp
)
    
flags
=
[
]
    
for
i
in
[
base
]
+
(
args
.
I
or
[
]
)
:
        
flags
.
extend
(
[
"
-
I
"
i
]
)
    
if
args
.
acf
:
        
flags
.
extend
(
[
"
-
acf
"
os
.
path
.
join
(
base
os
.
path
.
basename
(
args
.
acf
)
)
]
)
    
flags
.
extend
(
remainder
)
    
return
output
flags
def
midl
(
out
input
*
flags
)
:
    
out
.
avoid_writing_to_file
(
)
    
midl_flags
=
buildconfig
.
substs
[
"
MIDL_FLAGS
"
]
    
base
=
os
.
path
.
dirname
(
out
.
name
)
or
"
.
"
    
tmpdir
=
None
    
try
:
        
if
"
-
no_cpp
"
in
midl_flags
:
            
tmpdir
=
os
.
path
.
join
(
base
os
.
path
.
basename
(
input
)
+
"
.
tmp
"
)
            
os
.
makedirs
(
tmpdir
exist_ok
=
True
)
            
try
:
                
input
flags
=
preprocess
(
tmpdir
input
flags
)
            
except
subprocess
.
CalledProcessError
as
e
:
                
return
e
.
returncode
        
midl
=
buildconfig
.
substs
[
"
MIDL
"
]
        
wine
=
buildconfig
.
substs
.
get
(
"
WINE
"
)
        
if
midl
.
lower
(
)
.
endswith
(
"
.
exe
"
)
and
wine
:
            
command
=
[
wine
midl
]
        
else
:
            
command
=
[
midl
]
        
command
.
extend
(
midl_flags
)
        
command
.
extend
(
[
relativize
(
f
base
)
for
f
in
flags
]
)
        
command
.
append
(
"
-
Oicf
"
)
        
command
.
append
(
relativize
(
input
base
)
)
        
print
(
"
Executing
:
"
"
"
.
join
(
command
)
)
        
result
=
subprocess
.
run
(
command
check
=
False
cwd
=
base
)
        
return
result
.
returncode
    
finally
:
        
if
tmpdir
:
            
shutil
.
rmtree
(
tmpdir
)
def
merge_dlldata
(
out
*
inputs
)
:
    
inputs
=
[
open
(
i
)
for
i
in
inputs
]
    
read_a_line
=
[
True
]
*
len
(
inputs
)
    
while
True
:
        
lines
=
[
            
f
.
readline
(
)
if
read_a_line
[
n
]
else
lines
[
n
]
for
n
f
in
enumerate
(
inputs
)
        
]
        
unique_lines
=
set
(
lines
)
        
if
len
(
unique_lines
)
=
=
1
:
            
if
not
lines
[
0
]
:
                
break
            
out
.
write
(
lines
[
0
]
)
            
read_a_line
=
[
True
]
*
len
(
inputs
)
        
elif
(
            
len
(
unique_lines
)
=
=
2
            
and
len
(
[
l
for
l
in
unique_lines
if
"
#
define
"
in
l
]
)
=
=
1
        
)
:
            
a
=
unique_lines
.
pop
(
)
            
if
"
#
define
"
in
a
:
                
out
.
write
(
a
)
            
else
:
                
out
.
write
(
unique_lines
.
pop
(
)
)
            
read_a_line
=
[
"
#
define
"
in
l
for
l
in
lines
]
        
elif
len
(
unique_lines
)
!
=
len
(
lines
)
:
            
print
(
                
f
"
Error
while
merging
dlldata
.
Last
lines
read
:
{
lines
}
"
                
file
=
sys
.
stderr
            
)
            
return
1
        
else
:
            
for
line
in
lines
:
                
out
.
write
(
line
)
            
read_a_line
=
[
True
]
*
len
(
inputs
)
    
return
0
