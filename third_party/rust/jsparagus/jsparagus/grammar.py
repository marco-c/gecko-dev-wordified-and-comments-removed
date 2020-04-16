"
"
"
Data
structures
for
representing
grammars
.
"
"
"
from
__future__
import
annotations
import
copy
import
typing
import
dataclasses
from
dataclasses
import
dataclass
from
.
ordered
import
OrderedSet
OrderedFrozenSet
from
.
import
types
def
example_grammar
(
)
-
>
Grammar
:
    
rules
:
typing
.
Dict
[
typing
.
Union
[
str
InitNt
Nt
]
LenientNtDef
]
=
{
        
'
expr
'
:
[
            
[
'
term
'
]
            
[
'
expr
'
'
+
'
'
term
'
]
            
[
'
expr
'
'
-
'
'
term
'
]
        
]
        
'
term
'
:
[
            
[
'
unary
'
]
            
[
'
term
'
'
*
'
'
unary
'
]
            
[
'
term
'
'
/
'
'
unary
'
]
        
]
        
'
unary
'
:
[
            
[
'
prim
'
]
            
[
'
-
'
'
unary
'
]
        
]
        
'
prim
'
:
[
            
[
'
NUM
'
]
            
[
'
VAR
'
]
            
[
'
(
'
'
expr
'
'
)
'
]
        
]
    
}
    
return
Grammar
(
rules
goal_nts
=
[
'
expr
'
]
variable_terminals
=
[
'
NUM
'
'
VAR
'
]
)
Condition
=
typing
.
Tuple
[
str
bool
]
dataclass
class
Production
:
    
__slots__
=
[
'
body
'
'
reducer
'
'
condition
'
]
    
body
:
typing
.
List
[
Element
]
    
reducer
:
ReduceExprOrAccept
    
condition
:
typing
.
Optional
[
Condition
]
    
def
__init__
(
self
                 
body
:
typing
.
List
[
Element
]
                 
reducer
:
ReduceExprOrAccept
                 
*
                 
condition
:
typing
.
Optional
[
Condition
]
=
None
)
:
        
self
.
body
=
body
        
self
.
reducer
=
reducer
        
self
.
condition
=
condition
    
def
__repr__
(
self
)
-
>
str
:
        
if
self
.
condition
is
None
:
            
return
"
Production
(
{
!
r
}
reducer
=
{
!
r
}
)
"
.
format
(
self
.
body
self
.
reducer
)
        
else
:
            
return
(
"
Production
(
{
!
r
}
reducer
=
{
!
r
}
condition
=
{
!
r
}
)
"
                    
.
format
(
self
.
body
self
.
reducer
self
.
condition
)
)
    
def
copy_with
(
self
*
*
kwargs
)
-
>
Production
:
        
return
dataclasses
.
replace
(
self
*
*
kwargs
)
dataclass
(
frozen
=
True
)
class
CallMethod
:
    
"
"
"
Express
a
method
call
and
give
it
a
given
set
of
arguments
.
A
trait
is
    
added
as
the
parser
should
implement
this
trait
to
call
this
method
.
"
"
"
    
method
:
str
    
args
:
typing
.
Tuple
[
ReduceExpr
.
.
.
]
    
trait
:
types
.
Type
=
types
.
Type
(
"
AstBuilder
"
)
    
fallible
:
bool
=
False
dataclass
(
frozen
=
True
)
class
Some
:
    
inner
:
ReduceExpr
def
expr_to_str
(
expr
:
ReduceExprOrAccept
)
-
>
str
:
    
if
isinstance
(
expr
int
)
:
        
return
"
{
}
"
.
format
(
expr
)
    
elif
isinstance
(
expr
CallMethod
)
:
        
return
"
{
}
:
:
{
}
(
{
}
)
{
}
"
.
format
(
            
expr
.
trait
expr
.
method
            
'
'
.
join
(
expr_to_str
(
arg
)
for
arg
in
expr
.
args
)
            
expr
.
fallible
and
'
?
'
or
'
'
)
    
elif
expr
is
None
:
        
return
"
None
"
    
elif
isinstance
(
expr
Some
)
:
        
return
"
Some
(
{
}
)
"
.
format
(
expr_to_str
(
expr
.
inner
)
)
    
elif
expr
=
=
"
accept
"
:
        
return
"
<
accept
>
"
    
else
:
        
raise
ValueError
(
"
unrecognized
expression
:
{
!
r
}
"
.
format
(
expr
)
)
Internable
=
typing
.
TypeVar
(
"
Internable
"
)
SyntheticTerminalsDict
=
typing
.
Dict
[
str
OrderedFrozenSet
[
str
]
]
class
Grammar
:
    
"
"
"
A
collection
of
productions
.
    
*
self
.
variable_terminals
-
OrderedFrozenSet
[
str
]
-
Terminals
that
carry
        
data
like
(
in
JS
)
numeric
literals
and
RegExps
.
    
*
self
.
terminals
-
OrderedFrozenSet
[
str
]
-
All
terminals
used
in
the
        
language
including
those
in
self
.
variable_terminals
and
        
self
.
synthetic_terminals
.
    
*
self
.
synthetic_terminals
-
{
str
:
OrderedFrozenSet
[
str
]
}
-
Maps
terminals
        
to
sets
of
terminals
.
An
entry
name
:
set
in
this
dictionary
means
        
that
name
is
shorthand
for
"
one
of
the
terminals
in
set
"
.
    
*
self
.
nonterminals
-
{
LenientNt
:
NtDef
}
-
Keys
are
either
(
str
|
InitNt
)
early
        
in
the
pipeline
or
Nt
objects
later
on
.
Values
are
the
NtDef
objects
        
that
contain
the
actual
Productions
.
    
*
self
.
methods
-
{
str
:
MethodType
}
-
Type
information
for
methods
.
    
*
self
.
init_nts
-
[
InitNt
or
Nt
]
-
The
list
of
all
elements
of
        
self
.
nonterminals
.
keys
(
)
that
are
init
nonterminals
.
    
*
self
.
exec_modes
-
DefaultDict
{
str
OrderedSet
[
Type
]
}
or
None
-
?
    
*
self
.
type_to_mods
-
{
Type
:
[
str
]
}
or
None
-
?
    
*
self
.
_cache
-
{
object
:
object
}
-
Cache
of
immutable
objects
used
by
        
Grammar
.
intern
(
)
.
    
"
"
"
    
variable_terminals
:
OrderedFrozenSet
[
str
]
    
terminals
:
OrderedFrozenSet
[
typing
.
Union
[
str
End
]
]
    
synthetic_terminals
:
SyntheticTerminalsDict
    
nonterminals
:
typing
.
Dict
[
LenientNt
NtDef
]
    
methods
:
typing
.
Dict
[
str
types
.
MethodType
]
    
init_nts
:
typing
.
List
[
typing
.
Union
[
Nt
InitNt
]
]
    
exec_modes
:
typing
.
Optional
[
typing
.
DefaultDict
[
str
OrderedSet
[
types
.
Type
]
]
]
    
type_to_modes
:
typing
.
Optional
[
typing
.
Mapping
[
types
.
Type
typing
.
List
[
str
]
]
]
    
_cache
:
typing
.
Dict
[
object
object
]
    
def
__init__
(
            
self
            
nonterminals
:
typing
.
Mapping
[
LenientNt
LenientNtDef
]
            
*
            
goal_nts
:
typing
.
Optional
[
typing
.
Iterable
[
LenientNt
]
]
=
None
            
variable_terminals
:
typing
.
Iterable
[
str
]
=
(
)
            
synthetic_terminals
:
typing
.
Dict
[
str
OrderedFrozenSet
]
=
None
            
method_types
:
typing
.
Optional
[
typing
.
Dict
[
str
types
.
MethodType
]
]
=
None
            
exec_modes
:
typing
.
Optional
[
typing
.
DefaultDict
[
str
OrderedSet
[
types
.
Type
]
]
]
=
None
            
type_to_modes
:
typing
.
Optional
[
typing
.
Mapping
[
types
.
Type
typing
.
List
[
str
]
]
]
=
None
)
:
        
my_nonterminals
:
typing
.
Dict
[
LenientNt
LenientNtDef
]
=
dict
(
nonterminals
.
items
(
)
)
        
if
goal_nts
is
None
:
            
my_goal_nts
=
[
]
            
for
name
in
my_nonterminals
:
                
my_goal_nts
.
append
(
name
)
                
break
        
else
:
            
my_goal_nts
=
list
(
goal_nts
)
        
self
.
variable_terminals
=
OrderedFrozenSet
(
variable_terminals
)
        
if
synthetic_terminals
is
None
:
            
synthetic_terminals
=
{
}
        
else
:
            
synthetic_terminals
=
{
                
name
:
OrderedFrozenSet
(
set
)
                
for
name
set
in
synthetic_terminals
.
items
(
)
            
}
            
for
synthetic_key
values
in
synthetic_terminals
.
items
(
)
:
                
if
synthetic_key
in
my_nonterminals
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
{
!
r
}
is
both
a
terminal
and
a
nonterminal
"
                        
.
format
(
synthetic_key
)
)
                
for
t
in
values
:
                    
if
t
in
my_nonterminals
:
                        
raise
ValueError
(
                            
"
invalid
grammar
:
{
!
r
}
is
both
"
.
format
(
t
)
                            
+
"
a
representation
of
a
synthetic
terminal
and
a
nonterminal
"
)
                    
if
t
in
synthetic_terminals
:
                        
raise
ValueError
(
                            
"
unsupported
:
synthetic
terminals
can
'
t
include
other
"
                            
"
synthetic
terminals
;
{
!
r
}
includes
{
!
r
}
"
                            
.
format
(
synthetic_key
t
)
)
        
self
.
synthetic_terminals
=
{
}
        
keys_are_nt
=
isinstance
(
next
(
iter
(
my_nonterminals
)
)
Nt
)
        
key_type
:
typing
.
Union
[
typing
.
Type
typing
.
Tuple
[
typing
.
Type
.
.
.
]
]
        
key_type
=
Nt
if
keys_are_nt
else
(
str
InitNt
)
        
self
.
_cache
=
{
}
        
str_to_nt
:
typing
.
Dict
[
typing
.
Union
[
str
InitNt
]
Nt
]
=
{
}
        
nt_params
:
typing
.
Dict
[
typing
.
Union
[
str
InitNt
]
typing
.
Tuple
[
str
.
.
.
]
]
=
{
}
        
for
key
in
my_nonterminals
:
            
if
not
isinstance
(
key
key_type
)
:
                
raise
ValueError
(
                    
"
invalid
grammar
:
conflicting
key
types
in
nonterminals
dict
-
"
                    
"
expected
either
all
str
or
all
Nt
got
{
!
r
}
"
                    
.
format
(
key
.
__class__
.
__name__
)
)
            
nt_name
:
typing
.
Union
[
str
InitNt
]
            
param_names
:
typing
.
Tuple
[
str
.
.
.
]
            
if
keys_are_nt
:
                
assert
isinstance
(
key
Nt
)
                
nt_name
=
key
.
name
                
param_names
=
tuple
(
name
for
name
value
in
key
.
args
)
            
else
:
                
assert
isinstance
(
key
(
str
InitNt
)
)
                
nt_name
=
key
                
param_names
=
(
)
                
my_nt
=
my_nonterminals
[
key
]
                
if
isinstance
(
my_nt
NtDef
)
:
                    
param_names
=
tuple
(
my_nt
.
params
)
            
if
nt_name
not
in
nt_params
:
                
nt_params
[
nt_name
]
=
param_names
            
else
:
                
if
nt_params
[
nt_name
]
!
=
param_names
:
                    
raise
ValueError
(
                        
"
conflicting
parameter
name
lists
for
nt
{
!
r
}
:
"
                        
"
both
{
!
r
}
and
{
!
r
}
"
                        
.
format
(
nt_name
nt_params
[
nt_name
]
param_names
)
)
            
if
param_names
=
=
(
)
and
nt_name
not
in
str_to_nt
:
                
str_to_nt
[
nt_name
]
=
self
.
intern
(
Nt
(
nt_name
)
)
        
all_terminals
:
OrderedSet
[
typing
.
Union
[
str
End
]
]
=
OrderedSet
(
self
.
variable_terminals
)
        
all_terminals
.
add
(
End
(
)
)
        
def
note_terminal
(
t
:
str
)
-
>
None
:
            
"
"
"
Add
t
(
and
all
representations
of
it
if
synthetic
)
to
all_terminals
.
"
"
"
            
if
t
not
in
all_terminals
:
                
all_terminals
.
add
(
t
)
                
if
t
in
self
.
synthetic_terminals
:
                    
for
k
in
self
.
synthetic_terminals
[
t
]
:
                        
note_terminal
(
k
)
        
def
validate_element
(
                
nt
:
LenientNt
                
i
:
typing
.
Union
[
int
str
]
                
j
:
typing
.
Union
[
int
str
]
                
e
:
Element
                
context_params
:
typing
.
Tuple
[
str
.
.
.
]
        
)
-
>
Element
:
            
if
isinstance
(
e
str
)
:
                
if
e
in
nt_params
:
                    
if
nt_params
[
e
]
!
=
(
)
:
                        
raise
ValueError
(
                            
"
invalid
grammar
:
missing
parameters
for
{
!
r
}
"
                            
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
inner
:
{
!
r
}
"
                            
.
format
(
e
nt
i
j
nt_params
[
e
]
)
)
                    
return
str_to_nt
[
e
]
                
else
:
                    
note_terminal
(
e
)
                    
return
e
            
elif
isinstance
(
e
Optional
)
:
                
if
not
isinstance
(
e
.
inner
(
str
Nt
)
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
unrecognized
element
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
inner
:
{
!
r
}
"
                        
.
format
(
nt
i
j
e
.
inner
)
)
                
inner
=
validate_element
(
nt
i
j
e
.
inner
context_params
)
                
return
self
.
intern
(
Optional
(
inner
)
)
            
elif
isinstance
(
e
Literal
)
:
                
if
not
isinstance
(
e
.
text
str
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
unrecognized
element
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
text
:
{
!
r
}
"
                        
.
format
(
nt
i
j
e
.
text
)
)
                
return
self
.
intern
(
e
)
            
elif
isinstance
(
e
UnicodeCategory
)
:
                
if
not
isinstance
(
e
.
cat_prefix
str
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
unrecognized
element
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
cat_prefix
:
{
!
r
}
"
                        
.
format
(
nt
i
j
e
.
cat_prefix
)
)
                
return
self
.
intern
(
e
)
            
elif
isinstance
(
e
Exclude
)
:
                
if
not
isinstance
(
e
.
inner
(
str
Nt
)
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
unrecognized
element
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
inner
:
{
!
r
}
"
                        
.
format
(
nt
i
j
e
.
inner
)
)
                
exclusion_list
=
[
]
                
for
value
in
e
.
exclusion_list
:
                    
if
not
isinstance
(
value
(
str
Nt
)
)
:
                        
raise
TypeError
(
                            
"
invalid
grammar
:
unrecognized
element
"
                            
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
.
exclusion_list
:
{
!
r
}
"
                            
.
format
(
nt
i
j
value
)
)
                    
value
=
validate_element
(
nt
i
j
value
context_params
)
                    
exclusion_list
.
append
(
value
)
                
inner
=
validate_element
(
nt
i
j
e
.
inner
context_params
)
                
return
self
.
intern
(
Exclude
(
inner
tuple
(
exclusion_list
)
)
)
            
elif
isinstance
(
e
Nt
)
:
                
if
e
not
in
my_nonterminals
and
e
.
name
not
in
my_nonterminals
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
unrecognized
nonterminal
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
:
{
!
r
}
"
                        
.
format
(
nt
i
j
e
.
name
)
)
                
args
=
tuple
(
pair
[
0
]
for
pair
in
e
.
args
)
                
if
e
.
name
in
nt_params
and
args
!
=
nt_params
[
e
.
name
]
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
wrong
arguments
passed
to
{
!
r
}
"
                        
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
:
"
                        
"
passed
{
!
r
}
expected
{
!
r
}
"
                        
.
format
(
e
.
name
nt
i
j
                                
args
nt_params
[
e
.
name
]
)
)
                
for
param_name
arg_expr
in
e
.
args
:
                    
if
isinstance
(
arg_expr
Var
)
:
                        
if
arg_expr
.
name
not
in
context_params
:
                            
raise
ValueError
(
                                
"
invalid
grammar
:
undefined
variable
{
!
r
}
"
                                
"
in
production
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
"
                                
.
format
(
arg_expr
.
name
nt
i
j
)
)
                
return
self
.
intern
(
e
)
            
elif
isinstance
(
e
(
LookaheadRule
End
ErrorSymbol
)
)
:
                
return
self
.
intern
(
e
)
            
elif
e
is
NoLineTerminatorHere
:
                
return
e
            
elif
isinstance
(
e
CallMethod
)
:
                
return
self
.
intern
(
e
)
            
else
:
                
raise
TypeError
(
                    
"
invalid
grammar
:
unrecognized
element
in
production
"
                    
"
grammar
[
{
!
r
}
]
[
{
}
]
[
{
}
]
:
{
!
r
}
"
                    
.
format
(
nt
i
j
e
)
)
            
assert
False
"
unreachable
"
        
def
check_reduce_expr
(
                
nt
:
LenientNt
                
i
:
int
                
rhs
:
Production
                
expr
:
ReduceExprOrAccept
)
-
>
None
:
            
if
isinstance
(
expr
int
)
:
                
concrete_len
=
sum
(
1
for
e
in
rhs
.
body
                                   
if
is_concrete_element
(
e
)
)
                
if
not
(
0
<
=
expr
<
concrete_len
)
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
element
number
{
}
out
of
range
for
"
                        
"
production
{
!
r
}
in
grammar
[
{
!
r
}
]
[
{
}
]
.
reducer
(
{
!
r
}
)
"
                        
.
format
(
expr
nt
rhs
.
body
i
rhs
.
reducer
)
)
            
elif
isinstance
(
expr
CallMethod
)
:
                
if
not
isinstance
(
expr
.
method
str
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
method
names
must
be
strings
"
                        
"
not
{
!
r
}
in
grammar
[
{
!
r
}
[
{
}
]
.
reducer
"
                        
.
format
(
expr
.
method
nt
i
)
)
                
if
not
expr
.
method
.
isidentifier
(
)
:
                    
name
space
pn
=
expr
.
method
.
partition
(
'
'
)
                    
if
space
=
=
'
'
and
name
.
isidentifier
(
)
and
pn
.
isdigit
(
)
:
                        
pass
                    
else
:
                        
raise
ValueError
(
                            
"
invalid
grammar
:
invalid
method
name
{
!
r
}
"
                            
"
(
not
an
identifier
)
in
grammar
[
{
!
r
}
[
{
}
]
.
reducer
"
                            
.
format
(
expr
.
method
nt
i
)
)
                
for
arg_expr
in
expr
.
args
:
                    
check_reduce_expr
(
nt
i
rhs
arg_expr
)
            
elif
expr
is
None
:
                
pass
            
elif
isinstance
(
expr
Some
)
:
                
check_reduce_expr
(
nt
i
rhs
expr
.
inner
)
            
else
:
                
raise
TypeError
(
                    
"
invalid
grammar
:
unrecognized
reduce
expression
{
!
r
}
"
                    
"
in
grammar
[
{
!
r
}
]
[
{
}
]
.
reducer
"
                    
.
format
(
expr
nt
i
)
)
        
def
copy_rhs
(
                
nt
:
LenientNt
                
i
:
int
                
sole_production
:
bool
                
rhs
:
LenientProduction
                
context_params
:
typing
.
Tuple
[
str
.
.
.
]
)
-
>
Production
:
            
if
isinstance
(
rhs
list
)
:
                
nargs
=
sum
(
1
for
e
in
rhs
if
is_concrete_element
(
e
)
)
                
reducer
:
ReduceExpr
                
if
len
(
rhs
)
=
=
1
and
nargs
=
=
1
:
                    
reducer
=
0
                
else
:
                    
if
sole_production
:
                        
method
=
str
(
nt
)
                    
else
:
                        
method
=
'
{
}
_
{
}
'
.
format
(
nt
i
)
                    
reducer
=
CallMethod
(
method
tuple
(
range
(
nargs
)
)
)
                
rhs
=
Production
(
rhs
reducer
)
            
if
not
isinstance
(
rhs
Production
)
:
                
raise
TypeError
(
                    
"
invalid
grammar
:
grammar
[
{
!
r
}
]
[
{
}
]
should
be
"
                    
"
a
Production
or
list
of
grammar
symbols
not
{
!
r
}
"
                    
.
format
(
nt
i
rhs
)
)
            
if
rhs
.
condition
is
not
None
:
                
param
value
=
rhs
.
condition
                
if
param
not
in
context_params
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
undefined
parameter
{
!
r
}
"
                        
"
in
conditional
for
grammar
[
{
!
r
}
]
[
{
}
]
"
                        
.
format
(
param
nt
i
)
)
            
if
rhs
.
reducer
!
=
'
accept
'
:
                
check_reduce_expr
(
nt
i
rhs
rhs
.
reducer
)
            
assert
isinstance
(
rhs
.
body
list
)
            
return
rhs
.
copy_with
(
body
=
[
                
validate_element
(
nt
i
j
e
context_params
)
                
for
j
e
in
enumerate
(
rhs
.
body
)
            
]
)
        
def
copy_nt_def
(
                
nt
:
LenientNt
                
nt_def
:
typing
.
Union
[
NtDef
typing
.
List
[
LenientProduction
]
]
        
)
-
>
NtDef
:
            
rhs_list
:
typing
.
Sequence
[
LenientProduction
]
            
if
isinstance
(
nt_def
NtDef
)
:
                
for
i
param
in
enumerate
(
nt_def
.
params
)
:
                    
if
not
isinstance
(
param
str
)
:
                        
raise
TypeError
(
                            
"
invalid
grammar
:
parameter
{
}
of
{
}
should
be
"
                            
"
a
string
not
{
!
r
}
"
                            
.
format
(
i
+
1
nt
param
)
)
                
params
=
nt_def
.
params
                
rhs_list
=
nt_def
.
rhs_list
                
ty
=
nt_def
.
type
            
else
:
                
params
=
(
)
                
rhs_list
=
nt_def
                
ty
=
None
            
if
not
isinstance
(
rhs_list
list
)
:
                
raise
TypeError
(
                    
"
invalid
grammar
:
grammar
[
{
!
r
}
]
should
be
either
a
"
                    
"
list
of
right
-
hand
sides
or
NtDef
not
{
!
r
}
"
                    
.
format
(
nt
type
(
rhs_list
)
.
__name__
)
)
            
sole_production
=
len
(
rhs_list
)
=
=
1
            
productions
=
[
copy_rhs
(
nt
i
sole_production
rhs
params
)
                           
for
i
rhs
in
enumerate
(
rhs_list
)
]
            
return
NtDef
(
params
productions
ty
)
        
def
check_nt_key
(
nt
:
LenientNt
)
-
>
None
:
            
if
isinstance
(
nt
str
)
:
                
if
not
nt
.
isidentifier
(
)
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
nonterminal
names
must
be
identifiers
not
{
!
r
}
"
                        
.
format
(
nt
)
)
                
if
nt
in
self
.
variable_terminals
or
nt
in
self
.
synthetic_terminals
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
{
!
r
}
is
both
a
nonterminal
and
a
variable
terminal
"
                        
.
format
(
nt
)
)
            
elif
isinstance
(
nt
Nt
)
:
                
assert
keys_are_nt
                
if
not
(
isinstance
(
nt
.
name
(
str
InitNt
)
)
                        
and
isinstance
(
nt
.
args
tuple
)
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
expected
str
or
Nt
(
name
=
str
"
                        
"
args
=
tuple
)
keys
in
nonterminals
dict
got
{
!
r
}
"
                        
.
format
(
nt
)
)
                
check_nt_key
(
nt
.
name
)
                
for
pair
in
nt
.
args
:
                    
if
(
not
isinstance
(
pair
tuple
)
                            
or
len
(
pair
)
!
=
2
                            
or
not
isinstance
(
pair
[
0
]
str
)
                            
or
not
isinstance
(
pair
[
1
]
bool
)
)
:
                        
raise
TypeError
(
                            
"
invalid
grammar
:
expected
tuple
(
(
str
bool
)
)
args
got
{
!
r
}
"
                            
.
format
(
nt
)
)
            
elif
isinstance
(
nt
InitNt
)
:
                
if
not
isinstance
(
nt
.
goal
Nt
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
InitNt
.
goal
should
be
a
nonterminal
"
                        
"
got
{
!
r
}
"
                        
.
format
(
nt
)
)
                
validate_element
(
nt
'
?
'
'
?
'
nt
.
goal
(
)
)
                
if
nt
.
goal
not
in
my_goal_nts
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
nonterminal
referenced
by
InitNt
"
                        
"
is
not
in
the
list
of
goals
:
{
!
r
}
"
                        
.
format
(
nt
)
)
            
else
:
                
raise
TypeError
(
                    
"
invalid
grammar
:
expected
string
keys
in
nonterminals
dict
got
{
!
r
}
"
                    
.
format
(
nt
)
)
        
def
validate_nt
(
                
nt
:
LenientNt
                
nt_def
:
LenientNtDef
        
)
-
>
typing
.
Tuple
[
LenientNt
NtDef
]
:
            
check_nt_key
(
nt
)
            
if
isinstance
(
nt
InitNt
)
:
                
if
not
isinstance
(
nt_def
NtDef
)
:
                    
raise
TypeError
(
                        
"
invalid
grammar
:
key
{
!
r
}
must
map
to
"
                        
"
value
of
type
NtDef
not
{
!
r
}
"
                        
.
format
(
nt
nt_def
)
)
                
rhs_list
=
nt_def
.
rhs_list
                
g
=
nt
.
goal
                
if
(
rhs_list
!
=
[
Production
(
[
g
]
0
)
                                 
Production
(
[
Nt
(
nt
(
)
)
End
(
)
]
'
accept
'
)
]
                    
and
rhs_list
!
=
[
Production
(
[
Optional
(
g
)
]
0
)
                                     
Production
(
[
Nt
(
nt
(
)
)
End
(
)
]
'
accept
'
)
]
                    
and
rhs_list
!
=
[
Production
(
[
End
(
)
]
'
accept
'
)
                                     
Production
(
[
g
End
(
)
]
'
accept
'
)
                                     
Production
(
[
Nt
(
nt
(
)
)
End
(
)
]
'
accept
'
)
]
)
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
grammar
[
{
!
r
}
]
is
not
one
of
"
                        
"
the
expected
forms
:
got
{
!
r
}
"
                        
.
format
(
nt
rhs_list
)
)
            
return
nt
copy_nt_def
(
nt
nt_def
)
        
self
.
nonterminals
=
{
}
        
for
nt1
nt_def1
in
my_nonterminals
.
items
(
)
:
            
nt
nt_def
=
validate_nt
(
nt1
nt_def1
)
            
self
.
nonterminals
[
nt
]
=
nt_def
        
for
syn_term_name
t_set
in
synthetic_terminals
.
items
(
)
:
            
nt_def
=
NtDef
(
(
syn_term_name
)
[
Production
(
[
e
]
0
)
for
e
in
t_set
]
None
)
            
nt
nt_def
=
validate_nt
(
syn_term_name
nt_def
)
            
self
.
nonterminals
[
nt
]
=
nt_def
            
all_terminals
.
remove
(
syn_term_name
)
        
self
.
terminals
=
OrderedFrozenSet
(
all_terminals
)
        
if
method_types
is
None
:
            
types
.
infer_types
(
self
)
        
else
:
            
for
nt
nt_def
in
self
.
nonterminals
.
items
(
)
:
                
assert
isinstance
(
nt_def
NtDef
)
                
assert
isinstance
(
nt_def
.
type
types
.
Type
)
            
self
.
methods
=
method_types
        
self
.
init_nts
=
[
]
        
for
goal
in
my_goal_nts
:
            
if
isinstance
(
goal
str
)
:
                
ok
=
goal
in
str_to_nt
                
if
ok
:
                    
goal
=
str_to_nt
[
goal
]
            
elif
isinstance
(
goal
Nt
)
:
                
if
keys_are_nt
:
                    
ok
=
goal
in
my_nonterminals
                
else
:
                    
ok
=
goal
.
name
in
my_nonterminals
            
if
not
ok
:
                
raise
ValueError
(
                    
"
goal
nonterminal
{
!
r
}
is
undefined
"
.
format
(
goal
)
)
            
assert
isinstance
(
goal
Nt
)
            
init_nt
=
InitNt
(
goal
)
            
init_key
:
LenientNt
=
init_nt
            
goal_nt
=
Nt
(
init_nt
(
)
)
            
if
keys_are_nt
:
                
init_key
=
goal_nt
            
if
init_key
not
in
self
.
nonterminals
:
                
self
.
nonterminals
[
init_key
]
=
NtDef
(
                    
(
)
                    
[
Production
(
[
goal
]
0
)
                     
Production
(
[
goal_nt
End
(
)
]
'
accept
'
)
]
                    
types
.
NoReturnType
)
            
self
.
init_nts
.
append
(
goal_nt
)
        
self
.
exec_modes
=
exec_modes
        
self
.
type_to_modes
=
type_to_modes
    
def
patch
(
self
extensions
:
typing
.
List
)
-
>
None
:
        
assert
self
.
type_to_modes
is
not
None
        
assert
self
.
exec_modes
is
not
None
        
if
extensions
=
=
[
]
:
            
return
        
nonterminals
=
copy
.
copy
(
self
.
nonterminals
)
        
for
ext
in
extensions
:
            
for
mode
in
self
.
type_to_modes
[
ext
.
target
.
for_type
]
:
                
self
.
exec_modes
[
mode
]
.
add
(
ext
.
target
.
trait
)
            
ext
.
apply_patch
(
self
nonterminals
)
        
self
.
nonterminals
=
nonterminals
    
def
intern
(
self
obj
:
Internable
)
-
>
Internable
:
        
"
"
"
Return
a
shared
copy
of
the
immutable
object
obj
.
        
This
saves
memory
and
consistent
use
allows
code
to
use
is
for
        
equality
testing
.
        
"
"
"
        
try
:
            
return
self
.
_cache
[
obj
]
        
except
KeyError
:
            
self
.
_cache
[
obj
]
=
obj
            
return
obj
    
def
is_terminal
(
self
element
:
object
)
-
>
bool
:
        
return
type
(
element
)
is
str
    
def
expand_set_of_terminals
(
            
self
            
terminals
:
typing
.
Iterable
[
typing
.
Union
[
str
None
ErrorSymbol
]
]
    
)
-
>
OrderedSet
[
typing
.
Union
[
str
None
ErrorSymbol
]
]
:
        
"
"
"
Copy
a
set
of
terminals
replacing
any
synthetic
terminals
with
their
representations
.
        
Returns
a
new
OrderedSet
.
        
terminals
-
an
iterable
of
terminals
and
/
or
other
unique
elements
like
        
None
or
ErrorSymbol
.
        
"
"
"
        
result
:
OrderedSet
[
typing
.
Union
[
str
None
ErrorSymbol
]
]
=
OrderedSet
(
)
        
for
t
in
terminals
:
            
if
isinstance
(
t
str
)
and
t
in
self
.
synthetic_terminals
:
                
result
|
=
self
.
expand_set_of_terminals
(
self
.
synthetic_terminals
[
t
]
)
            
else
:
                
result
.
add
(
t
)
        
return
result
    
def
goals
(
self
)
-
>
typing
.
List
[
Nt
]
:
        
"
"
"
Return
a
list
of
this
grammar
'
s
goal
nonterminals
.
"
"
"
        
return
[
init_nt
.
name
.
goal
for
init_nt
in
self
.
init_nts
]
    
def
with_nonterminals
(
            
self
            
nonterminals
:
typing
.
Mapping
[
LenientNt
LenientNtDef
]
    
)
-
>
Grammar
:
        
"
"
"
Return
a
copy
of
self
with
the
same
attributes
except
different
nonterminals
.
"
"
"
        
if
self
.
methods
is
not
None
:
            
for
nt_def
in
nonterminals
.
values
(
)
:
                
assert
isinstance
(
nt_def
NtDef
)
                
assert
nt_def
.
type
is
not
None
        
return
Grammar
(
            
nonterminals
            
goal_nts
=
self
.
goals
(
)
            
variable_terminals
=
self
.
variable_terminals
            
synthetic_terminals
=
self
.
synthetic_terminals
            
method_types
=
self
.
methods
            
exec_modes
=
self
.
exec_modes
            
type_to_modes
=
self
.
type_to_modes
)
    
def
element_to_str
(
self
e
:
Element
)
-
>
str
:
        
if
isinstance
(
e
Nt
)
:
            
return
e
.
pretty
(
)
        
elif
self
.
is_terminal
(
e
)
:
            
assert
isinstance
(
e
str
)
            
if
e
in
self
.
variable_terminals
or
e
in
self
.
synthetic_terminals
:
                
return
e
            
return
'
"
'
+
repr
(
e
)
[
1
:
-
1
]
+
'
"
'
        
elif
isinstance
(
e
Optional
)
:
            
return
self
.
element_to_str
(
e
.
inner
)
+
"
?
"
        
elif
isinstance
(
e
LookaheadRule
)
:
            
if
len
(
e
.
set
)
=
=
1
:
                
op
=
"
=
=
"
if
e
.
positive
else
"
!
=
"
                
s
=
repr
(
list
(
e
.
set
)
[
0
]
)
            
else
:
                
op
=
"
in
"
if
e
.
positive
else
"
not
in
"
                
s
=
'
{
'
+
repr
(
list
(
e
.
set
)
)
[
1
:
-
1
]
+
'
}
'
            
return
"
[
lookahead
{
}
{
}
]
"
.
format
(
op
s
)
        
elif
isinstance
(
e
End
)
:
            
return
"
<
END
>
"
        
elif
e
is
NoLineTerminatorHere
:
            
return
"
[
no
LineTerminator
here
]
"
        
elif
isinstance
(
e
CallMethod
)
:
            
return
"
{
{
{
}
}
}
"
.
format
(
expr_to_str
(
e
)
)
        
else
:
            
return
str
(
e
)
    
def
symbols_to_str
(
self
rhs
:
typing
.
Iterable
[
Element
]
)
-
>
str
:
        
return
"
"
.
join
(
self
.
element_to_str
(
e
)
for
e
in
rhs
)
    
def
rhs_to_str
(
self
rhs
:
LenientProduction
)
:
        
if
isinstance
(
rhs
Production
)
:
            
if
rhs
.
condition
is
None
:
                
prefix
=
'
'
            
else
:
                
param
value
=
rhs
.
condition
                
if
value
is
True
:
                    
condition
=
"
+
"
+
param
                
elif
value
is
False
:
                    
condition
=
"
~
"
+
param
                
else
:
                    
condition
=
"
{
}
=
=
{
!
r
}
"
.
format
(
param
value
)
                
prefix
=
"
#
[
if
{
}
]
"
.
format
(
condition
)
            
return
prefix
+
self
.
rhs_to_str
(
rhs
.
body
)
        
elif
len
(
rhs
)
=
=
0
:
            
return
"
[
empty
]
"
        
else
:
            
return
self
.
symbols_to_str
(
rhs
)
    
def
production_to_str
(
            
self
            
nt
:
typing
.
Union
[
str
Nt
]
            
rhs
:
LenientProduction
            
*
reducer
:
ReduceExpr
    
)
-
>
str
:
        
return
"
{
}
:
:
=
{
}
{
}
"
.
format
(
            
self
.
element_to_str
(
nt
)
            
self
.
rhs_to_str
(
rhs
)
            
"
"
.
join
(
"
=
>
"
+
expr_to_str
(
expr
)
for
expr
in
reducer
)
)
    
def
lr_item_to_str
(
self
prods
:
typing
.
List
item
)
-
>
str
:
        
prod
=
prods
[
item
.
prod_index
]
        
if
item
.
lookahead
is
None
:
            
la
=
[
]
        
else
:
            
la
=
[
self
.
element_to_str
(
item
.
lookahead
)
]
        
return
"
{
}
:
:
=
{
}
>
>
{
{
{
}
}
}
"
.
format
(
            
self
.
element_to_str
(
prod
.
nt
)
            
"
"
.
join
(
[
self
.
element_to_str
(
e
)
for
e
in
prod
.
rhs
[
:
item
.
offset
]
]
                     
+
[
"
\
N
{
MIDDLE
DOT
}
"
]
                     
+
la
                     
+
[
self
.
element_to_str
(
e
)
for
e
in
prod
.
rhs
[
item
.
offset
:
]
]
)
            
"
"
.
join
(
                
"
"
if
t
is
None
else
self
.
element_to_str
(
t
)
                
for
t
in
item
.
followed_by
)
        
)
    
def
item_set_to_str
(
            
self
            
prods
:
typing
.
List
            
item_set
:
OrderedFrozenSet
    
)
-
>
str
:
        
return
"
{
{
{
}
}
}
"
.
format
(
            
"
"
.
join
(
self
.
lr_item_to_str
(
prods
item
)
for
item
in
item_set
)
        
)
    
def
expand_terminal
(
self
t
:
str
)
-
>
OrderedFrozenSet
[
str
]
:
        
return
self
.
synthetic_terminals
.
get
(
t
)
or
OrderedFrozenSet
(
[
t
]
)
    
def
compatible_elements
(
self
e1
:
Element
e2
:
Element
)
-
>
bool
:
        
return
(
e1
=
=
e2
                
or
(
self
.
is_terminal
(
e1
)
                    
and
self
.
is_terminal
(
e2
)
                    
and
len
(
self
.
expand_terminal
(
e1
)
                            
&
self
.
expand_terminal
(
e2
)
)
>
0
)
)
    
def
compatible_sequences
(
            
self
            
seq1
:
typing
.
Sequence
[
Element
]
            
seq2
:
typing
.
Sequence
[
Element
]
)
-
>
bool
:
        
"
"
"
True
if
the
two
sequences
could
be
the
same
terminals
.
"
"
"
        
return
(
len
(
seq1
)
=
=
len
(
seq1
)
                
and
all
(
self
.
compatible_elements
(
e1
e2
)
for
e1
e2
in
zip
(
seq1
seq2
)
)
)
    
def
dump
(
self
)
:
        
for
nt
nt_def
in
self
.
nonterminals
.
items
(
)
:
            
left_side
=
self
.
element_to_str
(
nt
)
            
if
nt_def
.
params
:
                
left_side
+
=
"
[
"
+
"
"
.
join
(
nt_def
.
params
)
+
"
]
"
            
print
(
left_side
+
"
:
:
=
"
)
            
for
rhs
in
nt_def
.
rhs_list
:
                
print
(
"
"
self
.
rhs_to_str
(
rhs
)
)
            
print
(
)
    
def
dump_type_info
(
self
)
:
        
for
nt
nt_def
in
self
.
nonterminals
.
items
(
)
:
            
print
(
nt
nt_def
.
type
)
        
for
name
mty
in
self
.
methods
.
items
(
)
:
            
print
(
"
fn
{
}
(
{
}
)
-
>
{
}
"
                  
.
format
(
name
                          
"
"
.
join
(
types
.
type_to_str
(
ty
)
for
ty
in
mty
.
argument_types
)
                          
types
.
type_to_str
(
mty
.
return_type
)
)
)
    
def
is_shifted_element
(
self
e
:
Element
)
-
>
bool
:
        
if
isinstance
(
e
Nt
)
:
            
return
True
        
elif
self
.
is_terminal
(
e
)
:
            
return
True
        
elif
isinstance
(
e
Optional
)
:
            
return
True
        
elif
isinstance
(
e
LookaheadRule
)
:
            
return
False
        
elif
isinstance
(
e
End
)
:
            
return
True
        
elif
e
is
NoLineTerminatorHere
:
            
return
True
        
return
False
dataclass
(
frozen
=
True
)
class
InitNt
:
    
"
"
"
InitNt
(
goal
)
is
the
name
of
the
init
nonterminal
for
the
given
goal
.
    
One
init
nonterminal
is
created
internally
for
each
goal
symbol
in
the
grammar
.
    
The
idea
is
to
have
a
nonterminal
that
the
user
has
no
control
over
that
is
    
never
used
in
any
production
but
*
only
*
as
an
entry
point
for
the
grammar
    
that
always
has
a
single
production
"
init_nt
:
:
=
goal_nt
"
.
This
predictable
    
structure
makes
it
easier
to
get
into
and
out
of
parsing
at
run
time
.
    
When
an
init
nonterminal
is
matched
we
take
the
"
accept
"
action
rather
than
    
a
"
reduce
"
action
.
    
"
"
"
    
goal
:
Nt
def
is_concrete_element
(
e
:
Element
)
-
>
bool
:
    
"
"
"
True
if
parsing
the
element
e
produces
a
value
.
    
A
production
'
s
concrete
elements
can
be
used
in
reduce
expressions
.
    
"
"
"
    
return
not
isinstance
(
e
(
LookaheadRule
ErrorSymbol
NoLineTerminatorHereClass
)
)
class
Nt
:
    
"
"
"
Nt
(
name
(
(
param0
arg0
)
.
.
.
)
)
-
An
invocation
of
a
nonterminal
.
    
Nonterminals
are
like
lambdas
.
Each
nonterminal
in
a
grammar
is
defined
by
an
    
NtDef
which
has
0
or
more
parameters
.
    
Parameter
names
are
strings
.
The
arguments
are
typically
booleans
.
They
can
be
    
whatever
you
want
but
each
function
nonterminal
gets
expanded
into
a
set
of
    
productions
one
for
every
different
argument
tuple
that
is
ever
passed
to
it
.
    
"
"
"
    
__slots__
=
[
'
name
'
'
args
'
]
    
name
:
typing
.
Union
[
str
InitNt
]
    
args
:
typing
.
Tuple
[
typing
.
Tuple
[
str
typing
.
Hashable
]
.
.
.
]
    
def
__init__
(
self
                 
name
:
typing
.
Union
[
str
InitNt
]
                 
args
:
typing
.
Tuple
[
typing
.
Tuple
[
str
typing
.
Hashable
]
.
.
.
]
=
(
)
)
:
        
self
.
name
=
name
        
self
.
args
=
args
    
def
__hash__
(
self
)
-
>
int
:
        
return
hash
(
(
'
nt
'
self
.
name
self
.
args
)
)
    
def
__eq__
(
self
other
)
-
>
bool
:
        
return
(
isinstance
(
other
Nt
)
                
and
(
self
.
name
self
.
args
)
=
=
(
other
.
name
other
.
args
)
)
    
def
__repr__
(
self
)
-
>
str
:
        
if
self
.
args
:
            
return
'
Nt
(
{
!
r
}
{
!
r
}
)
'
.
format
(
self
.
name
self
.
args
)
        
else
:
            
return
'
Nt
(
{
!
r
}
)
'
.
format
(
self
.
name
)
    
def
pretty
(
self
)
-
>
str
:
        
"
"
"
Unique
version
of
this
Nt
to
use
in
the
Python
runtime
.
        
Also
used
in
debug
/
verbose
output
.
        
"
"
"
        
def
arg_to_str
(
name
value
)
:
            
if
value
is
True
:
                
return
'
+
'
+
name
            
elif
value
is
False
:
                
return
'
~
'
+
name
            
elif
isinstance
(
value
Var
)
:
                
if
value
.
name
=
=
name
:
                    
return
'
?
'
+
value
.
name
                
return
name
+
"
=
"
+
value
.
name
            
else
:
                
return
name
+
"
=
"
+
repr
(
value
)
        
if
isinstance
(
self
.
name
InitNt
)
:
            
return
"
Start_
"
+
self
.
name
.
goal
.
pretty
(
)
        
if
len
(
self
.
args
)
=
=
0
:
            
return
self
.
name
        
return
"
{
}
[
{
}
]
"
.
format
(
self
.
name
                               
"
"
.
join
(
arg_to_str
(
name
value
)
                                         
for
name
value
in
self
.
args
)
)
dataclass
(
frozen
=
True
)
class
Optional
:
    
"
"
"
Optional
(
nt
)
matches
either
nothing
or
the
given
nt
.
    
Optional
elements
are
expanded
out
before
states
are
calculated
so
the
    
core
of
the
algorithm
never
sees
them
.
    
"
"
"
    
inner
:
Element
dataclass
(
frozen
=
True
)
class
Literal
:
    
"
"
"
Literal
(
str
)
matches
a
sequence
of
characters
.
    
Literal
elements
are
sequences
of
characters
which
are
expected
to
appear
    
verbatim
in
the
input
.
    
"
"
"
    
text
:
str
dataclass
(
frozen
=
True
)
class
UnicodeCategory
:
    
"
"
"
UnicodeCategory
(
str
)
matches
any
character
with
a
category
matching
    
the
cat_prefix
.
    
UnicodeCategory
elements
are
a
set
of
literal
elements
which
correspond
to
a
    
given
unicode
cat_prefix
.
    
"
"
"
    
cat_prefix
:
str
dataclass
(
frozen
=
True
)
class
LookaheadRule
:
    
"
"
"
LookaheadRule
(
set
pos
)
imposes
a
lookahead
restriction
on
whatever
follows
.
    
It
never
consumes
any
tokens
itself
.
Instead
the
right
-
hand
side
    
[
LookaheadRule
(
frozenset
(
[
'
a
'
'
b
'
]
)
False
)
'
Thing
'
]
    
matches
a
Thing
that
does
not
start
with
the
token
a
or
b
.
    
"
"
"
    
set
:
typing
.
FrozenSet
[
str
]
    
positive
:
bool
def
lookahead_contains
(
rule
:
typing
.
Optional
[
LookaheadRule
]
t
:
str
)
:
    
"
"
"
True
if
the
given
lookahead
restriction
rule
allows
the
terminal
t
.
"
"
"
    
return
(
rule
is
None
            
or
(
t
in
rule
.
set
if
rule
.
positive
                
else
t
not
in
rule
.
set
)
)
def
lookahead_intersect
(
        
a
:
typing
.
Optional
[
LookaheadRule
]
        
b
:
typing
.
Optional
[
LookaheadRule
]
)
-
>
typing
.
Optional
[
LookaheadRule
]
:
    
"
"
"
Returns
a
single
rule
enforcing
both
a
and
b
allowing
only
terminals
that
pass
both
.
"
"
"
    
if
a
is
None
:
        
return
b
    
elif
b
is
None
:
        
return
a
    
elif
a
.
positive
:
        
if
b
.
positive
:
            
return
LookaheadRule
(
a
.
set
&
b
.
set
True
)
        
else
:
            
return
LookaheadRule
(
a
.
set
-
b
.
set
True
)
    
else
:
        
if
b
.
positive
:
            
return
LookaheadRule
(
b
.
set
-
a
.
set
True
)
        
else
:
            
return
LookaheadRule
(
a
.
set
|
b
.
set
False
)
class
NoLineTerminatorHereClass
:
    
def
__str__
(
self
)
:
        
return
'
NoLineTerminatorHere
'
NoLineTerminatorHere
=
NoLineTerminatorHereClass
(
)
dataclass
(
frozen
=
True
)
class
Exclude
:
    
"
"
"
Exclude
(
nt1
nt2
)
matches
if
nt1
matches
and
nt2
does
not
.
"
"
"
    
inner
:
Element
    
exclusion_list
:
typing
.
Tuple
[
Element
.
.
.
]
dataclass
(
frozen
=
True
)
class
End
:
    
"
"
"
End
(
)
represents
the
end
of
the
input
content
.
"
"
"
dataclass
(
frozen
=
True
)
class
ErrorSymbol
:
    
"
"
"
Special
grammar
symbol
that
can
be
consumed
to
handle
a
syntax
error
.
"
"
"
    
error_code
:
int
Element
=
typing
.
Union
[
    
str
    
Optional
    
Literal
    
UnicodeCategory
    
Exclude
    
Nt
    
LookaheadRule
    
End
    
ErrorSymbol
    
NoLineTerminatorHereClass
    
CallMethod
]
dataclass
class
NtDef
:
    
"
"
"
Definition
of
a
nonterminal
.
    
Instances
have
three
attributes
:
    
.
params
-
Tuple
of
strings
the
names
of
the
parameters
.
    
.
rhs_list
-
List
of
Production
objects
.
Arguments
to
Nt
elements
in
the
    
productions
can
be
Var
(
s
)
where
s
in
params
indicating
that
parameter
    
should
be
passed
through
unchanged
.
    
.
type
-
The
type
of
runtime
value
produced
by
parsing
an
instance
of
this
    
nonterminal
or
None
.
    
An
NtDef
is
a
sort
of
lambda
.
    
Some
langauges
have
constructs
that
are
allowed
or
disallowed
in
particular
    
situations
.
For
example
in
many
languages
return
statements
are
allowed
    
only
inside
functions
or
methods
.
The
ECMAScript
standard
(
5
.
1
.
5
"
Grammar
    
Notation
"
)
offers
this
example
of
the
notation
it
uses
to
specify
this
sort
    
of
thing
:
        
StatementList
[
Return
]
:
            
[
+
Return
]
ReturnStatement
            
ExpressionStatement
    
This
is
an
abbreviation
for
:
        
StatementList
:
            
ExpressionStatement
        
StatementList_Return
:
            
ReturnStatement
            
ExpressionStatement
    
We
offer
NtDef
.
params
as
a
way
of
representing
this
in
our
system
.
        
"
StatementList
"
:
NtDef
(
(
"
Return
"
)
[
            
Production
(
[
"
ReturnStatement
"
]
condition
=
(
"
Return
"
True
)
)
            
[
"
ExpressionStatement
"
]
        
]
None
)
    
This
is
an
abbreviation
for
:
        
"
StatementList_0
"
:
[
            
[
"
ExpressionStatement
"
]
        
]
        
"
StatementList_1
"
:
[
            
[
"
ReturnStatement
"
]
            
[
"
ExpressionStatement
"
]
        
]
    
"
"
"
    
__slots__
=
[
'
params
'
'
rhs_list
'
'
type
'
]
    
params
:
typing
.
Tuple
[
str
.
.
.
]
    
rhs_list
:
typing
.
List
[
Production
]
    
type
:
typing
.
Optional
[
types
.
Type
]
    
def
with_rhs_list
(
self
new_rhs_list
:
typing
.
List
[
Production
]
)
-
>
NtDef
:
        
return
dataclasses
.
replace
(
self
rhs_list
=
new_rhs_list
)
dataclass
(
frozen
=
True
)
class
Var
:
    
"
"
"
Var
(
name
)
represents
the
run
-
time
value
of
the
parameter
with
the
given
name
.
"
"
"
    
name
:
str
ReduceExpr
=
typing
.
Union
[
int
CallMethod
None
Some
]
ReduceExprOrAccept
=
typing
.
Union
[
ReduceExpr
str
]
LenientNt
=
typing
.
Union
[
Nt
str
InitNt
]
LenientProduction
=
typing
.
Union
[
Production
typing
.
List
[
Element
]
]
LenientNtDef
=
typing
.
Union
[
NtDef
typing
.
List
[
LenientProduction
]
]
