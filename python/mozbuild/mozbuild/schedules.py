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
INCLUSIVE_COMPONENTS
=
[
    
"
docs
"
    
"
py
-
lint
"
    
"
js
-
lint
"
    
"
yaml
-
lint
"
    
"
jittest
"
    
"
test
-
verify
"
    
"
test
-
verify
-
gpu
"
    
"
test
-
verify
-
wpt
"
    
"
test
-
coverage
"
    
"
test
-
coverage
-
wpt
"
    
"
jsreftest
"
    
"
android
-
hw
-
gfx
"
    
"
rusttests
"
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
    
"
android
"
    
"
linux
"
    
"
macosx
"
    
"
windows
"
    
"
ios
"
    
"
firefox
"
    
"
fenix
"
    
"
focus
-
android
"
    
"
awsy
"
    
"
condprofile
"
    
"
cppunittest
"
    
"
firefox
-
ui
"
    
"
fuzztest
"
    
"
geckoview
-
junit
"
    
"
gtest
"
    
"
marionette
-
unittest
"
    
"
marionette
-
integration
"
    
"
mochitest
"
    
"
raptor
"
    
"
reftest
"
    
"
talos
"
    
"
telemetry
-
tests
-
client
"
    
"
xpcshell
"
    
"
xpcshell
-
coverage
"
    
"
web
-
platform
-
tests
"
    
"
crashtest
"
    
"
mochitest
-
a11y
"
    
"
mochitest
-
browser
-
a11y
"
    
"
mochitest
-
browser
-
media
"
    
"
mochitest
-
browser
-
chrome
"
    
"
mochitest
-
browser
-
translations
"
    
"
mochitest
-
chrome
"
    
"
mochitest
-
plain
"
    
"
web
-
platform
-
tests
-
crashtest
"
    
"
web
-
platform
-
tests
-
print
-
reftest
"
    
"
web
-
platform
-
tests
-
reftest
"
    
"
web
-
platform
-
tests
-
wdspec
"
    
"
nss
"
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
