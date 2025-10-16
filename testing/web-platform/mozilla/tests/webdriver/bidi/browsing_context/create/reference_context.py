import
pytest
from
.
.
import
using_context
pytestmark
=
pytest
.
mark
.
asyncio
def
assert_tab_order
(
session
expected_context_ids
)
:
    
with
using_context
(
session
"
chrome
"
)
:
        
context_ids
=
session
.
execute_script
(
            
"
"
"
            
const
{
NavigableManager
}
=
                
ChromeUtils
.
importESModule
(
"
chrome
:
/
/
remote
/
content
/
shared
/
NavigableManager
.
sys
.
mjs
"
)
;
            
const
{
TabManager
}
=
                
ChromeUtils
.
importESModule
(
"
chrome
:
/
/
remote
/
content
/
shared
/
TabManager
.
sys
.
mjs
"
)
;
            
const
contextId
=
arguments
[
0
]
;
            
const
browsingContext
=
NavigableManager
.
getBrowsingContextById
(
contextId
)
;
            
const
chromeWindow
=
browsingContext
.
top
.
embedderWindowGlobal
.
browsingContext
.
window
;
            
const
tabBrowser
=
TabManager
.
getTabBrowser
(
chromeWindow
)
;
            
return
tabBrowser
.
browsers
.
map
(
browser
=
>
NavigableManager
.
getIdForBrowser
(
browser
)
)
;
            
"
"
"
            
args
=
(
expected_context_ids
[
0
]
)
        
)
        
assert
context_ids
=
=
expected_context_ids
pytest
.
mark
.
allow_system_access
async
def
test_reference_context
(
bidi_session
current_session
)
:
    
result
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
window
"
)
    
tab1_context_id
=
result
[
"
context
"
]
    
result
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
window
"
)
    
tab2_context_id
=
result
[
"
context
"
]
    
result
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
reference_context
=
tab1_context_id
    
)
    
tab3_context_id
=
result
[
"
context
"
]
    
result
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
reference_context
=
tab2_context_id
    
)
    
tab4_context_id
=
result
[
"
context
"
]
    
result
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
reference_context
=
tab2_context_id
    
)
    
tab5_context_id
=
result
[
"
context
"
]
    
result
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
window
"
reference_context
=
tab2_context_id
    
)
    
tab6_context_id
=
result
[
"
context
"
]
    
assert_tab_order
(
current_session
[
tab1_context_id
tab3_context_id
]
)
    
assert_tab_order
(
        
current_session
[
tab2_context_id
tab5_context_id
tab4_context_id
]
    
)
    
assert_tab_order
(
current_session
[
tab6_context_id
]
)
