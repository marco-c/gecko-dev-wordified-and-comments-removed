import
pytest
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
ScriptEvaluateResultException
from
.
.
.
import
any_int
any_string
recursive_compare
from
.
.
import
any_stack_trace
pytest
.
mark
.
asyncio
async
def
test_sandbox
(
bidi_session
new_tab
)
:
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
=
1
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
    
)
    
result_in_sandbox
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox
=
=
{
"
type
"
:
"
undefined
"
}
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
bar
=
1
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox
"
)
        
await_promise
=
True
    
)
    
result_in_sandbox
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
bar
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox
=
=
{
"
type
"
:
"
number
"
"
value
"
:
1
}
    
result
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
bar
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
    
)
    
assert
result
=
=
{
"
type
"
:
"
undefined
"
}
pytest
.
mark
.
asyncio
async
def
test_sandbox_with_empty_name
(
bidi_session
new_tab
)
:
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
=
'
bar
'
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
"
)
        
await_promise
=
True
    
)
    
result
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
"
)
        
await_promise
=
True
    
)
    
assert
result
=
=
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
    
result
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
    
)
    
assert
result
=
=
{
"
type
"
:
"
undefined
"
}
pytest
.
mark
.
asyncio
async
def
test_switch_sandboxes
(
bidi_session
new_tab
)
:
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
=
1
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_1
"
)
        
await_promise
=
True
    
)
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
=
2
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_2
"
)
        
await_promise
=
True
    
)
    
result_in_sandbox_1
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_1
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox_1
=
=
{
"
type
"
:
"
number
"
"
value
"
:
1
}
    
result_in_sandbox_2
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
window
.
foo
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_2
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox_2
=
=
{
"
type
"
:
"
number
"
"
value
"
:
2
}
pytest
.
mark
.
asyncio
async
def
test_sandbox_with_side_effects
(
bidi_session
new_tab
)
:
    
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
document
.
querySelector
(
'
body
'
)
.
textContent
=
'
foo
'
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_1
"
)
        
await_promise
=
True
    
)
    
expected_value
=
{
"
type
"
:
"
string
"
"
value
"
:
"
foo
"
}
    
result_in_sandbox_1
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
document
.
querySelector
(
'
body
'
)
.
textContent
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_1
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox_1
=
=
expected_value
    
result_in_sandbox_2
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
"
document
.
querySelector
(
'
body
'
)
.
textContent
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox_2
"
)
        
await_promise
=
True
    
)
    
assert
result_in_sandbox_2
=
=
expected_value
pytest
.
mark
.
asyncio
pytest
.
mark
.
parametrize
(
"
await_promise
"
[
True
False
]
)
async
def
test_exception_details
(
bidi_session
new_tab
await_promise
)
:
    
if
await_promise
:
        
expression
=
"
Promise
.
reject
(
1
)
"
    
else
:
        
expression
=
"
throw
1
"
    
with
pytest
.
raises
(
ScriptEvaluateResultException
)
as
exception
:
        
await
bidi_session
.
script
.
evaluate
(
            
expression
=
expression
            
target
=
ContextTarget
(
new_tab
[
"
context
"
]
"
sandbox
"
)
            
await_promise
=
await_promise
        
)
    
recursive_compare
(
        
{
            
"
realm
"
:
any_string
            
"
exceptionDetails
"
:
{
                
"
columnNumber
"
:
any_int
                
"
exception
"
:
{
"
type
"
:
"
number
"
"
value
"
:
1
}
                
"
lineNumber
"
:
any_int
                
"
stackTrace
"
:
any_stack_trace
                
"
text
"
:
any_string
            
}
        
}
        
exception
.
value
.
result
    
)
