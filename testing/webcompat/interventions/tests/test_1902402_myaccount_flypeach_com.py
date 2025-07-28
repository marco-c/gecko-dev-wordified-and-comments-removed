import
pytest
from
webdriver
.
error
import
UnexpectedAlertOpenException
URL
=
"
https
:
/
/
myaccount
.
flypeach
.
com
/
login
"
LOGIN_CSS
=
"
input
[
name
=
email
]
"
async
def
check_saw_message
(
client
)
:
    
await
client
.
make_preload_script
(
        
"
"
"
      
delete
navigator
.
__proto__
.
webdriver
;
      
new
MutationObserver
(
(
mutations
observer
)
=
>
{
        
const
search
=
document
.
evaluate
(
          
"
/
/
*
[
text
(
)
[
contains
(
.
'
Google
Chrome
'
)
]
]
"
          
document
          
null
          
4
        
)
;
        
const
found
=
search
.
iterateNext
(
)
;
        
if
(
found
)
{
          
const
box
=
found
.
getBoundingClientRect
(
)
;
          
if
(
box
.
width
|
|
box
.
height
)
{
            
alert
(
"
found
"
)
          
}
        
}
      
}
)
.
observe
(
document
.
documentElement
{
        
childList
:
true
        
subtree
:
true
      
}
)
;
      
"
"
"
    
)
    
try
:
        
await
client
.
navigate
(
URL
wait
=
"
none
"
)
        
assert
client
.
await_css
(
LOGIN_CSS
is_displayed
=
True
)
        
return
False
    
except
UnexpectedAlertOpenException
:
        
return
True
pytest
.
mark
.
asyncio
pytest
.
mark
.
with_interventions
async
def
test_enabled
(
client
)
:
    
assert
not
await
check_saw_message
(
client
)
pytest
.
mark
.
asyncio
pytest
.
mark
.
without_interventions
async
def
test_disabled
(
client
)
:
    
assert
await
check_saw_message
(
client
)
