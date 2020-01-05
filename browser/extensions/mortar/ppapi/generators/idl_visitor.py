"
"
"
Visitor
Object
for
traversing
AST
"
"
"
class
IDLVisitor
(
object
)
:
  
def
__init__
(
self
)
:
    
pass
  
def
VisitFilter
(
self
node
data
)
:
    
return
True
  
def
Visit
(
self
node
data
)
:
    
if
not
self
.
VisitFilter
(
node
data
)
:
return
None
    
childdata
=
[
]
    
newdata
=
self
.
Arrive
(
node
data
)
    
for
child
in
node
.
GetChildren
(
)
:
      
ret
=
self
.
Visit
(
child
newdata
)
      
if
ret
is
not
None
:
        
childdata
.
append
(
ret
)
    
return
self
.
Depart
(
node
newdata
childdata
)
  
def
Arrive
(
self
node
data
)
:
    
__pychecker__
=
'
unusednames
=
node
'
    
return
data
  
def
Depart
(
self
node
data
childdata
)
:
    
__pychecker__
=
'
unusednames
=
node
childdata
'
    
return
data
