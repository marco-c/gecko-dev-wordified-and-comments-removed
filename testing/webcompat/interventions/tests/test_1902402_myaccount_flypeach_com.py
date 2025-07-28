import
pytest
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
visit_site
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
;
            
observer
.
disconnect
(
)
;
          
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
    
await
visit_site
(
client
)
    
client
.
await_css
(
LOGIN_CSS
is_displayed
=
True
timeout
=
20
)
    
assert
not
await
client
.
find_alert
(
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
    
await
visit_site
(
client
)
    
assert
await
client
.
await_alert
(
"
found
"
)
