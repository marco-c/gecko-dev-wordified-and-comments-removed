import
json
import
re
import
subprocess
import
sys
def
count_ctors
(
filename
)
:
    
proc
=
subprocess
.
Popen
(
        
[
'
readelf
'
'
-
W
'
'
-
S
'
filename
]
stdout
=
subprocess
.
PIPE
)
    
n_init_array_ctors
=
0
    
have_init_array
=
False
    
n_ctors_ctors
=
0
    
have_ctors
=
False
    
for
line
in
proc
.
stdout
:
        
f
=
line
.
split
(
)
        
if
len
(
f
)
!
=
11
:
            
continue
        
if
not
re
.
match
(
"
\
\
[
\
\
d
+
\
\
]
"
f
[
0
]
)
:
            
continue
        
section_name
contents
size
align
=
f
[
1
]
f
[
2
]
int
(
f
[
5
]
16
)
int
(
f
[
10
]
)
        
if
section_name
=
=
"
.
ctors
"
and
contents
=
=
"
PROGBITS
"
:
            
have_ctors
=
True
            
n_ctors_ctors
=
size
/
align
-
2
        
if
section_name
=
=
"
.
init_array
"
and
contents
=
=
"
INIT_ARRAY
"
:
            
have_init_array
=
True
            
n_init_array_ctors
=
size
/
align
    
if
have_init_array
:
        
if
have_ctors
and
n_ctors_ctors
!
=
0
:
            
print
>
>
sys
.
stderr
"
Unexpected
.
ctors
contents
for
"
filename
            
sys
.
exit
(
1
)
        
return
n_init_array_ctors
    
if
have_ctors
:
        
return
n_ctors_ctors
    
print
>
>
sys
.
stderr
"
Couldn
'
t
find
.
init_array
or
.
ctors
in
"
filename
    
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
'
__main__
'
:
    
for
f
in
sys
.
argv
[
1
:
]
:
        
perfherder_data
=
{
            
"
framework
"
:
{
"
name
"
:
"
build_metrics
"
}
            
"
suites
"
:
[
{
                
"
name
"
:
"
compiler_metrics
"
                
"
subtests
"
:
[
{
                    
"
name
"
:
"
num_static_constructors
"
                    
"
value
"
:
count_ctors
(
f
)
                    
"
alertThreshold
"
:
0
.
25
                
}
]
}
            
]
        
}
        
print
"
PERFHERDER_DATA
:
%
s
"
%
json
.
dumps
(
perfherder_data
)
