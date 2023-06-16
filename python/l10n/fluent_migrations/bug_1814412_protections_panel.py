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
STRIP_LEARNMORE_REPLACE_MOZILLA
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
Mozilla
"
"
{
-
vendor
-
short
-
name
}
"
)
        
link_start
=
node
.
value
.
find
(
'
<
label
data
-
l10n
-
name
=
"
learn
-
more
"
>
'
)
        
if
link_start
!
=
-
1
:
            
node
.
value
=
node
.
value
[
:
link_start
]
.
rstrip
(
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
1814412
-
Use
moz
-
support
-
link
in
protections
panel
part
{
index
}
.
"
"
"
    
protectionsPanel_ftl
=
"
browser
/
browser
/
protectionsPanel
.
ftl
"
    
ctx
.
add_transforms
(
        
protectionsPanel_ftl
        
protectionsPanel_ftl
        
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
protections
-
panel
-
content
-
blocking
-
breakage
-
report
-
view
-
description2
"
                
)
                
value
=
STRIP_LEARNMORE_REPLACE_MOZILLA
(
                    
protectionsPanel_ftl
                    
"
protections
-
panel
-
content
-
blocking
-
breakage
-
report
-
view
-
description
"
                
)
            
)
        
]
    
)
