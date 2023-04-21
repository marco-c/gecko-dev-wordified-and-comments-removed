import
fluent
.
syntax
.
ast
as
FTL
from
fluent
.
migrate
.
transforms
import
TransformPattern
class
REPLACE_LABEL
(
TransformPattern
)
:
    
def
visit_TextElement
(
self
node
)
:
        
node
.
value
=
node
.
value
.
replace
(
"
<
label
"
"
<
a
"
)
        
return
node
def
migrate
(
ctx
)
:
    
"
"
"
Bug
1820654
-
Use
html
:
a
in
manualUpdate
box
part
{
index
}
.
"
"
"
    
aboutDialog_ftl
=
"
browser
/
browser
/
aboutDialog
.
ftl
"
    
ctx
.
add_transforms
(
        
aboutDialog_ftl
        
aboutDialog_ftl
        
[
            
FTL
.
Message
(
                
id
=
FTL
.
Identifier
(
"
aboutdialog
-
update
-
manual
"
)
                
value
=
REPLACE_LABEL
(
aboutDialog_ftl
"
update
-
manual
"
)
            
)
        
]
    
)
