import
sys
from
logalloc_munge
import
split_log_line
def
get_size
(
line
)
:
    
try
:
        
pid
tid
func
args
result
=
split_log_line
(
line
)
        
if
func
=
=
"
malloc
"
:
            
return
int
(
args
[
0
]
)
        
elif
func
=
=
"
calloc
"
:
            
return
int
(
args
[
0
]
)
*
int
(
args
[
1
]
)
        
elif
func
=
=
"
memalign
"
:
            
return
int
(
args
[
1
]
)
        
elif
func
=
=
"
realloc
"
:
            
return
int
(
args
[
1
]
)
        
else
:
            
return
None
    
except
Exception
:
        
return
None
def
main
(
)
:
    
small
=
0
    
large
=
0
    
huge
=
0
    
for
line
in
sys
.
stdin
:
        
size
=
get_size
(
line
.
strip
(
)
)
        
if
not
size
:
            
continue
        
if
size
<
4096
:
            
small
+
=
1
        
elif
size
<
1024
*
1024
:
            
large
+
=
1
        
else
:
            
huge
+
=
1
    
total
=
small
+
large
+
huge
    
def
print_percent
(
name
value
)
:
        
pct
=
100
*
value
/
total
        
print
(
f
"
{
name
:
<
5
}
:
{
value
:
>
12
}
{
pct
:
6
.
2f
}
%
"
)
    
print_percent
(
"
Small
"
small
)
    
print_percent
(
"
Large
"
large
)
    
print_percent
(
"
Huge
"
huge
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
