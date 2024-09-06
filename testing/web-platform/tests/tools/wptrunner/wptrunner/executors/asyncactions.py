webdriver
=
None
def
do_delayed_imports
(
)
:
    
global
webdriver
    
import
webdriver
class
BidiSessionSubscribeAction
:
    
name
=
"
bidi
.
session
.
subscribe
"
    
def
__init__
(
self
logger
protocol
)
:
        
do_delayed_imports
(
)
        
self
.
logger
=
logger
        
self
.
protocol
=
protocol
    
async
def
__call__
(
self
payload
)
:
        
events
=
payload
[
"
events
"
]
        
contexts
=
None
        
if
payload
[
"
contexts
"
]
is
not
None
:
            
contexts
=
[
]
            
for
context
in
payload
[
"
contexts
"
]
:
                
if
isinstance
(
context
str
)
:
                    
contexts
.
append
(
context
)
                
elif
isinstance
(
context
webdriver
.
bidi
.
protocol
.
BidiWindow
)
:
                    
contexts
.
append
(
context
.
browsing_context
)
                
else
:
                    
raise
ValueError
(
"
Unexpected
context
type
:
%
s
"
%
context
)
        
return
await
self
.
protocol
.
bidi_events
.
subscribe
(
events
contexts
)
async_actions
=
[
BidiSessionSubscribeAction
]
