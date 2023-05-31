import
fluent
.
syntax
.
ast
as
FTL
from
.
errors
import
SkipTransform
from
.
util
import
get_message
get_transform
def
merge_resource
(
ctx
reference
current
transforms
in_changeset
)
:
    
"
"
"
Transform
legacy
translations
into
FTL
.
    
Use
the
reference
FTL
AST
as
a
template
.
For
each
en
-
US
string
in
the
    
reference
first
check
for
an
existing
translation
in
the
current
FTL
    
localization
and
use
it
if
it
'
s
present
;
then
if
the
string
has
    
a
transform
defined
in
the
migration
specification
and
if
it
'
s
in
the
    
currently
processed
changeset
evaluate
the
transform
.
    
"
"
"
    
def
merge_body
(
body
)
:
        
return
[
            
entry
            
for
entry
in
map
(
merge_entry
body
)
            
if
entry
is
not
None
        
]
    
def
merge_entry
(
entry
)
:
        
if
isinstance
(
entry
FTL
.
BaseComment
)
:
            
return
entry
        
if
isinstance
(
entry
FTL
.
Junk
)
:
            
return
None
        
ident
=
entry
.
id
.
name
        
existing
=
get_message
(
current
.
body
ident
)
        
if
existing
is
not
None
:
            
return
existing
        
transform
=
get_transform
(
transforms
ident
)
        
if
transform
is
not
None
and
in_changeset
(
ident
)
:
            
if
transform
.
comment
is
None
:
                
transform
.
comment
=
entry
.
comment
            
try
:
                
return
ctx
.
evaluate
(
transform
)
            
except
SkipTransform
:
                
return
None
    
body
=
merge_body
(
reference
.
body
)
    
return
FTL
.
Resource
(
body
)
