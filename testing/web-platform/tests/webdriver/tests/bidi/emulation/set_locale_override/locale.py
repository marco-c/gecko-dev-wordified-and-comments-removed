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
top_context
        
get_current_locale
default_locale
some_locale
another_locale
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
some_locale
    
)
    
assert
await
get_current_locale
(
top_context
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
top_context
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
top_context
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
None
    
)
    
assert
await
get_current_locale
(
top_context
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
value
"
[
    
"
en
"
    
"
ast
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
    
"
de
-
DE
-
1996
"
    
"
sl
-
Roza
-
biske
"
    
"
ca
-
ES
-
valencia
"
    
"
sl
-
1994
"
    
"
th
-
TH
-
u
-
nu
-
thai
"
    
"
en
-
US
-
u
-
ca
-
gregory
"
    
"
yue
"
    
"
apc
"
    
"
gsw
"
]
)
async
def
test_locale_values
(
bidi_session
top_context
get_current_locale
        
default_locale
value
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
value
    
)
    
assert
await
get_current_locale
(
top_context
)
=
=
value
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
zh
-
Latn
-
CN
-
variant1
-
a
-
extend1
-
u
-
co
-
pinyin
-
x
-
private
"
     
"
zh
-
Latn
-
CN
-
variant1
"
)
    
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
    
(
"
es
-
419
"
"
es
-
MX
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
