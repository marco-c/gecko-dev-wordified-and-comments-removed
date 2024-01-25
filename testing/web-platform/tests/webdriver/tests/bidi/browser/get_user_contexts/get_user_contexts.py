import
pytest
from
.
.
import
get_user_context_ids
pytest
.
mark
.
asyncio
async
def
test_default
(
bidi_session
)
:
    
user_context_ids
=
await
get_user_context_ids
(
bidi_session
)
    
assert
len
(
user_context_ids
)
>
0
    
assert
"
default
"
in
user_context_ids
pytest
.
mark
.
asyncio
async
def
test_create_remove_contexts
(
bidi_session
create_user_context
)
:
    
user_context_1
=
await
create_user_context
(
)
    
user_context_2
=
await
create_user_context
(
)
    
user_context_ids
=
await
get_user_context_ids
(
bidi_session
)
    
assert
len
(
user_context_ids
)
>
=
3
    
assert
user_context_1
in
user_context_ids
    
assert
user_context_2
in
user_context_ids
    
assert
"
default
"
in
user_context_ids
    
await
bidi_session
.
browser
.
remove_user_context
(
user_context
=
user_context_1
)
    
user_context_ids
=
await
get_user_context_ids
(
bidi_session
)
    
assert
user_context_1
not
in
user_context_ids
    
assert
user_context_2
in
user_context_ids
    
assert
"
default
"
in
user_context_ids
    
await
bidi_session
.
browser
.
remove_user_context
(
user_context
=
user_context_2
)
    
user_context_ids
=
await
get_user_context_ids
(
bidi_session
)
    
assert
user_context_1
not
in
user_context_ids
    
assert
user_context_2
not
in
user_context_ids
    
assert
"
default
"
in
user_context_ids
