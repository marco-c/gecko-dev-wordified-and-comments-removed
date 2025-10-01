import
textwrap
from
marionette_harness
.
marionette_test
import
MarionetteTestCase
class
TestEnginesOnRestart
(
MarionetteTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
TestEnginesOnRestart
self
)
.
setUp
(
)
        
self
.
marionette
.
enforce_gecko_prefs
(
            
{
                
"
browser
.
search
.
log
"
:
True
            
}
        
)
    
def
get_default_search_engine
(
self
)
:
        
"
"
"
Retrieve
the
identifier
of
the
default
search
engine
.
"
"
"
        
script
=
"
"
"
\
        
let
[
resolve
]
=
arguments
;
        
let
searchService
=
Components
.
classes
[
                
"
mozilla
.
org
/
browser
/
search
-
service
;
1
"
]
            
.
getService
(
Components
.
interfaces
.
nsISearchService
)
;
        
return
searchService
.
init
(
)
.
then
(
function
(
)
{
          
resolve
(
searchService
.
defaultEngine
.
id
)
;
        
}
)
;
        
"
"
"
        
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
)
:
            
return
self
.
marionette
.
execute_async_script
(
textwrap
.
dedent
(
script
)
)
    
def
test_engines
(
self
)
:
        
self
.
assertEqual
(
self
.
get_default_search_engine
(
)
"
google
"
)
        
self
.
marionette
.
set_pref
(
"
intl
.
locale
.
requested
"
"
kk_KZ
"
)
        
self
.
marionette
.
restart
(
clean
=
False
in_app
=
True
)
        
self
.
assertEqual
(
self
.
get_default_search_engine
(
)
"
google
"
)
