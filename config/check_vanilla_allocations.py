from
__future__
import
absolute_import
from
__future__
import
print_function
import
argparse
import
re
import
subprocess
import
sys
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
'
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
'
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
'
-
-
aggressive
'
action
=
'
store_true
'
                        
help
=
'
also
check
for
malloc
calloc
realloc
and
free
'
)
    
parser
.
add_argument
(
'
file
'
type
=
str
                        
help
=
'
name
of
the
file
to
check
'
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
'
NM
'
)
or
'
nm
'
    
cmd
=
[
nm
'
-
u
'
'
-
C
'
'
-
A
'
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
'
\
n
'
)
    
alloc_fns
=
[
        
r
'
operator
new
\
(
unsigned
'
        
r
'
operator
new
\
[
\
]
\
(
unsigned
'
        
r
'
memalign
'
    
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
'
malloc
'
            
r
'
calloc
'
            
r
'
realloc
'
            
r
'
free
'
            
r
'
strdup
'
        
]
    
alloc_fns_unescaped
=
[
fn
.
translate
(
None
r
'
\
\
'
)
for
fn
in
alloc_fns
]
    
alloc_fns_re
=
r
'
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
U
(
'
+
r
'
|
'
.
join
(
alloc_fns
)
+
r
'
)
'
    
util_Utility_cpp
=
set
(
[
]
)
    
emit_line_info
=
False
    
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
alloc_fns_re
line
)
        
if
m
is
None
:
            
continue
        
filename
=
m
.
group
(
1
)
        
if
'
stdc
+
+
compat
'
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
filename
=
=
'
umutex
.
o
'
:
            
continue
        
if
filename
=
=
'
Decimal
.
o
'
:
            
continue
        
fn
=
m
.
group
(
2
)
        
if
filename
=
=
'
Utility
.
o
'
:
            
util_Utility_cpp
.
add
(
fn
)
        
else
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
'
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
'
+
             
'
'
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
'
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
'
)
        
print
(
'
check_vanilla_allocations
.
py
:
Accurate
in
unoptimized
builds
;
'
              
'
util
/
Utility
.
cpp
expected
.
'
)
        
cmd
=
[
'
nm
'
'
-
u
'
'
-
C
'
'
-
l
'
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
'
\
n
'
)
        
alloc_lines_re
=
r
'
U
(
(
'
+
r
'
|
'
.
join
(
alloc_fns
)
+
r
'
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
'
        
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
'
check_vanilla_allocations
.
py
:
'
                      
m
.
group
(
1
)
'
called
at
'
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
'
TEST
-
PASS
|
check_vanilla_allocations
.
py
|
ok
'
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
'
__main__
'
:
    
main
(
)
