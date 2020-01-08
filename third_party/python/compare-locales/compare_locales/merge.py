'
Merge
resources
across
channels
.
'
from
collections
import
OrderedDict
defaultdict
from
codecs
import
encode
import
six
from
compare_locales
import
parser
as
cl
from
compare_locales
.
compare
import
AddRemove
class
MergeNotSupportedError
(
ValueError
)
:
    
pass
def
merge_channels
(
name
*
resources
)
:
    
try
:
        
parser
=
cl
.
getParser
(
name
)
    
except
UserWarning
:
        
raise
MergeNotSupportedError
(
            
'
Unsupported
file
format
(
{
}
)
.
'
.
format
(
name
)
)
    
entities
=
merge_resources
(
parser
*
resources
)
    
return
encode
(
serialize_legacy_resource
(
entities
)
parser
.
encoding
)
def
merge_resources
(
parser
*
resources
)
:
    
comments
=
{
}
    
def
parse_resource
(
resource
)
:
        
counter
=
defaultdict
(
int
)
        
if
isinstance
(
resource
bytes
)
:
            
parser
.
readContents
(
resource
)
            
resource
=
parser
.
walk
(
)
        
pairs
=
[
get_key_value
(
entity
counter
)
for
entity
in
resource
]
        
return
OrderedDict
(
pairs
)
    
def
get_key_value
(
entity
counter
)
:
        
if
isinstance
(
entity
cl
.
Comment
)
:
            
counter
[
entity
.
val
]
+
=
1
            
return
(
(
entity
.
val
counter
[
entity
.
val
]
)
entity
)
        
if
isinstance
(
entity
cl
.
Whitespace
)
:
            
return
(
entity
entity
)
        
if
isinstance
(
entity
cl
.
Entity
)
and
entity
.
pre_comment
:
            
comments
[
entity
.
pre_comment
]
=
entity
.
key
        
return
(
entity
.
key
entity
)
    
entities
=
six
.
moves
.
reduce
(
        
lambda
x
y
:
merge_two
(
comments
x
y
)
        
map
(
parse_resource
resources
)
)
    
return
entities
def
merge_two
(
comments
newer
older
)
:
    
diff
=
AddRemove
(
)
    
diff
.
set_left
(
newer
.
keys
(
)
)
    
diff
.
set_right
(
older
.
keys
(
)
)
    
def
get_entity
(
key
)
:
        
entity
=
newer
.
get
(
key
None
)
        
if
entity
is
not
None
:
            
return
entity
        
entity
=
older
.
get
(
key
)
        
if
isinstance
(
entity
cl
.
Comment
)
and
entity
in
comments
:
            
next_entity
=
newer
.
get
(
comments
[
entity
]
None
)
            
if
next_entity
is
not
None
and
next_entity
.
pre_comment
:
                
return
None
        
return
entity
    
contents
=
[
(
key
get_entity
(
key
)
)
for
_
key
in
diff
]
    
def
prune
(
acc
cur
)
:
        
_
entity
=
cur
        
if
entity
is
None
:
            
return
acc
        
if
len
(
acc
)
and
isinstance
(
entity
cl
.
Whitespace
)
:
            
_
prev_entity
=
acc
[
-
1
]
            
if
isinstance
(
prev_entity
cl
.
Whitespace
)
:
                
if
len
(
entity
.
all
)
>
len
(
prev_entity
.
all
)
:
                    
acc
[
-
1
]
=
(
entity
entity
)
                
return
acc
        
acc
.
append
(
cur
)
        
return
acc
    
pruned
=
six
.
moves
.
reduce
(
prune
contents
[
]
)
    
return
OrderedDict
(
pruned
)
def
serialize_legacy_resource
(
entities
)
:
    
return
"
"
.
join
(
(
entity
.
all
for
entity
in
entities
.
values
(
)
)
)
