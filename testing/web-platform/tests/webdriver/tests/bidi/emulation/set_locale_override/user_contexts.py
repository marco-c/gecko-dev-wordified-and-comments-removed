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
test_user_contexts
(
    
bidi_session
    
create_user_context
    
new_tab
    
assert_locale_against_default
    
assert_locale_against_value
    
some_locale
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context
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
    
await
assert_locale_against_default
(
new_tab
)
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
user_context
]
locale
=
some_locale
    
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context
)
    
await
assert_locale_against_default
(
new_tab
)
    
another_context_in_user_context
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
    
await
assert_locale_against_value
(
some_locale
another_context_in_user_context
)
async
def
test_set_to_default_user_context
(
    
bidi_session
    
new_tab
    
create_user_context
    
assert_locale_against_default
    
assert_locale_against_value
    
some_locale
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context
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
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
"
default
"
]
        
locale
=
some_locale
    
)
    
await
assert_locale_against_default
(
context_in_user_context
)
    
await
assert_locale_against_value
(
some_locale
new_tab
)
    
context_in_default_context
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
assert_locale_against_value
(
some_locale
context_in_default_context
)
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
"
default
"
]
locale
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
    
bidi_session
    
create_user_context
    
assert_locale_against_value
    
some_locale
)
:
    
user_context_1
=
await
create_user_context
(
)
    
context_in_user_context_1
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
user_context_1
type_hint
=
"
tab
"
    
)
    
user_context_2
=
await
create_user_context
(
)
    
context_in_user_context_2
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
user_context_2
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
        
user_contexts
=
[
user_context_1
user_context_2
]
locale
=
some_locale
    
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_1
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_2
)
async
def
test_set_to_user_context_and_then_to_context
(
    
bidi_session
    
create_user_context
    
another_locale
    
assert_locale_against_default
    
assert_locale_against_value
    
some_locale
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context_1
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
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
user_context
]
locale
=
some_locale
    
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
context_in_user_context_1
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
context_in_user_context_1
)
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context_1
[
"
context
"
]
wait
=
"
complete
"
    
)
    
await
assert_locale_against_value
(
another_locale
context_in_user_context_1
)
    
context_in_user_context_2
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
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_2
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
context_in_user_context_1
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
assert_locale_against_value
(
some_locale
context_in_user_context_1
)
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
user_context
]
        
locale
=
None
    
)
    
await
assert_locale_against_default
(
context_in_user_context_1
)
async
def
test_set_to_context_and_then_to_user_context
(
    
bidi_session
    
create_user_context
    
another_locale
    
assert_locale_against_default
    
assert_locale_against_value
    
some_locale
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context_1
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
context_in_user_context_1
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
context_in_user_context_1
)
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
user_context
]
locale
=
another_locale
    
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_1
)
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context_1
[
"
context
"
]
wait
=
"
complete
"
    
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_1
)
    
context_in_user_context_2
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
    
await
assert_locale_against_value
(
another_locale
context_in_user_context_2
)
    
await
bidi_session
.
emulation
.
set_locale_override
(
        
user_contexts
=
[
user_context
]
        
locale
=
None
    
)
    
await
assert_locale_against_value
(
some_locale
context_in_user_context_1
)
    
await
assert_locale_against_default
(
context_in_user_context_2
)
