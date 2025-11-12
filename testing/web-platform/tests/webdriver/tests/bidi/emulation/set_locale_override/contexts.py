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
    
assert_locale_against_default
    
assert_locale_against_value
    
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
]
locale
=
some_locale
    
)
    
await
assert_locale_against_value
(
some_locale
new_tab
)
    
await
assert_locale_against_default
(
new_context
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
]
locale
=
None
    
)
    
await
assert_locale_against_default
(
new_tab
)
    
await
assert_locale_against_default
(
new_context
)
async
def
test_multiple_contexts
(
    
bidi_session
    
new_tab
    
assert_locale_against_default
    
assert_locale_against_value
    
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
    
await
assert_locale_against_value
(
some_locale
new_tab
)
    
await
assert_locale_against_value
(
some_locale
new_context
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
None
    
)
    
await
assert_locale_against_default
(
new_tab
)
    
await
assert_locale_against_default
(
new_context
)
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
    
inline
    
another_locale
    
assert_locale_against_value
    
some_locale
    
domain
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
    
await
assert_locale_against_value
(
some_locale
new_tab
)
    
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
    
await
assert_locale_against_value
(
some_locale
iframe
)
    
sandbox_name
=
"
test
"
    
await
assert_locale_against_value
(
some_locale
iframe
sandbox_name
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
]
locale
=
another_locale
    
)
    
await
assert_locale_against_value
(
another_locale
iframe
)
    
await
assert_locale_against_value
(
another_locale
iframe
sandbox_name
)
async
def
test_locale_override_applies_to_new_sandbox
(
    
bidi_session
new_tab
some_locale
assert_locale_against_value
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
    
await
assert_locale_against_value
(
some_locale
new_tab
"
test
"
)
async
def
test_locale_override_applies_to_existing_sandbox
(
    
bidi_session
    
new_tab
    
another_locale
    
assert_locale_against_default
    
assert_locale_against_value
)
:
    
sandbox_name
=
"
test
"
    
await
assert_locale_against_default
(
new_tab
sandbox_name
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
]
locale
=
another_locale
    
)
    
await
assert_locale_against_value
(
another_locale
new_tab
sandbox_name
)
