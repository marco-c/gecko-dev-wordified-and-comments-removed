import
sys
import
typing
from
datetime
import
timedelta
MAX_WAIT
=
sys
.
maxsize
/
2
def
find_ordinal
(
pos_num
:
int
)
-
>
str
:
    
if
pos_num
=
=
0
:
        
return
"
th
"
    
elif
pos_num
=
=
1
:
        
return
"
st
"
    
elif
pos_num
=
=
2
:
        
return
"
nd
"
    
elif
pos_num
=
=
3
:
        
return
"
rd
"
    
elif
4
<
=
pos_num
<
=
20
:
        
return
"
th
"
    
else
:
        
return
find_ordinal
(
pos_num
%
10
)
def
to_ordinal
(
pos_num
:
int
)
-
>
str
:
    
return
f
"
{
pos_num
}
{
find_ordinal
(
pos_num
)
}
"
def
get_callback_name
(
cb
:
typing
.
Callable
[
.
.
.
typing
.
Any
]
)
-
>
str
:
    
"
"
"
Get
a
callback
fully
-
qualified
name
.
    
If
no
name
can
be
produced
repr
(
cb
)
is
called
and
returned
.
    
"
"
"
    
segments
=
[
]
    
try
:
        
segments
.
append
(
cb
.
__qualname__
)
    
except
AttributeError
:
        
try
:
            
segments
.
append
(
cb
.
__name__
)
        
except
AttributeError
:
            
pass
    
if
not
segments
:
        
return
repr
(
cb
)
    
else
:
        
try
:
            
if
cb
.
__module__
:
                
segments
.
insert
(
0
cb
.
__module__
)
        
except
AttributeError
:
            
pass
        
return
"
.
"
.
join
(
segments
)
time_unit_type
=
typing
.
Union
[
int
float
timedelta
]
def
to_seconds
(
time_unit
:
time_unit_type
)
-
>
float
:
    
return
float
(
time_unit
.
total_seconds
(
)
if
isinstance
(
time_unit
timedelta
)
else
time_unit
)
