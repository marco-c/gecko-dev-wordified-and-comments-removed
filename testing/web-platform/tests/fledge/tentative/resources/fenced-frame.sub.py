def
main
(
request
response
)
:
    
response
.
status
=
(
200
b
"
OK
"
)
    
response
.
headers
.
set
(
b
"
Content
-
Type
"
b
"
text
/
html
"
)
    
response
.
headers
.
set
(
b
"
Supports
-
Loading
-
Mode
"
b
"
fenced
-
frame
"
)
    
return
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
!
-
-
-
Allow
injected
scripts
to
use
functions
in
fledge
-
util
.
js
-
-
-
>
        
<
base
href
=
"
.
.
"
>
        
<
script
src
=
"
/
resources
/
testharness
.
js
"
>
<
/
script
>
        
<
script
src
=
"
/
common
/
utils
.
js
"
>
<
/
script
>
        
<
script
src
=
"
resources
/
fledge
-
util
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
        
{
{
GET
[
script
]
}
}
        
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
