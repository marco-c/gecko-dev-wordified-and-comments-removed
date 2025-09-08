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
test_contexts
(
        
bidi_session
new_tab
top_context
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
default_screen_orientation
)
:
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
        
new_tab
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
async
def
test_multiple_contexts
(
        
bidi_session
new_tab
top_context
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
default_screen_orientation
)
:
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
contexts
=
[
top_context
[
"
context
"
]
new_tab
[
"
context
"
]
]
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
some_web_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
        
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
top_context
)
=
=
some_web_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
contexts
=
[
top_context
[
"
context
"
]
]
        
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
pytest
.
mark
.
parametrize
(
"
domain
"
[
"
"
"
alt
"
]
ids
=
[
"
same_origin
"
"
cross_origin
"
]
)
async
def
test_iframe
(
    
bidi_session
    
new_tab
    
get_screen_orientation
    
some_bidi_screen_orientation
    
some_web_screen_orientation
    
another_bidi_screen_orientation
    
another_web_screen_orientation
    
inline
    
domain
)
:
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
some_web_screen_orientation
    
iframe_url
=
inline
(
"
<
div
id
=
'
in
-
iframe
'
>
foo
<
/
div
>
"
domain
=
domain
)
    
page_url
=
inline
(
f
"
<
iframe
src
=
'
{
iframe_url
}
'
>
<
/
iframe
>
"
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
page_url
        
wait
=
"
complete
"
    
)
    
contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
root
=
new_tab
[
"
context
"
]
)
    
iframe
=
contexts
[
0
]
[
"
children
"
]
[
0
]
    
assert
(
        
await
get_screen_orientation
(
iframe
top_context
=
new_tab
)
        
=
=
some_web_screen_orientation
    
)
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
        
screen_orientation
=
another_bidi_screen_orientation
    
)
    
assert
(
        
await
get_screen_orientation
(
iframe
top_context
=
new_tab
)
        
=
=
another_web_screen_orientation
    
)
