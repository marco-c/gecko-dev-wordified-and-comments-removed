from
__future__
import
absolute_import
from
firefox_ui_harness
.
testcases
import
UpdateTestCase
class
TestFallbackUpdate
(
UpdateTestCase
)
:
    
def
setUp
(
self
)
:
        
UpdateTestCase
.
setUp
(
self
is_fallback
=
True
)
    
def
tearDown
(
self
)
:
        
try
:
            
self
.
puppeteer
.
windows
.
close_all
(
[
self
.
browser
]
)
        
finally
:
            
UpdateTestCase
.
tearDown
(
self
)
    
def
test_update
(
self
)
:
        
self
.
download_and_apply_available_update
(
force_fallback
=
True
)
        
self
.
download_and_apply_forced_update
(
)
        
self
.
check_update_applied
(
)
