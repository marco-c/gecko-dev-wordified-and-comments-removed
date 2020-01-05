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
        
print
(
'
-
Qunused
-
arguments
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
