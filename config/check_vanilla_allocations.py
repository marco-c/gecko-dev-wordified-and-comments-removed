import
argparse
import
re
import
subprocess
import
sys
from
collections
import
defaultdict
import
buildconfig
has_failed
=
False
def
fail
(
msg
)
:
    
print
(
"
TEST
-
UNEXPECTED
-
FAIL
|
check_vanilla_allocations
.
py
|
"
msg
)
    
global
has_failed
    
has_failed
=
True
def
main
(
)
:
    
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
-
aggressive
"
        
action
=
"
store_true
"
        
help
=
"
also
check
for
malloc
calloc
realloc
and
free
"
    
)
    
parser
.
add_argument
(
"
file
"
type
=
str
help
=
"
name
of
the
file
to
check
"
)
    
args
=
parser
.
parse_args
(
)
    
nm
=
buildconfig
.
substs
.
get
(
"
NM
"
)
or
"
nm
"
    
cmd
=
[
nm
"
-
C
"
"
-
A
"
args
.
file
]
    
lines
=
subprocess
.
check_output
(
        
cmd
universal_newlines
=
True
stderr
=
subprocess
.
PIPE
    
)
.
split
(
"
\
n
"
)
    
alloc_fns
=
[
        
r
"
operator
new
\
(
unsigned
"
        
r
"
operator
new
\
[
\
]
\
(
unsigned
"
        
r
"
memalign
"
    
]
    
if
args
.
aggressive
:
        
alloc_fns
+
=
[
r
"
malloc
"
r
"
calloc
"
r
"
realloc
"
r
"
free
"
r
"
strdup
"
]
    
alloc_fns_unescaped
=
[
fn
.
replace
(
"
\
\
"
"
"
)
for
fn
in
alloc_fns
]
    
nm_line_re
=
re
.
compile
(
r
"
(
[
^
:
/
]
+
)
:
\
s
+
[
0
-
9a
-
fA
-
F
]
*
\
s
+
(
[
TU
]
)
(
.
*
)
"
)
    
alloc_fns_re
=
re
.
compile
(
r
"
|
"
.
join
(
alloc_fns
)
)
    
functions
=
defaultdict
(
set
)
    
files
=
defaultdict
(
int
)
    
ignored_files
=
[
        
"
umutex
.
o
"
        
"
Decimal
.
o
"
        
"
regexp
-
ast
.
o
"
    
]
    
all_ignored_files
=
set
(
(
f
1
)
for
f
in
ignored_files
)
    
emit_line_info
=
False
    
prev_filename
=
None
    
for
line
in
lines
:
        
m
=
nm_line_re
.
search
(
line
)
        
if
m
is
None
:
            
continue
        
filename
symtype
fn
=
m
.
groups
(
)
        
if
prev_filename
!
=
filename
:
            
files
[
filename
]
+
=
1
            
prev_filename
=
filename
        
if
"
stdc
+
+
compat
"
in
filename
:
            
continue
        
if
"
_memory_
"
in
filename
:
            
continue
        
if
"
Fuzzer
"
in
filename
:
            
continue
        
if
"
ProfilingStack
"
in
filename
:
            
continue
        
if
symtype
=
=
"
T
"
:
            
if
fn
.
startswith
(
"
mozilla
:
:
intl
:
:
"
)
:
                
all_ignored_files
.
add
(
(
filename
files
[
filename
]
)
)
        
else
:
            
m
=
alloc_fns_re
.
match
(
fn
)
            
if
m
:
                
functions
[
(
filename
files
[
filename
]
)
]
.
add
(
m
.
group
(
0
)
)
    
util_Utility_cpp
=
functions
.
pop
(
(
"
Utility
.
o
"
1
)
)
    
if
(
"
Utility
.
o
"
2
)
in
functions
:
        
fail
(
"
There
should
be
only
one
Utility
.
o
file
"
)
    
for
f
n
in
all_ignored_files
:
        
functions
.
pop
(
(
f
n
)
None
)
        
if
f
in
ignored_files
and
(
f
2
)
in
functions
:
            
fail
(
f
"
There
should
be
only
one
{
f
}
file
"
)
    
for
(
filename
n
)
in
sorted
(
functions
)
:
        
for
fn
in
functions
[
(
filename
n
)
]
:
            
fail
(
"
'
"
+
fn
+
"
'
present
in
"
+
filename
)
            
emit_line_info
=
True
    
for
fn
in
alloc_fns_unescaped
:
        
if
fn
not
in
util_Utility_cpp
:
            
fail
(
"
'
"
+
fn
+
"
'
isn
'
t
used
as
expected
in
util
/
Utility
.
cpp
"
)
        
else
:
            
util_Utility_cpp
.
remove
(
fn
)
    
if
util_Utility_cpp
:
        
fail
(
            
"
unexpected
allocation
fns
used
in
util
/
Utility
.
cpp
:
"
            
+
"
"
.
join
(
util_Utility_cpp
)
        
)
    
if
emit_line_info
:
        
print
(
"
check_vanilla_allocations
.
py
:
Source
lines
with
allocation
calls
:
"
)
        
print
(
            
"
check_vanilla_allocations
.
py
:
Accurate
in
unoptimized
builds
;
"
            
"
util
/
Utility
.
cpp
expected
.
"
        
)
        
cmd
=
[
"
nm
"
"
-
u
"
"
-
C
"
"
-
l
"
args
.
file
]
        
lines
=
subprocess
.
check_output
(
            
cmd
universal_newlines
=
True
stderr
=
subprocess
.
PIPE
        
)
.
split
(
"
\
n
"
)
        
alloc_lines_re
=
r
"
U
(
(
"
+
r
"
|
"
.
join
(
alloc_fns
)
+
r
"
)
.
*
)
\
s
+
(
\
S
+
:
\
d
+
)
"
        
for
line
in
lines
:
            
m
=
re
.
search
(
alloc_lines_re
line
)
            
if
m
:
                
print
(
                    
"
check_vanilla_allocations
.
py
:
"
m
.
group
(
1
)
"
called
at
"
m
.
group
(
3
)
                
)
    
if
has_failed
:
        
sys
.
exit
(
1
)
    
print
(
"
TEST
-
PASS
|
check_vanilla_allocations
.
py
|
ok
"
)
    
sys
.
exit
(
0
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
