import
pytest
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_click_in_display_none_frame
(
session
inline
)
:
    
frame_url
=
inline
(
        
"
"
"
        
<
button
>
click
to
hide
<
/
button
>
        
<
script
type
=
"
text
/
javascript
"
>
            
const
btn
=
document
.
querySelector
(
'
button
'
)
;
            
btn
.
addEventListener
(
'
click
'
ev
=
>
{
                
window
.
parent
.
postMessage
(
"
test
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
        
"
"
"
    
)
    
url
=
inline
(
        
f
"
"
"
        
<
div
id
=
"
content
"
>
            
<
iframe
src
=
'
{
frame_url
}
'
>
<
/
iframe
>
        
<
/
div
>
        
<
script
>
            
window
.
addEventListener
(
"
message
"
ev
=
>
{
{
                
document
.
querySelector
(
"
iframe
"
)
.
style
.
display
=
"
none
"
;
            
}
}
false
)
;
        
<
/
script
>
        
"
"
"
    
)
    
session
.
url
=
url
    
frame
=
session
.
find
.
css
(
"
iframe
"
all
=
False
)
    
session
.
switch_frame
(
frame
)
    
button
=
session
.
find
.
css
(
"
button
"
all
=
False
)
    
mouse_chain
=
session
.
actions
.
sequence
(
        
"
pointer
"
"
pointer_id
"
{
"
pointerType
"
:
"
mouse
"
}
    
)
    
mouse_chain
.
pointer_move
(
0
0
origin
=
button
)
.
pointer_down
(
)
.
pointer_up
(
)
.
pause
(
        
100
    
)
.
perform
(
)
