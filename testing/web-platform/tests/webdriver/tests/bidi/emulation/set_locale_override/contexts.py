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
get_current_locale
        
default_locale
some_locale
)
:
    
await
bidi_session
.
emulation
.
set_locale_override
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
        
locale
=
some_locale
    
)
    
assert
await
get_current_locale
(
new_tab
)
=
=
some_locale
    
assert
await
get_current_locale
(
top_context
)
=
=
default_locale
    
await
bidi_session
.
emulation
.
set_locale_override
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
        
locale
=
None
)
    
assert
await
get_current_locale
(
new_tab
)
=
=
default_locale
    
assert
await
get_current_locale
(
top_context
)
=
=
default_locale
async
def
test_multiple_contexts
(
bidi_session
new_tab
get_current_locale
        
default_locale
some_locale
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
set_locale_override
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
        
locale
=
some_locale
    
)
    
assert
await
get_current_locale
(
new_tab
)
=
=
some_locale
    
assert
await
get_current_locale
(
new_context
)
=
=
some_locale
    
await
bidi_session
.
emulation
.
set_locale_override
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
        
locale
=
None
)
    
assert
await
get_current_locale
(
new_tab
)
=
=
default_locale
    
assert
await
get_current_locale
(
new_context
)
=
=
default_locale
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
    
get_current_locale
    
some_locale
    
domain
    
inline
    
another_locale
)
:
    
await
bidi_session
.
emulation
.
set_locale_override
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
locale
=
some_locale
    
)
    
assert
await
get_current_locale
(
new_tab
)
=
=
some_locale
    
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
get_current_locale
(
iframe
)
=
=
some_locale
    
await
bidi_session
.
emulation
.
set_locale_override
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
locale
=
another_locale
    
)
    
assert
await
get_current_locale
(
iframe
)
=
=
another_locale
