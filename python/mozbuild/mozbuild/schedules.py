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
gtest
'
    
'
jittest
'
    
'
marionette
'
    
'
mochitest
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
