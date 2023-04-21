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
label
data
-
l10n
-
name
=
"
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
1814261
-
Use
moz
-
support
-
link
in
the
mixed
-
content
section
of
the
identity
panel
part
{
index
}
.
"
"
"
    
browser_ftl
=
"
browser
/
browser
/
browser
.
ftl
"
    
ctx
.
add_transforms
(
        
browser_ftl
        
browser_ftl
        
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
identity
-
description
-
active
-
blocked2
"
)
                
value
=
STRIP_LEARNMORE
(
                    
browser_ftl
"
identity
-
description
-
active
-
blocked
"
                
)
            
)
            
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
identity
-
description
-
passive
-
loaded
-
insecure2
"
)
                
value
=
STRIP_LEARNMORE
(
                    
browser_ftl
"
identity
-
description
-
passive
-
loaded
-
insecure
"
                
)
            
)
            
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
identity
-
description
-
passive
-
loaded
-
mixed2
"
)
                
value
=
STRIP_LEARNMORE
(
                    
browser_ftl
"
identity
-
description
-
passive
-
loaded
-
mixed
"
                
)
            
)
        
]
    
)
