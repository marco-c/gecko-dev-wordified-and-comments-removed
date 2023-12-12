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
COPY
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
1868154
-
Convert
RFPHelper
strings
to
Fluent
part
{
index
}
.
"
"
"
    
source
=
"
browser
/
chrome
/
browser
/
browser
.
properties
"
    
target
=
"
toolkit
/
toolkit
/
global
/
resistFingerPrinting
.
ftl
"
    
ctx
.
add_transforms
(
        
target
        
target
        
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
privacy
-
spoof
-
english
"
)
                
value
=
COPY
(
source
"
privacy
.
spoof_english
"
)
            
)
        
]
    
)
