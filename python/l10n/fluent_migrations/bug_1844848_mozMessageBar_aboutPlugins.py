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
STRIP_LEARNMORE
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
a
data
-
l10n
-
name
=
"
deprecation
-
link
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
1844848
-
Use
moz
-
message
-
bar
in
about
:
plugins
part
{
index
}
.
"
"
"
    
abouPlugins_ftl
=
"
toolkit
/
toolkit
/
about
/
aboutPlugins
.
ftl
"
    
ctx
.
add_transforms
(
        
abouPlugins_ftl
        
abouPlugins_ftl
        
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
deprecation
-
description2
"
)
                
attributes
=
[
                    
FTL
.
Attribute
(
                        
id
=
FTL
.
Identifier
(
"
message
"
)
                        
value
=
STRIP_LEARNMORE
(
                            
abouPlugins_ftl
                            
"
deprecation
-
description
"
                        
)
                    
)
                
]
            
)
        
]
    
)
