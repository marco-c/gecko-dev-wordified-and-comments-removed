"
"
"
Early
-
pipeline
operations
that
error
-
check
and
lower
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
collections
import
dataclasses
from
dataclasses
import
dataclass
import
typing
from
.
grammar
import
(
CallMethod
Element
End
ErrorSymbol
Exclude
Grammar
                      
LenientNt
Literal
LookaheadRule
Optional
                      
NoLineTerminatorHere
Nt
NtDef
NtParameter
Production
                      
ReduceExpr
ReduceExprOrAccept
Some
UnicodeCategory
                      
Var
is_concrete_element
)
from
.
ordered
import
OrderedFrozenSet
OrderedSet
from
.
runtime
import
ErrorToken
ErrorTokenClass
T
=
typing
.
TypeVar
(
"
T
"
)
def
fix
(
f
:
typing
.
Callable
[
[
T
]
T
]
start
:
T
)
-
>
T
:
    
"
"
"
Compute
a
fixed
point
of
f
the
hard
way
starting
from
start
.
"
"
"
    
prev
current
=
start
f
(
start
)
    
while
current
!
=
prev
:
        
prev
current
=
current
f
(
current
)
    
return
current
def
empty_nt_set
(
grammar
:
Grammar
)
-
>
typing
.
Dict
[
LenientNt
ReduceExprOrAccept
]
:
    
"
"
"
Determine
which
nonterminals
in
grammar
can
produce
the
empty
string
.
    
Return
a
dict
{
nt
:
expr
}
that
maps
each
such
nonterminal
to
the
expr
    
that
should
be
evaluated
when
reducing
the
empty
string
to
nt
.
    
So
for
example
if
we
have
a
production
        
a
:
:
=
b
?
c
?
=
>
CallMethod
(
"
a
"
[
0
1
]
)
    
then
the
resulting
dictionary
will
contain
the
entry
    
(
"
a
"
CallMethod
(
"
a
"
[
None
None
]
)
)
.
    
"
"
"
    
empties
:
typing
.
Dict
[
LenientNt
ReduceExprOrAccept
]
=
{
}
    
def
production_is_empty
(
p
:
Production
)
-
>
bool
:
        
return
all
(
isinstance
(
e
LookaheadRule
)
                   
or
isinstance
(
e
Optional
)
                   
or
(
isinstance
(
e
Nt
)
and
e
in
empties
)
                   
or
e
is
NoLineTerminatorHere
                   
for
e
in
p
.
body
)
    
def
evaluate_reducer_with_empty_matches
(
p
:
Production
)
-
>
ReduceExprOrAccept
:
        
stack
=
[
e
for
e
in
p
.
body
if
is_concrete_element
(
e
)
]
        
Expr
=
typing
.
TypeVar
(
"
Expr
"
ReduceExpr
ReduceExprOrAccept
)
        
def
eval
(
expr
:
Expr
)
-
>
Expr
:
            
if
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
Some
)
:
                
return
Some
(
eval
(
expr
.
inner
)
)
            
elif
isinstance
(
expr
CallMethod
)
:
                
return
dataclasses
.
replace
(
                    
expr
                    
args
=
tuple
(
eval
(
arg_expr
)
for
arg_expr
in
expr
.
args
)
                
)
            
elif
isinstance
(
expr
int
)
:
                
e
=
stack
[
expr
]
                
if
isinstance
(
e
Optional
)
:
                    
return
None
                
else
:
                    
assert
isinstance
(
e
Nt
)
                    
result
=
empties
[
e
]
                    
assert
not
isinstance
(
result
str
)
                    
return
result
            
elif
expr
=
=
'
accept
'
:
                
return
'
accept
'
            
else
:
                
raise
TypeError
(
                    
"
internal
error
:
unhandled
reduce
expression
type
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
        
return
eval
(
p
.
reducer
)
    
done
=
False
    
while
not
done
:
        
done
=
True
        
for
nt
nt_def
in
grammar
.
nonterminals
.
items
(
)
:
            
if
nt
not
in
empties
:
                
for
p
in
nt_def
.
rhs_list
:
                    
if
production_is_empty
(
p
)
:
                        
if
nt
in
empties
:
                            
raise
ValueError
(
                                
"
ambiguous
grammar
:
multiple
productions
for
"
                                
"
{
!
r
}
match
the
empty
string
"
                                
.
format
(
nt
)
)
                        
done
=
False
                        
empties
[
nt
]
=
evaluate_reducer_with_empty_matches
(
p
)
    
return
empties
def
check_cycle_free
(
grammar
:
Grammar
)
-
>
None
:
    
"
"
"
Throw
an
exception
if
any
nonterminal
in
grammar
produces
itself
    
via
a
cycle
of
1
or
more
productions
.
    
"
"
"
    
empties
=
empty_nt_set
(
grammar
)
    
direct_produces
:
typing
.
Dict
[
LenientNt
typing
.
Set
[
Nt
]
]
=
{
}
    
for
orig
in
grammar
.
nonterminals
:
        
direct_produces
[
orig
]
=
set
(
)
        
for
source_production
in
grammar
.
nonterminals
[
orig
]
.
rhs_list
:
            
for
rhs
_r
in
expand_optional_symbols_in_rhs
(
source_production
.
body
grammar
empties
)
:
                
result
:
typing
.
List
[
Nt
]
=
[
]
                
all_possibly_empty_so_far
=
True
                
for
e
in
rhs
:
                    
if
grammar
.
is_terminal
(
e
)
:
                        
break
                    
elif
isinstance
(
e
Nt
)
:
                        
if
e
in
empties
:
                            
if
all_possibly_empty_so_far
:
                                
result
.
append
(
e
)
                        
else
:
                            
if
not
all_possibly_empty_so_far
:
                                
break
                            
all_possibly_empty_so_far
=
False
                            
result
=
[
e
]
                    
elif
isinstance
(
e
Exclude
)
:
                        
if
isinstance
(
e
.
inner
Nt
)
:
                            
result
.
append
(
e
.
inner
)
                    
elif
isinstance
(
e
LookaheadRule
)
:
                        
pass
                    
elif
e
is
NoLineTerminatorHere
:
                        
pass
                    
elif
isinstance
(
e
Literal
)
:
                        
if
e
.
text
!
=
"
"
:
                            
break
                    
elif
isinstance
(
e
UnicodeCategory
)
:
                        
break
                    
elif
isinstance
(
e
End
)
:
                        
break
                    
elif
isinstance
(
e
CallMethod
)
:
                        
pass
                    
else
:
                        
assert
isinstance
(
e
ErrorSymbol
)
                
else
:
                    
direct_produces
[
orig
]
|
=
set
(
result
)
    
def
step
(
            
produces
:
typing
.
Dict
[
LenientNt
typing
.
Set
[
Nt
]
]
    
)
-
>
typing
.
Dict
[
LenientNt
typing
.
Set
[
Nt
]
]
:
        
return
{
            
orig
:
dest
|
set
(
b
for
a
in
dest
for
b
in
produces
[
a
]
)
            
for
orig
dest
in
produces
.
items
(
)
        
}
    
produces
=
fix
(
step
direct_produces
)
    
for
nt
in
grammar
.
nonterminals
:
        
if
nt
in
produces
[
nt
]
:
            
raise
ValueError
(
                
"
invalid
grammar
:
nonterminal
{
}
can
produce
itself
"
                
.
format
(
nt
)
)
def
check_lookahead_rules
(
grammar
:
Grammar
)
-
>
None
:
    
"
"
"
Check
that
no
LookaheadRule
appears
at
the
end
of
a
production
(
or
before
    
elements
that
can
produce
the
empty
string
)
.
    
If
there
are
any
offending
lookahead
rules
throw
a
ValueError
.
    
"
"
"
    
empties
=
empty_nt_set
(
grammar
)
    
check_cycle_free
(
grammar
)
    
for
nt
in
grammar
.
nonterminals
:
        
for
source_production
in
grammar
.
nonterminals
[
nt
]
.
rhs_list
:
            
body
=
source_production
.
body
            
for
rhs
_r
in
expand_optional_symbols_in_rhs
(
body
grammar
empties
)
:
                
if
rhs
and
isinstance
(
rhs
[
-
1
]
LookaheadRule
)
:
                    
raise
ValueError
(
                        
"
invalid
grammar
:
lookahead
restriction
"
                        
"
at
end
of
production
:
{
}
"
                        
.
format
(
grammar
.
production_to_str
(
nt
body
)
)
)
def
check_no_line_terminator_here
(
grammar
:
Grammar
)
-
>
None
:
    
empties
=
empty_nt_set
(
grammar
)
    
def
check
(
e
:
Element
nt
:
LenientNt
body
:
typing
.
List
[
Element
]
)
-
>
None
:
        
if
grammar
.
is_terminal
(
e
)
:
            
pass
        
elif
isinstance
(
e
Nt
)
:
            
if
e
in
empties
:
                
raise
ValueError
(
                    
"
invalid
grammar
:
[
no
LineTerminator
here
]
cannot
appear
next
to
"
                    
"
a
nonterminal
that
matches
the
empty
string
\
n
"
                    
"
in
production
:
{
}
"
.
format
(
grammar
.
production_to_str
(
nt
body
)
)
)
        
else
:
            
raise
ValueError
(
                
"
invalid
grammar
:
[
no
LineTerminator
here
]
must
appear
only
"
                
"
between
terminals
and
/
or
nonterminals
\
n
"
                
"
in
production
:
{
}
"
.
format
(
grammar
.
production_to_str
(
nt
body
)
)
)
    
for
nt
in
grammar
.
nonterminals
:
        
for
production
in
grammar
.
nonterminals
[
nt
]
.
rhs_list
:
            
body
=
production
.
body
            
for
i
e
in
enumerate
(
body
)
:
                
if
e
is
NoLineTerminatorHere
:
                    
if
i
=
=
0
or
i
=
=
len
(
body
)
-
1
:
                        
raise
ValueError
(
                            
"
invalid
grammar
:
[
no
LineTerminator
here
]
must
be
between
two
symbols
\
n
"
                            
"
in
production
:
{
}
"
.
format
(
grammar
.
production_to_str
(
nt
body
)
)
)
                    
check
(
body
[
i
-
1
]
nt
body
)
                    
check
(
body
[
i
+
1
]
nt
body
)
def
expand_parameterized_nonterminals
(
grammar
:
Grammar
)
-
>
Grammar
:
    
"
"
"
Replace
parameterized
nonterminals
with
specialized
copies
.
    
For
example
a
single
pair
nt_name
:
NtDef
(
params
=
(
'
A
'
'
B
'
)
.
.
.
)
in
    
grammar
.
nonterminals
will
be
replaced
with
(
assuming
A
and
B
are
boolean
    
parameters
)
up
to
four
pairs
each
having
an
Nt
object
as
the
key
and
an
    
NtDef
with
no
parameters
as
the
value
.
    
grammar
.
nonterminals
must
have
string
keys
.
    
Returns
a
new
copy
of
grammar
with
Nt
keys
whose
NtDefs
all
have
    
nt_def
.
params
=
=
[
]
.
    
"
"
"
    
todo
=
collections
.
deque
(
grammar
.
goals
(
)
)
    
new_nonterminals
=
{
}
    
def
expand
(
nt
:
Nt
)
-
>
NtDef
:
        
"
"
"
Expand
grammar
.
nonterminals
[
nt
]
(
*
*
args
)
.
        
Returns
the
expanded
NtDef
which
contains
no
conditional
        
productions
or
Nt
objects
.
        
"
"
"
        
if
nt
.
args
is
None
:
            
args_dict
=
None
        
else
:
            
args_dict
=
dict
(
nt
.
args
)
        
def
evaluate_arg
(
arg
:
NtParameter
)
-
>
NtParameter
:
            
if
isinstance
(
arg
Var
)
:
                
return
args_dict
[
arg
.
name
]
            
else
:
                
return
arg
        
def
expand_element
(
e
:
Element
)
-
>
Element
:
            
if
isinstance
(
e
Optional
)
:
                
return
Optional
(
expand_element
(
e
.
inner
)
)
            
elif
isinstance
(
e
Exclude
)
:
                
return
Exclude
(
expand_element
(
e
.
inner
)
tuple
(
map
(
expand_element
e
.
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
                
args
=
tuple
(
(
name
evaluate_arg
(
arg
)
)
                             
for
name
arg
in
e
.
args
)
                
e
=
Nt
(
e
.
name
args
)
                
if
e
not
in
new_nonterminals
:
                    
todo
.
append
(
e
)
                
return
e
            
else
:
                
return
e
        
def
expand_production
(
p
:
Production
)
-
>
Production
:
            
return
p
.
copy_with
(
                
body
=
[
expand_element
(
e
)
for
e
in
p
.
body
]
                
condition
=
None
)
        
def
expand_productions
(
nt_def
:
NtDef
)
-
>
NtDef
:
            
result
=
[
]
            
for
p
in
nt_def
.
rhs_list
:
                
if
p
.
condition
is
None
:
                    
included
=
True
                
else
:
                    
param
value
=
p
.
condition
                    
included
=
(
args_dict
[
param
]
=
=
value
)
                
if
included
:
                    
result
.
append
(
expand_production
(
p
)
)
            
return
NtDef
(
(
)
result
nt_def
.
type
)
        
nt_def
=
grammar
.
nonterminals
[
nt
.
name
]
        
assert
tuple
(
name
for
name
value
in
nt
.
args
)
=
=
nt_def
.
params
        
return
expand_productions
(
nt_def
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
not
in
new_nonterminals
:
            
new_nonterminals
[
nt
]
=
expand
(
nt
)
    
return
grammar
.
with_nonterminals
(
new_nonterminals
)
EMPTY
=
"
(
empty
)
"
END
=
None
TerminalOrEmpty
=
str
TerminalOrEmptyOrErrorToken
=
typing
.
Union
[
str
ErrorTokenClass
]
StartSets
=
typing
.
Dict
[
Nt
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
]
def
start_sets
(
grammar
:
Grammar
)
-
>
StartSets
:
    
"
"
"
Compute
the
start
sets
for
nonterminals
in
a
grammar
.
    
A
nonterminal
'
s
start
set
is
the
set
of
tokens
that
a
match
for
that
    
nonterminal
may
start
with
plus
EMPTY
if
it
can
match
the
empty
string
    
and
ErrorToken
if
it
can
start
with
an
error
.
    
"
"
"
    
assert
all
(
isinstance
(
nt
Nt
)
for
nt
in
grammar
.
nonterminals
)
    
start
:
StartSets
    
start
=
{
typing
.
cast
(
Nt
nt
)
:
OrderedFrozenSet
(
)
for
nt
in
grammar
.
nonterminals
}
    
done
=
False
    
while
not
done
:
        
done
=
True
        
for
nt
nt_def
in
grammar
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
nt
Nt
)
            
nt_start
=
OrderedFrozenSet
(
                
t
for
p
in
nt_def
.
rhs_list
for
t
in
seq_start
(
grammar
start
p
.
body
)
)
            
if
nt_start
!
=
start
[
nt
]
:
                
start
[
nt
]
=
nt_start
                
done
=
False
    
return
start
def
seq_start
(
        
grammar
:
Grammar
        
start
:
StartSets
        
seq
:
typing
.
List
[
Element
]
)
-
>
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
:
    
"
"
"
Compute
the
start
set
for
a
sequence
of
elements
.
"
"
"
    
s
:
OrderedSet
[
TerminalOrEmptyOrErrorToken
]
=
OrderedSet
(
[
EMPTY
]
)
    
for
i
e
in
enumerate
(
seq
)
:
        
if
EMPTY
not
in
s
:
            
break
        
s
.
remove
(
EMPTY
)
        
if
grammar
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
            
s
.
add
(
e
)
        
elif
isinstance
(
e
ErrorSymbol
)
:
            
s
.
add
(
ErrorToken
)
        
elif
isinstance
(
e
Nt
)
:
            
s
|
=
start
[
e
]
        
elif
e
is
NoLineTerminatorHere
:
            
s
.
add
(
EMPTY
)
        
else
:
            
assert
isinstance
(
e
LookaheadRule
)
            
future
=
seq_start
(
grammar
start
seq
[
i
+
1
:
]
)
            
if
e
.
positive
:
                
future
&
=
e
.
set
            
else
:
                
future
-
=
e
.
set
            
return
OrderedFrozenSet
(
future
)
    
return
OrderedFrozenSet
(
s
)
StartSetCache
=
typing
.
List
[
typing
.
List
[
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
]
]
def
make_start_set_cache
(
        
grammar
:
Grammar
        
prods
:
typing
.
List
[
Prod
]
        
start
:
StartSets
)
-
>
StartSetCache
:
    
"
"
"
Compute
start
sets
for
all
suffixes
of
productions
in
the
grammar
.
    
Returns
a
list
of
lists
cache
such
that
    
cache
[
n
]
[
i
]
=
=
seq_start
(
grammar
start
prods
[
n
]
[
i
:
]
)
.
    
(
The
cache
is
for
speed
since
seq_start
was
being
called
millions
of
    
times
.
)
    
"
"
"
    
def
suffix_start_list
(
            
rhs
:
typing
.
List
[
Element
]
    
)
-
>
typing
.
List
[
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
]
:
        
sets
:
typing
.
List
[
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
]
        
sets
=
[
OrderedFrozenSet
(
[
EMPTY
]
)
]
        
for
e
in
reversed
(
rhs
)
:
            
s
:
OrderedFrozenSet
[
TerminalOrEmptyOrErrorToken
]
            
if
grammar
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
                
s
=
OrderedFrozenSet
(
[
e
]
)
            
elif
isinstance
(
e
ErrorSymbol
)
:
                
s
=
OrderedFrozenSet
(
[
ErrorToken
]
)
            
elif
isinstance
(
e
Nt
)
:
                
s
=
start
[
e
]
                
if
EMPTY
in
s
:
                    
s
=
OrderedFrozenSet
(
(
s
-
{
EMPTY
}
)
|
sets
[
-
1
]
)
            
elif
e
is
NoLineTerminatorHere
:
                
s
=
sets
[
-
1
]
            
else
:
                
assert
isinstance
(
e
LookaheadRule
)
                
if
e
.
positive
:
                    
s
=
OrderedFrozenSet
(
sets
[
-
1
]
&
e
.
set
)
                
else
:
                    
s
=
OrderedFrozenSet
(
sets
[
-
1
]
-
e
.
set
)
            
assert
isinstance
(
s
OrderedFrozenSet
)
            
assert
s
=
=
seq_start
(
grammar
start
rhs
[
len
(
rhs
)
-
len
(
sets
)
:
]
)
            
sets
.
append
(
s
)
        
sets
.
reverse
(
)
        
assert
sets
=
=
[
seq_start
(
grammar
start
rhs
[
i
:
]
)
                        
for
i
in
range
(
len
(
rhs
)
+
1
)
]
        
return
sets
    
return
[
suffix_start_list
(
prod
.
rhs
)
for
prod
in
prods
]
FollowSet
=
OrderedSet
[
typing
.
Union
[
TerminalOrEmptyOrErrorToken
None
]
]
FollowSets
=
typing
.
DefaultDict
[
Nt
FollowSet
]
def
follow_sets
(
        
grammar
:
Grammar
        
prods_with_indexes_by_nt
:
typing
.
DefaultDict
[
            
LenientNt
            
typing
.
List
[
typing
.
Tuple
[
int
typing
.
List
[
Element
]
]
]
        
]
        
start_set_cache
:
StartSetCache
)
-
>
FollowSets
:
    
"
"
"
Compute
all
follow
sets
for
nonterminals
in
a
grammar
.
    
The
follow
set
for
a
nonterminal
A
as
defined
in
the
book
is
"
the
set
    
of
terminals
that
can
appear
immediately
to
the
right
of
A
in
some
    
sentential
form
"
;
plus
"
If
A
can
be
the
rightmost
symbol
in
some
    
sentential
form
then
is
in
FOLLOW
(
A
)
.
"
    
Returns
a
default
-
dictionary
mapping
nts
to
follow
sets
.
    
"
"
"
    
visited
=
set
(
)
    
follow
:
FollowSets
=
collections
.
defaultdict
(
OrderedSet
)
    
subsumes_relation
:
OrderedSet
[
typing
.
Tuple
[
Nt
Nt
]
]
    
subsumes_relation
=
OrderedSet
(
)
    
for
init_nt
in
grammar
.
init_nts
:
        
assert
isinstance
(
init_nt
Nt
)
        
follow
[
init_nt
]
.
add
(
END
)
    
def
visit
(
nt
:
Nt
)
-
>
None
:
        
if
nt
in
visited
:
            
return
        
visited
.
add
(
nt
)
        
for
prod_index
rhs
in
prods_with_indexes_by_nt
[
nt
]
:
            
for
i
symbol
in
enumerate
(
rhs
)
:
                
if
isinstance
(
symbol
Nt
)
:
                    
visit
(
symbol
)
                    
after
=
start_set_cache
[
prod_index
]
[
i
+
1
]
                    
if
EMPTY
in
after
:
                        
after
-
=
{
EMPTY
}
                        
subsumes_relation
.
add
(
(
symbol
nt
)
)
                    
follow
[
symbol
]
|
=
after
    
for
nt
in
grammar
.
init_nts
:
        
assert
isinstance
(
nt
Nt
)
        
visit
(
nt
)
    
done
=
False
    
while
not
done
:
        
done
=
True
        
for
target
source
in
subsumes_relation
:
            
if
follow
[
source
]
-
follow
[
target
]
:
                
follow
[
target
]
|
=
follow
[
source
]
                
done
=
False
    
return
follow
dataclass
class
Prod
:
    
nt
:
Nt
    
index
:
int
    
rhs
:
typing
.
List
    
reducer
:
ReduceExprOrAccept
def
expand_optional_symbols_in_rhs
(
        
rhs
:
typing
.
List
[
Element
]
        
grammar
:
Grammar
        
empties
:
typing
.
Dict
[
LenientNt
ReduceExprOrAccept
]
        
start_index
:
int
=
0
)
-
>
typing
.
Iterable
[
typing
.
Tuple
[
typing
.
List
[
Element
]
typing
.
Dict
[
int
ReduceExpr
]
]
]
:
    
"
"
"
Expand
a
sequence
with
optional
symbols
into
sequences
that
have
none
.
    
rhs
is
a
list
of
symbols
possibly
containing
optional
elements
.
This
    
yields
every
list
that
can
be
made
by
replacing
each
optional
element
    
either
with
its
.
inner
value
or
with
nothing
.
    
Each
list
is
accompanied
by
the
list
of
the
indices
of
optional
elements
in
    
rhs
that
were
dropped
.
    
For
example
expand_optional_symbols_in_rhs
(
[
"
if
"
Optional
(
"
else
"
)
]
)
    
yields
the
two
pairs
(
[
"
if
"
]
[
1
]
)
and
[
"
if
"
"
else
"
]
[
]
.
    
"
"
"
    
replacement
:
ReduceExpr
    
for
i
in
range
(
start_index
len
(
rhs
)
)
:
        
e
=
rhs
[
i
]
        
if
isinstance
(
e
Optional
)
:
            
if
isinstance
(
e
.
inner
Nt
)
and
e
.
inner
in
empties
:
                
raise
ValueError
(
                    
"
ambiguous
grammar
:
{
}
is
ambiguous
because
{
}
can
match
"
                    
"
the
empty
string
"
                    
.
format
(
grammar
.
element_to_str
(
e
)
                            
grammar
.
element_to_str
(
e
.
inner
)
)
)
            
replacement
=
None
            
break
        
elif
isinstance
(
e
Nt
)
and
e
in
empties
:
            
empty_expr
=
empties
[
e
]
            
assert
not
isinstance
(
empty_expr
str
)
            
replacement
=
empty_expr
            
break
    
else
:
        
yield
rhs
[
start_index
:
]
{
}
        
return
    
for
expanded
r
in
expand_optional_symbols_in_rhs
(
rhs
grammar
empties
i
+
1
)
:
        
e
=
rhs
[
i
]
        
rhs_inner
=
e
.
inner
if
isinstance
(
e
Optional
)
else
e
        
r2
=
r
.
copy
(
)
        
r2
[
i
]
=
replacement
        
yield
rhs
[
start_index
:
i
]
+
expanded
r2
        
yield
rhs
[
start_index
:
i
]
+
[
rhs_inner
]
+
expanded
r
def
expand_all_optional_elements
(
grammar
:
Grammar
)
-
>
typing
.
Tuple
[
        
Grammar
        
typing
.
List
[
Prod
]
        
typing
.
DefaultDict
[
LenientNt
typing
.
List
[
typing
.
Tuple
[
int
typing
.
List
[
Element
]
]
]
]
]
:
    
"
"
"
Expand
optional
elements
in
the
grammar
.
    
We
replace
each
production
that
contains
an
optional
element
with
two
    
productions
:
one
with
and
one
without
.
Downstream
of
this
step
we
can
    
ignore
the
possibility
of
optional
elements
.
    
"
"
"
    
expanded_grammar
:
typing
.
Dict
[
LenientNt
NtDef
]
=
{
}
    
empties
:
typing
.
Dict
[
LenientNt
ReduceExprOrAccept
]
=
{
}
    
prods
:
typing
.
List
[
Prod
]
=
[
]
    
prods_with_indexes_by_nt
:
\
        
typing
.
DefaultDict
[
LenientNt
typing
.
List
[
typing
.
Tuple
[
int
typing
.
List
[
Element
]
]
]
]
=
\
        
collections
.
defaultdict
(
list
)
    
for
nt
nt_def
in
grammar
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
nt
Nt
)
        
prods_expanded
=
[
]
        
for
prod_index
p
in
enumerate
(
nt_def
.
rhs_list
)
:
            
reduce_expr_to_offset
=
[
                
i
                
for
i
e
in
enumerate
(
p
.
body
)
                
if
is_concrete_element
(
e
)
            
]
            
for
pair
in
expand_optional_symbols_in_rhs
(
p
.
body
grammar
empties
)
:
                
expanded_rhs
removals
=
pair
                
Expr
=
typing
.
TypeVar
(
"
Expr
"
ReduceExpr
ReduceExprOrAccept
)
                
def
adjust_reduce_expr
(
expr
:
Expr
)
-
>
Expr
:
                    
if
isinstance
(
expr
int
)
:
                        
i
=
reduce_expr_to_offset
[
expr
]
                        
if
i
in
removals
:
                            
return
removals
[
i
]
                        
was_optional
=
isinstance
(
p
.
body
[
i
]
Optional
)
                        
expr
-
=
sum
(
1
for
r
in
removals
if
r
<
i
)
                        
if
was_optional
:
                            
return
Some
(
expr
)
                        
else
:
                            
return
expr
                    
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
Some
)
:
                        
return
Some
(
adjust_reduce_expr
(
expr
.
inner
)
)
                    
elif
isinstance
(
expr
CallMethod
)
:
                        
return
dataclasses
.
replace
(
                            
expr
                            
args
=
tuple
(
adjust_reduce_expr
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
                        
)
                    
elif
expr
=
=
'
accept
'
:
                        
return
'
accept
'
                    
else
:
                        
raise
TypeError
(
                            
"
internal
error
:
unrecognized
element
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
                
adjusted_reducer
=
adjust_reduce_expr
(
p
.
reducer
)
                
prods_expanded
.
append
(
                    
Production
(
body
=
expanded_rhs
                               
reducer
=
adjusted_reducer
)
)
                
prods
.
append
(
Prod
(
nt
prod_index
expanded_rhs
                                  
adjusted_reducer
)
)
                
prods_with_indexes_by_nt
[
nt
]
.
append
(
                    
(
len
(
prods
)
-
1
expanded_rhs
)
)
        
expanded_grammar
[
nt
]
=
nt_def
.
with_rhs_list
(
prods_expanded
)
    
return
(
grammar
.
with_nonterminals
(
expanded_grammar
)
            
prods
            
prods_with_indexes_by_nt
)
class
CanonicalGrammar
:
    
__slots__
=
[
"
prods
"
"
prods_with_indexes_by_nt
"
"
grammar
"
]
    
prods
:
typing
.
List
[
Prod
]
    
prods_with_indexes_by_nt
:
typing
.
Mapping
[
        
LenientNt
        
typing
.
List
[
typing
.
Tuple
[
int
typing
.
List
[
Element
]
]
]
]
    
grammar
:
Grammar
    
def
__init__
(
self
grammar
:
Grammar
)
-
>
None
:
        
grammar
=
expand_parameterized_nonterminals
(
grammar
)
        
check_cycle_free
(
grammar
)
        
check_no_line_terminator_here
(
grammar
)
        
grammar
prods
prods_with_indexes_by_nt
=
\
            
expand_all_optional_elements
(
grammar
)
        
self
.
prods
=
prods
        
self
.
prods_with_indexes_by_nt
=
prods_with_indexes_by_nt
        
self
.
grammar
=
grammar
