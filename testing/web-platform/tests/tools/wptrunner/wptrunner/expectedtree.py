from
math
import
log
from
collections
import
defaultdict
class
Node
(
object
)
:
    
def
__init__
(
self
prop
value
)
:
        
self
.
prop
=
prop
        
self
.
value
=
value
        
self
.
parent
=
None
        
self
.
children
=
set
(
)
        
self
.
run_info
=
set
(
)
        
self
.
result_values
=
defaultdict
(
int
)
    
def
add
(
self
node
)
:
        
self
.
children
.
add
(
node
)
        
node
.
parent
=
self
    
def
__iter__
(
self
)
:
        
yield
self
        
for
node
in
self
.
children
:
            
for
item
in
node
:
                
yield
item
    
def
__len__
(
self
)
:
        
return
1
+
sum
(
len
(
item
)
for
item
in
self
.
children
)
def
entropy
(
results
)
:
    
"
"
"
This
is
basically
a
measure
of
the
uniformity
of
the
values
in
results
    
based
on
the
shannon
entropy
"
"
"
    
result_counts
=
defaultdict
(
int
)
    
total
=
float
(
len
(
results
)
)
    
for
values
in
results
.
values
(
)
:
        
for
value
in
values
:
            
result_counts
[
value
]
+
=
1
    
entropy_sum
=
0
    
for
count
in
result_counts
.
values
(
)
:
        
prop
=
float
(
count
)
/
total
        
entropy_sum
-
=
prop
*
log
(
prop
2
)
    
return
entropy_sum
def
split_results
(
prop
results
)
:
    
"
"
"
Split
a
dictionary
of
results
into
a
dictionary
of
dictionaries
where
    
each
sub
-
dictionary
has
a
specific
value
of
the
given
property
"
"
"
    
by_prop
=
defaultdict
(
dict
)
    
for
run_info
value
in
results
.
items
(
)
:
        
by_prop
[
run_info
[
prop
]
]
[
run_info
]
=
value
    
return
by_prop
def
build_tree
(
properties
dependent_props
results
tree
=
None
)
:
    
"
"
"
Build
a
decision
tree
mapping
properties
to
results
    
:
param
properties
:
-
A
list
of
run_info
properties
to
consider
                         
in
the
tree
    
:
param
dependent_props
:
-
A
dictionary
mapping
property
name
                              
to
properties
that
should
only
be
considered
                              
after
the
properties
in
the
key
.
For
example
                              
{
"
os
"
:
[
"
version
"
]
}
means
that
"
version
"
won
'
t
                              
be
used
until
after
os
.
    
:
param
results
:
Dictionary
mapping
run_info
to
set
of
results
    
:
tree
:
A
Node
object
to
use
as
the
root
of
the
(
sub
)
tree
"
"
"
    
if
tree
is
None
:
        
tree
=
Node
(
None
None
)
    
prop_index
=
{
prop
:
i
for
i
prop
in
enumerate
(
properties
)
}
    
all_results
=
defaultdict
(
int
)
    
for
result_values
in
results
.
values
(
)
:
        
for
result_value
count
in
result_values
.
items
(
)
:
            
all_results
[
result_value
]
+
=
count
    
if
not
properties
or
len
(
all_results
)
=
=
1
:
        
for
value
count
in
all_results
.
items
(
)
:
            
tree
.
result_values
[
value
]
+
=
count
        
tree
.
run_info
|
=
set
(
results
.
keys
(
)
)
        
return
tree
    
results_partitions
=
[
]
    
remove_properties
=
set
(
)
    
for
prop
in
properties
:
        
result_sets
=
split_results
(
prop
results
)
        
if
len
(
result_sets
)
=
=
1
:
            
remove_properties
.
add
(
prop
)
            
continue
        
new_entropy
=
0
.
        
results_sets_entropy
=
[
]
        
for
prop_value
result_set
in
result_sets
.
items
(
)
:
            
results_sets_entropy
.
append
(
(
entropy
(
result_set
)
prop_value
result_set
)
)
            
new_entropy
+
=
(
float
(
len
(
result_set
)
)
/
len
(
results
)
)
*
results_sets_entropy
[
-
1
]
[
0
]
        
results_partitions
.
append
(
(
new_entropy
                                   
prop
                                   
results_sets_entropy
)
)
    
if
not
results_partitions
:
        
for
value
count
in
all_results
.
items
(
)
:
            
tree
.
result_values
[
value
]
+
=
count
        
tree
.
run_info
|
=
set
(
results
.
keys
(
)
)
        
return
tree
    
results_partitions
.
sort
(
key
=
lambda
x
:
(
x
[
0
]
prop_index
[
x
[
1
]
]
)
)
    
_
best_prop
sub_results
=
results_partitions
[
0
]
    
new_props
=
properties
[
:
prop_index
[
best_prop
]
]
+
properties
[
prop_index
[
best_prop
]
+
1
:
]
    
new_props
.
extend
(
dependent_props
.
get
(
best_prop
[
]
)
)
    
if
remove_properties
:
        
new_props
=
[
item
for
item
in
new_props
if
item
not
in
remove_properties
]
    
for
_
prop_value
results_sets
in
sub_results
:
        
node
=
Node
(
best_prop
prop_value
)
        
tree
.
add
(
node
)
        
build_tree
(
new_props
dependent_props
results_sets
node
)
    
return
tree
