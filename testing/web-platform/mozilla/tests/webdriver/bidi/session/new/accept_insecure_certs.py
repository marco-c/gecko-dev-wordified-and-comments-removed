from
copy
import
deepcopy
import
pytest
from
tests
.
bidi
.
browsing_context
.
navigate
import
navigate_and_assert
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
accept_insecure_certs
"
[
True
False
]
)
async
def
test_accept_insecure_certs
(
    
configuration
url
create_custom_profile
geckodriver
accept_insecure_certs
)
:
    
custom_profile
=
create_custom_profile
(
clone
=
False
)
    
config
=
deepcopy
(
configuration
)
    
config
[
"
capabilities
"
]
[
"
moz
:
firefoxOptions
"
]
[
"
args
"
]
=
[
        
"
-
-
profile
"
        
custom_profile
.
profile
    
]
    
config
[
"
capabilities
"
]
[
"
acceptInsecureCerts
"
]
=
accept_insecure_certs
    
config
[
"
capabilities
"
]
[
"
webSocketUrl
"
]
=
True
    
driver
=
geckodriver
(
config
=
config
)
    
driver
.
new_session
(
)
    
bidi_session
=
driver
.
session
.
bidi_session
    
await
bidi_session
.
start
(
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
max_depth
=
0
)
    
await
navigate_and_assert
(
        
bidi_session
        
contexts
[
0
]
        
url
(
"
/
common
/
blank
.
html
"
protocol
=
"
https
"
)
        
expected_error
=
not
accept_insecure_certs
    
)
    
await
driver
.
delete_session
(
)
