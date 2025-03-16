import
pytest
from
.
.
.
import
create_console_api_message
recursive_compare
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_subscribe_one_user_context
(
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
default_context
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
        
user_context
=
"
default
"
    
)
    
other_context
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
        
user_context
=
user_context
    
)
    
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
await
create_console_api_message
(
bidi_session
default_context
"
text1
"
)
        
await
create_console_api_message
(
bidi_session
other_context
"
text2
"
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
"
text2
"
            
}
            
events
[
0
]
[
1
]
        
)
async
def
test_subscribe_default_user_context
(
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
default_context
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
        
user_context
=
"
default
"
    
)
    
other_context
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
        
user_context
=
user_context
    
)
    
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
"
default
"
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
await
create_console_api_message
(
bidi_session
default_context
"
text1
"
)
        
await
create_console_api_message
(
bidi_session
other_context
"
text2
"
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
"
text1
"
            
}
            
events
[
0
]
[
1
]
        
)
async
def
test_subscribe_multiple_user_contexts
(
bidi_session
subscribe_events
wait_for_events
create_user_context
)
:
    
user_context
=
await
create_user_context
(
)
    
default_context
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
        
user_context
=
"
default
"
    
)
    
other_context
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
        
user_context
=
user_context
    
)
    
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
"
default
"
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
await
create_console_api_message
(
bidi_session
default_context
"
text1
"
)
        
await
create_console_api_message
(
bidi_session
other_context
"
text2
"
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
2
)
        
assert
len
(
events
)
=
=
2
async
def
test_buffered_event
(
    
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
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
user_context
=
user_context
    
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
await
create_console_api_message
(
bidi_session
new_context
"
text1
"
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
0
)
        
assert
len
(
events
)
=
=
0
        
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
"
text1
"
            
}
            
events
[
0
]
[
1
]
        
)
async
def
test_subscribe_to_user_context_and_then_globally
(
    
bidi_session
subscribe_events
create_user_context
new_tab
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
new_context_in_user_context
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
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
event_expected_text
=
await
create_console_api_message
(
            
bidi_session
new_tab
"
text1
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
0
)
        
assert
len
(
events
)
=
=
0
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text2
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
        
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
2
)
        
assert
len
(
events
)
=
=
2
        
recursive_compare
(
            
{
                
"
text
"
:
event_expected_text
            
}
            
events
[
1
]
[
1
]
        
)
        
expected_text
=
await
create_console_api_message
(
bidi_session
new_tab
"
text3
"
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
3
)
        
assert
len
(
events
)
=
=
3
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
2
]
[
1
]
        
)
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text4
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
4
)
        
assert
len
(
events
)
=
=
4
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
3
]
[
1
]
        
)
async
def
test_subscribe_to_user_context_and_then_to_browsing_context
(
    
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
new_context_in_user_context
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
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
    
await
subscribe_events
(
        
events
=
[
"
log
.
entryAdded
"
]
contexts
=
[
new_context_in_user_context
[
"
context
"
]
]
    
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text2
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
    
new_context_in_default_user_context
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
subscribe_events
(
        
events
=
[
"
log
.
entryAdded
"
]
        
contexts
=
[
new_context_in_default_user_context
[
"
context
"
]
]
    
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_default_user_context
"
text3
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
async
def
test_subscribe_globally_and_then_to_user_context
(
    
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
new_context_in_user_context
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
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
    
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text2
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
async
def
test_subscribe_to_browsing_context_and_then_to_user_context
(
    
bidi_session
subscribe_events
create_user_context
wait_for_events
)
:
    
user_context
=
await
create_user_context
(
)
    
new_context_in_user_context
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
subscribe_events
(
        
events
=
[
"
log
.
entryAdded
"
]
contexts
=
[
new_context_in_user_context
[
"
context
"
]
]
    
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
    
await
subscribe_events
(
events
=
[
"
log
.
entryAdded
"
]
user_contexts
=
[
user_context
]
)
    
with
wait_for_events
(
[
"
log
.
entryAdded
"
]
)
as
waiter
:
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context
"
text2
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
1
)
        
assert
len
(
events
)
=
=
1
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
0
]
[
1
]
        
)
        
new_context_in_user_context_2
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
        
expected_text
=
await
create_console_api_message
(
            
bidi_session
new_context_in_user_context_2
"
text3
"
        
)
        
events
=
await
waiter
.
get_events
(
lambda
events
:
len
(
events
)
>
=
2
)
        
assert
len
(
events
)
=
=
2
        
recursive_compare
(
            
{
                
"
text
"
:
expected_text
            
}
            
events
[
1
]
[
1
]
        
)
