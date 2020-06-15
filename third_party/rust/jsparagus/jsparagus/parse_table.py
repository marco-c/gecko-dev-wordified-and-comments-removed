from
__future__
import
annotations
import
collections
import
hashlib
import
os
import
pickle
import
typing
from
.
import
types
from
.
utils
import
consume
keep_until
split
from
.
ordered
import
OrderedSet
OrderedFrozenSet
from
.
actions
import
Action
FilterFlag
from
.
grammar
import
End
ErrorSymbol
InitNt
Nt
from
.
rewrites
import
CanonicalGrammar
from
.
lr0
import
LR0Generator
Term
from
.
aps
import
APS
Edge
Path
StateId
=
int
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
locations
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
delayed_actions
"
"
backedges
"
"
_hash
"
                 
"
stable_hash
"
]
    
index
:
StateId
    
locations
:
OrderedFrozenSet
[
str
]
    
terminals
:
typing
.
Dict
[
str
StateId
]
    
nonterminals
:
typing
.
Dict
[
Nt
StateId
]
    
errors
:
typing
.
Dict
[
ErrorSymbol
StateId
]
    
epsilon
:
typing
.
List
[
typing
.
Tuple
[
Action
StateId
]
]
    
delayed_actions
:
OrderedFrozenSet
[
Action
]
    
backedges
:
OrderedSet
[
Edge
]
    
_hash
:
int
    
stable_hash
:
str
    
def
__init__
(
            
self
            
index
:
StateId
            
locations
:
OrderedFrozenSet
[
str
]
            
delayed_actions
:
OrderedFrozenSet
[
Action
]
=
OrderedFrozenSet
(
)
    
)
-
>
None
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
-
>
typing
.
Iterator
[
object
]
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
                
yield
"
\
n
"
            
yield
"
delayed_actions
"
            
for
action
in
self
.
delayed_actions
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
        
h
=
hashlib
.
md5
(
)
        
h
.
update
(
"
"
.
join
(
map
(
str
hashed_content
(
)
)
)
.
encode
(
)
)
        
self
.
stable_hash
=
h
.
hexdigest
(
)
[
:
6
]
    
def
is_inconsistent
(
self
)
-
>
bool
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
-
>
typing
.
Iterator
[
            
typing
.
Tuple
[
typing
.
Union
[
str
Nt
ErrorSymbol
]
StateId
]
    
]
:
        
k
:
Term
        
s
:
StateId
        
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
-
>
typing
.
Iterator
[
typing
.
Tuple
[
Term
StateId
]
]
:
        
k
:
Term
        
s
:
StateId
        
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
:
typing
.
Dict
[
StateId
StateId
]
    
)
-
>
None
:
        
def
apply_on_term
(
term
:
typing
.
Union
[
Term
None
]
)
-
>
Term
:
            
assert
term
is
not
None
            
if
isinstance
(
term
Action
)
:
                
return
term
.
rewrite_state_indexes
(
state_map
)
            
return
term
        
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
.
rewrite_state_indexes
(
state_map
)
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
OrderedSet
(
            
Edge
(
state_map
[
edge
.
src
]
apply_on_term
(
edge
.
term
)
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
-
>
typing
.
Optional
[
ErrorSymbol
]
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
:
object
)
-
>
bool
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
:
Term
)
-
>
StateId
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
:
Term
default
:
object
)
-
>
object
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
stable_str
(
self
states
:
typing
.
List
[
StateAndTransitions
]
)
-
>
str
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
stable_hash
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
states
[
s
]
.
stable_hash
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
__str__
(
self
)
-
>
str
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
:
object
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
StateAndTransitions
)
                
and
sorted
(
self
.
locations
)
=
=
sorted
(
other
.
locations
)
                
and
sorted
(
self
.
delayed_actions
)
=
=
sorted
(
other
.
delayed_actions
)
)
    
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
DebugInfo
=
typing
.
Dict
[
StateId
int
]
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
debug_info
"
"
exec_modes
"
"
assume_inconsistent
"
    
]
    
actions
:
typing
.
List
[
Action
]
    
states
:
typing
.
List
[
StateAndTransitions
]
    
state_cache
:
typing
.
Dict
[
StateAndTransitions
StateAndTransitions
]
    
named_goals
:
typing
.
List
[
typing
.
Tuple
[
Nt
StateId
]
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
    
nonterminals
:
typing
.
List
[
Nt
]
    
debug_info
:
typing
.
Union
[
bool
DebugInfo
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
    
assume_inconsistent
:
bool
    
def
__init__
(
            
self
            
grammar
:
CanonicalGrammar
            
verbose
:
bool
=
False
            
progress
:
bool
=
False
            
debug
:
bool
=
False
    
)
-
>
None
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
typing
.
cast
(
            
typing
.
List
[
Nt
]
            
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
)
        
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
self
.
nonterminals
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
assume_inconsistent
=
True
        
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
:
os
.
PathLike
)
-
>
None
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
:
os
.
PathLike
)
-
>
ParseTable
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
-
>
bool
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
rewrite_state_indexes
(
self
state_map
:
typing
.
Dict
[
StateId
StateId
]
)
-
>
None
:
        
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
:
                
s
.
rewrite_state_indexes
(
state_map
)
        
self
.
named_goals
=
[
            
(
nt
state_map
[
s
]
)
for
nt
s
in
self
.
named_goals
        
]
    
def
rewrite_reordered_state_indexes
(
self
)
-
>
None
:
        
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
            
if
s
is
not
None
        
}
        
self
.
rewrite_state_indexes
(
state_map
)
    
def
new_state
(
            
self
            
locations
:
OrderedFrozenSet
[
str
]
            
delayed_actions
:
OrderedFrozenSet
[
Action
]
=
OrderedFrozenSet
(
)
    
)
-
>
typing
.
Tuple
[
bool
StateAndTransitions
]
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
:
OrderedFrozenSet
[
str
]
            
delayed_actions
:
OrderedFrozenSet
[
Action
]
=
OrderedFrozenSet
(
)
    
)
-
>
StateAndTransitions
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
:
StateId
maybe_unreachable_set
:
OrderedSet
[
StateId
]
)
-
>
None
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
:
StateAndTransitions
            
term
:
Term
            
dest
:
StateId
    
)
-
>
None
:
        
assert
term
not
in
src
        
assert
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
:
StateAndTransitions
            
term
:
Term
            
dest
:
StateId
            
maybe_unreachable_set
:
OrderedSet
[
StateId
]
    
)
-
>
None
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
        
self
.
assert_state_invariants
(
src
)
    
def
replace_edge
(
            
self
            
src
:
StateAndTransitions
            
term
:
Term
            
dest
:
StateId
            
maybe_unreachable_set
:
OrderedSet
[
StateId
]
    
)
-
>
None
:
        
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
        
edge_existed
=
term
in
src
        
if
edge_existed
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
        
self
.
assert_state_invariants
(
src
)
        
self
.
assert_state_invariants
(
dest
)
        
if
edge_existed
:
            
self
.
assert_state_invariants
(
old_dest
)
    
def
remove_edge
(
            
self
            
src
:
StateAndTransitions
            
term
:
Term
            
maybe_unreachable_set
:
OrderedSet
[
StateId
]
    
)
-
>
None
:
        
edge_existed
=
term
in
src
        
if
edge_existed
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
        
elif
isinstance
(
term
Nt
)
:
            
del
src
.
nonterminals
[
term
]
        
elif
isinstance
(
term
ErrorSymbol
)
:
            
del
src
.
errors
[
term
]
        
else
:
            
del
src
.
terminals
[
term
]
        
self
.
assert_state_invariants
(
src
)
        
if
edge_existed
:
            
self
.
assert_state_invariants
(
old_dest
)
    
def
clear_edges
(
            
self
            
src
:
StateAndTransitions
            
maybe_unreachable_set
:
OrderedSet
[
StateId
]
    
)
-
>
None
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
assert_state_invariants
(
self
src
:
typing
.
Union
[
StateId
StateAndTransitions
]
)
-
>
None
:
        
if
not
self
.
debug_info
:
            
return
        
if
isinstance
(
src
int
)
:
            
src
=
self
.
states
[
src
]
        
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
            
assert
Edge
(
src
.
index
term
)
in
self
.
states
[
dest
]
.
backedges
        
for
e
in
src
.
backedges
:
            
assert
e
.
term
is
not
None
            
assert
self
.
states
[
e
.
src
]
[
e
.
term
]
=
=
src
.
index
    
def
remove_unreachable_states
(
            
self
            
maybe_unreachable_set
:
OrderedSet
[
StateId
]
    
)
-
>
None
:
        
init
:
OrderedSet
[
StateId
]
        
init
=
OrderedSet
(
goal
for
name
goal
in
self
.
named_goals
)
        
while
maybe_unreachable_set
:
            
next_set
:
OrderedSet
[
StateId
]
=
OrderedSet
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
:
StateId
)
-
>
bool
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
:
OrderedSet
[
StateId
]
=
OrderedSet
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
debug_dump
(
self
)
-
>
None
:
        
temp
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
        
temp
=
sorted
(
temp
key
=
lambda
s
:
s
.
stable_hash
)
        
for
s
in
temp
:
            
print
(
s
.
stable_str
(
self
.
states
)
)
    
def
create_lr0_table
(
            
self
            
grammar
:
CanonicalGrammar
            
verbose
:
bool
            
progress
:
bool
    
)
-
>
None
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
:
typing
.
Deque
[
typing
.
Tuple
[
LR0Generator
StateAndTransitions
]
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
stable_locations
(
)
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
-
>
typing
.
Iterator
[
None
]
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
nMapping
state
{
}
to
LR0
:
\
n
{
}
"
.
format
(
s
.
stable_hash
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
stable_locations
(
)
                    
if
not
self
.
term_is_shifted
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
        
if
verbose
:
            
print
(
"
Create
LR
(
0
)
Table
Result
:
"
)
            
self
.
debug_dump
(
)
    
def
term_is_shifted
(
self
term
:
typing
.
Optional
[
Term
]
)
-
>
bool
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
:
typing
.
Sequence
[
Edge
]
            
state
:
typing
.
Optional
[
StateId
]
=
None
    
)
-
>
bool
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
            
assert
isinstance
(
state
StateId
)
            
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
            
assert
term
is
not
None
            
state
=
row
[
term
]
        
return
True
    
def
term_is_stacked
(
self
term
:
typing
.
Optional
[
Term
]
)
-
>
bool
:
        
assert
term
is
not
None
        
return
not
isinstance
(
term
Action
)
    
def
aps_visitor
(
self
aps
:
APS
visit
:
typing
.
Callable
[
[
APS
]
bool
]
)
-
>
None
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
a
callback
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
.
The
visit
function
might
capture
APS
given
as
        
argument
to
be
used
for
other
analysis
.
        
"
"
"
        
todo
=
[
aps
]
        
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
aps
.
shift_next
(
self
)
)
    
def
context_lanes
(
self
state
:
StateId
)
-
>
typing
.
Tuple
[
bool
typing
.
List
[
APS
]
]
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
        
def
not_interesting
(
aps
:
APS
)
-
>
bool
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
history
if
self
.
term_is_shifted
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
:
typing
.
DefaultDict
[
typing
.
Tuple
[
Edge
.
.
.
]
typing
.
List
[
Edge
]
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
        
def
has_enough_context
(
aps
:
APS
)
-
>
bool
:
            
try
:
                
assert
aps
.
history
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
APS
.
start
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
history
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
history
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
aps
.
shift_next
(
self
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
:
StateId
)
-
>
typing
.
List
[
APS
]
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
        
record
=
[
]
        
seen_edge_after_reduce
:
typing
.
Set
[
typing
.
Tuple
[
Edge
StateId
typing
.
Optional
[
Term
]
]
]
        
seen_edge_after_reduce
=
set
(
)
        
def
find_first_reduce
(
                
edges
:
Path
        
)
-
>
typing
.
Tuple
[
int
typing
.
Optional
[
Edge
]
]
:
            
for
i
edge
in
enumerate
(
edges
)
:
                
if
not
self
.
term_is_shifted
(
edge
.
term
)
:
                    
return
i
edge
            
return
0
None
        
def
find_last_reduce
(
                
edges
:
Path
        
)
-
>
typing
.
Tuple
[
int
typing
.
Optional
[
Edge
]
]
:
            
for
i
edge
in
zip
(
reversed
(
range
(
len
(
edges
)
)
)
reversed
(
edges
)
)
:
                
if
not
self
.
term_is_shifted
(
edge
.
term
)
:
                    
return
i
edge
            
return
0
None
        
def
visit
(
aps
:
APS
)
-
>
bool
:
            
reduce_key
=
None
            
first_index
first_reduce
=
find_first_reduce
(
aps
.
history
)
            
last_index
last_reduce
=
find_last_reduce
(
aps
.
history
)
            
if
first_index
!
=
last_index
and
first_reduce
and
last_reduce
:
                
if
not
isinstance
(
aps
.
history
[
-
1
]
.
term
Action
)
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
last_reduce
.
term
)
            
has_seen_edge_after_reduce
=
reduce_key
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
reduce_key
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
APS
.
start
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
:
StateId
aps_lanes
:
typing
.
List
[
APS
]
)
-
>
None
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
:
StateId
aps_lanes
:
typing
.
List
[
APS
]
)
-
>
None
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
        
if
self
.
debug_info
:
            
for
aps
in
aps_lanes
:
                
print
(
str
(
aps
)
)
        
maybe_unreachable_set
:
OrderedSet
[
StateId
]
=
OrderedSet
(
)
        
shift_map
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
typing
.
Tuple
[
StateAndTransitions
typing
.
List
[
Edge
]
]
]
        
]
        
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
history
            
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
            
assert
term
=
=
aps
.
lookahead
[
0
]
            
assert
isinstance
(
term
(
str
End
ErrorSymbol
Nt
)
)
            
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
term_is_shifted
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
                
edge_term
=
edge
.
term
                
assert
isinstance
(
edge_term
Action
)
                
new_term
=
edge_term
.
shifted_action
(
term
)
                
if
isinstance
(
new_term
bool
)
:
                    
if
new_term
is
False
:
                        
accept
=
False
                        
break
                    
else
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
                
target_id
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
target_id
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
:
StateAndTransitions
                
shift_map
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
typing
.
Tuple
[
StateAndTransitions
typing
.
List
[
Edge
]
]
]
                
]
                
depth
:
str
        
)
-
>
None
:
            
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
:
OrderedSet
[
str
]
=
OrderedSet
(
)
                
delayed
:
OrderedSet
[
Action
]
=
OrderedSet
(
)
                
new_shift_map
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
typing
.
Tuple
[
StateAndTransitions
typing
.
List
[
Edge
]
]
]
                
]
                
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
term_is_shifted
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
                            
action_term
=
action
.
term
                            
assert
isinstance
(
action_term
Action
)
                            
delayed
.
add
(
action_term
)
                        
edge_term
=
edge
.
term
                        
assert
edge_term
is
not
None
                        
new_shift_map
[
edge_term
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
next_dest_id
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
next_dest_id
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
                
is_new
new_target
=
self
.
new_state
(
                    
OrderedFrozenSet
(
locations
)
OrderedFrozenSet
(
delayed
)
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
self
.
debug_info
:
                    
print
(
"
{
}
is_new
=
{
}
index
=
{
}
"
.
format
(
depth
is_new
new_target
.
index
)
)
                    
print
(
"
{
}
Add
:
{
}
-
-
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
depth
state
.
index
str
(
term
)
new_target
.
index
)
)
                    
print
(
"
{
}
continue
:
(
is_new
:
{
}
)
or
(
recurse
:
{
}
)
"
.
format
(
depth
is_new
recurse
)
)
                
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
target_id
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
target_id
)
            
if
self
.
debug_info
:
                
print
(
"
{
}
replaced
by
{
}
\
n
"
.
format
(
depth
state
)
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
:
StateId
verbose
:
bool
)
-
>
bool
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
:
bool
progress
:
bool
)
-
>
None
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
        
self
.
assume_inconsistent
=
True
        
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
:
typing
.
Deque
[
StateId
]
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
-
>
typing
.
Iterator
[
None
]
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
.
stable_str
(
self
.
states
)
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
.
stable_str
(
self
.
states
)
                                    
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
        
self
.
assume_inconsistent
=
False
        
if
verbose
:
            
print
(
"
Fix
Inconsistent
Table
Result
:
"
)
            
self
.
debug_dump
(
)
    
def
remove_all_unreachable_state
(
self
verbose
:
bool
progress
:
bool
)
-
>
None
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
        
self
.
rewrite_reordered_state_indexes
(
)
    
def
fold_identical_endings
(
self
verbose
:
bool
progress
:
bool
)
-
>
None
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
        
def
rewrite_backedges
(
state_list
:
typing
.
List
[
StateAndTransitions
]
                              
state_map
:
typing
.
Dict
[
StateId
StateId
]
                              
maybe_unreachable
:
OrderedSet
[
StateId
]
)
-
>
bool
:
            
ref
=
state_list
.
pop
(
)
            
replace_edges
=
[
e
for
s
in
state_list
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
                
edge_term
=
edge
.
term
                
assert
edge_term
is
not
None
                
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
                
old_dest
=
src
[
edge_term
]
                
self
.
replace_edge
(
src
edge_term
ref
.
index
maybe_unreachable
)
                
state_map
[
old_dest
]
=
ref
.
index
                
hit
=
True
            
return
hit
        
def
rewrite_if_same_outedges
(
state_list
:
typing
.
List
[
StateAndTransitions
]
)
-
>
bool
:
            
maybe_unreachable
:
OrderedSet
[
StateId
]
=
OrderedSet
(
)
            
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
            
state_map
=
{
i
:
i
for
i
_
in
enumerate
(
self
.
states
)
}
            
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
state_map
maybe_unreachable
)
or
hit
            
if
hit
:
                
self
.
remove_unreachable_states
(
maybe_unreachable
)
                
self
.
rewrite_state_indexes
(
state_map
)
                
self
.
remove_all_unreachable_state
(
verbose
progress
)
            
return
hit
        
def
visit_table
(
)
-
>
typing
.
Iterator
[
None
]
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
    
def
group_epsilon_states
(
self
verbose
:
bool
progress
:
bool
)
-
>
None
:
        
def
all_action_inedges
(
s
:
StateAndTransitions
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
.
term
Action
)
for
e
in
s
.
backedges
)
        
shift_states
action_states
=
split
(
self
.
states
lambda
s
:
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
        
from_act_action_states
from_shf_action_states
=
split
(
action_states
all_action_inedges
)
        
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
from_shf_action_states
)
        
self
.
states
.
extend
(
from_act_action_states
)
        
self
.
rewrite_reordered_state_indexes
(
)
    
def
count_shift_states
(
self
)
-
>
int
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
s
is
not
None
and
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
-
>
int
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
s
is
not
None
and
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
count_action_from_shift_states
(
self
)
-
>
int
:
        
def
from_shift_states
(
s
:
StateAndTransitions
)
-
>
bool
:
            
return
any
(
not
isinstance
(
e
.
term
Action
)
for
e
in
s
.
backedges
)
        
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
and
from_shift_states
(
s
)
)
    
def
prepare_debug_context
(
self
)
-
>
DebugInfo
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
or
not
s
.
epsilon
:
                
continue
            
aps
=
APS
.
start
(
s
.
index
)
            
for
aps_next
in
aps
.
shift_next
(
self
)
:
                
if
not
aps_next
.
reducing
:
                    
continue
                
for
i
edge
in
enumerate
(
aps_next
.
stack
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
        
return
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
    
def
debug_context
(
            
self
            
state
:
StateId
            
split_txt
:
str
=
"
;
"
            
prefix
:
str
=
"
"
    
)
-
>
str
:
        
"
"
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
"
"
        
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
        
debug_info
=
typing
.
cast
(
typing
.
Dict
[
StateId
int
]
self
.
debug_info
)
        
record
=
[
]
        
def
visit
(
aps
:
APS
)
-
>
bool
:
            
if
aps
.
history
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
history
[
-
1
]
.
term
            
is_unwind
=
isinstance
(
last
Action
)
and
last
.
update_stack
(
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
is_unwind
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
1
            
save
=
save
and
is_unwind
            
if
save
:
                
assert
isinstance
(
last
Action
)
                
save
=
last
.
update_stack_with
(
)
.
nt
in
self
.
states
[
aps
.
shift
[
0
]
.
src
]
            
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
APS
.
start
(
state
)
visit
)
        
context
:
OrderedSet
[
str
]
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
history
!
=
[
]
            
action
=
aps
.
history
[
-
1
]
.
term
            
assert
isinstance
(
action
Action
)
            
assert
action
.
update_stack
(
)
            
stack_diff
=
action
.
update_stack_with
(
)
            
replay
=
stack_diff
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
history
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
stack_diff
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
