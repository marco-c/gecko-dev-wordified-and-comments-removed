"
"
"
Constants
for
SCHEDULES
configuration
in
moz
.
build
files
and
for
skip
-
unless
-
schedules
optimizations
in
task
-
graph
generation
.
"
"
"
from
__future__
import
absolute_import
unicode_literals
print_function
INCLUSIVE_COMPONENTS
=
[
    
'
docs
'
    
'
py
-
lint
'
    
'
js
-
lint
'
    
'
yaml
-
lint
'
    
'
jittest
'
    
'
test
-
verify
'
    
'
test
-
verify
-
gpu
'
    
'
test
-
verify
-
wpt
'
    
'
test
-
coverage
'
    
'
test
-
coverage
-
wpt
'
    
'
jsreftest
'
]
INCLUSIVE_COMPONENTS
=
sorted
(
INCLUSIVE_COMPONENTS
)
EXCLUSIVE_COMPONENTS
=
[
    
'
android
'
    
'
linux
'
    
'
macosx
'
    
'
windows
'
    
'
awsy
'
    
'
cppunittest
'
    
'
firefox
-
ui
'
    
'
geckoview
'
    
'
geckoview
-
junit
'
    
'
gtest
'
    
'
marionette
'
    
'
mochitest
'
    
'
raptor
'
    
'
reftest
'
    
'
robocop
'
    
'
talos
'
    
'
telemetry
-
tests
-
client
'
    
'
xpcshell
'
    
'
xpcshell
-
coverage
'
    
'
web
-
platform
-
tests
'
    
'
web
-
platform
-
tests
-
reftests
'
    
'
web
-
platform
-
tests
-
wdspec
'
    
'
mozmill
'
]
EXCLUSIVE_COMPONENTS
=
sorted
(
EXCLUSIVE_COMPONENTS
)
ALL_COMPONENTS
=
INCLUSIVE_COMPONENTS
+
EXCLUSIVE_COMPONENTS
