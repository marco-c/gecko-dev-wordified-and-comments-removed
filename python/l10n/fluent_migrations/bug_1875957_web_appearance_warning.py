import
re
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
STRIP_LINK
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
re
.
sub
(
            
'
\
s
?
<
a
data
-
l10n
-
name
=
"
colors
-
link
"
>
.
+
?
<
/
a
>
\
s
?
'
            
"
"
            
node
.
value
        
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
1875957
-
Use
moz
-
message
-
bar
for
web
appearance
warning
part
{
index
}
"
"
"
    
preferences_ftl
=
"
browser
/
browser
/
preferences
/
preferences
.
ftl
"
    
ctx
.
add_transforms
(
        
preferences_ftl
        
preferences_ftl
        
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
preferences
-
web
-
appearance
-
override
-
warning2
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
STRIP_LINK
(
                            
preferences_ftl
                            
"
preferences
-
web
-
appearance
-
override
-
warning
"
                        
)
                    
)
                
]
            
)
        
]
    
)
