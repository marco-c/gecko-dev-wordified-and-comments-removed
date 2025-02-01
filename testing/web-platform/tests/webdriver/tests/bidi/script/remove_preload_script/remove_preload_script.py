import
pytest
import
webdriver
.
bidi
.
error
as
error
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
type_hint
"
[
"
tab
"
"
window
"
]
)
async
def
test_remove_preload_script
(
bidi_session
type_hint
)
:
    
script
=
await
bidi_session
.
script
.
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
foo
=
'
bar
'
;
}
"
    
)
    
new_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
type_hint
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
new_context
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
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script
)
    
new_tab_2
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
type_hint
)
    
result_2
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
new_tab_2
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
result_2
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
test_remove_preload_script_twice
(
bidi_session
)
:
    
script
=
await
bidi_session
.
script
.
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
foo
=
'
bar
'
;
}
"
    
)
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script
)
    
with
pytest
.
raises
(
error
.
NoSuchScriptException
)
:
        
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script
)
pytest
.
mark
.
asyncio
async
def
test_remove_one_of_preload_scripts
(
bidi_session
)
:
    
script_1
=
await
bidi_session
.
script
.
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
bar
=
'
foo
'
;
}
"
    
)
    
script_2
=
await
bidi_session
.
script
.
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
baz
=
'
bar
'
;
}
"
    
)
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script_1
)
    
new_tab
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
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
    
result_2
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
baz
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
result_2
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
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script_2
)
pytest
.
mark
.
asyncio
async
def
test_remove_script_set_up_for_one_context
(
    
bidi_session
add_preload_script
new_tab
test_page
test_page_cross_origin
)
:
    
script
=
await
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
baz
=
42
;
}
"
        
contexts
=
[
new_tab
[
"
context
"
]
]
    
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
new_tab
[
"
context
"
]
        
url
=
test_page
        
wait
=
"
complete
"
    
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
baz
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
number
"
"
value
"
:
42
}
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
new_tab
[
"
context
"
]
        
url
=
test_page_cross_origin
        
wait
=
"
complete
"
    
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
baz
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
test_remove_script_set_up_for_user_context
(
    
bidi_session
add_preload_script
new_tab
create_user_context
inline
)
:
    
user_context
=
await
create_user_context
(
)
    
script
=
await
add_preload_script
(
        
function_declaration
=
"
(
)
=
>
{
window
.
foo
=
'
bar
'
;
}
"
user_contexts
=
[
user_context
]
    
)
    
new_context_1
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
    
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
new_context_1
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
    
await
bidi_session
.
script
.
remove_preload_script
(
script
=
script
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
new_context_1
[
"
context
"
]
        
url
=
inline
(
"
<
div
>
test
<
/
div
>
"
)
        
wait
=
"
complete
"
    
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
    
new_context_2
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
    
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
new_context_2
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
    
await
bidi_session
.
browsing_context
.
close
(
context
=
new_context_1
[
"
context
"
]
)
    
await
bidi_session
.
browsing_context
.
close
(
context
=
new_context_2
[
"
context
"
]
)
