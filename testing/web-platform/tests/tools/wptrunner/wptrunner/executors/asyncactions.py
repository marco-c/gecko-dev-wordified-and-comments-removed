from
webdriver
.
bidi
.
protocol
import
BidiWindow
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
