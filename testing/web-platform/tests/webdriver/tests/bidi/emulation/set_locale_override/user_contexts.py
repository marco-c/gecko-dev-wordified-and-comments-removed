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
        
get_current_locale
        
default_locale
        
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
    
assert
await
get_current_locale
(
new_tab
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
        
user_contexts
=
[
user_context
]
        
locale
=
some_locale
)
    
assert
await
get_current_locale
(
context_in_user_context
)
=
=
some_locale
    
assert
await
get_current_locale
(
new_tab
)
=
=
default_locale
    
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
    
assert
await
get_current_locale
(
        
another_context_in_user_context
)
=
=
some_locale
async
def
test_set_to_default_user_context
(
        
bidi_session
        
new_tab
        
create_user_context
        
get_current_locale
        
default_locale
        
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
    
assert
await
get_current_locale
(
context_in_user_context
)
=
=
default_locale
    
assert
await
get_current_locale
(
new_tab
)
=
=
some_locale
    
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
    
assert
await
get_current_locale
(
context_in_default_context
)
=
=
some_locale
    
assert
await
get_current_locale
(
context_in_default_context
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
        
get_current_locale
        
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
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
some_locale
    
assert
await
get_current_locale
(
context_in_user_context_2
)
=
=
some_locale
async
def
test_set_to_user_context_and_then_to_context
(
        
bidi_session
        
create_user_context
        
get_current_locale
        
default_locale
        
some_locale
        
another_locale
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
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
another_locale
    
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
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
another_locale
    
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
    
assert
await
get_current_locale
(
context_in_user_context_2
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
    
assert
await
get_current_locale
(
context_in_user_context_1
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
        
user_contexts
=
[
user_context
]
        
locale
=
None
    
)
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
default_locale
async
def
test_set_to_context_and_then_to_user_context
(
    
bidi_session
    
create_user_context
    
get_current_locale
    
default_locale
    
some_locale
    
another_locale
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
    
assert
await
get_current_locale
(
context_in_user_context_1
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
        
user_contexts
=
[
user_context
]
locale
=
another_locale
    
)
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
some_locale
    
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
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
some_locale
    
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
    
assert
await
get_current_locale
(
context_in_user_context_2
)
=
=
another_locale
    
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
    
assert
await
get_current_locale
(
context_in_user_context_1
)
=
=
some_locale
    
assert
await
get_current_locale
(
context_in_user_context_2
)
=
=
default_locale
