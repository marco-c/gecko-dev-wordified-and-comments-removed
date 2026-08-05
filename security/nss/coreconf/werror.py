import
os
import
subprocess
def
main
(
)
:
    
cc
=
os
.
environ
.
get
(
'
CC
'
'
cc
'
)
    
sink
=
open
(
os
.
devnull
'
wb
'
)
    
try
:
        
cc_is_clang
=
'
clang
'
in
subprocess
.
check_output
(
          
[
cc
'
-
-
version
'
]
universal_newlines
=
True
stderr
=
sink
)
    
except
OSError
:
        
return
    
def
warning_supported
(
warning
)
:
        
return
subprocess
.
call
(
[
cc
'
-
x
'
'
c
'
'
-
E
'
'
-
Werror
'
                                
'
-
W
%
s
'
%
warning
os
.
devnull
]
stdout
=
sink
stderr
=
sink
)
=
=
0
    
def
can_enable
(
)
:
        
if
not
warning_supported
(
'
all
'
)
:
            
return
False
        
if
not
cc_is_clang
:
            
try
:
                
v
=
subprocess
.
check_output
(
[
cc
'
-
dumpversion
'
]
stderr
=
sink
)
.
decode
(
"
utf
-
8
"
)
                
v
=
v
.
strip
(
'
\
r
\
n
'
)
.
split
(
'
.
'
)
                
v
=
list
(
map
(
int
v
)
)
                
if
v
[
0
]
<
4
or
(
v
[
0
]
=
=
4
and
v
[
1
]
<
8
)
:
                    
return
False
            
except
OSError
:
                
return
False
        
return
True
    
if
not
can_enable
(
)
:
        
print
(
'
-
DNSS_NO_GCC48
'
)
        
return
    
print
(
'
-
Werror
'
)
    
print
(
'
-
Wall
'
)
    
def
set_warning
(
warning
contra
=
'
'
)
:
        
if
warning_supported
(
warning
)
:
            
print
(
'
-
W
%
s
%
s
'
%
(
contra
warning
)
)
    
if
cc_is_clang
:
        
for
w
in
[
'
array
-
bounds
'
                  
'
unevaluated
-
expression
'
                  
'
parentheses
-
equality
'
                  
'
tautological
-
type
-
limit
-
compare
'
                  
'
sign
-
compare
'
                  
'
comma
'
                  
'
implicit
-
fallthrough
'
                  
]
:
            
set_warning
(
w
'
no
-
'
)
        
for
w
in
[
'
tautological
-
constant
-
in
-
range
-
compare
'
                  
'
bitfield
-
enum
-
conversion
'
                  
'
empty
-
body
'
                  
'
format
-
type
-
confusion
'
                  
'
ignored
-
qualifiers
'
                  
'
pointer
-
arith
'
                  
'
type
-
limits
'
                  
'
unreachable
-
code
'
                  
'
unreachable
-
code
-
return
'
                  
'
duplicated
-
cond
'
                  
'
logical
-
op
'
                  
'
implicit
-
function
-
declaration
'
                  
]
:
            
set_warning
(
w
'
'
)
        
print
(
'
-
Qunused
-
arguments
'
)
    
set_warning
(
'
shadow
'
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
