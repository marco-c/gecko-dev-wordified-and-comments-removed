import
railroad
from
pip
.
_vendor
import
pyparsing
import
typing
from
typing
import
(
    
List
    
NamedTuple
    
Generic
    
TypeVar
    
Dict
    
Callable
    
Set
    
Iterable
)
from
jinja2
import
Template
from
io
import
StringIO
import
inspect
jinja2_template_source
=
"
"
"
\
{
%
if
not
embed
%
}
<
!
DOCTYPE
html
>
<
html
>
<
head
>
{
%
endif
%
}
    
{
%
if
not
head
%
}
        
<
style
>
            
.
railroad
-
heading
{
                
font
-
family
:
monospace
;
            
}
        
<
/
style
>
    
{
%
else
%
}
        
{
{
head
|
safe
}
}
    
{
%
endif
%
}
{
%
if
not
embed
%
}
<
/
head
>
<
body
>
{
%
endif
%
}
{
{
body
|
safe
}
}
{
%
for
diagram
in
diagrams
%
}
    
<
div
class
=
"
railroad
-
group
"
>
        
<
h1
class
=
"
railroad
-
heading
"
>
{
{
diagram
.
title
}
}
<
/
h1
>
        
<
div
class
=
"
railroad
-
description
"
>
{
{
diagram
.
text
}
}
<
/
div
>
        
<
div
class
=
"
railroad
-
svg
"
>
            
{
{
diagram
.
svg
}
}
        
<
/
div
>
    
<
/
div
>
{
%
endfor
%
}
{
%
if
not
embed
%
}
<
/
body
>
<
/
html
>
{
%
endif
%
}
"
"
"
template
=
Template
(
jinja2_template_source
)
NamedDiagram
=
NamedTuple
(
    
"
NamedDiagram
"
    
[
(
"
name
"
str
)
(
"
diagram
"
typing
.
Optional
[
railroad
.
DiagramItem
]
)
(
"
index
"
int
)
]
)
"
"
"
A
simple
structure
for
associating
a
name
with
a
railroad
diagram
"
"
"
T
=
TypeVar
(
"
T
"
)
class
EachItem
(
railroad
.
Group
)
:
    
"
"
"
    
Custom
railroad
item
to
compose
a
:
    
-
Group
containing
a
      
-
OneOrMore
containing
a
        
-
Choice
of
the
elements
in
the
Each
    
with
the
group
label
indicating
that
all
must
be
matched
    
"
"
"
    
all_label
=
"
[
ALL
]
"
    
def
__init__
(
self
*
items
)
:
        
choice_item
=
railroad
.
Choice
(
len
(
items
)
-
1
*
items
)
        
one_or_more_item
=
railroad
.
OneOrMore
(
item
=
choice_item
)
        
super
(
)
.
__init__
(
one_or_more_item
label
=
self
.
all_label
)
class
AnnotatedItem
(
railroad
.
Group
)
:
    
"
"
"
    
Simple
subclass
of
Group
that
creates
an
annotation
label
    
"
"
"
    
def
__init__
(
self
label
:
str
item
)
:
        
super
(
)
.
__init__
(
item
=
item
label
=
"
[
{
}
]
"
.
format
(
label
)
if
label
else
label
)
class
EditablePartial
(
Generic
[
T
]
)
:
    
"
"
"
    
Acts
like
a
functools
.
partial
but
can
be
edited
.
In
other
words
it
represents
a
type
that
hasn
'
t
yet
been
    
constructed
.
    
"
"
"
    
def
__init__
(
self
func
:
Callable
[
.
.
.
T
]
args
:
list
kwargs
:
dict
)
:
        
self
.
func
=
func
        
self
.
args
=
args
        
self
.
kwargs
=
kwargs
    
classmethod
    
def
from_call
(
cls
func
:
Callable
[
.
.
.
T
]
*
args
*
*
kwargs
)
-
>
"
EditablePartial
[
T
]
"
:
        
"
"
"
        
If
you
call
this
function
in
the
same
way
that
you
would
call
the
constructor
it
will
store
the
arguments
        
as
you
expect
.
For
example
EditablePartial
.
from_call
(
Fraction
1
3
)
(
)
=
=
Fraction
(
1
3
)
        
"
"
"
        
return
EditablePartial
(
func
=
func
args
=
list
(
args
)
kwargs
=
kwargs
)
    
property
    
def
name
(
self
)
:
        
return
self
.
kwargs
[
"
name
"
]
    
def
__call__
(
self
)
-
>
T
:
        
"
"
"
        
Evaluate
the
partial
and
return
the
result
        
"
"
"
        
args
=
self
.
args
.
copy
(
)
        
kwargs
=
self
.
kwargs
.
copy
(
)
        
arg_spec
=
inspect
.
getfullargspec
(
self
.
func
)
        
if
arg_spec
.
varargs
in
self
.
kwargs
:
            
args
+
=
kwargs
.
pop
(
arg_spec
.
varargs
)
        
return
self
.
func
(
*
args
*
*
kwargs
)
def
railroad_to_html
(
diagrams
:
List
[
NamedDiagram
]
embed
=
False
*
*
kwargs
)
-
>
str
:
    
"
"
"
    
Given
a
list
of
NamedDiagram
produce
a
single
HTML
string
that
visualises
those
diagrams
    
:
params
kwargs
:
kwargs
to
be
passed
in
to
the
template
    
"
"
"
    
data
=
[
]
    
for
diagram
in
diagrams
:
        
if
diagram
.
diagram
is
None
:
            
continue
        
io
=
StringIO
(
)
        
try
:
            
css
=
kwargs
.
get
(
'
css
'
)
            
diagram
.
diagram
.
writeStandalone
(
io
.
write
css
=
css
)
        
except
AttributeError
:
            
diagram
.
diagram
.
writeSvg
(
io
.
write
)
        
title
=
diagram
.
name
        
if
diagram
.
index
=
=
0
:
            
title
+
=
"
(
root
)
"
        
data
.
append
(
{
"
title
"
:
title
"
text
"
:
"
"
"
svg
"
:
io
.
getvalue
(
)
}
)
    
return
template
.
render
(
diagrams
=
data
embed
=
embed
*
*
kwargs
)
def
resolve_partial
(
partial
:
"
EditablePartial
[
T
]
"
)
-
>
T
:
    
"
"
"
    
Recursively
resolves
a
collection
of
Partials
into
whatever
type
they
are
    
"
"
"
    
if
isinstance
(
partial
EditablePartial
)
:
        
partial
.
args
=
resolve_partial
(
partial
.
args
)
        
partial
.
kwargs
=
resolve_partial
(
partial
.
kwargs
)
        
return
partial
(
)
    
elif
isinstance
(
partial
list
)
:
        
return
[
resolve_partial
(
x
)
for
x
in
partial
]
    
elif
isinstance
(
partial
dict
)
:
        
return
{
key
:
resolve_partial
(
x
)
for
key
x
in
partial
.
items
(
)
}
    
else
:
        
return
partial
def
to_railroad
(
    
element
:
pyparsing
.
ParserElement
    
diagram_kwargs
:
typing
.
Optional
[
dict
]
=
None
    
vertical
:
int
=
3
    
show_results_names
:
bool
=
False
    
show_groups
:
bool
=
False
)
-
>
List
[
NamedDiagram
]
:
    
"
"
"
    
Convert
a
pyparsing
element
tree
into
a
list
of
diagrams
.
This
is
the
recommended
entrypoint
to
diagram
    
creation
if
you
want
to
access
the
Railroad
tree
before
it
is
converted
to
HTML
    
:
param
element
:
base
element
of
the
parser
being
diagrammed
    
:
param
diagram_kwargs
:
kwargs
to
pass
to
the
Diagram
(
)
constructor
    
:
param
vertical
:
(
optional
)
-
int
-
limit
at
which
number
of
alternatives
should
be
       
shown
vertically
instead
of
horizontally
    
:
param
show_results_names
-
bool
to
indicate
whether
results
name
annotations
should
be
       
included
in
the
diagram
    
:
param
show_groups
-
bool
to
indicate
whether
groups
should
be
highlighted
with
an
unlabeled
       
surrounding
box
    
"
"
"
    
lookup
=
ConverterState
(
diagram_kwargs
=
diagram_kwargs
or
{
}
)
    
_to_diagram_element
(
        
element
        
lookup
=
lookup
        
parent
=
None
        
vertical
=
vertical
        
show_results_names
=
show_results_names
        
show_groups
=
show_groups
    
)
    
root_id
=
id
(
element
)
    
if
root_id
in
lookup
:
        
if
not
element
.
customName
:
            
lookup
[
root_id
]
.
name
=
"
"
        
lookup
[
root_id
]
.
mark_for_extraction
(
root_id
lookup
force
=
True
)
    
diags
=
list
(
lookup
.
diagrams
.
values
(
)
)
    
if
len
(
diags
)
>
1
:
        
seen
=
set
(
)
        
deduped_diags
=
[
]
        
for
d
in
diags
:
            
if
d
.
name
=
=
"
.
.
.
"
:
                
continue
            
if
d
.
name
is
not
None
and
d
.
name
not
in
seen
:
                
seen
.
add
(
d
.
name
)
                
deduped_diags
.
append
(
d
)
        
resolved
=
[
resolve_partial
(
partial
)
for
partial
in
deduped_diags
]
    
else
:
        
resolved
=
[
resolve_partial
(
partial
)
for
partial
in
diags
]
    
return
sorted
(
resolved
key
=
lambda
diag
:
diag
.
index
)
def
_should_vertical
(
    
specification
:
int
exprs
:
Iterable
[
pyparsing
.
ParserElement
]
)
-
>
bool
:
    
"
"
"
    
Returns
true
if
we
should
return
a
vertical
list
of
elements
    
"
"
"
    
if
specification
is
None
:
        
return
False
    
else
:
        
return
len
(
_visible_exprs
(
exprs
)
)
>
=
specification
class
ElementState
:
    
"
"
"
    
State
recorded
for
an
individual
pyparsing
Element
    
"
"
"
    
def
__init__
(
        
self
        
element
:
pyparsing
.
ParserElement
        
converted
:
EditablePartial
        
parent
:
EditablePartial
        
number
:
int
        
name
:
str
=
None
        
parent_index
:
typing
.
Optional
[
int
]
=
None
    
)
:
        
self
.
element
:
pyparsing
.
ParserElement
=
element
        
self
.
name
:
typing
.
Optional
[
str
]
=
name
        
self
.
converted
:
EditablePartial
=
converted
        
self
.
parent
:
EditablePartial
=
parent
        
self
.
number
:
int
=
number
        
self
.
parent_index
:
typing
.
Optional
[
int
]
=
parent_index
        
self
.
extract
:
bool
=
False
        
self
.
complete
:
bool
=
False
    
def
mark_for_extraction
(
        
self
el_id
:
int
state
:
"
ConverterState
"
name
:
str
=
None
force
:
bool
=
False
    
)
:
        
"
"
"
        
Called
when
this
instance
has
been
seen
twice
and
thus
should
eventually
be
extracted
into
a
sub
-
diagram
        
:
param
el_id
:
id
of
the
element
        
:
param
state
:
element
/
diagram
state
tracker
        
:
param
name
:
name
to
use
for
this
element
'
s
text
        
:
param
force
:
If
true
force
extraction
now
regardless
of
the
state
of
this
.
Only
useful
for
extracting
the
        
root
element
when
we
know
we
'
re
finished
        
"
"
"
        
self
.
extract
=
True
        
if
not
self
.
name
:
            
if
name
:
                
self
.
name
=
name
            
elif
self
.
element
.
customName
:
                
self
.
name
=
self
.
element
.
customName
            
else
:
                
self
.
name
=
"
"
        
if
force
or
(
self
.
complete
and
_worth_extracting
(
self
.
element
)
)
:
            
state
.
extract_into_diagram
(
el_id
)
class
ConverterState
:
    
"
"
"
    
Stores
some
state
that
persists
between
recursions
into
the
element
tree
    
"
"
"
    
def
__init__
(
self
diagram_kwargs
:
typing
.
Optional
[
dict
]
=
None
)
:
        
self
.
_element_diagram_states
:
Dict
[
int
ElementState
]
=
{
}
        
self
.
diagrams
:
Dict
[
int
EditablePartial
[
NamedDiagram
]
]
=
{
}
        
self
.
unnamed_index
:
int
=
1
        
self
.
index
:
int
=
0
        
self
.
diagram_kwargs
:
dict
=
diagram_kwargs
or
{
}
        
self
.
extracted_diagram_names
:
Set
[
str
]
=
set
(
)
    
def
__setitem__
(
self
key
:
int
value
:
ElementState
)
:
        
self
.
_element_diagram_states
[
key
]
=
value
    
def
__getitem__
(
self
key
:
int
)
-
>
ElementState
:
        
return
self
.
_element_diagram_states
[
key
]
    
def
__delitem__
(
self
key
:
int
)
:
        
del
self
.
_element_diagram_states
[
key
]
    
def
__contains__
(
self
key
:
int
)
:
        
return
key
in
self
.
_element_diagram_states
    
def
generate_unnamed
(
self
)
-
>
int
:
        
"
"
"
        
Generate
a
number
used
in
the
name
of
an
otherwise
unnamed
diagram
        
"
"
"
        
self
.
unnamed_index
+
=
1
        
return
self
.
unnamed_index
    
def
generate_index
(
self
)
-
>
int
:
        
"
"
"
        
Generate
a
number
used
to
index
a
diagram
        
"
"
"
        
self
.
index
+
=
1
        
return
self
.
index
    
def
extract_into_diagram
(
self
el_id
:
int
)
:
        
"
"
"
        
Used
when
we
encounter
the
same
token
twice
in
the
same
tree
.
When
this
        
happens
we
replace
all
instances
of
that
token
with
a
terminal
and
        
create
a
new
subdiagram
for
the
token
        
"
"
"
        
position
=
self
[
el_id
]
        
if
position
.
parent
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
NonTerminal
text
=
position
.
name
)
            
if
"
item
"
in
position
.
parent
.
kwargs
:
                
position
.
parent
.
kwargs
[
"
item
"
]
=
ret
            
elif
"
items
"
in
position
.
parent
.
kwargs
:
                
position
.
parent
.
kwargs
[
"
items
"
]
[
position
.
parent_index
]
=
ret
        
if
position
.
converted
.
func
=
=
railroad
.
Group
:
            
content
=
position
.
converted
.
kwargs
[
"
item
"
]
        
else
:
            
content
=
position
.
converted
        
self
.
diagrams
[
el_id
]
=
EditablePartial
.
from_call
(
            
NamedDiagram
            
name
=
position
.
name
            
diagram
=
EditablePartial
.
from_call
(
                
railroad
.
Diagram
content
*
*
self
.
diagram_kwargs
            
)
            
index
=
position
.
number
        
)
        
del
self
[
el_id
]
def
_worth_extracting
(
element
:
pyparsing
.
ParserElement
)
-
>
bool
:
    
"
"
"
    
Returns
true
if
this
element
is
worth
having
its
own
sub
-
diagram
.
Simply
if
any
of
its
children
    
themselves
have
children
then
its
complex
enough
to
extract
    
"
"
"
    
children
=
element
.
recurse
(
)
    
return
any
(
child
.
recurse
(
)
for
child
in
children
)
def
_apply_diagram_item_enhancements
(
fn
)
:
    
"
"
"
    
decorator
to
ensure
enhancements
to
a
diagram
item
(
such
as
results
name
annotations
)
    
get
applied
on
return
from
_to_diagram_element
(
we
do
this
since
there
are
several
    
returns
in
_to_diagram_element
)
    
"
"
"
    
def
_inner
(
        
element
:
pyparsing
.
ParserElement
        
parent
:
typing
.
Optional
[
EditablePartial
]
        
lookup
:
ConverterState
=
None
        
vertical
:
int
=
None
        
index
:
int
=
0
        
name_hint
:
str
=
None
        
show_results_names
:
bool
=
False
        
show_groups
:
bool
=
False
    
)
-
>
typing
.
Optional
[
EditablePartial
]
:
        
ret
=
fn
(
            
element
            
parent
            
lookup
            
vertical
            
index
            
name_hint
            
show_results_names
            
show_groups
        
)
        
if
show_results_names
and
ret
is
not
None
:
            
element_results_name
=
element
.
resultsName
            
if
element_results_name
:
                
element_results_name
+
=
"
"
if
element
.
modalResults
else
"
*
"
                
ret
=
EditablePartial
.
from_call
(
                    
railroad
.
Group
item
=
ret
label
=
element_results_name
                
)
        
return
ret
    
return
_inner
def
_visible_exprs
(
exprs
:
Iterable
[
pyparsing
.
ParserElement
]
)
:
    
non_diagramming_exprs
=
(
        
pyparsing
.
ParseElementEnhance
        
pyparsing
.
PositionToken
        
pyparsing
.
And
.
_ErrorStop
    
)
    
return
[
        
e
        
for
e
in
exprs
        
if
not
(
e
.
customName
or
e
.
resultsName
or
isinstance
(
e
non_diagramming_exprs
)
)
    
]
_apply_diagram_item_enhancements
def
_to_diagram_element
(
    
element
:
pyparsing
.
ParserElement
    
parent
:
typing
.
Optional
[
EditablePartial
]
    
lookup
:
ConverterState
=
None
    
vertical
:
int
=
None
    
index
:
int
=
0
    
name_hint
:
str
=
None
    
show_results_names
:
bool
=
False
    
show_groups
:
bool
=
False
)
-
>
typing
.
Optional
[
EditablePartial
]
:
    
"
"
"
    
Recursively
converts
a
PyParsing
Element
to
a
railroad
Element
    
:
param
lookup
:
The
shared
converter
state
that
keeps
track
of
useful
things
    
:
param
index
:
The
index
of
this
element
within
the
parent
    
:
param
parent
:
The
parent
of
this
element
in
the
output
tree
    
:
param
vertical
:
Controls
at
what
point
we
make
a
list
of
elements
vertical
.
If
this
is
an
integer
(
the
default
)
    
it
sets
the
threshold
of
the
number
of
items
before
we
go
vertical
.
If
True
always
go
vertical
if
False
never
    
do
so
    
:
param
name_hint
:
If
provided
this
will
override
the
generated
name
    
:
param
show_results_names
:
bool
flag
indicating
whether
to
add
annotations
for
results
names
    
:
returns
:
The
converted
version
of
the
input
element
but
as
a
Partial
that
hasn
'
t
yet
been
constructed
    
:
param
show_groups
:
bool
flag
indicating
whether
to
show
groups
using
bounding
box
    
"
"
"
    
exprs
=
element
.
recurse
(
)
    
name
=
name_hint
or
element
.
customName
or
element
.
__class__
.
__name__
    
el_id
=
id
(
element
)
    
element_results_name
=
element
.
resultsName
    
if
not
element
.
customName
:
        
if
isinstance
(
            
element
            
(
                
pyparsing
.
Located
            
)
        
)
:
            
if
exprs
:
                
if
not
exprs
[
0
]
.
customName
:
                    
propagated_name
=
name
                
else
:
                    
propagated_name
=
None
                
return
_to_diagram_element
(
                    
element
.
expr
                    
parent
=
parent
                    
lookup
=
lookup
                    
vertical
=
vertical
                    
index
=
index
                    
name_hint
=
propagated_name
                    
show_results_names
=
show_results_names
                    
show_groups
=
show_groups
                
)
    
if
_worth_extracting
(
element
)
:
        
if
el_id
in
lookup
:
            
looked_up
=
lookup
[
el_id
]
            
looked_up
.
mark_for_extraction
(
el_id
lookup
name
=
name_hint
)
            
ret
=
EditablePartial
.
from_call
(
railroad
.
NonTerminal
text
=
looked_up
.
name
)
            
return
ret
        
elif
el_id
in
lookup
.
diagrams
:
            
ret
=
EditablePartial
.
from_call
(
                
railroad
.
NonTerminal
text
=
lookup
.
diagrams
[
el_id
]
.
kwargs
[
"
name
"
]
            
)
            
return
ret
    
if
isinstance
(
element
pyparsing
.
And
)
:
        
if
not
exprs
:
            
return
None
        
if
len
(
set
(
(
e
.
name
e
.
resultsName
)
for
e
in
exprs
)
)
=
=
1
:
            
ret
=
EditablePartial
.
from_call
(
                
railroad
.
OneOrMore
item
=
"
"
repeat
=
str
(
len
(
exprs
)
)
            
)
        
elif
_should_vertical
(
vertical
exprs
)
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
Stack
items
=
[
]
)
        
else
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
Sequence
items
=
[
]
)
    
elif
isinstance
(
element
(
pyparsing
.
Or
pyparsing
.
MatchFirst
)
)
:
        
if
not
exprs
:
            
return
None
        
if
_should_vertical
(
vertical
exprs
)
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
Choice
0
items
=
[
]
)
        
else
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
HorizontalChoice
items
=
[
]
)
    
elif
isinstance
(
element
pyparsing
.
Each
)
:
        
if
not
exprs
:
            
return
None
        
ret
=
EditablePartial
.
from_call
(
EachItem
items
=
[
]
)
    
elif
isinstance
(
element
pyparsing
.
NotAny
)
:
        
ret
=
EditablePartial
.
from_call
(
AnnotatedItem
label
=
"
NOT
"
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
FollowedBy
)
:
        
ret
=
EditablePartial
.
from_call
(
AnnotatedItem
label
=
"
LOOKAHEAD
"
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
PrecededBy
)
:
        
ret
=
EditablePartial
.
from_call
(
AnnotatedItem
label
=
"
LOOKBEHIND
"
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
Group
)
:
        
if
show_groups
:
            
ret
=
EditablePartial
.
from_call
(
AnnotatedItem
label
=
"
"
item
=
"
"
)
        
else
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
Group
label
=
"
"
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
TokenConverter
)
:
        
label
=
type
(
element
)
.
__name__
.
lower
(
)
        
if
label
=
=
"
tokenconverter
"
:
            
ret
=
EditablePartial
.
from_call
(
railroad
.
Sequence
items
=
[
]
)
        
else
:
            
ret
=
EditablePartial
.
from_call
(
AnnotatedItem
label
=
label
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
Opt
)
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
Optional
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
OneOrMore
)
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
OneOrMore
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
ZeroOrMore
)
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
ZeroOrMore
item
=
"
"
)
    
elif
isinstance
(
element
pyparsing
.
Group
)
:
        
ret
=
EditablePartial
.
from_call
(
            
railroad
.
Group
item
=
None
label
=
element_results_name
        
)
    
elif
isinstance
(
element
pyparsing
.
Empty
)
and
not
element
.
customName
:
        
ret
=
None
    
elif
isinstance
(
element
pyparsing
.
ParseElementEnhance
)
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
Sequence
items
=
[
]
)
    
elif
len
(
exprs
)
>
0
and
not
element_results_name
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
Group
item
=
"
"
label
=
name
)
    
elif
len
(
exprs
)
>
0
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
Sequence
items
=
[
]
)
    
else
:
        
terminal
=
EditablePartial
.
from_call
(
railroad
.
Terminal
element
.
defaultName
)
        
ret
=
terminal
    
if
ret
is
None
:
        
return
    
lookup
[
el_id
]
=
ElementState
(
        
element
=
element
        
converted
=
ret
        
parent
=
parent
        
parent_index
=
index
        
number
=
lookup
.
generate_index
(
)
    
)
    
if
element
.
customName
:
        
lookup
[
el_id
]
.
mark_for_extraction
(
el_id
lookup
element
.
customName
)
    
i
=
0
    
for
expr
in
exprs
:
        
if
"
items
"
in
ret
.
kwargs
:
            
ret
.
kwargs
[
"
items
"
]
.
insert
(
i
None
)
        
item
=
_to_diagram_element
(
            
expr
            
parent
=
ret
            
lookup
=
lookup
            
vertical
=
vertical
            
index
=
i
            
show_results_names
=
show_results_names
            
show_groups
=
show_groups
        
)
        
if
item
is
not
None
:
            
if
"
item
"
in
ret
.
kwargs
:
                
ret
.
kwargs
[
"
item
"
]
=
item
            
elif
"
items
"
in
ret
.
kwargs
:
                
ret
.
kwargs
[
"
items
"
]
[
i
]
=
item
                
i
+
=
1
        
elif
"
items
"
in
ret
.
kwargs
:
            
del
ret
.
kwargs
[
"
items
"
]
[
i
]
    
if
ret
and
(
        
(
"
items
"
in
ret
.
kwargs
and
len
(
ret
.
kwargs
[
"
items
"
]
)
=
=
0
)
        
or
(
"
item
"
in
ret
.
kwargs
and
ret
.
kwargs
[
"
item
"
]
is
None
)
    
)
:
        
ret
=
EditablePartial
.
from_call
(
railroad
.
Terminal
name
)
    
if
el_id
in
lookup
:
        
lookup
[
el_id
]
.
complete
=
True
    
if
el_id
in
lookup
and
lookup
[
el_id
]
.
extract
and
lookup
[
el_id
]
.
complete
:
        
lookup
.
extract_into_diagram
(
el_id
)
        
if
ret
is
not
None
:
            
ret
=
EditablePartial
.
from_call
(
                
railroad
.
NonTerminal
text
=
lookup
.
diagrams
[
el_id
]
.
kwargs
[
"
name
"
]
            
)
    
return
ret
