TEST_HTML
=
"
<
input
id
=
'
target
'
aria
-
disabled
=
'
false
'
>
"
def
test_atspi
(
atspi
session
inline
)
:
    
session
.
url
=
inline
(
TEST_HTML
)
    
node
=
atspi
.
find_node
(
"
target
"
session
.
url
)
    
assert
"
STATE_ENABLED
"
in
atspi
.
get_state_list_helper
(
node
)
    
def
toggle_aria_disabled
(
)
:
        
session
.
execute_script
(
            
"
target
.
ariaDisabled
=
target
.
ariaDisabled
=
=
=
'
true
'
?
'
false
'
:
'
true
'
"
        
)
    
event
=
atspi
.
expect_event
(
        
"
object
:
state
-
changed
:
enabled
"
dom_id
=
"
target
"
        
action
=
toggle_aria_disabled
    
)
    
assert
event
.
detail1
=
=
0
    
assert
"
STATE_ENABLED
"
not
in
atspi
.
get_state_list_helper
(
node
)
    
event
=
atspi
.
expect_event
(
        
"
object
:
state
-
changed
:
enabled
"
dom_id
=
"
target
"
        
action
=
toggle_aria_disabled
    
)
    
assert
event
.
detail1
=
=
1
    
assert
"
STATE_ENABLED
"
in
atspi
.
get_state_list_helper
(
node
)
    
event
=
atspi
.
expect_event
(
        
"
object
:
state
-
changed
:
sensitive
"
dom_id
=
"
target
"
        
action
=
toggle_aria_disabled
    
)
    
assert
event
.
detail1
=
=
0
    
assert
"
STATE_ENABLED
"
not
in
atspi
.
get_state_list_helper
(
node
)
    
event
=
atspi
.
expect_event
(
        
"
object
:
state
-
changed
:
sensitive
"
dom_id
=
"
target
"
        
action
=
toggle_aria_disabled
    
)
    
assert
event
.
detail1
=
=
1
    
assert
"
STATE_ENABLED
"
in
atspi
.
get_state_list_helper
(
node
)
