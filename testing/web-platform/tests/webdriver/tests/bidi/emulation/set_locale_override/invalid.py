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
undefined
import
UNDEFINED
pytestmark
=
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
value
"
[
False
42
"
foo
"
{
}
]
)
async
def
test_params_contexts_invalid_type
(
bidi_session
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
contexts
=
value
        
)
async
def
test_params_contexts_empty_list
(
bidi_session
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
contexts
=
[
]
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
None
False
42
[
]
{
}
]
)
async
def
test_params_contexts_context_invalid_type
(
bidi_session
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
contexts
=
[
value
]
)
async
def
test_params_contexts_entry_invalid_value
(
bidi_session
)
:
    
with
pytest
.
raises
(
error
.
NoSuchFrameException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
contexts
=
[
"
_invalid_
"
]
        
)
async
def
test_params_contexts_iframe
(
bidi_session
new_tab
get_test_page
)
:
    
url
=
get_test_page
(
as_frame
=
True
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
url
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
    
assert
len
(
contexts
)
=
=
1
    
frames
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
    
assert
len
(
frames
)
=
=
1
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
contexts
=
[
frames
[
0
]
[
"
context
"
]
]
        
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
True
"
foo
"
42
{
}
]
)
async
def
test_params_user_contexts_invalid_type
(
bidi_session
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
user_contexts
=
value
        
)
async
def
test_params_user_contexts_empty_list
(
bidi_session
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
user_contexts
=
[
]
        
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
None
False
42
{
}
[
]
]
)
async
def
test_params_user_contexts_entry_invalid_type
(
bidi_session
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
user_contexts
=
[
value
]
        
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
"
"
somestring
"
]
)
async
def
test_params_user_contexts_entry_invalid_value
(
bidi_session
value
)
:
    
with
pytest
.
raises
(
error
.
NoSuchUserContextException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
None
            
user_contexts
=
[
value
]
        
)
async
def
test_params_locale_missing
(
bidi_session
top_context
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
UNDEFINED
            
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
False
42
{
}
[
]
]
)
async
def
test_params_locale_invalid_type
(
bidi_session
top_context
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
value
            
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
"
    
"
a
"
    
"
abcd
"
    
"
12
"
    
"
en
"
    
"
en_US
"
    
"
en
-
U
"
    
"
en
-
USAXASDASD
"
    
"
en
-
U1
"
    
"
en
-
US
"
    
"
en
-
Lat
"
    
"
en
-
Somelongsubtag
"
    
"
en
-
La1n
"
    
"
en
-
Lat
"
    
"
en
-
US
-
var
"
    
"
en
-
US
-
variant
"
    
"
en
-
u
-
"
    
"
de
-
t
-
"
    
"
x
-
"
    
"
x
-
another
-
private
-
tag
"
    
"
en
-
x
-
private_use
"
    
"
en
-
-
US
"
    
"
-
en
-
US
"
    
"
en
-
US
-
"
    
"
-
"
    
"
en
-
US
-
"
    
"
i
-
notarealtag
"
    
"
en
-
01
"
    
"
en
-
0A1
"
    
"
123
"
    
"
Latn
"
    
"
Latn
-
en
"
    
"
en
-
-
US
"
    
"
en
-
US
-
!
"
    
"
en
-
Latn
-
Cyrl
-
US
"
]
)
async
def
test_params_locale_invalid_value
(
bidi_session
top_context
value
)
:
    
with
pytest
.
raises
(
error
.
InvalidArgumentException
)
:
        
await
bidi_session
.
emulation
.
set_locale_override
(
            
locale
=
value
            
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
        
)
