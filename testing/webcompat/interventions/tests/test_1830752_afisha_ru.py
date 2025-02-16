import
asyncio
import
pytest
from
webdriver
.
error
import
(
    
ElementClickInterceptedException
    
NoSuchElementException
    
StaleElementReferenceException
)
URL
=
"
https
:
/
/
www
.
afisha
.
ru
/
msk
/
theatre
/
"
POPUP_CLOSE_CSS
=
"
[
data
-
popmechanic
-
close
]
"
COOKIES_CSS
=
"
button
.
Txfw7
"
OPT_CSS
=
"
button
[
aria
-
label
=
]
"
SLIDER_CSS
=
"
input
[
type
=
'
range
'
]
[
data
-
index
=
'
0
'
]
"
async
def
slider_is_clickable
(
client
)
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
    
popups
=
[
client
.
css
(
COOKIES_CSS
)
client
.
css
(
POPUP_CLOSE_CSS
)
]
    
for
i
in
range
(
3
)
:
        
try
:
            
try
:
                
for
j
in
range
(
10
)
:
                    
client
.
click
(
                        
client
.
await_css
(
OPT_CSS
is_displayed
=
True
)
popups
=
popups
                    
)
                    
await
asyncio
.
sleep
(
0
.
2
)
                    
if
client
.
find_css
(
SLIDER_CSS
is_displayed
=
True
)
:
                        
break
            
except
NoSuchElementException
:
                
pytest
.
xfail
(
                    
"
Site
may
have
shown
a
captcha
;
please
run
this
test
again
"
                
)
                
return
            
except
StaleElementReferenceException
:
                
pass
            
slider
=
client
.
await_css
(
SLIDER_CSS
is_displayed
=
True
timeout
=
2
)
            
break
        
except
NoSuchElementException
:
            
continue
    
client
.
scroll_into_view
(
slider
)
    
try
:
        
client
.
click
(
slider
popups
=
popups
)
        
return
True
    
except
(
ElementClickInterceptedException
StaleElementReferenceException
)
:
        
return
False
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
await
slider_is_clickable
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
not
await
slider_is_clickable
(
client
)
