import
os
from
firefox_ui_harness
.
testcases
import
FirefoxTestCase
from
marionette_driver
import
Wait
class
TestSafeBrowsingInitialDownload
(
FirefoxTestCase
)
:
    
test_data
=
[
{
            
'
platforms
'
:
[
'
linux
'
'
windows_nt
'
'
darwin
'
]
            
'
files
'
:
[
                
"
goog
-
badbinurl
-
shavar
.
cache
"
                
"
goog
-
badbinurl
-
shavar
.
pset
"
                
"
goog
-
badbinurl
-
shavar
.
sbstore
"
                
"
goog
-
malware
-
shavar
.
cache
"
                
"
goog
-
malware
-
shavar
.
pset
"
                
"
goog
-
malware
-
shavar
.
sbstore
"
                
"
goog
-
phish
-
shavar
.
cache
"
                
"
goog
-
phish
-
shavar
.
pset
"
                
"
goog
-
phish
-
shavar
.
sbstore
"
                
"
goog
-
unwanted
-
shavar
.
cache
"
                
"
goog
-
unwanted
-
shavar
.
pset
"
                
"
goog
-
unwanted
-
shavar
.
sbstore
"
                
"
base
-
track
-
digest256
.
cache
"
                
"
base
-
track
-
digest256
.
pset
"
                
"
base
-
track
-
digest256
.
sbstore
"
                
"
mozstd
-
trackwhite
-
digest256
.
cache
"
                
"
mozstd
-
trackwhite
-
digest256
.
pset
"
                
"
mozstd
-
trackwhite
-
digest256
.
sbstore
"
                
]
            
}
        
{
            
'
platforms
'
:
[
'
windows_nt
'
]
            
'
files
'
:
[
                
"
goog
-
downloadwhite
-
digest256
.
cache
"
                
"
goog
-
downloadwhite
-
digest256
.
pset
"
                
"
goog
-
downloadwhite
-
digest256
.
sbstore
"
            
]
        
}
    
]
    
browser_prefs
=
{
        
'
browser
.
safebrowsing
.
downloads
.
enabled
'
:
'
true
'
        
'
browser
.
safebrowsing
.
phishing
.
enabled
'
:
'
true
'
        
'
browser
.
safebrowsing
.
malware
.
enabled
'
:
'
true
'
        
'
browser
.
safebrowsing
.
provider
.
google
.
nextupdatetime
'
:
1
        
'
browser
.
safebrowsing
.
provider
.
mozilla
.
nextupdatetime
'
:
1
        
'
privacy
.
trackingprotection
.
enabled
'
:
'
true
'
        
'
privacy
.
trackingprotection
.
pbmode
.
enabled
'
:
'
true
'
    
}
    
def
setUp
(
self
)
:
        
FirefoxTestCase
.
setUp
(
self
)
        
self
.
marionette
.
enforce_gecko_prefs
(
self
.
browser_prefs
)
        
self
.
sb_files_path
=
os
.
path
.
join
(
self
.
marionette
.
instance
.
profile
.
profile
'
safebrowsing
'
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
restart
(
clean
=
True
)
        
finally
:
            
FirefoxTestCase
.
tearDown
(
self
)
    
def
test_safe_browsing_initial_download
(
self
)
:
        
wait
=
Wait
(
self
.
marionette
timeout
=
self
.
browser
.
timeout_page_load
)
        
for
data
in
self
.
test_data
:
            
if
self
.
platform
not
in
data
[
'
platforms
'
]
:
                
continue
            
for
item
in
data
[
'
files
'
]
:
                
wait
.
until
(
                    
lambda
_
:
os
.
path
.
exists
(
os
.
path
.
join
(
self
.
sb_files_path
item
)
)
                    
message
=
'
Safe
Browsing
File
:
{
}
not
found
!
'
.
format
(
item
)
)
