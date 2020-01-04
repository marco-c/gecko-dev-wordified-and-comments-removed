from
firefox_puppeteer
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
