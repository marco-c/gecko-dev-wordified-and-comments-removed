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
learnmore
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
class
EXTRACT_LEARNMORE
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
        
text_start
=
node
.
value
.
find
(
"
>
"
)
+
1
        
text_end
=
node
.
value
.
find
(
"
<
/
a
>
"
)
        
if
text_start
!
=
-
1
and
text_end
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
text_start
:
text_end
]
.
strip
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
1825792
-
Use
moz
-
support
-
link
in
the
addon
abuse
report
dialog
part
{
index
}
.
"
"
"
    
abuse_reports
=
"
toolkit
/
toolkit
/
about
/
abuseReports
.
ftl
"
    
ctx
.
add_transforms
(
        
abuse_reports
        
abuse_reports
        
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
abuse
-
report
-
learnmore
-
intro
"
)
                
value
=
STRIP_LEARNMORE
(
                    
abuse_reports
                    
"
abuse
-
report
-
learnmore
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
abuse
-
report
-
learnmore
-
link
"
)
                
value
=
EXTRACT_LEARNMORE
(
                    
abuse_reports
                    
"
abuse
-
report
-
learnmore
"
                
)
            
)
        
]
    
)
