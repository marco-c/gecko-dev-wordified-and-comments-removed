"
"
"
gen
.
py
-
Fifth
stab
at
a
parser
generator
.
*
*
Grammars
.
*
*
A
grammar
is
a
dictionary
{
str
:
[
[
symbol
]
]
}
mapping
names
of
nonterminals
to
lists
of
right
-
hand
sides
.
Each
right
-
hand
side
is
a
list
of
symbols
.
There
are
several
kinds
of
symbols
;
see
grammar
.
py
to
learn
more
.
Instead
of
a
list
of
right
-
hand
sides
the
value
of
a
grammar
entry
may
be
a
function
;
see
grammar
.
Nt
for
details
.
*
*
Token
streams
.
*
*
The
user
passes
to
each
method
an
object
representing
the
input
sequence
.
This
object
must
support
two
methods
:
*
src
.
peek
(
)
returns
the
kind
of
the
next
token
or
None
at
the
end
of
    
input
.
*
src
.
take
(
kind
)
throws
an
exception
if
src
.
peek
(
)
!
=
kind
;
    
otherwise
it
removes
the
next
token
from
the
input
stream
and
returns
it
.
    
The
special
case
src
.
take
(
None
)
checks
that
the
input
stream
is
empty
:
    
if
so
it
returns
None
;
if
not
it
throws
.
For
very
basic
needs
see
lexer
.
LexicalGrammar
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
io
import
pickle
import
sys
import
typing
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
grammar
import
(
Grammar
                      
NtDef
Production
Some
CallMethod
InitNt
                      
ReduceExprOrAccept
                      
is_concrete_element
                      
Optional
Exclude
Literal
UnicodeCategory
Nt
Var
                      
End
NoLineTerminatorHere
ErrorSymbol
                      
LookaheadRule
lookahead_contains
lookahead_intersect
)
from
.
actions
import
(
Action
Reduce
Lookahead
CheckNotOnNewLine
FilterFlag
                      
FunCall
Seq
)
from
.
import
emit
from
.
runtime
import
ACCEPT
ErrorToken
from
.
utils
import
keep_until
from
.
import
types
def
fix
(
f
start
)
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
)
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
=
{
}
    
def
production_is_empty
(
nt
p
)
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
)
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
        
def
eval
(
expr
)
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
CallMethod
(
                    
expr
.
method
                    
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
                    
expr
.
trait
                    
expr
.
fallible
                
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
                    
return
empties
[
e
]
            
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
nt
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
)
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
    
assert
isinstance
(
grammar
Grammar
)
    
empties
=
empty_nt_set
(
grammar
)
    
direct_produces
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
)
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
)
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
)
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
nt
body
)
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
)
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
)
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
)
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
)
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
)
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
)
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
def
start_sets
(
grammar
)
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
.
    
"
"
"
    
start
=
{
nt
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
start
seq
)
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
def
make_start_set_cache
(
grammar
prods
start
)
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
)
:
        
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
            
if
grammar
.
is_terminal
(
e
)
:
                
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
def
follow_sets
(
grammar
prods_with_indexes_by_nt
start_set_cache
)
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
=
collections
.
defaultdict
(
OrderedSet
)
    
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
)
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
str
    
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
grammar
empties
start_index
=
0
)
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
            
replacement
=
empties
[
e
]
            
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
        
rhs_inner
=
rhs
[
i
]
.
inner
if
isinstance
(
rhs
[
i
]
Optional
)
else
rhs
[
i
]
        
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
)
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
=
{
}
    
empties
=
{
}
    
prods
=
[
]
    
prods_with_indexes_by_nt
=
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
                
def
adjust_reduce_expr
(
expr
)
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
CallMethod
(
expr
.
method
[
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
]
                                          
expr
.
trait
                                          
expr
.
fallible
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
def
find_path
(
start_set
successors
test
)
:
    
"
"
"
Find
a
path
from
a
value
in
start_set
to
a
value
that
passes
test
.
    
start_set
is
an
iterable
of
"
points
"
.
successors
is
a
function
mapping
    
a
point
to
an
iterable
of
(
edge
point
)
pairs
.
test
is
a
predicate
on
    
points
.
All
points
must
support
hashing
;
edges
can
be
any
value
.
    
Returns
the
shortest
list
path
such
that
:
    
-
path
[
0
]
in
start_set
;
    
-
for
every
triplet
a
e
b
of
adjacent
elements
in
path
      
starting
with
an
even
index
(
e
b
)
in
successors
(
a
)
;
    
-
test
(
path
[
-
1
]
)
.
    
If
no
such
path
exists
returns
None
.
    
"
"
"
    
links
=
{
}
    
todo
=
collections
.
deque
(
)
    
for
p
in
start_set
:
        
if
p
not
in
links
:
            
links
[
p
]
=
None
            
if
test
(
p
)
:
                
return
[
p
]
            
todo
.
append
(
p
)
    
found
=
False
    
while
todo
:
        
a
=
todo
.
popleft
(
)
        
for
edge
b
in
successors
(
a
)
:
            
if
b
not
in
links
:
                
links
[
b
]
=
a
edge
                
if
test
(
b
)
:
                    
found
=
True
                    
todo
.
clear
(
)
                    
break
                
todo
.
append
(
b
)
    
if
not
found
:
        
return
None
    
path
=
[
b
]
    
while
links
[
b
]
is
not
None
:
        
a
edge
=
links
[
b
]
        
path
.
append
(
edge
)
        
path
.
append
(
a
)
        
b
=
a
    
path
.
reverse
(
)
    
return
path
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
typing
.
Set
[
typing
.
Optional
[
str
]
]
def
assert_items_are_compatible
(
grammar
prods
items
)
:
    
"
"
"
Assert
that
no
two
elements
of
items
have
conflicting
history
.
    
All
items
in
the
same
state
must
be
produced
by
the
same
history
    
the
same
sequence
of
terminals
and
nonterminals
.
    
"
"
"
    
if
len
(
items
)
=
=
0
:
        
return
    
def
item_history
(
item
)
:
        
return
[
e
                
for
e
in
prods
[
item
.
prod_index
]
.
rhs
[
:
item
.
offset
]
                
if
is_concrete_element
(
e
)
]
    
pairs
=
[
(
item
item_history
(
item
)
)
for
item
in
items
]
    
max_item
known_history
=
max
(
pairs
key
=
lambda
pair
:
len
(
pair
[
1
]
)
)
    
for
item
history
in
pairs
:
        
assert
grammar
.
compatible_sequences
(
history
known_history
[
-
len
(
history
)
:
]
)
\
            
"
incompatible
LR
items
:
\
n
{
}
\
n
{
}
\
n
"
.
format
(
                
grammar
.
lr_item_to_str
(
prods
max_item
)
                
grammar
.
lr_item_to_str
(
prods
item
)
)
class
PgenContext
:
    
"
"
"
The
immutable
part
of
the
parser
generator
'
s
data
.
"
"
"
    
def
__init__
(
self
grammar
prods
prods_with_indexes_by_nt
                 
nt_start_sets
start_set_cache
follow
)
:
        
self
.
grammar
=
grammar
        
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
nt_start_sets
=
nt_start_sets
        
self
.
start_set_cache
=
start_set_cache
        
self
.
follow
=
follow
    
def
make_lr_item
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
Create
an
LRItem
tuple
and
advance
it
past
any
lookahead
rules
.
        
The
main
algorithm
assumes
that
the
"
next
element
"
in
any
LRItem
is
        
never
a
lookahead
rule
.
We
ensure
that
is
true
by
processing
lookahead
        
elements
before
the
LRItem
is
even
exposed
.
        
We
don
'
t
bother
doing
extra
work
here
to
eliminate
lookahead
        
restrictions
that
are
redundant
with
what
'
s
coming
up
next
in
the
        
grammar
like
[
lookahead
!
=
NUM
]
when
the
production
is
        
name
:
:
=
IDENT
.
We
also
don
'
t
eliminate
items
that
can
'
t
match
        
like
name
:
:
=
IDENT
when
we
have
[
lookahead
not
in
{
IDENT
}
]
.
        
Such
silly
items
can
exist
;
but
we
would
only
care
if
it
caused
        
get_state_index
to
treat
equivalent
states
as
distinct
.
I
haven
'
t
seen
        
that
happen
for
any
grammar
yet
.
        
"
"
"
        
prods
=
self
.
prods
        
item
=
LRItem
(
*
args
*
*
kwargs
)
        
assert
isinstance
(
item
.
followed_by
OrderedFrozenSet
)
        
rhs
=
prods
[
item
.
prod_index
]
.
rhs
        
while
(
item
.
offset
<
len
(
rhs
)
               
and
isinstance
(
rhs
[
item
.
offset
]
LookaheadRule
)
)
:
            
item
=
item
.
_replace
(
                
offset
=
item
.
offset
+
1
                
lookahead
=
lookahead_intersect
(
item
.
lookahead
                                              
rhs
[
item
.
offset
]
)
)
        
if
False
:
            
expected
=
self
.
start_set_cache
[
item
.
prod_index
]
[
item
.
offset
]
            
if
item
.
lookahead
.
positive
:
                
ok_set
=
expected
&
item
.
lookahead
.
set
            
else
:
                
ok_set
=
expected
-
item
.
lookahead
.
set
            
if
len
(
ok_set
)
=
=
0
:
                
return
None
            
elif
ok_set
=
=
expected
:
                
look
=
None
            
else
:
                
look
=
LookaheadRule
(
OrderedFrozenSet
(
ok_set
)
True
)
            
item
=
item
.
_replace
(
lookahead
=
look
)
        
return
item
    
def
raise_reduce_reduce_conflict
(
self
state
t
i
j
)
:
        
scenario_str
=
state
.
traceback
(
)
        
p1
=
self
.
prods
[
i
]
        
p2
=
self
.
prods
[
j
]
        
raise
ValueError
(
            
"
reduce
-
reduce
conflict
when
looking
at
{
}
followed
by
{
}
\
n
"
            
"
can
'
t
decide
whether
to
reduce
with
:
\
n
"
            
"
{
}
\
n
"
            
"
or
with
:
\
n
"
            
"
{
}
\
n
"
            
.
format
(
scenario_str
self
.
grammar
.
element_to_str
(
t
)
                    
self
.
grammar
.
production_to_str
(
p1
.
nt
p1
.
rhs
)
                    
self
.
grammar
.
production_to_str
(
p2
.
nt
p2
.
rhs
)
)
)
    
def
why_start
(
self
t
prod_index
offset
)
:
        
"
"
"
Explain
why
t
in
START
(
prods
[
prod_index
]
[
offset
:
]
)
.
        
Yields
a
sequence
of
productions
showing
how
the
specified
suffix
can
        
expand
to
something
starting
with
t
.
        
If
prods
[
prod_index
]
[
offset
]
is
actually
t
the
sequence
is
empty
.
        
"
"
"
        
assert
t
in
self
.
start_set_cache
[
prod_index
]
[
offset
]
        
def
successors
(
pair
)
:
            
prod_index
offset
=
pair
            
rhs
=
self
.
prods
[
prod_index
]
.
rhs
            
nt
=
rhs
[
offset
]
            
if
not
isinstance
(
nt
Nt
)
:
                
return
            
for
next_prod_index
next_rhs
in
self
.
prods_with_indexes_by_nt
[
nt
]
:
                
if
t
in
self
.
start_set_cache
[
next_prod_index
]
[
0
]
:
                    
yield
next_prod_index
(
next_prod_index
0
)
        
def
done
(
pair
)
:
            
prod_index
offset
=
pair
            
rhs
=
self
.
prods
[
prod_index
]
.
rhs
            
return
rhs
[
offset
]
=
=
t
        
path
=
find_path
(
[
(
prod_index
offset
)
]
                         
successors
                         
done
)
        
if
path
is
None
:
            
return
        
for
prod_index
in
path
[
1
:
:
2
]
:
            
prod
=
self
.
prods
[
prod_index
]
            
yield
prod
.
nt
prod
.
rhs
    
def
why_follow
(
self
nt
t
)
:
        
"
"
"
Explain
why
the
terminal
t
is
in
nt
'
s
follow
set
.
        
Yields
a
sequence
of
productions
showing
how
a
goal
symbol
can
produce
        
a
string
of
terminals
and
nonterminals
that
contains
nt
followed
by
t
.
        
"
"
"
        
start_points
=
{
}
        
for
prod_index
prod
in
enumerate
(
self
.
prods
)
:
            
rhs1
=
prod
.
rhs
            
for
i
in
range
(
len
(
rhs1
)
-
1
)
:
                
if
(
isinstance
(
rhs1
[
i
]
Nt
)
                        
and
t
in
self
.
start_set_cache
[
prod_index
]
[
i
+
1
]
)
:
                    
start_points
[
rhs1
[
i
]
]
=
(
prod_index
i
+
1
)
        
def
successors
(
nt
)
:
            
for
prod_index
rhs
in
self
.
prods_with_indexes_by_nt
[
nt
]
:
                
last
=
rhs
[
-
1
]
                
if
isinstance
(
last
Nt
)
:
                    
yield
prod_index
last
        
path
=
find_path
(
start_points
.
keys
(
)
successors
                         
lambda
point
:
point
=
=
nt
)
        
prod_index
offset
=
start_points
[
path
[
0
]
]
        
prod
=
self
.
prods
[
prod_index
]
        
yield
prod
.
nt
prod
.
rhs
        
for
index
in
path
[
1
:
:
2
]
:
            
prod
=
self
.
prods
[
index
]
            
yield
prod
.
nt
prod
.
rhs
        
for
xnt
xrhs
in
self
.
why_start
(
t
prod_index
offset
)
:
            
yield
xnt
xrhs
    
def
raise_shift_reduce_conflict
(
self
state
t
shift_options
nt
rhs
)
:
        
assert
shift_options
        
assert
t
in
self
.
follow
[
nt
]
        
grammar
=
self
.
grammar
        
some_shift_option
=
next
(
iter
(
shift_options
)
)
        
t_str
=
grammar
.
element_to_str
(
t
)
        
scenario_str
=
state
.
traceback
(
)
        
productions
=
"
"
.
join
(
            
"
"
+
grammar
.
production_to_str
(
nt
rhs
)
+
"
\
n
"
            
for
nt
rhs
in
self
.
why_follow
(
nt
t
)
)
        
raise
ValueError
(
            
"
shift
-
reduce
conflict
when
looking
at
{
}
followed
by
{
}
\
n
"
            
"
can
'
t
decide
whether
to
shift
into
:
\
n
"
            
"
{
}
\
n
"
            
"
or
reduce
using
:
\
n
"
            
"
{
}
\
n
"
            
"
\
n
"
            
"
These
productions
show
how
{
}
can
appear
after
{
}
"
            
"
(
if
we
reduce
)
:
\
n
"
            
"
{
}
"
            
.
format
(
                
scenario_str
                
t_str
                
grammar
.
lr_item_to_str
(
                    
self
.
prods
some_shift_option
)
                
grammar
.
production_to_str
(
nt
rhs
)
                
t_str
                
nt
                
productions
)
)
class
State
:
    
"
"
"
A
parser
state
.
A
state
is
basically
a
set
of
LRItems
.
    
During
parser
generation
states
are
annotated
with
attributes
    
.
action_row
and
.
ctn_row
that
tell
the
actual
parser
what
to
do
at
run
    
time
.
These
will
become
rows
of
the
parser
tables
.
    
(
For
convenience
each
State
also
has
an
attribute
self
.
context
that
    
points
to
the
PgenContext
that
has
the
grammar
and
various
cached
data
;
and
    
an
attribute
_debug_traceback
used
in
error
messages
.
But
for
the
most
    
part
when
we
talk
about
a
"
state
"
we
only
care
about
the
frozen
set
of
    
LRItems
in
self
.
_lr_items
.
)
    
"
"
"
    
__slots__
=
[
        
'
context
'
        
'
_lr_items
'
        
'
_debug_traceback
'
        
'
key
'
        
'
_hash
'
        
'
action_row
'
        
'
ctn_row
'
        
'
error_code
'
        
'
id
'
    
]
    
def
__init__
(
self
context
items
debug_traceback
=
None
)
:
        
self
.
context
=
context
        
self
.
_debug_traceback
=
debug_traceback
        
a
=
collections
.
defaultdict
(
OrderedSet
)
        
for
item
in
items
:
            
a
[
item
.
prod_index
item
.
offset
item
.
lookahead
]
|
=
item
.
followed_by
        
self
.
_lr_items
=
OrderedFrozenSet
(
            
LRItem
(
*
k
OrderedFrozenSet
(
v
)
)
for
k
v
in
a
.
items
(
)
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
item
.
lookahead
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
_lr_items
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
        
assert_items_are_compatible
(
            
context
.
grammar
context
.
prods
self
.
_lr_items
)
    
def
__eq__
(
self
other
)
:
        
return
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
context
.
grammar
.
lr_item_to_str
(
self
.
context
.
prods
item
)
                
for
item
in
self
.
_lr_items
)
)
    
def
update
(
self
new_state
)
:
        
"
"
"
Merge
another
State
into
self
.
        
This
is
called
0
or
more
times
as
we
build
out
the
graph
of
states
.
        
It
'
s
called
each
time
an
edge
is
found
that
points
to
self
except
        
the
first
time
.
The
caller
has
created
a
State
object
new_state
but
        
then
found
that
this
compatible
State
object
already
exists
.
Merge
the
        
two
nodes
.
The
caller
discards
new_state
afterwards
.
        
Returns
True
if
anything
changed
.
        
"
"
"
        
assert
new_state
.
key
=
=
self
.
key
        
assert
len
(
self
.
_lr_items
)
=
=
len
(
new_state
.
_lr_items
)
        
def
item_key
(
item
)
:
            
return
item
.
prod_index
item
.
offset
item
.
lookahead
        
new_followed_by
=
{
            
item_key
(
item
)
:
item
.
followed_by
            
for
item
in
new_state
.
_lr_items
        
}
        
if
not
any
(
new_followed_by
[
item_key
(
item
)
]
-
item
.
followed_by
                   
for
item
in
self
.
_lr_items
)
:
            
return
False
        
self
.
_lr_items
=
OrderedFrozenSet
(
            
LRItem
(
*
item_key
(
item
)
                   
item
.
followed_by
|
new_followed_by
[
item_key
(
item
)
]
)
            
for
item
in
self
.
_lr_items
        
)
        
return
True
    
def
closure
(
self
)
:
        
"
"
"
Compute
transitive
closure
of
this
state
under
left
-
calls
.
        
That
is
return
a
superset
of
self
that
adds
every
item
that
'
s
        
reachable
from
it
by
"
stepping
in
"
to
nonterminals
without
consuming
        
any
tokens
.
Note
that
it
'
s
often
possible
to
"
step
in
"
repeatedly
.
        
This
is
the
only
part
of
the
system
that
makes
items
with
lookahead
        
restrictions
.
        
"
"
"
        
context
=
self
.
context
        
grammar
=
context
.
grammar
        
prods
=
context
.
prods
        
prods_with_indexes_by_nt
=
context
.
prods_with_indexes_by_nt
        
start_set_cache
=
context
.
start_set_cache
        
closure
=
OrderedSet
(
self
.
_lr_items
)
        
closure_todo
=
collections
.
deque
(
self
.
_lr_items
)
        
while
closure_todo
:
            
item
=
closure_todo
.
popleft
(
)
            
rhs
=
prods
[
item
.
prod_index
]
.
rhs
            
if
item
.
offset
<
len
(
rhs
)
:
                
next_symbol
=
rhs
[
item
.
offset
]
                
if
isinstance
(
next_symbol
Nt
)
:
                    
for
pair
in
prods_with_indexes_by_nt
[
next_symbol
]
:
                        
dest_prod_index
callee_rhs
=
pair
                        
if
(
callee_rhs
                                
or
any
(
p
.
body
=
=
callee_rhs
                                       
for
p
in
grammar
.
nonterminals
[
next_symbol
]
.
rhs_list
)
)
:
                            
followers
=
specific_follow
(
                                
start_set_cache
                                
item
.
prod_index
                                
item
.
offset
                                
item
.
followed_by
)
                            
new_item
=
context
.
make_lr_item
(
                                
dest_prod_index
                                
0
                                
item
.
lookahead
                                
followers
)
                            
if
(
new_item
is
not
None
                                    
and
new_item
not
in
closure
)
:
                                
closure
.
add
(
new_item
)
                                
closure_todo
.
append
(
new_item
)
        
return
closure
    
def
split_if_restricted
(
self
)
:
        
"
"
"
Handle
any
restricted
productions
relevant
to
this
state
.
        
If
any
items
in
this
state
have
a
[
no
LineTerminator
here
]
restriction
next
        
this
splits
the
state
and
returns
two
State
objects
:
        
-
The
first
is
a
clone
of
this
state
but
with
each
item
advanced
            
past
the
restriction
.
(
This
State
represents
the
situation
where
            
the
next
token
is
on
the
same
line
.
)
        
-
The
second
is
a
clone
of
this
state
but
with
all
restricted
            
productions
dropped
.
(
The
situation
where
the
next
token
is
on
a
            
new
line
.
)
        
If
no
items
in
this
state
have
a
[
no
LineTerminator
here
]
restriction
        
next
this
does
nothing
and
returns
None
.
        
"
"
"
        
restricted_items
=
[
]
        
prods
=
self
.
context
.
prods
        
for
i
item
in
enumerate
(
self
.
_lr_items
)
:
            
rhs
=
prods
[
item
.
prod_index
]
.
rhs
            
if
item
.
offset
<
len
(
rhs
)
and
rhs
[
item
.
offset
]
is
NoLineTerminatorHere
:
                
restricted_items
.
append
(
i
)
        
if
restricted_items
:
            
items_1
=
[
]
            
items_2
=
[
]
            
for
i
item
in
enumerate
(
self
.
_lr_items
)
:
                
if
i
in
restricted_items
:
                    
item
=
item
.
_replace
(
offset
=
item
.
offset
+
1
)
                
else
:
                    
items_2
.
append
(
item
)
                
items_1
.
append
(
item
)
            
s1
=
State
(
self
.
context
items_1
self
.
_debug_traceback
)
            
s2
=
State
(
self
.
context
items_2
self
.
_debug_traceback
)
            
return
s1
s2
        
else
:
            
return
None
    
def
merge_rows
(
self
s1
s2
)
:
        
action_row
=
{
}
        
for
t
in
OrderedSet
(
s1
.
action_row
)
|
OrderedSet
(
s2
.
action_row
)
:
            
s1_act
=
s1
.
action_row
.
get
(
t
)
            
s2_act
=
s2
.
action_row
.
get
(
t
)
            
if
s1_act
=
=
s2_act
:
                
action_row
[
t
]
=
s1_act
            
else
:
                
action_row
[
t
]
=
(
"
IfSameLine
"
s1_act
s2_act
)
        
ctn_row
=
{
}
        
for
nt
in
OrderedSet
(
s1
.
ctn_row
)
|
OrderedSet
(
s2
.
ctn_row
)
:
            
s1_ctn
=
s1
.
ctn_row
.
get
(
nt
)
            
s2_ctn
=
s2
.
ctn_row
.
get
(
nt
)
            
if
s1_ctn
is
None
:
                
ctn_row
[
nt
]
=
s2_ctn
            
elif
s2_ctn
is
None
or
s1_ctn
=
=
s2_ctn
:
                
ctn_row
[
nt
]
=
s1_ctn
            
else
:
                
raise
ValueError
(
"
conflicting
continuation
states
!
"
)
        
if
s1
.
error_code
!
=
s2
.
error_code
:
            
raise
ValueError
(
"
conflicting
error
codes
!
"
)
        
self
.
action_row
=
action_row
        
self
.
ctn_row
=
ctn_row
        
self
.
error_code
=
s1
.
error_code
    
def
analyze_if_restricted
(
self
get_state_index
*
verbose
=
False
)
:
        
split_result
=
self
.
split_if_restricted
(
)
        
if
split_result
is
None
:
            
return
False
        
else
:
            
s1
s2
=
split_result
            
s1
.
analyze
(
get_state_index
verbose
=
verbose
)
            
s2
.
analyze
(
get_state_index
verbose
=
verbose
)
            
self
.
merge_rows
(
s1
s2
)
            
return
True
    
def
analyze
(
self
get_state_index
*
verbose
=
False
)
:
        
"
"
"
Generate
the
LR
parser
table
entry
for
this
state
.
        
This
is
done
without
iterating
or
recursing
on
states
.
But
we
sometimes
        
need
state
-
ids
for
states
we
haven
'
t
considered
yet
so
it
calls
        
get_state_index
(
)
-
-
a
callback
that
can
enqueue
new
states
to
be
        
visited
later
.
        
"
"
"
        
if
self
.
analyze_if_restricted
(
get_state_index
verbose
=
verbose
)
:
            
return
        
context
=
self
.
context
        
grammar
=
context
.
grammar
        
prods
=
context
.
prods
        
follow
=
context
.
follow
        
nt_start_sets
=
context
.
nt_start_sets
        
if
verbose
:
            
print
(
"
State
{
}
.
"
.
format
(
self
.
id
)
)
            
for
item
in
self
.
_lr_items
:
                
print
(
"
"
+
grammar
.
lr_item_to_str
(
prods
item
)
)
            
print
(
)
        
shift_items
=
collections
.
defaultdict
(
            
OrderedSet
)
        
ctn_items
=
collections
.
defaultdict
(
            
OrderedSet
)
        
reduce_prods
=
{
}
        
error_item
=
None
        
error_code
=
None
        
def
add_edge
(
table
item
e
)
:
            
"
"
"
Make
an
edge
from
one
item
to
a
new
item
.
"
"
"
            
if
e
in
grammar
.
synthetic_terminals
:
                
for
rep
in
grammar
.
synthetic_terminals
[
e
]
:
                    
add_edge
(
table
item
rep
)
            
else
:
                
if
grammar
.
is_terminal
(
e
)
:
                    
if
not
lookahead_contains
(
item
.
lookahead
e
)
:
                        
return
                
elif
isinstance
(
e
Nt
)
:
                    
if
not
any
(
lookahead_contains
(
item
.
lookahead
t
)
                               
for
t
in
nt_start_sets
[
e
]
)
:
                        
return
                
else
:
                    
assert
e
=
=
ErrorToken
                
next_item
=
context
.
make_lr_item
(
                    
item
.
prod_index
                    
offset
+
1
                    
lookahead
=
None
                    
followed_by
=
item
.
followed_by
)
                
if
next_item
is
not
None
:
                    
table
[
e
]
.
add
(
next_item
)
        
for
item
in
self
.
closure
(
)
:
            
offset
=
item
.
offset
            
prod
=
prods
[
item
.
prod_index
]
            
nt
=
prod
.
nt
            
rhs
=
prod
.
rhs
            
if
offset
<
len
(
rhs
)
:
                
next_symbol
=
rhs
[
offset
]
                
if
(
grammar
.
is_terminal
(
next_symbol
)
                        
or
isinstance
(
next_symbol
ErrorSymbol
)
)
:
                    
if
isinstance
(
next_symbol
ErrorSymbol
)
:
                        
t
=
ErrorToken
                        
if
error_item
is
None
:
                            
error_item
=
item
                            
error_code
=
next_symbol
.
error_code
                        
else
:
                            
context
.
raise_error_conflict
(
error_item
item
)
                    
else
:
                        
t
=
next_symbol
                    
add_edge
(
shift_items
item
t
)
                
else
:
                    
assert
isinstance
(
next_symbol
Nt
)
                    
add_edge
(
ctn_items
item
next_symbol
)
            
else
:
                
if
item
.
lookahead
is
not
None
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
still
active
"
                        
"
at
end
of
production
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
rhs
)
)
)
                
for
t
in
grammar
.
expand_set_of_terminals
(
item
.
followed_by
)
:
                    
if
t
in
grammar
.
expand_set_of_terminals
(
follow
[
nt
]
)
:
                        
if
t
in
reduce_prods
:
                            
context
.
raise_reduce_reduce_conflict
(
                                
self
t
reduce_prods
[
t
]
item
.
prod_index
)
                        
reduce_prods
[
t
]
=
item
.
prod_index
        
assert
not
any
(
t
in
grammar
.
synthetic_terminals
for
t
in
shift_items
)
        
assert
not
any
(
t
in
grammar
.
synthetic_terminals
for
t
in
ctn_items
)
        
action_row
=
{
}
        
for
t
shift_state
in
shift_items
.
items
(
)
:
            
shift_state
=
State
(
context
shift_state
self
)
            
action_row
[
t
]
=
get_state_index
(
shift_state
)
        
for
t
prod_index
in
reduce_prods
.
items
(
)
:
            
prod
=
prods
[
prod_index
]
            
if
t
in
action_row
:
                
if
t
=
=
"
else
"
and
(
len
(
prod
.
rhs
)
=
=
5
                                    
and
prod
.
rhs
[
0
]
=
=
'
if
'
                                    
and
prod
.
rhs
[
1
]
=
=
'
(
'
                                    
and
prod
.
rhs
[
3
]
=
=
'
)
'
)
:
                    
assert
action_row
[
t
]
>
=
0
\
                        
"
the
action
we
already
have
should
be
a
shift
"
                    
continue
                
else
:
                    
context
.
raise_shift_reduce_conflict
(
                        
self
t
shift_items
[
t
]
prod
.
nt
prod
.
rhs
)
            
action_row
[
t
]
=
(
                
ACCEPT
if
isinstance
(
prod
.
nt
.
name
InitNt
)
                
else
-
prod_index
-
1
)
        
ctn_row
=
{
nt
:
get_state_index
(
State
(
context
ss
self
)
)
                   
for
nt
ss
in
ctn_items
.
items
(
)
}
        
self
.
action_row
=
action_row
        
self
.
ctn_row
=
ctn_row
        
self
.
error_code
=
error_code
    
def
traceback_scenario
(
self
)
:
        
"
"
"
Return
example
input
that
could
have
gotten
us
here
.
        
The
result
is
a
list
of
terminals
and
nonterminals
.
        
"
"
"
        
traceback
=
[
]
        
state
=
self
        
while
state
is
not
None
:
            
traceback
.
append
(
state
)
            
state
=
state
.
_debug_traceback
        
assert
next
(
iter
(
traceback
[
-
1
]
.
_lr_items
)
)
.
offset
=
=
0
        
del
traceback
[
-
1
]
        
traceback
.
reverse
(
)
        
scenario
=
[
]
        
for
state
in
traceback
:
            
item
=
next
(
iter
(
state
.
_lr_items
)
)
            
prod
=
self
.
context
.
prods
[
item
.
prod_index
]
            
i
=
item
.
offset
-
1
            
assert
i
>
=
0
            
while
isinstance
(
prod
.
rhs
[
i
]
LookaheadRule
)
:
                
i
-
=
1
                
assert
i
>
=
0
            
scenario
.
append
(
prod
.
rhs
[
i
]
)
        
return
scenario
    
def
traceback
(
self
)
:
        
"
"
"
Return
a
string
giving
example
input
that
could
have
gotten
us
here
.
        
This
is
for
error
messages
.
        
"
"
"
        
return
self
.
context
.
grammar
.
symbols_to_str
(
self
.
traceback_scenario
(
)
)
def
specific_follow
(
start_set_cache
prod_id
offset
followed_by
)
:
    
"
"
"
Return
the
set
of
tokens
that
match
after
the
nonterminal
rhs
[
offset
]
    
given
that
after
rhs
the
next
token
will
be
a
terminal
in
followed_by
.
    
"
"
"
    
result
=
start_set_cache
[
prod_id
]
[
offset
+
1
]
    
if
EMPTY
in
result
:
        
result
=
OrderedSet
(
result
)
        
result
.
remove
(
EMPTY
)
        
result
|
=
followed_by
    
return
OrderedFrozenSet
(
result
)
def
analyze_states
(
context
prods
*
verbose
=
False
progress
=
False
)
:
    
"
"
"
The
core
of
the
parser
generation
algorithm
.
"
"
"
    
states
=
[
]
    
states_by_key
=
{
}
    
todo
=
collections
.
deque
(
)
    
def
get_state_index
(
successor
)
:
        
"
"
"
Get
a
number
for
a
state
assigning
a
new
number
if
needed
.
"
"
"
        
assert
isinstance
(
successor
State
)
        
state
=
states_by_key
.
get
(
successor
.
key
)
        
if
state
is
not
None
:
            
if
state
.
update
(
successor
)
:
                
todo
.
append
(
state
)
        
else
:
            
state
=
successor
            
state
.
id
=
len
(
states
)
            
states
.
append
(
state
)
            
states_by_key
[
state
.
key
]
=
state
            
todo
.
append
(
state
)
        
return
state
.
id
    
init_state_map
=
{
}
    
for
init_nt
in
context
.
grammar
.
init_nts
:
        
init_prod_index
=
prods
.
index
(
            
Prod
(
init_nt
0
[
init_nt
.
name
.
goal
]
reducer
=
"
accept
"
)
)
        
start_item
=
context
.
make_lr_item
(
init_prod_index
                                          
0
                                          
lookahead
=
None
                                          
followed_by
=
OrderedFrozenSet
(
[
END
]
)
)
        
if
start_item
is
None
:
            
init_state
=
State
(
context
[
]
)
        
else
:
            
init_state
=
State
(
context
[
start_item
]
)
        
init_state_map
[
init_nt
.
name
.
goal
]
=
get_state_index
(
init_state
)
    
def
analyze_all_states
(
)
:
        
while
todo
:
            
yield
            
todo
.
popleft
(
)
.
analyze
(
get_state_index
verbose
=
verbose
)
    
consume
(
analyze_all_states
(
)
progress
)
    
return
ParserStates
(
context
.
grammar
prods
states
init_state_map
)
def
consume
(
iterator
progress
)
:
    
"
"
"
Drain
the
iterator
.
If
progress
is
true
print
dots
on
stdout
.
"
"
"
    
i
=
0
    
to_feed
=
str
(
i
)
    
try
:
        
for
_
in
iterator
:
            
if
progress
:
                
if
len
(
to_feed
)
>
0
:
                    
sys
.
stdout
.
write
(
to_feed
[
0
]
)
                    
to_feed
=
to_feed
[
1
:
]
                
else
:
                    
sys
.
stdout
.
write
(
"
.
"
)
                
i
+
=
1
                
if
i
%
100
=
=
0
:
                    
sys
.
stdout
.
write
(
"
\
n
"
)
                    
to_feed
=
str
(
i
)
                
sys
.
stdout
.
flush
(
)
    
finally
:
        
if
progress
and
i
!
=
0
:
            
sys
.
stdout
.
write
(
"
\
n
"
)
            
sys
.
stdout
.
flush
(
)
class
ParserStates
:
    
"
"
"
The
output
of
LALR
analysis
of
a
Grammar
.
"
"
"
    
def
__init__
(
self
grammar
prods
states
init_state_map
)
:
        
self
.
grammar
=
grammar
        
self
.
prods
=
prods
        
self
.
states
=
states
        
self
.
init_state_map
=
init_state_map
    
def
save
(
self
filename
)
:
        
with
open
(
filename
'
wb
'
)
as
f
:
            
pickle
.
dump
(
self
f
)
    
classmethod
    
def
load
(
cls
filename
)
:
        
with
open
(
filename
'
rb
'
)
as
f
:
            
obj
=
pickle
.
load
(
f
)
            
if
len
(
f
.
read
(
)
)
!
=
0
:
                
raise
ValueError
(
"
file
has
unexpected
extra
bytes
at
end
"
)
        
if
not
isinstance
(
obj
cls
)
:
            
raise
TypeError
(
"
file
contains
wrong
kind
of
object
:
expected
{
}
got
{
}
"
                            
.
format
(
cls
.
__name__
obj
.
__class__
.
__name__
)
)
        
return
obj
class
CanonicalGrammar
:
    
__slots__
=
"
prods
"
"
prods_with_indexes_by_nt
"
"
grammar
"
    
def
__init__
(
self
grammar
old
=
False
)
:
        
assert
isinstance
(
grammar
Grammar
)
        
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
dataclass
(
frozen
=
True
)
class
Edge
:
    
"
"
"
An
edge
in
a
Parse
table
is
a
tuple
of
a
source
state
and
the
term
followed
    
to
exit
this
state
.
The
destination
is
not
saved
here
as
it
can
easily
be
    
inferred
by
looking
it
up
in
the
parse
table
.
    
Note
the
term
might
be
None
if
no
term
is
specified
yet
.
This
is
useful
    
when
manipulating
a
list
of
edges
and
we
know
that
we
are
taking
transitions
    
from
a
given
state
but
not
yet
with
which
term
.
      
src
:
Index
of
the
state
from
which
this
directed
edge
is
coming
from
.
      
term
:
Edge
transition
value
this
can
be
a
terminal
non
-
terminal
or
an
          
action
to
be
executed
on
an
epsilon
transition
.
    
"
"
"
    
src
:
int
    
term
:
typing
.
Union
[
str
Nt
Action
]
def
edge_str
(
edge
)
:
    
assert
isinstance
(
edge
Edge
)
    
return
"
{
}
-
-
{
}
-
-
>
"
.
format
(
edge
.
src
str
(
edge
.
term
)
)
class
Conflict
(
Exception
)
:
    
pass
class
StateAndTransitions
:
    
"
"
"
This
is
one
state
of
the
parse
table
which
has
transitions
based
on
    
terminals
(
text
)
non
-
terminals
(
grammar
rules
)
and
epsilon
(
reduce
)
.
    
In
this
model
epsilon
transitions
are
used
to
represent
code
to
be
executed
    
such
as
reduce
actions
and
any
others
actions
.
    
"
"
"
    
__slots__
=
[
        
"
index
"
        
"
terminals
"
        
"
nonterminals
"
        
"
errors
"
        
"
epsilon
"
        
"
locations
"
        
"
delayed_actions
"
        
"
backedges
"
        
"
_hash
"
    
]
    
def
__init__
(
self
index
locations
delayed_actions
=
OrderedFrozenSet
(
)
)
:
        
assert
isinstance
(
locations
OrderedFrozenSet
)
        
assert
isinstance
(
delayed_actions
OrderedFrozenSet
)
        
self
.
index
=
index
        
self
.
terminals
=
{
}
        
self
.
nonterminals
=
{
}
        
self
.
errors
=
{
}
        
self
.
epsilon
=
[
]
        
self
.
locations
=
locations
        
self
.
delayed_actions
=
delayed_actions
        
self
.
backedges
=
OrderedSet
(
)
        
def
hashed_content
(
)
:
            
for
item
in
sorted
(
self
.
locations
)
:
                
yield
item
.
prod_index
                
yield
item
.
offset
            
yield
"
delayed_actions
"
            
for
action
in
sorted
(
delayed_actions
)
:
                
yield
hash
(
action
)
        
self
.
_hash
=
hash
(
tuple
(
hashed_content
(
)
)
)
    
def
is_inconsistent
(
self
)
:
        
"
Returns
True
if
the
state
transitions
are
inconsistent
.
"
        
if
len
(
self
.
terminals
)
+
len
(
self
.
nonterminals
)
+
len
(
self
.
errors
)
>
0
and
len
(
self
.
epsilon
)
>
0
:
            
return
True
        
elif
len
(
self
.
epsilon
)
=
=
1
:
            
if
any
(
k
.
is_inconsistent
(
)
for
k
s
in
self
.
epsilon
)
:
                
return
True
        
elif
len
(
self
.
epsilon
)
>
1
:
            
if
any
(
k
.
is_inconsistent
(
)
for
k
s
in
self
.
epsilon
)
:
                
return
True
            
if
any
(
not
k
.
is_condition
(
)
for
k
s
in
self
.
epsilon
)
:
                
return
True
            
if
any
(
not
isinstance
(
k
.
condition
(
)
FilterFlag
)
for
k
s
in
self
.
epsilon
)
:
                
return
True
            
if
len
(
set
(
k
.
condition
(
)
.
flag
for
k
s
in
self
.
epsilon
)
)
>
1
:
                
return
True
            
if
len
(
self
.
epsilon
)
!
=
len
(
set
(
k
.
condition
(
)
.
value
for
k
s
in
self
.
epsilon
)
)
:
                
return
True
        
else
:
            
try
:
                
self
.
get_error_symbol
(
)
            
except
ValueError
:
                
return
True
        
return
False
    
def
shifted_edges
(
self
)
:
        
for
k
s
in
self
.
terminals
.
items
(
)
:
            
yield
(
k
s
)
        
for
k
s
in
self
.
nonterminals
.
items
(
)
:
            
yield
(
k
s
)
        
for
k
s
in
self
.
errors
.
items
(
)
:
            
yield
(
k
s
)
    
def
edges
(
self
)
:
        
for
k
s
in
self
.
terminals
.
items
(
)
:
            
yield
(
k
s
)
        
for
k
s
in
self
.
nonterminals
.
items
(
)
:
            
yield
(
k
s
)
        
for
k
s
in
self
.
errors
.
items
(
)
:
            
yield
(
k
s
)
        
for
k
s
in
self
.
epsilon
:
            
yield
(
k
s
)
    
def
rewrite_state_indexes
(
self
state_map
)
:
        
self
.
index
=
state_map
[
self
.
index
]
        
self
.
terminals
=
{
            
k
:
state_map
[
s
]
for
k
s
in
self
.
terminals
.
items
(
)
        
}
        
self
.
nonterminals
=
{
            
k
:
state_map
[
s
]
for
k
s
in
self
.
nonterminals
.
items
(
)
        
}
        
self
.
errors
=
{
            
k
:
state_map
[
s
]
for
k
s
in
self
.
errors
.
items
(
)
        
}
        
self
.
epsilon
=
[
            
(
k
state_map
[
s
]
)
for
k
s
in
self
.
epsilon
        
]
        
self
.
backedges
=
set
(
            
Edge
(
state_map
[
edge
.
src
]
edge
.
term
)
for
edge
in
self
.
backedges
        
)
    
def
get_error_symbol
(
self
)
:
        
if
len
(
self
.
errors
)
>
1
:
            
raise
ValueError
(
"
More
than
one
error
symbol
on
the
same
state
.
"
)
        
else
:
            
return
next
(
iter
(
self
.
errors
)
None
)
    
def
__contains__
(
self
term
)
:
        
if
isinstance
(
term
Action
)
:
            
for
t
s
in
self
.
epsilon
:
                
if
t
=
=
term
:
                    
return
True
            
return
False
        
elif
isinstance
(
term
Nt
)
:
            
return
term
in
self
.
nonterminals
        
elif
isinstance
(
term
ErrorSymbol
)
:
            
return
term
in
self
.
errors
        
else
:
            
return
term
in
self
.
terminals
    
def
__getitem__
(
self
term
)
:
        
if
isinstance
(
term
Action
)
:
            
for
t
s
in
self
.
epsilon
:
                
if
t
=
=
term
:
                    
return
s
            
raise
KeyError
(
term
)
        
elif
isinstance
(
term
Nt
)
:
            
return
self
.
nonterminals
[
term
]
        
if
isinstance
(
term
ErrorSymbol
)
:
            
return
self
.
errors
[
term
]
        
else
:
            
return
self
.
terminals
[
term
]
    
def
get
(
self
term
default
)
:
        
try
:
            
return
self
.
__getitem__
(
term
)
        
except
KeyError
:
            
return
default
    
def
__str__
(
self
)
:
        
conflict
=
"
"
        
if
self
.
is_inconsistent
(
)
:
            
conflict
=
"
(
inconsistent
)
"
        
return
"
{
}
{
}
:
\
n
{
}
"
.
format
(
self
.
index
conflict
"
\
n
"
.
join
(
[
            
"
\
t
{
}
-
-
>
{
}
"
.
format
(
k
s
)
for
k
s
in
self
.
edges
(
)
]
)
)
    
def
__eq__
(
self
other
)
:
        
assert
isinstance
(
other
StateAndTransitions
)
        
if
sorted
(
self
.
locations
)
!
=
sorted
(
other
.
locations
)
:
            
return
False
        
if
sorted
(
self
.
delayed_actions
)
!
=
sorted
(
other
.
delayed_actions
)
:
            
return
False
        
return
True
    
def
__hash__
(
self
)
:
        
return
self
.
_hash
def
on_stack
(
grammar
term
)
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
pop
ret
depth
funcalls
)
:
    
alias_set
=
[
"
parser
"
]
    
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
            
expr
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
                           
alias_read
=
alias_set
alias_write
=
alias_set
)
            
funcalls
.
append
(
expr
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
)
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
        
expr
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
                       
alias_read
=
alias_set
                       
alias_write
=
alias_set
)
        
funcalls
.
append
(
expr
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
        
expr
=
FunCall
(
"
accept
"
(
)
                       
trait
=
types
.
Type
(
"
ParserTrait
"
)
                       
fallible
=
False
                       
set_to
=
ret
                       
alias_read
=
alias_set
                       
alias_write
=
alias_set
)
        
funcalls
.
append
(
expr
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
    
def
__init__
(
self
grammar
lr_items
=
[
]
)
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
)
:
        
return
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
    
staticmethod
    
def
start
(
grammar
nt
)
:
        
assert
isinstance
(
grammar
CanonicalGrammar
)
        
assert
isinstance
(
grammar
.
grammar
Grammar
)
        
lr_items
=
[
]
        
todo
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
tuple
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
=
collections
.
defaultdict
(
lambda
:
[
]
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
        
for
k
lr_items
in
followed_by
.
items
(
)
:
            
followed_by
[
k
]
=
LR0Generator
(
self
.
grammar
lr_items
)
        
return
followed_by
    
def
item_transitions
(
self
lr_item
followed_by
)
:
        
"
"
"
Given
one
LR
Item
register
all
the
transitions
and
LR
Items
reachables
        
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
prod
.
nt
pop
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
tuple
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
tuple
(
)
                
)
followed_by
)
dataclass
(
frozen
=
True
)
class
APS
:
    
"
"
"
Abstract
parser
state
.
    
To
fix
inconsistencies
of
the
grammar
we
have
to
traverse
the
grammar
both
    
forward
by
using
the
lookahead
and
backward
by
using
the
parser
'
s
emulated
    
stack
recovered
from
reduce
actions
.
    
To
do
so
we
define
the
notion
of
abstract
parser
state
(
APS
)
which
is
a
    
tuple
which
represent
the
known
state
of
the
parser
as
:
      
(
stack
shift
lookahead
actions
)
      
stack
:
This
is
the
stack
at
the
location
where
we
started
investigating
.
             
Which
means
that
the
last
element
of
the
stack
would
be
the
location
             
where
we
started
.
      
shift
:
This
is
the
stack
computed
after
the
traversal
of
edges
.
It
is
             
reduced
each
time
a
reduce
action
is
encountered
and
the
rest
of
             
the
production
content
is
added
back
to
the
stack
as
newly
acquired
             
context
.
The
last
element
is
the
last
state
reached
through
the
             
sequence
of
lookahead
and
actions
.
      
lookahead
:
This
is
the
list
of
terminals
encountered
while
pushing
edges
             
through
the
list
of
terminals
.
      
actions
:
This
is
the
list
of
actions
that
would
be
executed
as
we
push
             
edges
.
Maybe
we
should
rename
this
history
.
This
is
a
list
of
edges
             
taken
which
helps
tracking
which
state
got
visited
since
we
             
started
.
      
replay
:
This
is
the
list
of
lookahead
terminals
and
non
-
terminals
which
             
remains
to
be
executed
.
This
represents
the
fact
that
reduce
actions
             
are
popping
elements
which
are
below
the
top
of
the
stack
and
add
             
them
back
to
the
stack
.
    
"
"
"
    
stack
:
typing
.
List
[
Edge
]
    
shift
:
typing
.
List
[
Edge
]
    
lookahead
:
typing
.
List
[
str
]
    
actions
:
typing
.
List
[
Edge
]
    
replay
:
typing
.
List
[
typing
.
Union
[
str
Nt
]
]
def
aps_str
(
aps
name
=
"
aps
"
)
:
    
return
"
"
"
{
}
.
stack
=
[
{
}
]
{
}
.
shift
=
[
{
}
]
{
}
.
lookahead
=
[
{
}
]
{
}
.
actions
=
[
{
}
]
{
}
.
replay
=
[
{
}
]
    
"
"
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
edge_str
(
e
)
for
e
in
aps
.
stack
)
        
name
"
"
.
join
(
edge_str
(
e
)
for
e
in
aps
.
shift
)
        
name
"
"
.
join
(
repr
(
e
)
for
e
in
aps
.
lookahead
)
        
name
"
"
.
join
(
edge_str
(
e
)
for
e
in
aps
.
actions
)
        
name
"
"
.
join
(
repr
(
e
)
for
e
in
aps
.
replay
)
    
)
def
aps_lanes_str
(
aps_lanes
header
=
"
lanes
:
"
name
=
"
\
taps
"
)
:
    
return
"
{
}
\
n
{
}
"
.
format
(
header
"
\
n
"
.
join
(
aps_str
(
aps
name
)
for
aps
in
aps_lanes
)
)
def
is_valid_aps
(
aps
)
:
    
"
Returns
whether
an
APS
contains
the
right
content
.
"
    
check
=
True
    
check
&
=
all
(
isinstance
(
st
Edge
)
for
st
in
aps
.
stack
)
    
check
&
=
all
(
isinstance
(
sh
Edge
)
for
sh
in
aps
.
shift
)
    
check
&
=
all
(
not
isinstance
(
la
Action
)
for
la
in
aps
.
lookahead
)
    
check
&
=
all
(
isinstance
(
ac
Edge
)
for
ac
in
aps
.
actions
)
    
check
&
=
all
(
not
isinstance
(
rp
Action
)
for
rp
in
aps
.
replay
)
    
return
check
class
ParseTable
:
    
"
"
"
The
parser
can
be
represented
as
a
matrix
of
state
transitions
where
on
one
    
side
we
have
the
current
state
and
on
the
other
we
have
the
expected
    
terminal
non
-
terminal
or
epsilon
transition
.
            
a
b
c
A
B
C
#
1
#
2
#
3
          
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
-
+
-
-
-
-
+
-
-
-
-
+
      
s1
|
|
|
|
|
|
|
|
|
|
      
s2
|
|
|
|
|
|
|
|
|
|
      
s3
|
|
|
|
|
|
|
|
|
|
       
.
|
|
|
|
|
|
|
|
|
|
       
.
|
|
|
|
|
|
|
|
|
|
       
.
|
|
|
|
|
|
|
|
|
|
      
s67
|
|
|
|
|
|
|
|
|
|
      
s68
|
|
|
|
|
|
|
|
|
|
      
s69
|
|
|
|
|
|
|
|
|
|
          
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
+
-
-
-
-
+
-
-
-
-
+
-
-
-
-
+
    
The
terminals
a
are
the
token
which
are
read
from
the
input
.
The
    
non
-
terminals
A
are
the
token
which
are
pushed
by
the
reduce
actions
of
    
the
epsilon
transitions
.
The
epsilon
transitions
#
1
are
the
actions
which
    
have
to
be
executed
as
code
by
the
parser
.
    
A
parse
table
is
inconsistent
if
there
is
any
state
which
has
an
epsilon
    
transitions
and
terminals
/
non
-
terminals
transitions
(
shift
-
reduce
    
conflict
)
or
a
state
with
more
than
one
epsilon
transitions
(
reduce
-
reduce
    
conflict
)
.
This
is
equivalent
to
having
a
non
deterministic
state
machine
.
    
"
"
"
    
__slots__
=
[
        
"
actions
"
        
"
states
"
        
"
state_cache
"
        
"
named_goals
"
        
"
terminals
"
        
"
nonterminals
"
        
"
flags
"
        
"
debug_info
"
        
"
exec_modes
"
    
]
    
def
__init__
(
self
grammar
verbose
=
False
progress
=
False
debug
=
False
)
:
        
self
.
actions
=
[
]
        
self
.
states
=
[
]
        
self
.
state_cache
=
{
}
        
self
.
named_goals
=
[
]
        
self
.
terminals
=
grammar
.
grammar
.
terminals
        
self
.
nonterminals
=
list
(
grammar
.
grammar
.
nonterminals
.
keys
(
)
)
        
self
.
debug_info
=
debug
        
self
.
exec_modes
=
grammar
.
grammar
.
exec_modes
        
self
.
create_lr0_table
(
grammar
verbose
progress
)
        
self
.
fix_inconsistent_table
(
verbose
progress
)
        
self
.
remove_all_unreachable_state
(
verbose
progress
)
        
self
.
fold_identical_endings
(
verbose
progress
)
        
self
.
group_epsilon_states
(
verbose
progress
)
    
def
save
(
self
filename
)
:
        
with
open
(
filename
'
wb
'
)
as
f
:
            
pickle
.
dump
(
self
f
)
    
classmethod
    
def
load
(
cls
filename
)
:
        
with
open
(
filename
'
rb
'
)
as
f
:
            
obj
=
pickle
.
load
(
f
)
            
if
len
(
f
.
read
(
)
)
!
=
0
:
                
raise
ValueError
(
"
file
has
unexpected
extra
bytes
at
end
"
)
        
if
not
isinstance
(
obj
cls
)
:
            
raise
TypeError
(
"
file
contains
wrong
kind
of
object
:
expected
{
}
got
{
}
"
                            
.
format
(
cls
.
__name__
obj
.
__class__
.
__name__
)
)
        
return
obj
    
def
is_inconsistent
(
self
)
:
        
"
Returns
True
if
the
grammar
contains
any
inconsistent
state
.
"
        
for
s
in
self
.
states
:
            
if
s
is
not
None
and
s
.
is_inconsistent
(
)
:
                
return
True
        
return
False
    
def
new_state
(
self
locations
delayed_actions
=
OrderedFrozenSet
(
)
)
:
        
"
"
"
Get
or
create
state
with
an
LR0
location
and
delayed
actions
.
Returns
a
tuple
        
where
the
first
element
is
whether
the
element
is
newly
created
and
        
the
second
element
is
the
State
object
.
"
"
"
        
index
=
len
(
self
.
states
)
        
state
=
StateAndTransitions
(
index
locations
delayed_actions
)
        
try
:
            
return
False
self
.
state_cache
[
state
]
        
except
KeyError
:
            
self
.
state_cache
[
state
]
=
state
            
self
.
states
.
append
(
state
)
            
return
True
state
    
def
get_state
(
self
locations
delayed_actions
=
OrderedFrozenSet
(
)
)
:
        
"
"
"
Like
new_state
(
)
but
only
returns
the
state
without
returning
whether
it
is
        
newly
created
or
not
.
"
"
"
        
_
state
=
self
.
new_state
(
locations
delayed_actions
)
        
return
state
    
def
remove_state
(
self
s
maybe_unreachable_set
)
:
        
state
=
self
.
states
[
s
]
        
self
.
clear_edges
(
state
maybe_unreachable_set
)
        
del
self
.
state_cache
[
state
]
        
self
.
states
[
s
]
=
None
    
def
add_edge
(
self
src
term
dest
)
:
        
assert
isinstance
(
src
StateAndTransitions
)
        
assert
term
not
in
src
        
assert
isinstance
(
dest
int
)
and
dest
<
len
(
self
.
states
)
        
if
isinstance
(
term
Action
)
:
            
src
.
epsilon
.
append
(
(
term
dest
)
)
        
elif
isinstance
(
term
Nt
)
:
            
src
.
nonterminals
[
term
]
=
dest
        
elif
isinstance
(
term
ErrorSymbol
)
:
            
src
.
errors
[
term
]
=
dest
        
else
:
            
src
.
terminals
[
term
]
=
dest
        
self
.
states
[
dest
]
.
backedges
.
add
(
Edge
(
src
.
index
term
)
)
    
def
remove_backedge
(
self
src
term
dest
maybe_unreachable_set
)
:
        
self
.
states
[
dest
]
.
backedges
.
remove
(
Edge
(
src
.
index
term
)
)
        
maybe_unreachable_set
.
add
(
dest
)
    
def
replace_edge
(
self
src
term
dest
maybe_unreachable_set
)
:
        
assert
isinstance
(
src
StateAndTransitions
)
        
assert
isinstance
(
dest
int
)
and
dest
<
len
(
self
.
states
)
        
if
term
in
src
:
            
old_dest
=
src
[
term
]
            
self
.
remove_backedge
(
src
term
old_dest
maybe_unreachable_set
)
        
if
isinstance
(
term
Action
)
:
            
src
.
epsilon
=
[
(
t
d
)
for
t
d
in
src
.
epsilon
if
t
!
=
term
]
            
src
.
epsilon
.
append
(
(
term
dest
)
)
        
elif
isinstance
(
term
Nt
)
:
            
src
.
nonterminals
[
term
]
=
dest
        
elif
isinstance
(
term
ErrorSymbol
)
:
            
src
.
errors
[
term
]
=
dest
        
else
:
            
src
.
terminals
[
term
]
=
dest
        
self
.
states
[
dest
]
.
backedges
.
add
(
Edge
(
src
.
index
term
)
)
    
def
clear_edges
(
self
src
maybe_unreachable_set
)
:
        
"
"
"
Remove
all
existing
edges
in
order
to
replace
them
by
new
one
.
This
is
used
        
when
resolving
shift
-
reduce
conflicts
.
"
"
"
        
assert
isinstance
(
src
StateAndTransitions
)
        
for
term
dest
in
src
.
edges
(
)
:
            
self
.
remove_backedge
(
src
term
dest
maybe_unreachable_set
)
        
src
.
terminals
=
{
}
        
src
.
nonterminals
=
{
}
        
src
.
errors
=
{
}
        
src
.
epsilon
=
[
]
    
def
remove_unreachable_states
(
self
maybe_unreachable_set
)
:
        
_
init
=
zip
(
*
self
.
named_goals
)
        
init
=
set
(
init
)
        
while
maybe_unreachable_set
:
            
next_set
=
set
(
)
            
for
s
in
maybe_unreachable_set
:
                
if
len
(
self
.
states
[
s
]
.
backedges
)
=
=
0
and
s
not
in
init
:
                    
self
.
remove_state
(
s
next_set
)
            
maybe_unreachable_set
=
next_set
    
def
is_reachable_state
(
self
s
)
:
        
"
"
"
Check
whether
the
current
state
is
reachable
or
not
.
"
"
"
        
assert
isinstance
(
s
int
)
        
if
self
.
states
[
s
]
is
None
:
            
return
False
        
reachable_back
=
set
(
)
        
todo
=
[
s
]
        
while
todo
:
            
s
=
todo
.
pop
(
)
            
reachable_back
.
add
(
s
)
            
for
edge
in
self
.
states
[
s
]
.
backedges
:
                
if
edge
.
src
not
in
reachable_back
:
                    
todo
.
append
(
edge
.
src
)
        
for
_
s
in
self
.
named_goals
:
            
if
s
in
reachable_back
:
                
return
True
        
return
False
    
def
get_flag_for
(
self
nts
)
:
        
nts
=
OrderedFrozenSet
(
nts
)
        
self
.
flags
.
add
(
nts
)
        
return
"
_
"
.
join
(
[
"
flag
"
*
nts
]
)
    
def
create_lr0_table
(
self
grammar
verbose
progress
)
:
        
if
verbose
or
progress
:
            
print
(
"
Create
LR
(
0
)
parse
table
.
"
)
        
assert
isinstance
(
grammar
CanonicalGrammar
)
        
assert
isinstance
(
grammar
.
grammar
Grammar
)
        
goals
=
grammar
.
grammar
.
goals
(
)
        
self
.
named_goals
=
[
]
        
todo
=
collections
.
deque
(
)
        
for
nt
in
goals
:
            
init_nt
=
Nt
(
InitNt
(
nt
)
(
)
)
            
it
=
LR0Generator
.
start
(
grammar
init_nt
)
            
s
=
self
.
get_state
(
it
.
lr_items
)
            
todo
.
append
(
(
it
s
)
)
            
self
.
named_goals
.
append
(
(
nt
s
.
index
)
)
        
def
visit_grammar
(
)
:
            
while
todo
:
                
yield
                
s_it
s
=
todo
.
popleft
(
)
                
if
verbose
:
                    
print
(
"
\
nVisiting
:
\
n
{
}
"
.
format
(
s_it
)
)
                
for
k
sk_it
in
s_it
.
transitions
(
)
.
items
(
)
:
                    
locations
=
sk_it
.
lr_items
                    
if
not
self
.
is_term_shifted
(
k
)
:
                        
locations
=
OrderedFrozenSet
(
)
                    
is_new
sk
=
self
.
new_state
(
locations
)
                    
if
is_new
:
                        
todo
.
append
(
(
sk_it
sk
)
)
                    
self
.
add_edge
(
s
k
sk
.
index
)
        
consume
(
visit_grammar
(
)
progress
)
    
def
is_term_shifted
(
self
term
)
:
        
return
not
(
isinstance
(
term
Action
)
and
term
.
update_stack
(
)
)
    
def
is_valid_path
(
self
path
state
=
None
)
:
        
"
"
"
This
function
is
used
to
check
a
list
of
edges
and
returns
whether
it
        
corresponds
to
a
valid
path
within
the
parse
table
.
This
is
useful
when
        
merging
sequences
of
edges
from
various
locations
.
"
"
"
        
if
not
state
and
path
!
=
[
]
:
            
state
=
path
[
0
]
.
src
        
while
path
:
            
edge
=
path
[
0
]
            
path
=
path
[
1
:
]
            
if
state
!
=
edge
.
src
:
                
return
False
            
term
=
edge
.
term
            
if
term
is
None
and
len
(
path
)
=
=
0
:
                
return
True
            
row
=
self
.
states
[
state
]
            
if
term
not
in
row
:
                
return
False
            
state
=
row
[
term
]
        
return
True
    
def
shifted_path_to
(
self
n
right_of
)
:
        
"
Compute
all
paths
with
n
shifted
terms
ending
with
state
.
"
        
assert
isinstance
(
right_of
list
)
and
len
(
right_of
)
>
=
1
        
if
n
=
=
0
:
            
yield
right_of
        
state
=
right_of
[
0
]
.
src
        
assert
isinstance
(
state
int
)
        
for
edge
in
self
.
states
[
state
]
.
backedges
:
            
if
not
self
.
is_term_shifted
(
edge
.
term
)
:
                
print
(
repr
(
edge
)
)
                
print
(
self
.
states
[
edge
.
src
]
)
            
assert
self
.
is_term_shifted
(
edge
.
term
)
            
if
self
.
term_is_stacked
(
edge
.
term
)
:
                
s_n
=
n
-
1
                
if
n
=
=
0
:
                    
continue
            
else
:
                
s_n
=
n
            
from_edge
=
Edge
(
edge
.
src
edge
.
term
)
            
for
path
in
self
.
shifted_path_to
(
s_n
[
from_edge
]
+
right_of
)
:
                
yield
path
    
def
reduce_path
(
self
shifted
)
:
        
"
"
"
Compute
all
paths
which
might
be
reduced
by
a
given
action
.
This
function
        
assumes
that
the
state
is
reachable
from
the
starting
goals
and
that
        
the
depth
which
is
being
queried
has
valid
answers
.
"
"
"
        
assert
len
(
shifted
)
>
=
1
        
action
=
shifted
[
-
1
]
.
term
        
assert
action
.
update_stack
(
)
        
reducer
=
action
.
reduce_with
(
)
        
assert
isinstance
(
reducer
Reduce
)
        
depth
=
reducer
.
pop
+
reducer
.
replay
        
if
depth
>
0
:
            
stacked
=
[
i
for
i
e
in
enumerate
(
shifted
)
if
self
.
term_is_stacked
(
e
.
term
)
]
            
if
len
(
stacked
)
<
depth
:
                
shifted_from
=
0
                
depth
-
=
len
(
stacked
)
            
else
:
                
shifted_from
=
stacked
[
-
depth
]
                
depth
=
0
            
shifted_end
=
shifted
[
shifted_from
:
]
        
else
:
            
shifted_end
=
shifted
[
-
1
:
]
        
error_paths
=
[
]
        
success_paths
=
[
]
        
for
path
in
self
.
shifted_path_to
(
depth
shifted_end
)
:
            
head
=
self
.
states
[
path
[
0
]
.
src
]
            
if
reducer
.
nt
not
in
head
.
nonterminals
:
                
error_paths
.
append
(
path
)
                
continue
            
success_paths
.
append
(
path
)
            
assert
reducer
.
nt
in
head
.
nonterminals
            
to
=
head
.
nonterminals
[
reducer
.
nt
]
            
yield
path
[
Edge
(
path
[
0
]
.
src
reducer
.
nt
)
Edge
(
to
None
)
]
        
assert
success_paths
!
=
[
]
        
if
error_paths
:
            
def
stacked_path
(
path
)
:
                
return
tuple
(
e
for
e
in
path
if
self
.
term_is_stacked
(
e
.
term
)
)
            
stack_success_paths
=
set
(
map
(
stacked_path
success_paths
)
)
            
for
path
in
error_paths
:
                
if
stacked_path
(
path
)
not
in
stack_success_paths
:
                    
for
p
in
success_paths
:
                        
print
(
"
Success
path
:
{
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
map
(
edge_str
p
)
)
)
)
                    
head
=
self
.
states
[
path
[
0
]
.
src
]
                    
print
(
"
\
n
"
.
join
(
[
                        
"
Reduce
path
does
not
start
with
a
state
capable
of
shifting
the
non
-
terminal
{
}
.
"
                        
"
The
Reduce
path
is
:
{
}
"
                        
"
The
starting
state
is
{
}
"
                        
"
{
}
backedges
are
:
{
}
"
                    
]
)
.
format
(
reducer
.
nt
"
"
.
join
(
map
(
edge_str
path
)
)
head
                              
len
(
head
.
backedges
)
"
"
.
join
(
map
(
edge_str
head
.
backedges
)
)
)
)
                    
assert
reducer
.
nt
in
head
.
nonterminals
    
def
term_is_stacked
(
self
term
)
:
        
return
not
isinstance
(
term
Action
)
    
def
aps_start
(
self
state
replay
=
[
]
)
:
        
"
Return
a
parser
state
only
knowing
the
state
at
which
we
are
currently
.
"
        
edge
=
Edge
(
state
None
)
        
return
APS
(
[
edge
]
[
edge
]
[
]
[
]
replay
)
    
def
aps_next
(
self
aps
)
:
        
"
"
"
Visit
all
the
states
of
the
parse
table
as
-
if
we
were
running
a
        
Generalized
LR
parser
.
        
However
instead
parsing
content
we
use
this
algorithm
to
generate
        
both
the
content
which
remains
to
be
parsed
as
well
as
the
context
        
which
might
lead
us
to
be
in
the
state
which
from
which
we
started
.
        
This
algorithm
takes
an
APS
(
Abstract
Parser
State
)
and
consider
all
        
edges
of
the
parse
table
unless
restricted
by
one
of
the
previously
        
encountered
actions
.
These
restrictions
such
as
replayed
lookahead
or
        
the
path
which
might
be
reduced
are
used
for
filtering
out
states
which
        
are
not
handled
by
this
parse
table
.
        
For
each
edge
this
functions
recursively
calls
it
-
self
and
calls
the
        
visit
functions
to
know
whether
to
stop
or
continue
and
to
capture
the
        
result
.
        
"
"
"
        
assert
is_valid_aps
(
aps
)
        
st
=
aps
.
stack
        
sh
=
aps
.
shift
        
la
=
aps
.
lookahead
        
ac
=
aps
.
actions
        
rp
=
aps
.
replay
        
last_edge
=
sh
[
-
1
]
        
state
=
self
.
states
[
last_edge
.
src
]
        
if
aps
.
replay
=
=
[
]
:
            
for
term
to
in
state
.
shifted_edges
(
)
:
                
edge
=
Edge
(
last_edge
.
src
term
)
                
new_sh
=
aps
.
shift
[
:
-
1
]
+
[
edge
]
                
to
=
Edge
(
to
None
)
                
yield
APS
(
st
new_sh
+
[
to
]
la
+
[
term
]
ac
+
[
edge
]
rp
)
        
else
:
            
term
=
aps
.
replay
[
0
]
            
rp
=
aps
.
replay
[
1
:
]
            
if
term
in
state
:
                
edge
=
Edge
(
last_edge
.
src
term
)
                
new_sh
=
aps
.
shift
[
:
-
1
]
+
[
edge
]
                
to
=
state
[
term
]
                
to
=
Edge
(
to
None
)
                
yield
APS
(
st
new_sh
+
[
to
]
la
ac
+
[
edge
]
rp
)
        
term
=
None
        
rp
=
aps
.
replay
        
for
a
to
in
state
.
epsilon
:
            
edge
=
Edge
(
last_edge
.
src
a
)
            
prev_sh
=
aps
.
shift
[
:
-
1
]
+
[
edge
]
            
if
a
.
update_stack
(
)
:
                
reducer
=
a
.
reduce_with
(
)
                
for
path
reduced_path
in
self
.
reduce_path
(
prev_sh
)
:
                    
if
prev_sh
[
-
len
(
path
)
:
]
!
=
path
[
-
len
(
prev_sh
)
:
]
:
                        
continue
                    
new_st
=
path
[
:
max
(
len
(
path
)
-
len
(
prev_sh
)
0
)
]
+
st
                    
assert
self
.
is_valid_path
(
new_st
)
                    
new_sh
=
prev_sh
[
:
-
len
(
path
)
]
+
reduced_path
                    
assert
self
.
is_valid_path
(
new_sh
)
                    
new_replay
=
[
]
                    
if
reducer
.
replay
>
0
:
                        
new_replay
=
[
edge
.
term
for
edge
in
path
if
self
.
term_is_stacked
(
edge
.
term
)
]
                        
new_replay
=
new_replay
[
-
reducer
.
replay
:
]
                    
new_replay
=
new_replay
+
rp
                    
new_la
=
la
[
:
max
(
len
(
la
)
-
reducer
.
replay
0
)
]
                    
yield
APS
(
new_st
new_sh
new_la
ac
+
[
edge
]
new_replay
)
            
else
:
                
to
=
Edge
(
to
None
)
                
yield
APS
(
st
prev_sh
+
[
to
]
la
ac
+
[
edge
]
rp
)
    
def
aps_visitor
(
self
aps
visit
)
:
        
todo
=
[
]
        
todo
.
append
(
aps
)
        
while
todo
:
            
aps
=
todo
.
pop
(
)
            
cont
=
visit
(
aps
)
            
if
not
cont
:
                
continue
            
todo
.
extend
(
self
.
aps_next
(
aps
)
)
    
def
lanes
(
self
state
)
:
        
"
"
"
Compute
the
lanes
from
the
amount
of
lookahead
available
.
Only
consider
        
context
when
reduce
states
are
encountered
.
"
"
"
        
assert
isinstance
(
state
int
)
        
record
=
[
]
        
def
visit
(
aps
)
:
            
has_shift_loop
=
len
(
aps
.
shift
)
!
=
1
+
len
(
set
(
zip
(
aps
.
shift
aps
.
shift
[
1
:
]
)
)
)
            
has_stack_loop
=
len
(
aps
.
stack
)
!
=
1
+
len
(
set
(
zip
(
aps
.
stack
aps
.
stack
[
1
:
]
)
)
)
            
has_lookahead
=
len
(
aps
.
lookahead
)
>
=
1
            
stop
=
has_shift_loop
or
has_stack_loop
or
has_lookahead
            
if
stop
:
                
print
(
"
lanes_visit
stop
:
"
)
                
print
(
aps_str
(
aps
"
\
trecord
"
)
)
                
record
.
append
(
aps
)
            
return
not
stop
        
self
.
aps_visitor
(
self
.
aps_start
(
state
)
visit
)
        
return
record
    
def
context_lanes
(
self
state
)
:
        
"
"
"
Compute
lanes
such
that
each
reduce
action
can
have
set
of
unique
stack
to
        
reach
the
given
state
.
The
stacks
are
assumed
to
be
loop
-
free
by
        
reducing
edges
at
most
once
.
        
In
order
to
avoid
attempting
to
eagerly
solve
everything
using
context
        
information
we
break
this
loop
as
soon
as
we
have
one
token
of
        
lookahead
in
a
case
which
does
not
have
enough
context
.
        
The
return
value
is
a
tuple
where
the
first
element
is
a
boolean
which
        
is
True
if
we
should
fallback
on
solving
this
issue
with
more
        
lookahead
and
the
second
is
the
list
of
APS
lanes
which
are
providing
        
enough
context
to
disambiguate
the
inconsistency
of
the
given
state
.
"
"
"
        
assert
isinstance
(
state
int
)
        
def
not_interesting
(
aps
)
:
            
reduce_list
=
[
e
for
e
in
aps
.
actions
if
self
.
is_term_shifted
(
e
.
term
)
]
            
has_reduce_loop
=
len
(
reduce_list
)
!
=
len
(
set
(
reduce_list
)
)
            
return
has_reduce_loop
        
context
=
collections
.
defaultdict
(
lambda
:
[
]
)
        
def
has_enough_context
(
aps
)
:
            
try
:
                
assert
aps
.
actions
[
0
]
in
context
[
tuple
(
aps
.
stack
)
]
                
return
len
(
set
(
context
[
tuple
(
aps
.
stack
)
]
)
)
<
=
1
            
except
IndexError
:
                
return
False
        
collect
=
[
self
.
aps_start
(
state
)
]
        
enough_context
=
False
        
while
not
enough_context
:
            
recurse
=
[
]
            
context
=
collections
.
defaultdict
(
lambda
:
[
]
)
            
while
collect
:
                
aps
=
collect
.
pop
(
)
                
recurse
.
append
(
aps
)
                
if
aps
.
actions
=
=
[
]
:
                    
continue
                
for
i
in
range
(
len
(
aps
.
stack
)
)
:
                    
context
[
tuple
(
aps
.
stack
[
i
:
]
)
]
.
append
(
aps
.
actions
[
0
]
)
            
assert
collect
=
=
[
]
            
enough_context
=
True
            
while
recurse
:
                
aps
=
recurse
.
pop
(
)
                
if
not_interesting
(
aps
)
:
                    
continue
                
if
has_enough_context
(
aps
)
:
                    
collect
.
append
(
aps
)
                    
continue
                
if
len
(
aps
.
lookahead
)
>
=
1
:
                    
return
True
[
]
                
enough_context
=
False
                
collect
.
extend
(
self
.
aps_next
(
aps
)
)
            
assert
recurse
=
=
[
]
        
return
False
collect
    
def
lookahead_lanes
(
self
state
)
:
        
"
"
"
Compute
lanes
to
collect
all
lookahead
symbols
available
.
After
each
reduce
        
action
there
is
no
need
to
consider
the
same
non
-
terminal
multiple
        
times
we
are
only
interested
in
lookahead
token
and
not
in
the
context
        
information
provided
by
reducing
action
.
"
"
"
        
assert
isinstance
(
state
int
)
        
record
=
[
]
        
seen_edge_after_reduce
=
set
(
)
        
def
visit
(
aps
)
:
            
first_reduce
=
next
(
(
e
for
e
in
aps
.
actions
[
:
-
1
]
if
not
self
.
is_term_shifted
(
e
.
term
)
)
None
)
            
if
first_reduce
:
                
reduce_key
=
(
first_reduce
aps
.
shift
[
0
]
.
src
aps
.
actions
[
-
1
]
.
term
)
            
has_seen_edge_after_reduce
=
first_reduce
and
reduce_key
in
seen_edge_after_reduce
            
has_lookahead
=
len
(
aps
.
lookahead
)
>
=
1
            
stop
=
has_seen_edge_after_reduce
or
has_lookahead
            
if
stop
:
                
if
has_lookahead
:
                    
record
.
append
(
aps
)
            
if
first_reduce
:
                
seen_edge_after_reduce
.
add
(
reduce_key
)
            
return
not
stop
        
self
.
aps_visitor
(
self
.
aps_start
(
state
)
visit
)
        
return
record
    
def
fix_with_context
(
self
s
aps_lanes
)
:
        
raise
ValueError
(
"
fix_with_context
:
Not
Implemented
"
)
    
def
fix_with_lookahead
(
self
s
aps_lanes
)
:
        
assert
all
(
len
(
aps
.
lookahead
)
>
=
1
for
aps
in
aps_lanes
)
        
maybe_unreachable_set
=
set
(
)
        
shift_map
=
collections
.
defaultdict
(
lambda
:
[
]
)
        
for
aps
in
aps_lanes
:
            
actions
=
aps
.
actions
            
assert
isinstance
(
actions
[
-
1
]
Edge
)
            
assert
actions
[
-
1
]
.
term
=
=
aps
.
lookahead
[
0
]
            
src
=
actions
[
-
1
]
.
src
            
term
=
actions
[
-
1
]
.
term
            
actions
=
list
(
keep_until
(
actions
[
:
-
1
]
lambda
edge
:
not
self
.
is_term_shifted
(
edge
.
term
)
)
)
            
assert
all
(
isinstance
(
edge
.
term
Action
)
for
edge
in
actions
)
            
new_actions
=
[
]
            
accept
=
True
            
for
edge
in
actions
:
                
new_term
=
edge
.
term
.
shifted_action
(
term
)
                
if
new_term
is
False
:
                    
accept
=
False
                    
break
                
elif
new_term
is
True
:
                    
continue
                
new_actions
.
append
(
Edge
(
edge
.
src
new_term
)
)
            
if
accept
:
                
target
=
self
.
states
[
src
]
[
term
]
                
target
=
self
.
states
[
target
]
                
shift_map
[
term
]
.
append
(
(
target
new_actions
)
)
        
def
restore_edges
(
state
shift_map
depth
)
:
            
assert
isinstance
(
state
StateAndTransitions
)
            
edges
=
{
}
            
for
term
actions_list
in
shift_map
.
items
(
)
:
                
locations
=
OrderedSet
(
)
                
delayed
=
OrderedSet
(
)
                
new_shift_map
=
collections
.
defaultdict
(
lambda
:
[
]
)
                
recurse
=
False
                
if
not
self
.
is_term_shifted
(
term
)
:
                    
actions_list
=
[
]
                
for
target
actions
in
actions_list
:
                    
assert
isinstance
(
target
StateAndTransitions
)
                    
locations
|
=
target
.
locations
                    
delayed
|
=
target
.
delayed_actions
                    
if
actions
!
=
[
]
:
                        
edge
=
actions
[
0
]
                        
assert
isinstance
(
edge
Edge
)
                        
for
action
in
actions
:
                            
delayed
.
add
(
action
.
term
)
                        
new_shift_map
[
edge
.
term
]
.
append
(
(
target
actions
[
1
:
]
)
)
                        
recurse
=
True
                    
else
:
                        
for
next_term
next_dest
in
target
.
edges
(
)
:
                            
next_dest
=
self
.
states
[
next_dest
]
                            
new_shift_map
[
next_term
]
.
append
(
(
next_dest
[
]
)
)
                
locations
=
OrderedFrozenSet
(
locations
)
                
delayed
=
OrderedFrozenSet
(
delayed
)
                
is_new
new_target
=
self
.
new_state
(
locations
delayed
)
                
edges
[
term
]
=
new_target
.
index
                
if
is_new
or
recurse
:
                    
restore_edges
(
new_target
new_shift_map
depth
+
"
"
)
            
self
.
clear_edges
(
state
maybe_unreachable_set
)
            
for
term
target
in
edges
.
items
(
)
:
                
self
.
add_edge
(
state
term
target
)
        
state
=
self
.
states
[
s
]
        
restore_edges
(
state
shift_map
"
"
)
        
self
.
remove_unreachable_states
(
maybe_unreachable_set
)
    
def
fix_inconsistent_state
(
self
s
verbose
)
:
        
state
=
self
.
states
[
s
]
        
if
state
is
None
or
not
state
.
is_inconsistent
(
)
:
            
return
False
        
all_reduce
=
all
(
a
.
update_stack
(
)
for
a
_
in
state
.
epsilon
)
        
any_shift
=
(
len
(
state
.
terminals
)
+
len
(
state
.
nonterminals
)
+
len
(
state
.
errors
)
)
>
0
        
try_with_context
=
all_reduce
and
not
any_shift
        
try_with_lookahead
=
not
try_with_context
        
if
try_with_context
:
            
if
verbose
:
                
print
(
"
\
tFix
with
context
.
"
)
            
try_with_lookahead
aps_lanes
=
self
.
context_lanes
(
s
)
            
if
not
try_with_lookahead
:
                
assert
aps_lanes
!
=
[
]
                
self
.
fix_with_context
(
s
aps_lanes
)
            
elif
verbose
:
                
print
(
"
\
tFallback
on
fixing
with
lookahead
.
"
)
        
if
try_with_lookahead
:
            
if
verbose
:
                
print
(
"
\
tFix
with
lookahead
.
"
)
            
aps_lanes
=
self
.
lookahead_lanes
(
s
)
            
assert
aps_lanes
!
=
[
]
            
self
.
fix_with_lookahead
(
s
aps_lanes
)
        
return
True
    
def
fix_inconsistent_table
(
self
verbose
progress
)
:
        
"
"
"
The
parse
table
might
be
inconsistent
.
We
fix
the
parse
table
by
looking
        
around
the
inconsistent
states
for
more
context
.
Either
by
looking
at
the
        
potential
stack
state
which
might
lead
to
the
inconsistent
state
or
by
        
increasing
the
lookahead
.
"
"
"
        
if
verbose
or
progress
:
            
print
(
"
Fix
parse
table
inconsistencies
.
"
)
        
todo
=
collections
.
deque
(
)
        
for
state
in
self
.
states
:
            
if
state
.
is_inconsistent
(
)
:
                
todo
.
append
(
state
.
index
)
        
if
verbose
and
todo
:
            
print
(
"
\
n
"
.
join
(
[
                
"
\
nGrammar
is
inconsistent
.
"
                
"
\
tNumber
of
States
=
{
}
"
                
"
\
tNumber
of
inconsistencies
found
=
{
}
"
]
)
.
format
(
                    
len
(
self
.
states
)
len
(
todo
)
)
)
        
count
=
0
        
def
visit_table
(
)
:
            
nonlocal
count
            
unreachable
=
[
]
            
while
todo
:
                
while
todo
:
                    
yield
                    
s
=
todo
.
popleft
(
)
                    
if
not
self
.
is_reachable_state
(
s
)
:
                        
unreachable
.
append
(
s
)
                        
continue
                    
assert
self
.
states
[
s
]
.
is_inconsistent
(
)
                    
start_len
=
len
(
self
.
states
)
                    
if
verbose
:
                        
count
=
count
+
1
                        
print
(
"
Fixing
state
{
}
\
n
"
.
format
(
self
.
states
[
s
]
)
)
                    
try
:
                        
self
.
fix_inconsistent_state
(
s
verbose
)
                    
except
Exception
as
exc
:
                        
self
.
debug_info
=
True
                        
raise
ValueError
(
                            
"
Error
while
fixing
conflict
in
state
{
}
\
n
\
n
"
                            
"
In
the
following
grammar
productions
:
\
n
{
}
"
                            
.
format
(
self
.
states
[
s
]
self
.
debug_context
(
s
"
\
n
"
"
\
t
"
)
)
                        
)
from
exc
                    
new_inconsistent_states
=
[
                        
s
.
index
for
s
in
self
.
states
[
start_len
:
]
                        
if
s
.
is_inconsistent
(
)
                    
]
                    
if
verbose
:
                        
print
(
"
\
tAdding
{
}
states
"
.
format
(
len
(
self
.
states
[
start_len
:
]
)
)
)
                        
print
(
"
\
tWith
{
}
inconsistent
states
"
.
format
(
len
(
new_inconsistent_states
)
)
)
                    
todo
.
extend
(
new_inconsistent_states
)
                
still_unreachable
=
[
]
                
for
s
in
unreachable
:
                    
if
self
.
is_reachable_state
(
s
)
:
                        
todo
.
append
(
s
)
                    
else
:
                        
still_unreachable
.
append
(
s
)
                
unreachable
=
still_unreachable
        
consume
(
visit_table
(
)
progress
)
        
if
verbose
:
            
print
(
"
\
n
"
.
join
(
[
                
"
\
nGrammar
is
now
consistent
.
"
                
"
\
tNumber
of
States
=
{
}
"
                
"
\
tNumber
of
inconsistencies
solved
=
{
}
"
]
)
.
format
(
                    
len
(
self
.
states
)
count
)
)
        
assert
not
self
.
is_inconsistent
(
)
    
def
remove_all_unreachable_state
(
self
verbose
progress
)
:
        
self
.
states
=
[
s
for
s
in
self
.
states
if
s
is
not
None
]
        
state_map
=
{
s
.
index
:
i
for
i
s
in
enumerate
(
self
.
states
)
}
        
for
s
in
self
.
states
:
            
s
.
rewrite_state_indexes
(
state_map
)
    
def
fold_identical_endings
(
self
verbose
progress
)
:
        
if
verbose
or
progress
:
            
print
(
"
Fold
identical
endings
.
"
)
        
maybe_unreachable
=
set
(
)
        
def
rewrite_backedges
(
state_list
)
:
            
ref
=
state_list
[
0
]
            
replace_edges
=
[
e
for
s
in
state_list
[
1
:
]
for
e
in
s
.
backedges
]
            
hit
=
False
            
for
edge
in
replace_edges
:
                
src
=
self
.
states
[
edge
.
src
]
                
self
.
replace_edge
(
src
edge
.
term
ref
.
index
maybe_unreachable
)
                
hit
=
True
            
return
hit
        
def
rewrite_if_same_outedges
(
state_list
)
:
            
outedges
=
collections
.
defaultdict
(
lambda
:
[
]
)
            
for
s
in
state_list
:
                
outedges
[
tuple
(
s
.
edges
(
)
)
]
.
append
(
s
)
            
hit
=
False
            
for
same
in
outedges
.
values
(
)
:
                
if
len
(
same
)
>
1
:
                    
hit
=
rewrite_backedges
(
same
)
or
hit
            
return
hit
        
def
visit_table
(
)
:
            
hit
=
True
            
while
hit
:
                
yield
                
hit
=
rewrite_if_same_outedges
(
self
.
states
)
        
consume
(
visit_table
(
)
progress
)
        
self
.
remove_unreachable_states
(
maybe_unreachable
)
        
self
.
remove_all_unreachable_state
(
verbose
progress
)
    
def
group_epsilon_states
(
self
verbose
progress
)
:
        
shift_states
=
[
s
for
s
in
self
.
states
if
len
(
s
.
epsilon
)
=
=
0
]
        
action_states
=
[
s
for
s
in
self
.
states
if
len
(
s
.
epsilon
)
>
0
]
        
self
.
states
=
[
]
        
self
.
states
.
extend
(
shift_states
)
        
self
.
states
.
extend
(
action_states
)
        
state_map
=
{
s
.
index
:
i
for
i
s
in
enumerate
(
self
.
states
)
}
        
for
s
in
self
.
states
:
            
s
.
rewrite_state_indexes
(
state_map
)
    
def
count_shift_states
(
self
)
:
        
return
sum
(
1
for
s
in
self
.
states
if
len
(
s
.
epsilon
)
=
=
0
)
    
def
count_action_states
(
self
)
:
        
return
sum
(
1
for
s
in
self
.
states
if
len
(
s
.
epsilon
)
>
0
)
    
def
prepare_debug_context
(
self
)
:
        
"
"
"
To
better
filter
out
the
traversal
of
the
grammar
in
debug
context
we
        
pre
-
compute
for
each
state
the
maximal
depth
of
each
state
within
a
        
production
.
Therefore
if
visiting
a
state
no
increases
the
reducing
        
depth
beyind
the
ability
to
shrink
the
shift
list
to
0
then
we
can
        
stop
going
deeper
as
we
entered
a
different
production
.
"
"
"
        
depths
=
collections
.
defaultdict
(
lambda
:
[
]
)
        
for
s
in
self
.
states
:
            
if
s
is
None
:
                
continue
            
for
t
d
in
s
.
epsilon
:
                
if
self
.
is_term_shifted
(
t
)
:
                    
continue
                
for
path
_
in
self
.
reduce_path
(
[
Edge
(
s
.
index
t
)
]
)
:
                    
for
i
edge
in
enumerate
(
path
)
:
                        
depths
[
edge
.
src
]
.
append
(
i
+
1
)
        
depths
=
{
s
:
max
(
ds
)
for
s
ds
in
depths
.
items
(
)
}
        
return
depths
    
def
debug_context
(
self
state
split_txt
=
"
;
"
prefix
=
"
"
)
:
        
"
Reconstruct
the
grammar
production
by
traversing
the
parse
table
.
"
        
assert
isinstance
(
state
int
)
        
if
self
.
debug_info
is
False
:
            
return
"
"
        
if
self
.
debug_info
is
True
:
            
self
.
debug_info
=
self
.
prepare_debug_context
(
)
        
record
=
[
]
        
def
visit
(
aps
)
:
            
if
aps
.
actions
=
=
[
]
:
                
return
True
            
last
=
aps
.
actions
[
-
1
]
.
term
            
is_reduce
=
not
self
.
is_term_shifted
(
last
)
            
has_shift_loop
=
len
(
aps
.
shift
)
!
=
1
+
len
(
set
(
zip
(
aps
.
shift
aps
.
shift
[
1
:
]
)
)
)
            
can_reduce_later
=
True
            
try
:
                
can_reduce_later
=
self
.
debug_info
[
aps
.
shift
[
-
1
]
.
src
]
>
=
len
(
aps
.
shift
)
            
except
KeyError
:
                
can_reduce_later
=
False
            
stop
=
is_reduce
or
has_shift_loop
or
not
can_reduce_later
            
save
=
stop
and
len
(
aps
.
shift
)
=
=
2
            
save
=
save
and
isinstance
(
aps
.
shift
[
0
]
.
term
Nt
)
            
save
=
save
and
not
self
.
is_term_shifted
(
aps
.
actions
[
-
1
]
.
term
)
            
if
save
:
                
record
.
append
(
aps
)
            
return
not
stop
        
self
.
aps_visitor
(
self
.
aps_start
(
state
)
visit
)
        
context
=
OrderedSet
(
)
        
for
aps
in
record
:
            
assert
aps
.
actions
!
=
[
]
            
assert
aps
.
actions
[
-
1
]
.
term
.
update_stack
(
)
            
reducer
=
aps
.
actions
[
-
1
]
.
term
.
reduce_with
(
)
            
replay
=
reducer
.
replay
            
before
=
[
repr
(
e
.
term
)
for
e
in
aps
.
stack
[
:
-
1
]
]
            
after
=
[
repr
(
e
.
term
)
for
e
in
aps
.
actions
[
:
-
1
]
]
            
prod
=
before
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
after
            
if
replay
<
len
(
after
)
and
replay
>
0
:
                
del
prod
[
-
replay
:
]
                
replay
=
0
            
if
replay
>
len
(
after
)
:
                
replay
+
=
1
            
if
replay
>
0
:
                
prod
=
prod
[
:
-
replay
]
+
[
"
[
lookahead
:
"
]
+
prod
[
-
replay
:
]
+
[
"
]
"
]
            
txt
=
"
{
}
{
}
:
:
=
{
}
"
.
format
(
                
prefix
                
repr
(
aps
.
actions
[
-
1
]
.
term
.
reduce_with
(
)
.
nt
)
                
"
"
.
join
(
prod
)
            
)
            
context
.
add
(
txt
)
        
if
split_txt
is
None
:
            
return
context
        
return
split_txt
.
join
(
txt
for
txt
in
sorted
(
context
)
)
def
generate_parser_states
(
grammar
*
verbose
=
False
progress
=
False
debug
=
False
)
:
    
assert
isinstance
(
grammar
Grammar
)
    
grammar
=
CanonicalGrammar
(
grammar
)
    
parse_table
=
ParseTable
(
grammar
verbose
progress
debug
)
    
return
parse_table
def
generate_parser
(
out
source
*
verbose
=
False
progress
=
False
debug
=
False
                    
target
=
'
python
'
handler_info
=
None
)
:
    
assert
target
in
(
'
python
'
'
rust
'
)
    
if
isinstance
(
source
Grammar
)
:
        
grammar
=
CanonicalGrammar
(
source
)
        
parser_data
=
generate_parser_states
(
            
source
verbose
=
verbose
progress
=
progress
)
    
elif
isinstance
(
source
ParseTable
)
:
        
parser_data
=
source
        
parser_data
.
debug_info
=
debug
    
elif
isinstance
(
source
ParserStates
)
:
        
parser_data
=
source
    
else
:
        
raise
TypeError
(
"
unrecognized
source
:
{
!
r
}
"
.
format
(
source
)
)
    
if
target
=
=
'
rust
'
:
        
if
isinstance
(
parser_data
ParseTable
)
:
            
emit
.
write_rust_parse_table
(
out
parser_data
handler_info
)
        
else
:
            
raise
ValueError
(
"
Unexpected
parser_data
kind
"
)
    
else
:
        
if
isinstance
(
parser_data
ParseTable
)
:
            
emit
.
write_python_parse_table
(
out
parser_data
)
        
else
:
            
raise
ValueError
(
"
Unexpected
parser_data
kind
"
)
def
compile
(
grammar
verbose
=
False
)
:
    
assert
isinstance
(
grammar
Grammar
)
    
out
=
io
.
StringIO
(
)
    
generate_parser
(
out
grammar
)
    
scope
=
{
}
    
if
verbose
:
        
with
open
(
"
parse_with_python
.
py
"
"
w
"
)
as
f
:
            
f
.
write
(
out
.
getvalue
(
)
)
    
exec
(
out
.
getvalue
(
)
scope
)
    
return
scope
[
'
Parser
'
]
def
demo
(
)
:
    
from
.
grammar
import
example_grammar
    
grammar
=
example_grammar
(
)
    
from
.
import
lexer
    
tokenize
=
lexer
.
LexicalGrammar
(
        
"
+
-
*
/
(
)
"
NUM
=
r
'
0
|
[
1
-
9
]
[
0
-
9
]
*
'
VAR
=
r
'
[
_A
-
Za
-
z
]
\
w
+
'
)
    
import
io
    
out
=
io
.
StringIO
(
)
    
generate_parser
(
out
grammar
)
    
code
=
out
.
getvalue
(
)
    
print
(
code
)
    
print
(
"
-
-
-
-
"
)
    
sandbox
=
{
}
    
exec
(
code
sandbox
)
    
Parser
=
sandbox
[
'
Parser
'
]
    
while
True
:
        
try
:
            
line
=
input
(
'
>
'
)
        
except
EOFError
:
            
break
        
try
:
            
parser
=
Parser
(
)
            
lexer
=
tokenize
(
parser
)
            
lexer
.
write
(
line
)
            
result
=
lexer
.
close
(
)
        
except
Exception
as
exc
:
            
print
(
exc
.
__class__
.
__name__
+
"
:
"
+
str
(
exc
)
)
        
else
:
            
print
(
result
)
if
__name__
=
=
'
__main__
'
:
    
demo
(
)
