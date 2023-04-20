import
os
import
sys
import
manifestparser
import
mozpack
.
path
as
mozpath
from
mozpack
.
copier
import
FileCopier
from
mozpack
.
manifests
import
InstallManifest
TEST_MANIFESTS
=
dict
(
    
A11Y
=
(
"
a11y
"
"
testing
/
mochitest
"
"
a11y
"
True
)
    
BROWSER_CHROME
=
(
"
browser
-
chrome
"
"
testing
/
mochitest
"
"
browser
"
True
)
    
ANDROID_INSTRUMENTATION
=
(
"
instrumentation
"
"
instrumentation
"
"
.
"
False
)
    
FIREFOX_UI_FUNCTIONAL
=
(
"
firefox
-
ui
-
functional
"
"
firefox
-
ui
"
"
.
"
False
)
    
FIREFOX_UI_UPDATE
=
(
"
firefox
-
ui
-
update
"
"
firefox
-
ui
"
"
.
"
False
)
    
PYTHON_UNITTEST
=
(
"
python
"
"
python
"
"
.
"
False
)
    
CRAMTEST
=
(
"
cram
"
"
cram
"
"
.
"
False
)
    
TELEMETRY_TESTS_CLIENT
=
(
        
"
telemetry
-
tests
-
client
"
        
"
toolkit
/
components
/
telemetry
/
tests
/
marionette
/
"
        
"
.
"
        
False
    
)
    
MARIONETTE
=
(
"
marionette
"
"
marionette
"
"
.
"
False
)
    
MARIONETTE_UNIT
=
(
"
marionette
"
"
marionette
"
"
.
"
False
)
    
MARIONETTE_WEBAPI
=
(
"
marionette
"
"
marionette
"
"
.
"
False
)
    
MOCHITEST
=
(
"
mochitest
"
"
testing
/
mochitest
"
"
tests
"
True
)
    
MOCHITEST_CHROME
=
(
"
chrome
"
"
testing
/
mochitest
"
"
chrome
"
True
)
    
WEBRTC_SIGNALLING_TEST
=
(
"
steeplechase
"
"
steeplechase
"
"
.
"
True
)
    
XPCSHELL_TESTS
=
(
"
xpcshell
"
"
xpcshell
"
"
.
"
True
)
    
PERFTESTS
=
(
"
perftest
"
"
testing
/
perf
"
"
perf
"
True
)
)
REFTEST_FLAVORS
=
(
"
crashtest
"
"
reftest
"
)
PUPPETEER_FLAVORS
=
(
"
puppeteer
"
)
WEB_PLATFORM_TESTS_FLAVORS
=
(
"
web
-
platform
-
tests
"
)
def
all_test_flavors
(
)
:
    
return
(
        
[
v
[
0
]
for
v
in
TEST_MANIFESTS
.
values
(
)
]
        
+
list
(
REFTEST_FLAVORS
)
        
+
list
(
PUPPETEER_FLAVORS
)
        
+
list
(
WEB_PLATFORM_TESTS_FLAVORS
)
    
)
class
TestInstallInfo
(
object
)
:
    
def
__init__
(
self
)
:
        
self
.
seen
=
set
(
)
        
self
.
pattern_installs
=
[
]
        
self
.
installs
=
[
]
        
self
.
external_installs
=
set
(
)
        
self
.
deferred_installs
=
set
(
)
    
def
__ior__
(
self
other
)
:
        
self
.
pattern_installs
.
extend
(
other
.
pattern_installs
)
        
self
.
installs
.
extend
(
other
.
installs
)
        
self
.
external_installs
|
=
other
.
external_installs
        
self
.
deferred_installs
|
=
other
.
deferred_installs
        
return
self
class
SupportFilesConverter
(
object
)
:
    
"
"
"
Processes
a
"
support
-
files
"
entry
from
a
test
object
either
from
    
a
parsed
object
from
a
test
manifests
or
its
representation
in
    
moz
.
build
and
returns
the
installs
to
perform
for
this
test
object
.
    
Processing
the
same
support
files
multiple
times
will
not
have
any
further
    
effect
and
the
structure
of
the
parsed
objects
from
manifests
will
have
a
    
lot
of
repeated
entries
so
this
class
takes
care
of
memoizing
.
    
"
"
"
    
def
__init__
(
self
)
:
        
self
.
_fields
=
(
            
(
"
head
"
set
(
)
)
            
(
"
support
-
files
"
set
(
)
)
            
(
"
generated
-
files
"
set
(
)
)
        
)
    
def
convert_support_files
(
self
test
install_root
manifest_dir
out_dir
)
:
        
info
=
TestInstallInfo
(
)
        
for
field
seen
in
self
.
_fields
:
            
value
=
test
.
get
(
field
"
"
)
            
for
pattern
in
value
.
split
(
)
:
                
key
=
field
pattern
out_dir
                
if
key
in
info
.
seen
:
                    
raise
ValueError
(
                        
"
%
s
appears
multiple
times
in
a
test
manifest
under
a
%
s
field
"
                        
"
please
omit
the
duplicate
entry
.
"
%
(
pattern
field
)
                    
)
                
info
.
seen
.
add
(
key
)
                
if
key
in
seen
:
                    
continue
                
seen
.
add
(
key
)
                
if
field
=
=
"
generated
-
files
"
:
                    
info
.
external_installs
.
add
(
                        
mozpath
.
normpath
(
mozpath
.
join
(
out_dir
pattern
)
)
                    
)
                
elif
pattern
[
0
]
=
=
"
!
"
:
                    
info
.
deferred_installs
.
add
(
pattern
)
                
elif
"
*
"
in
pattern
and
field
=
=
"
support
-
files
"
:
                    
info
.
pattern_installs
.
append
(
(
manifest_dir
pattern
out_dir
)
)
                
elif
pattern
[
0
]
=
=
"
/
"
:
                    
full
=
mozpath
.
normpath
(
                        
mozpath
.
join
(
manifest_dir
mozpath
.
basename
(
pattern
)
)
                    
)
                    
info
.
installs
.
append
(
                        
(
full
mozpath
.
join
(
install_root
pattern
[
1
:
]
)
)
                    
)
                
else
:
                    
full
=
mozpath
.
normpath
(
mozpath
.
join
(
manifest_dir
pattern
)
)
                    
dest_path
=
mozpath
.
join
(
out_dir
pattern
)
                    
if
not
full
.
startswith
(
manifest_dir
)
:
                        
if
field
=
=
"
support
-
files
"
:
                            
dest_path
=
mozpath
.
join
(
out_dir
os
.
path
.
basename
(
pattern
)
)
                        
else
:
                            
continue
                    
info
.
installs
.
append
(
(
full
mozpath
.
normpath
(
dest_path
)
)
)
        
return
info
def
install_test_files
(
topsrcdir
topobjdir
tests_root
)
:
    
"
"
"
Installs
the
requested
test
files
to
the
objdir
.
This
is
invoked
by
    
test
runners
to
avoid
installing
tens
of
thousands
of
test
files
when
    
only
a
few
tests
need
to
be
run
.
    
"
"
"
    
manifest
=
InstallManifest
(
        
mozpath
.
join
(
topobjdir
"
_build_manifests
"
"
install
"
"
_test_files
"
)
    
)
    
harness_files_manifest
=
mozpath
.
join
(
        
topobjdir
"
_build_manifests
"
"
install
"
tests_root
    
)
    
if
os
.
path
.
isfile
(
harness_files_manifest
)
:
        
manifest
|
=
InstallManifest
(
harness_files_manifest
)
    
copier
=
FileCopier
(
)
    
manifest
.
populate_registry
(
copier
)
    
copier
.
copy
(
mozpath
.
join
(
topobjdir
tests_root
)
remove_unaccounted
=
False
)
def
read_manifestparser_manifest
(
context
manifest_path
)
:
    
path
=
manifest_path
.
full_path
    
return
manifestparser
.
TestManifest
(
        
manifests
=
[
path
]
        
strict
=
True
        
rootdir
=
context
.
config
.
topsrcdir
        
finder
=
context
.
_finder
        
handle_defaults
=
False
    
)
def
read_reftest_manifest
(
context
manifest_path
)
:
    
import
reftest
    
path
=
manifest_path
.
full_path
    
manifest
=
reftest
.
ReftestManifest
(
finder
=
context
.
_finder
)
    
manifest
.
load
(
path
)
    
return
manifest
def
read_wpt_manifest
(
context
paths
)
:
    
manifest_path
tests_root
=
paths
    
full_path
=
mozpath
.
normpath
(
mozpath
.
join
(
context
.
srcdir
manifest_path
)
)
    
old_path
=
sys
.
path
[
:
]
    
try
:
        
paths_file
=
os
.
path
.
join
(
            
context
.
config
.
topsrcdir
            
"
testing
"
            
"
web
-
platform
"
            
"
tests
"
            
"
tools
"
            
"
localpaths
.
py
"
        
)
        
_globals
=
{
"
__file__
"
:
paths_file
}
        
execfile
(
paths_file
_globals
)
        
import
manifest
as
wptmanifest
    
finally
:
        
sys
.
path
=
old_path
        
f
=
context
.
_finder
.
get
(
full_path
)
        
try
:
            
rv
=
wptmanifest
.
manifest
.
load
(
tests_root
f
)
        
except
wptmanifest
.
manifest
.
ManifestVersionMismatch
:
            
rv
=
wptmanifest
.
manifest
.
Manifest
(
)
        
return
rv
