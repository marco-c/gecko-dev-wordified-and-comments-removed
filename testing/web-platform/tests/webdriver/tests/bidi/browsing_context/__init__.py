from
typing
import
Any
Mapping
from
webdriver
.
bidi
.
modules
.
script
import
ContextTarget
from
.
.
import
(
    
any_int
    
any_string
    
any_string_or_null
    
recursive_compare
)
def
assert_browsing_context
(
    
info
    
context
    
children
=
None
    
parent_expected
=
True
    
parent
=
None
    
url
=
None
    
user_context
=
"
default
"
    
original_opener
=
None
)
:
    
assert
"
children
"
in
info
    
if
children
is
not
None
:
        
assert
isinstance
(
info
[
"
children
"
]
list
)
        
assert
len
(
info
[
"
children
"
]
)
=
=
children
    
else
:
        
assert
info
[
"
children
"
]
is
None
    
assert
"
context
"
in
info
    
assert
isinstance
(
info
[
"
context
"
]
str
)
    
if
context
is
not
None
:
        
assert
info
[
"
context
"
]
=
=
context
    
if
parent_expected
:
        
if
parent
is
None
:
            
assert
info
[
"
parent
"
]
is
None
        
else
:
            
assert
"
parent
"
in
info
            
assert
isinstance
(
info
[
"
parent
"
]
str
)
            
assert
info
[
"
parent
"
]
=
=
parent
    
else
:
        
assert
"
parent
"
not
in
info
        
assert
parent
is
None
    
assert
"
url
"
in
info
    
assert
isinstance
(
info
[
"
url
"
]
str
)
    
assert
info
[
"
url
"
]
=
=
url
    
assert
info
[
"
userContext
"
]
=
=
user_context
    
assert
info
[
"
originalOpener
"
]
=
=
original_opener
async
def
assert_document_status
(
bidi_session
context
visible
focused
)
:
    
state
=
"
visible
"
if
visible
else
"
hidden
"
    
assert
await
get_visibility_state
(
bidi_session
context
)
=
=
state
    
assert
await
get_document_focus
(
bidi_session
context
)
is
focused
def
assert_navigation_info
(
event
expected_navigation_info
)
:
    
recursive_compare
(
        
{
            
"
context
"
:
any_string
            
"
navigation
"
:
any_string_or_null
            
"
timestamp
"
:
any_int
            
"
url
"
:
any_string
        
}
        
event
    
)
    
if
"
context
"
in
expected_navigation_info
:
        
assert
event
[
"
context
"
]
=
=
expected_navigation_info
[
"
context
"
]
    
if
"
navigation
"
in
expected_navigation_info
:
        
assert
event
[
"
navigation
"
]
=
=
expected_navigation_info
[
"
navigation
"
]
    
if
"
timestamp
"
in
expected_navigation_info
:
        
expected_navigation_info
[
"
timestamp
"
]
(
event
[
"
timestamp
"
]
)
    
if
"
url
"
in
expected_navigation_info
:
        
assert
event
[
"
url
"
]
=
=
expected_navigation_info
[
"
url
"
]
async
def
get_document_focus
(
bidi_session
context
:
Mapping
[
str
Any
]
)
-
>
str
:
    
result
=
await
bidi_session
.
script
.
call_function
(
        
function_declaration
=
"
"
"
(
)
=
>
{
        
return
document
.
hasFocus
(
)
;
    
}
"
"
"
        
target
=
ContextTarget
(
context
[
"
context
"
]
)
        
await_promise
=
False
)
    
return
result
[
"
value
"
]
async
def
get_visibility_state
(
bidi_session
context
:
Mapping
[
str
Any
]
)
-
>
str
:
    
result
=
await
bidi_session
.
script
.
call_function
(
        
function_declaration
=
"
"
"
(
)
=
>
{
        
return
document
.
visibilityState
;
    
}
"
"
"
        
target
=
ContextTarget
(
context
[
"
context
"
]
)
        
await_promise
=
False
)
    
return
result
[
"
value
"
]
