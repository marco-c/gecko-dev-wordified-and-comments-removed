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
test_locale_set_override_and_reset
(
    
bidi_session
    
new_tab
    
some_locale
    
another_locale
    
assert_locale_against_default
    
assert_locale_against_value
)
:
    
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
pytest
.
mark
.
parametrize
(
    
"
value
"
    
[
        
"
en
"
        
"
en
-
US
"
        
"
sr
-
Latn
"
        
"
zh
-
Hans
-
CN
"
    
]
)
async
def
test_locale_values
(
    
bidi_session
    
new_tab
    
assert_locale_against_default
    
assert_locale_against_value
    
value
)
:
    
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
value
    
)
    
await
assert_locale_against_value
(
value
new_tab
)
pytest
.
mark
.
parametrize
(
    
"
locale
expected_locale
"
    
[
        
(
"
de
-
DE
-
u
-
co
-
phonebk
"
"
de
-
DE
"
)
        
(
"
fr
-
ca
"
"
fr
-
CA
"
)
        
(
"
FR
-
CA
"
"
fr
-
CA
"
)
        
(
"
fR
-
cA
"
"
fr
-
CA
"
)
        
(
"
en
-
t
-
zh
"
"
en
"
)
    
]
)
async
def
test_locale_values_normalized_by_intl
(
    
bidi_session
    
top_context
    
get_current_locale
    
default_locale
    
locale
    
expected_locale
)
:
    
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
top_context
[
"
context
"
]
]
locale
=
locale
    
)
    
assert
await
get_current_locale
(
top_context
)
=
=
expected_locale
