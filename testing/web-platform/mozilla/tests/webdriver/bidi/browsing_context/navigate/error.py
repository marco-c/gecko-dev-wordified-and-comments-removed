import
os
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
async
def
test_insecure_certificate
(
configuration
url
custom_profile
geckodriver
)
:
    
try
:
        
os
.
remove
(
os
.
path
.
join
(
custom_profile
.
profile
"
cert9
.
db
"
)
)
    
except
Exception
:
        
pass
    
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
False
    
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
True
    
)
async
def
test_invalid_content_encoding
(
bidi_session
new_tab
inline
)
:
    
await
navigate_and_assert
(
        
bidi_session
        
new_tab
        
f
"
{
inline
(
'
<
div
>
foo
'
)
}
&
pipe
=
header
(
Content
-
Encoding
gzip
)
"
        
expected_error
=
True
    
)
