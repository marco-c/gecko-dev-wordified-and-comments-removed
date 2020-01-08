import
gdb
import
itertools
from
gdbpp
import
GeckoPrettyPrinter
def
walk_template_to_given_base
(
value
desired_tag_prefix
)
:
    
'
'
'
Given
a
value
of
some
template
subclass
walk
up
its
ancestry
until
we
    
hit
the
desired
type
then
return
the
appropriate
value
(
which
will
then
    
have
that
type
)
.
    
'
'
'
    
t
=
value
.
type
    
t
=
t
.
strip_typedefs
(
)
    
if
t
.
tag
.
startswith
(
desired_tag_prefix
)
:
        
return
value
    
for
f
in
t
.
fields
(
)
:
        
if
not
f
.
is_base_class
:
            
continue
        
fv
=
value
[
f
]
        
ft
=
fv
.
type
        
if
ft
.
tag
.
startswith
(
desired_tag_prefix
)
:
            
return
fv
        
return
walk_template_to_given_base
(
fv
desired_tag_prefix
)
    
return
None
GeckoPrettyPrinter
(
'
nsClassHashtable
'
'
^
nsClassHashtable
<
.
*
>
'
)
GeckoPrettyPrinter
(
'
nsDataHashtable
'
'
^
nsDataHashtable
<
.
*
>
'
)
GeckoPrettyPrinter
(
'
nsInterfaceHashtable
'
'
^
nsInterfaceHashtable
<
.
*
>
'
)
GeckoPrettyPrinter
(
'
nsRefPtrHashtable
'
'
^
nsRefPtrHashtable
<
.
*
>
'
)
GeckoPrettyPrinter
(
'
nsBaseHashtable
'
'
^
nsBaseHashtable
<
.
*
>
'
)
GeckoPrettyPrinter
(
'
nsTHashtable
'
'
^
nsTHashtable
<
.
*
>
'
)
class
thashtable_printer
(
object
)
:
    
def
__init__
(
self
outer_value
)
:
        
self
.
outermost_type
=
outer_value
.
type
        
value
=
walk_template_to_given_base
(
outer_value
'
nsTHashtable
<
'
)
        
self
.
value
=
value
        
self
.
entry_type
=
value
.
type
.
template_argument
(
0
)
        
self
.
is_table
=
self
.
entry_type
.
tag
.
startswith
(
'
nsBaseHashtableET
<
'
)
        
if
self
.
is_table
:
            
key_type
=
self
.
entry_type
.
template_argument
(
0
)
        
else
:
            
key_type
=
self
.
entry_type
        
self
.
key_field_name
=
None
        
for
f
in
key_type
.
fields
(
)
:
            
if
f
.
is_base_class
:
                
continue
            
if
f
.
name
=
=
'
mKeyHash
'
or
f
.
name
=
=
'
mData
'
:
                
continue
            
self
.
key_field_name
=
f
.
name
            
break
    
def
children
(
self
)
:
        
table
=
self
.
value
[
'
mTable
'
]
        
entryCount
=
table
[
'
mEntryCount
'
]
        
if
entryCount
=
=
0
:
            
return
        
hashType
=
gdb
.
lookup_type
(
'
mozilla
:
:
HashNumber
'
)
        
hashBits
=
hashType
.
sizeof
*
8
        
capacity
=
1
<
<
(
hashBits
-
table
[
'
mHashShift
'
]
)
        
store
=
table
[
'
mEntryStore
'
]
[
'
mEntryStore
'
]
        
key_field_name
=
self
.
key_field_name
        
pHashes
=
store
.
cast
(
hashType
.
pointer
(
)
)
        
pEntries
=
pHashes
+
capacity
        
pEntries
=
pEntries
.
cast
(
self
.
entry_type
.
pointer
(
)
)
        
seenCount
=
0
        
for
i
in
range
(
0
int
(
capacity
)
)
:
            
entryHash
=
(
pHashes
+
i
)
.
dereference
(
)
            
if
entryHash
<
=
1
:
                
continue
            
entry
=
(
pEntries
+
i
)
.
dereference
(
)
            
yield
(
'
%
d
'
%
i
entry
[
key_field_name
]
)
            
if
self
.
is_table
:
                
yield
(
'
%
d
'
%
i
entry
[
'
mData
'
]
)
            
seenCount
+
=
1
            
if
seenCount
>
=
entryCount
:
                
break
    
def
to_string
(
self
)
:
        
return
str
(
self
.
outermost_type
)
    
def
display_hint
(
self
)
:
        
if
self
.
is_table
:
            
return
'
map
'
        
else
:
            
return
'
array
'
