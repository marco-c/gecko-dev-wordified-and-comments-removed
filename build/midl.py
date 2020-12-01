import
buildconfig
import
subprocess
import
os
import
sys
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
buildconfig
.
substs
[
"
MIDL_FLAGS
"
]
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
cwd
=
base
)
    
return
result
.
returncode
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
}
"
.
format
(
lines
)
                
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
