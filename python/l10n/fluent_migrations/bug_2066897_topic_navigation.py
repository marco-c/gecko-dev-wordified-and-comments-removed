from
fluent
.
migrate
.
helpers
import
transforms_from
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
2066897
-
Implement
topic
navigation
strip
V1
part
{
index
}
.
"
"
"
    
newtab
=
"
browser
/
browser
/
newtab
/
newtab
.
ftl
"
    
ctx
.
add_transforms
(
        
newtab
        
newtab
        
transforms_from
(
            
"
"
"
newtab
-
topic
-
navigation
-
label
=
    
.
aria
-
label
=
{
COPY_PATTERN
(
from_path
"
newtab
-
section
-
mangage
-
topics
-
title
"
)
}
"
"
"
            
from_path
=
newtab
        
)
    
)
