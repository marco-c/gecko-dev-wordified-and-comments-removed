def
WebIDLTest
(
parser
harness
)
:
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
ObservableArray
<
void
>
foo
;
        
}
;
        
"
"
"
        
"
use
void
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
dictionary
A
{
          
boolean
member
;
        
}
;
        
interface
B
{
          
attribute
ObservableArray
<
A
>
foo
;
        
}
;
        
"
"
"
        
"
use
dictionary
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
ObservableArray
<
sequence
<
boolean
>
>
foo
;
        
}
;
        
"
"
"
        
"
use
sequence
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
dictionary
A
{
            
boolean
member
;
        
}
;
        
interface
B
{
          
attribute
ObservableArray
<
sequence
<
A
>
>
foo
;
        
}
;
        
"
"
"
        
"
use
sequence
<
dictionary
>
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
ObservableArray
<
record
<
DOMString
boolean
>
>
foo
;
        
}
;
        
"
"
"
        
"
use
record
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
dictionary
A
{
            
boolean
member
;
        
}
;
        
interface
B
{
          
attribute
ObservableArray
<
record
<
DOMString
A
>
>
foo
;
        
}
;
        
"
"
"
        
"
use
record
<
dictionary
>
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
ObservableArray
<
ObservableArray
<
boolean
>
>
foo
;
        
}
;
        
"
"
"
        
"
use
ObservableArray
as
inner
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
ObservableArray
<
boolean
>
?
foo
;
        
}
;
        
"
"
"
        
"
nullable
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
void
foo
(
sequence
<
ObservableArray
<
boolean
>
>
foo
)
;
        
}
;
        
"
"
"
        
"
used
in
sequence
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
void
foo
(
record
<
DOMString
ObservableArray
<
boolean
>
>
foo
)
;
        
}
;
        
"
"
"
        
"
used
in
record
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
Promise
<
ObservableArray
<
boolean
>
>
foo
(
)
;
        
}
;
        
"
"
"
        
"
used
in
promise
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
attribute
(
DOMString
or
ObservableArray
<
boolean
>
>
)
foo
;
        
}
;
        
"
"
"
        
"
used
in
union
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
dictionary
A
{
          
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
used
on
dictionary
member
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
void
foo
(
ObservableArray
<
boolean
>
foo
)
;
        
}
;
        
"
"
"
        
"
used
on
argument
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
static
attribute
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
used
on
static
attribute
type
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
iterable
<
ObservableArray
<
boolean
>
>
;
        
}
;
        
"
"
"
        
"
used
in
iterable
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
maplike
<
long
ObservableArray
<
boolean
>
>
;
        
}
;
        
"
"
"
        
"
used
in
maplike
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
setlike
<
ObservableArray
<
boolean
>
>
;
        
}
;
        
"
"
"
        
"
used
in
setlike
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
[
JSImplementation
=
"
mozilla
.
org
/
dom
/
test
-
interface
-
js
;
1
"
]
        
interface
A
{
          
readonly
attribute
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
used
in
JS
implemented
interface
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
namespace
A
{
          
readonly
attribute
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
used
in
namespaces
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
[
Cached
Pure
]
          
readonly
attribute
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
have
Cached
extended
attribute
"
    
)
    
harness
.
should_throw
(
        
parser
        
"
"
"
        
interface
A
{
          
[
StoreInSlot
Pure
]
          
readonly
attribute
ObservableArray
<
boolean
>
foo
;
        
}
;
        
"
"
"
        
"
have
StoreInSlot
extended
attribute
"
    
)
    
parser
=
parser
.
reset
(
)
    
parser
.
parse
(
        
"
"
"
        
interface
A
{
          
readonly
attribute
ObservableArray
<
boolean
>
foo
;
          
attribute
ObservableArray
<
[
Clamp
]
octet
>
bar
;
          
attribute
ObservableArray
<
long
?
>
baz
;
          
attribute
ObservableArray
<
(
boolean
or
long
)
>
qux
;
        
}
;
        
"
"
"
    
)
    
results
=
parser
.
finish
(
)
    
A
=
results
[
0
]
    
foo
=
A
.
members
[
0
]
    
harness
.
ok
(
foo
.
readonly
"
A
.
foo
is
readonly
attribute
"
)
    
harness
.
ok
(
foo
.
type
.
isObservableArray
(
)
"
A
.
foo
is
ObservableArray
type
"
)
    
harness
.
check
(
        
foo
.
slotIndices
[
A
.
identifier
.
name
]
0
"
A
.
foo
should
be
stored
in
slot
"
    
)
    
bar
=
A
.
members
[
1
]
    
harness
.
ok
(
bar
.
type
.
isObservableArray
(
)
"
A
.
bar
is
ObservableArray
type
"
)
    
harness
.
check
(
        
bar
.
slotIndices
[
A
.
identifier
.
name
]
1
"
A
.
bar
should
be
stored
in
slot
"
    
)
    
harness
.
ok
(
bar
.
type
.
inner
.
hasClamp
(
)
"
A
.
bar
'
s
inner
type
should
be
clamped
"
)
    
baz
=
A
.
members
[
2
]
    
harness
.
ok
(
baz
.
type
.
isObservableArray
(
)
"
A
.
baz
is
ObservableArray
type
"
)
    
harness
.
check
(
        
baz
.
slotIndices
[
A
.
identifier
.
name
]
2
"
A
.
baz
should
be
stored
in
slot
"
    
)
    
harness
.
ok
(
baz
.
type
.
inner
.
nullable
(
)
"
A
.
baz
'
s
inner
type
should
be
nullable
"
)
    
qux
=
A
.
members
[
3
]
    
harness
.
ok
(
qux
.
type
.
isObservableArray
(
)
"
A
.
qux
is
ObservableArray
type
"
)
    
harness
.
check
(
        
qux
.
slotIndices
[
A
.
identifier
.
name
]
3
"
A
.
qux
should
be
stored
in
slot
"
    
)
    
harness
.
ok
(
qux
.
type
.
inner
.
isUnion
(
)
"
A
.
qux
'
s
inner
type
should
be
union
"
)
