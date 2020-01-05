import
json
RESPONSE
=
"
"
"
<
!
DOCTYPE
html
>
<
html
>
  
<
head
>
    
<
title
>
Clear
-
Site
-
Data
<
/
title
>
    
<
script
src
=
"
test_utils
.
js
"
>
<
/
script
>
  
<
/
head
>
  
<
body
>
    
<
script
>
      
/
*
*
       
*
A
map
between
a
datatype
name
and
whether
it
is
empty
.
       
*
property
Object
.
<
string
boolean
>
       
*
/
      
var
report
=
{
}
;
      
Promise
.
all
(
TestUtils
.
DATATYPES
.
map
(
function
(
datatype
)
{
        
return
datatype
.
isEmpty
(
)
.
then
(
function
(
isEmpty
)
{
          
report
[
datatype
.
name
]
=
isEmpty
;
        
}
)
;
      
}
)
)
.
then
(
function
(
)
{
        
window
.
top
.
postMessage
(
report
"
*
"
)
;
      
}
)
;
    
<
/
script
>
  
<
/
body
>
<
/
html
>
"
"
"
def
main
(
request
response
)
:
    
types
=
[
key
for
key
in
request
.
GET
.
keys
(
)
]
    
header
=
json
.
dumps
(
{
"
types
"
:
types
}
)
    
return
(
[
(
"
Clear
-
Site
-
Data
"
header
)
             
(
"
Content
-
Type
"
"
text
/
html
"
)
]
            
RESPONSE
)
