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
        
is_scripting_enabled
)
:
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
        
enabled
=
False
    
)
    
assert
await
is_scripting_enabled
(
new_tab
)
is
False
    
assert
await
is_scripting_enabled
(
top_context
)
is
True
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
        
enabled
=
None
)
    
assert
await
is_scripting_enabled
(
new_tab
)
is
True
    
assert
await
is_scripting_enabled
(
top_context
)
is
True
async
def
test_multiple_contexts
(
bidi_session
new_tab
is_scripting_enabled
)
:
    
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
"
tab
"
)
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
new_context
[
"
context
"
]
]
        
enabled
=
False
    
)
    
assert
await
is_scripting_enabled
(
new_tab
)
is
False
    
assert
await
is_scripting_enabled
(
new_context
)
is
False
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
new_context
[
"
context
"
]
]
        
enabled
=
None
)
    
assert
await
is_scripting_enabled
(
new_tab
)
is
True
    
assert
await
is_scripting_enabled
(
new_context
)
is
True
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
        
is_scripting_enabled
        
domain
        
inline
)
:
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
enabled
=
False
    
)
    
assert
await
is_scripting_enabled
(
new_tab
)
is
False
    
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
await
is_scripting_enabled
(
iframe
)
is
False
    
await
bidi_session
.
emulation
.
set_scripting_enabled
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
enabled
=
None
    
)
    
assert
await
is_scripting_enabled
(
iframe
)
is
True
