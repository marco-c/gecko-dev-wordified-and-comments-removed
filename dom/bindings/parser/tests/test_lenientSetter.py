def
should_throw
(
parser
harness
message
code
)
:
    
parser
=
parser
.
reset
(
)
;
    
threw
=
False
    
try
:
        
parser
.
parse
(
code
)
        
parser
.
finish
(
)
    
except
:
        
threw
=
True
    
harness
.
ok
(
threw
"
Should
have
thrown
:
%
s
"
%
message
)
def
WebIDLTest
(
parser
harness
)
:
    
should_throw
(
parser
harness
"
no
arguments
"
"
"
"
        
interface
I
{
          
[
LenientSetter
=
X
]
readonly
attribute
long
A
;
        
}
;
    
"
"
"
)
    
should_throw
(
parser
harness
"
PutForwards
"
"
"
"
        
interface
I
{
          
[
PutForwards
=
B
LenientSetter
]
readonly
attribute
J
A
;
        
}
;
        
interface
J
{
          
attribute
long
B
;
        
}
;
    
"
"
"
)
    
should_throw
(
parser
harness
"
Replaceable
"
"
"
"
        
interface
I
{
          
[
Replaceable
LenientSetter
]
readonly
attribute
J
A
;
        
}
;
    
"
"
"
)
    
should_throw
(
parser
harness
"
writable
attribute
"
"
"
"
        
interface
I
{
          
[
LenientSetter
]
attribute
long
A
;
        
}
;
    
"
"
"
)
    
should_throw
(
parser
harness
"
static
attribute
"
"
"
"
        
interface
I
{
          
[
LenientSetter
]
static
readonly
attribute
long
A
;
        
}
;
    
"
"
"
)
