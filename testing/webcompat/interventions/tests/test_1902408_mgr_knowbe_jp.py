import
pytest
URL
=
"
https
:
/
/
mgr
.
knowbe
.
jp
/
"
FAILURE_TEXT
=
"
"
DOWN_TEXT
=
"
"
pytest
.
mark
.
asyncio
pytest
.
mark
.
with_interventions
async
def
test_enabled
(
client
)
:
    
await
client
.
navigate
(
URL
)
    
await
client
.
stall
(
3
)
    
assert
not
client
.
find_text
(
FAILURE_TEXT
is_displayed
=
True
)
pytest
.
mark
.
asyncio
pytest
.
mark
.
without_interventions
async
def
test_disabled
(
client
)
:
    
await
client
.
navigate
(
URL
)
    
failure
down
=
client
.
await_first_element_of
(
        
[
            
client
.
text
(
FAILURE_TEXT
)
            
client
.
text
(
DOWN_TEXT
)
        
]
        
is_displayed
=
True
    
)
    
if
down
:
        
pytest
.
skip
(
"
Site
is
down
right
now
.
"
)
    
assert
failure
