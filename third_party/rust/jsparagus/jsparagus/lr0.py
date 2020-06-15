"
"
"
Generate
a
simple
LR0
state
graph
from
a
CanonicalGrammar
.
The
resulting
graph
may
contain
inconsistent
states
which
must
be
resolved
by
the
ParseTable
before
a
parser
can
be
generated
.
"
"
"
from
__future__
import
annotations
import
collections
from
dataclasses
import
dataclass
import
typing
from
.
actions
import
(
Accept
Action
CheckNotOnNewLine
FunCall
Lookahead
                      
OutputExpr
Unwind
Reduce
Seq
)
from
.
ordered
import
OrderedFrozenSet
from
.
grammar
import
(
CallMethod
Element
End
ErrorSymbol
Grammar
                      
LookaheadRule
NoLineTerminatorHere
Nt
ReduceExpr
                      
ReduceExprOrAccept
Some
)
from
.
rewrites
import
CanonicalGrammar
Prod
from
.
import
types
dataclass
(
frozen
=
True
order
=
True
)
class
LRItem
:
    
"
"
"
A
snapshot
of
progress
through
a
single
specific
production
.
    
*
prod_index
identifies
the
production
.
(
Every
production
in
the
grammar
        
gets
a
unique
index
;
see
the
loop
that
computes
        
prods_with_indexes_by_nt
.
)
    
*
offset
is
the
position
of
the
cursor
within
the
production
.
    
lookahead
and
followed_by
are
two
totally
different
kinds
of
lookahead
.
    
*
lookahead
is
the
LookaheadRule
if
any
that
applies
to
the
immediately
        
upcoming
input
.
It
is
present
only
if
this
LRItem
is
subject
to
a
        
[
lookahead
]
restriction
;
otherwise
it
'
s
None
.
These
restrictions
can
'
t
        
extend
beyond
the
end
of
a
production
or
else
the
grammar
is
invalid
.
        
This
implements
the
lookahead
restrictions
in
the
ECMAScript
grammar
.
        
It
is
not
part
of
any
account
of
LR
I
'
ve
seen
.
    
*
followed_by
is
a
completely
different
kind
of
lookahead
restriction
.
        
This
is
the
kind
of
lookahead
that
is
a
central
part
of
canonical
LR
        
table
generation
.
It
applies
to
the
token
*
after
*
the
whole
current
        
production
so
followed_by
always
applies
to
completely
different
and
        
later
tokens
than
lookahead
.
followed_by
is
a
set
of
terminals
;
if
        
None
is
in
this
set
it
means
END
not
that
the
LRItem
is
        
unrestricted
.
    
"
"
"
    
prod_index
:
int
    
offset
:
int
    
lookahead
:
typing
.
Optional
[
LookaheadRule
]
    
followed_by
:
OrderedFrozenSet
[
typing
.
Optional
[
str
]
]
ShiftedTerm
=
typing
.
Union
[
str
Nt
ErrorSymbol
]
Term
=
typing
.
Union
[
ShiftedTerm
Action
]
def
on_stack
(
grammar
:
Grammar
term
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
Returns
whether
an
element
of
a
production
is
consuming
stack
space
or
    
not
.
"
"
"
    
if
isinstance
(
term
Nt
)
:
        
return
True
    
elif
grammar
.
is_terminal
(
term
)
:
        
return
True
    
elif
isinstance
(
term
LookaheadRule
)
:
        
return
False
    
elif
isinstance
(
term
ErrorSymbol
)
:
        
return
True
    
elif
isinstance
(
term
End
)
:
        
return
True
    
elif
term
is
NoLineTerminatorHere
:
        
return
False
    
elif
isinstance
(
term
CallMethod
)
:
        
return
False
    
raise
ValueError
(
term
)
def
callmethods_to_funcalls
(
        
expr
:
ReduceExprOrAccept
        
pop
:
int
        
ret
:
str
        
depth
:
int
        
funcalls
:
typing
.
List
[
Action
]
)
-
>
OutputExpr
:
    
"
"
"
Lower
a
reduce
-
expression
to
the
OutputExpr
language
.
    
CallMethod
expressions
are
replaced
with
FunCalls
;
all
new
FunCalls
created
    
in
this
way
are
appended
to
funcalls
.
    
"
"
"
    
if
isinstance
(
expr
int
)
:
        
stack_index
=
pop
-
expr
        
if
depth
=
=
0
:
            
call
=
FunCall
(
"
id
"
(
stack_index
)
fallible
=
False
                           
trait
=
types
.
Type
(
"
AstBuilder
"
)
set_to
=
ret
)
            
funcalls
.
append
(
call
)
            
return
ret
        
else
:
            
return
stack_index
    
elif
isinstance
(
expr
Some
)
:
        
res
=
callmethods_to_funcalls
(
expr
.
inner
pop
ret
depth
funcalls
)
        
return
Some
(
res
)
    
elif
expr
is
None
:
        
return
None
    
elif
isinstance
(
expr
CallMethod
)
:
        
def
convert_args
(
args
:
typing
.
Iterable
[
ReduceExpr
]
)
-
>
typing
.
Iterator
[
OutputExpr
]
:
            
for
i
arg
in
enumerate
(
args
)
:
                
yield
callmethods_to_funcalls
(
arg
pop
ret
+
"
_
{
}
"
.
format
(
i
)
depth
+
1
funcalls
)
        
args
=
tuple
(
convert_args
(
expr
.
args
)
)
        
call
=
FunCall
(
expr
.
method
args
                       
trait
=
expr
.
trait
                       
fallible
=
expr
.
fallible
                       
set_to
=
ret
)
        
funcalls
.
append
(
call
)
        
return
ret
    
elif
expr
=
=
"
accept
"
:
        
funcalls
.
append
(
Accept
(
)
)
        
return
ret
    
else
:
        
raise
ValueError
(
expr
)
class
LR0Generator
:
    
"
"
"
Provide
a
way
to
iterate
over
the
grammar
given
a
set
of
LR
items
.
"
"
"
    
__slots__
=
[
        
"
grammar
"
        
"
lr_items
"
        
"
key
"
        
"
_hash
"
    
]
    
grammar
:
CanonicalGrammar
    
lr_items
:
OrderedFrozenSet
[
LRItem
]
    
key
:
str
    
_hash
:
int
    
def
__init__
(
            
self
            
grammar
:
CanonicalGrammar
            
lr_items
:
typing
.
Iterable
[
LRItem
]
=
(
)
    
)
-
>
None
:
        
self
.
grammar
=
grammar
        
self
.
lr_items
=
OrderedFrozenSet
(
lr_items
)
        
self
.
key
=
"
"
.
join
(
repr
(
(
item
.
prod_index
item
.
offset
)
)
+
"
\
n
"
                           
for
item
in
sorted
(
self
.
lr_items
)
)
        
self
.
_hash
=
hash
(
self
.
key
)
    
def
__eq__
(
self
other
:
object
)
-
>
bool
:
        
return
isinstance
(
other
LR0Generator
)
and
self
.
key
=
=
other
.
key
    
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
self
.
_hash
    
def
__str__
(
self
)
-
>
str
:
        
s
=
"
"
        
for
lr_item
in
self
.
lr_items
:
            
s
+
=
self
.
grammar
.
grammar
.
lr_item_to_str
(
self
.
grammar
.
prods
lr_item
)
            
s
+
=
"
\
n
"
        
return
s
    
def
stable_locations
(
self
)
-
>
OrderedFrozenSet
[
str
]
:
        
locations
=
[
]
        
for
lr_item
in
self
.
lr_items
:
            
locations
.
append
(
self
.
grammar
.
grammar
.
lr_item_to_str
(
self
.
grammar
.
prods
lr_item
)
)
        
return
OrderedFrozenSet
(
sorted
(
locations
)
)
    
staticmethod
    
def
start
(
grammar
:
CanonicalGrammar
nt
:
Nt
)
-
>
LR0Generator
:
        
lr_items
:
typing
.
List
[
LRItem
]
=
[
]
        
todo
:
typing
.
Deque
[
Nt
]
=
collections
.
deque
(
)
        
visited_nts
=
[
]
        
todo
.
append
(
nt
)
        
while
todo
:
            
nt
=
todo
.
popleft
(
)
            
if
nt
in
visited_nts
:
                
continue
            
visited_nts
.
append
(
nt
)
            
for
prod_index
_
in
grammar
.
prods_with_indexes_by_nt
[
nt
]
:
                
assert
isinstance
(
prod_index
int
)
                
lr_items
.
append
(
LRItem
(
                    
prod_index
=
prod_index
                    
offset
=
0
                    
lookahead
=
None
                    
followed_by
=
OrderedFrozenSet
(
)
                
)
)
                
prod
=
grammar
.
prods
[
prod_index
]
                
assert
isinstance
(
prod
Prod
)
                
try
:
                    
term
=
prod
.
rhs
[
0
]
                    
if
isinstance
(
term
Nt
)
:
                        
todo
.
append
(
term
)
                
except
IndexError
:
                    
pass
        
return
LR0Generator
(
grammar
lr_items
)
    
def
transitions
(
self
)
-
>
typing
.
Dict
[
Term
LR0Generator
]
:
        
"
"
"
Returns
the
dictionary
which
maps
the
state
transitions
with
the
next
        
LR0Generators
.
This
can
be
used
to
generate
the
states
and
the
        
transitions
between
the
states
of
an
LR0
parse
table
.
"
"
"
        
followed_by
:
typing
.
DefaultDict
[
Term
typing
.
List
[
LRItem
]
]
        
followed_by
=
collections
.
defaultdict
(
list
)
        
for
lr_item
in
self
.
lr_items
:
            
self
.
item_transitions
(
lr_item
followed_by
)
        
return
{
k
:
LR0Generator
(
self
.
grammar
lr_items
)
                
for
k
lr_items
in
followed_by
.
items
(
)
}
    
def
item_transitions
(
            
self
            
lr_item
:
LRItem
            
followed_by
:
typing
.
DefaultDict
[
Term
typing
.
List
[
LRItem
]
]
    
)
-
>
None
:
        
"
"
"
Given
one
LRItem
register
all
the
transitions
and
LR
Items
reachable
        
through
these
transitions
.
"
"
"
        
prod
=
self
.
grammar
.
prods
[
lr_item
.
prod_index
]
        
assert
isinstance
(
prod
Prod
)
        
if
lr_item
.
offset
<
len
(
prod
.
rhs
)
:
            
term
=
prod
.
rhs
[
lr_item
.
offset
]
            
if
isinstance
(
term
Nt
)
:
                
pass
            
elif
self
.
grammar
.
grammar
.
is_terminal
(
term
)
:
                
pass
            
elif
isinstance
(
term
LookaheadRule
)
:
                
term
=
Lookahead
(
term
.
set
term
.
positive
)
            
elif
isinstance
(
term
ErrorSymbol
)
:
                
pass
            
elif
isinstance
(
term
End
)
:
                
pass
            
elif
term
is
NoLineTerminatorHere
:
                
term
=
CheckNotOnNewLine
(
)
            
elif
isinstance
(
term
CallMethod
)
:
                
funcalls
:
typing
.
List
[
Action
]
=
[
]
                
pop
=
sum
(
1
for
e
in
prod
.
rhs
[
:
lr_item
.
offset
]
if
on_stack
(
self
.
grammar
.
grammar
e
)
)
                
callmethods_to_funcalls
(
term
pop
"
expr
"
0
funcalls
)
                
term
=
Seq
(
funcalls
)
        
elif
lr_item
.
offset
=
=
len
(
prod
.
rhs
)
:
            
pop
=
sum
(
1
for
e
in
prod
.
rhs
if
on_stack
(
self
.
grammar
.
grammar
e
)
)
            
term
=
Reduce
(
Unwind
(
prod
.
nt
pop
)
)
            
expr
=
prod
.
reducer
            
if
expr
is
not
None
:
                
funcalls
=
[
]
                
callmethods_to_funcalls
(
expr
pop
"
value
"
0
funcalls
)
                
term
=
Seq
(
funcalls
+
[
term
]
)
        
else
:
            
return
        
new_transition
=
term
not
in
followed_by
        
followed_by
[
term
]
.
append
(
LRItem
(
            
prod_index
=
lr_item
.
prod_index
            
offset
=
lr_item
.
offset
+
1
            
lookahead
=
None
            
followed_by
=
OrderedFrozenSet
(
)
        
)
)
        
if
isinstance
(
term
Nt
)
and
new_transition
:
            
for
prod_index
_
in
self
.
grammar
.
prods_with_indexes_by_nt
[
term
]
:
                
assert
isinstance
(
prod_index
int
)
                
self
.
item_transitions
(
LRItem
(
                    
prod_index
=
prod_index
                    
offset
=
0
                    
lookahead
=
None
                    
followed_by
=
OrderedFrozenSet
(
)
                
)
followed_by
)
