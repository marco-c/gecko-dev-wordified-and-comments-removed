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
STRIP_PNG
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
r
"
\
.
png
"
"
"
node
.
value
flags
=
re
.
IGNORECASE
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
2040939
-
Drop
.
png
from
QR
code
save
filename
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
        
source
        
source
        
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
qrcode
-
save
-
filename
-
base
"
)
                
value
=
STRIP_PNG
(
source
"
qrcode
-
save
-
filename
"
)
            
)
        
]
    
)
