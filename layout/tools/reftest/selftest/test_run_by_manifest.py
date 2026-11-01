import
os
import
sys
from
types
import
SimpleNamespace
import
mozunit
from
mozlog
.
structuredlog
import
StructuredLogger
sys
.
path
.
insert
(
0
os
.
path
.
dirname
(
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
)
)
import
runreftest
MANIFEST_A
=
"
file
:
/
/
/
tests
/
a
/
reftest
.
list
"
MANIFEST_B
=
"
file
:
/
/
/
tests
/
b
/
reftest
.
list
"
def
test_browser_launch_is_attributed_to_its_manifest
(
)
:
    
"
"
"
Crashes
before
a
manifest
'
s
first
test
are
logged
with
that
manifest
'
s
    
group
and
name
not
with
what
the
previous
manifest
left
behind
.
"
"
"
    
reftest
=
runreftest
.
RefTest
(
"
reftest
"
)
    
reftest
.
log
=
StructuredLogger
(
"
test_run_by_manifest
"
)
    
reftest
.
outputHandler
=
SimpleNamespace
(
results
=
{
}
)
    
reftest
.
getGtkTheme
=
lambda
:
"
"
    
reftest
.
gtkTheme
=
"
"
    
reftest
.
getActiveTests
=
lambda
manifests
options
:
[
        
{
            
"
manifest
"
:
MANIFEST_A
            
"
manifestID
"
:
"
a
/
reftest
.
list
"
            
"
identifier
"
:
"
a
.
html
"
        
}
        
{
            
"
manifest
"
:
MANIFEST_B
            
"
manifestID
"
:
"
b
/
reftest
.
list
"
            
"
identifier
"
:
"
b
.
html
"
        
}
    
]
    
launches
=
[
]
    
def
run_app
(
options
tests
*
*
kwargs
)
:
        
launches
.
append
(
(
reftest
.
lastTestSeen
reftest
.
currentManifestID
)
)
        
reftest
.
lastTestSeen
=
tests
[
-
1
]
[
"
identifier
"
]
        
return
1
    
reftest
.
runApp
=
run_app
    
options
=
SimpleNamespace
(
        
debugger
=
None
        
timeout
=
300
        
symbolsPath
=
None
        
suite
=
"
reftest
"
    
)
    
reftest
.
runSerialTests
(
[
]
options
)
    
assert
launches
=
=
[
        
(
MANIFEST_A
"
a
/
reftest
.
list
"
)
        
(
MANIFEST_B
"
b
/
reftest
.
list
"
)
    
]
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
