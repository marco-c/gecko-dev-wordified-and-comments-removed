import
os
import
sys
try
:
    
from
gcp_devrel
.
testing
.
appengine
import
(
        
pytest_configure
        
pytest_runtest_call
        
testbed
    
)
except
ImportError
:
    
pass
import
pytest
import
six
__all__
=
[
    
"
pytest_configure
"
    
"
pytest_runtest_call
"
    
"
pytest_ignore_collect
"
    
"
testbed
"
    
"
sandbox
"
]
pytest
.
fixture
def
sandbox
(
testbed
)
:
    
"
"
"
    
Enables
parts
of
the
GAE
sandbox
that
are
relevant
.
    
Inserts
the
stub
module
import
hook
which
causes
the
usage
of
    
appengine
-
specific
httplib
httplib2
socket
etc
.
    
"
"
"
    
try
:
        
from
google
.
appengine
.
tools
.
devappserver2
.
python
import
sandbox
    
except
ImportError
:
        
from
google
.
appengine
.
tools
.
devappserver2
.
python
.
runtime
import
sandbox
    
for
name
in
list
(
sys
.
modules
)
:
        
if
name
in
sandbox
.
dist27
.
MODULE_OVERRIDES
:
            
del
sys
.
modules
[
name
]
    
sys
.
meta_path
.
insert
(
0
sandbox
.
StubModuleImportHook
(
)
)
    
sys
.
path_importer_cache
=
{
}
    
yield
testbed
    
sys
.
meta_path
=
[
        
x
for
x
in
sys
.
meta_path
if
not
isinstance
(
x
sandbox
.
StubModuleImportHook
)
    
]
    
sys
.
path_importer_cache
=
{
}
    
for
name
in
list
(
sys
.
modules
)
:
        
if
name
in
sandbox
.
dist27
.
MODULE_OVERRIDES
:
            
del
sys
.
modules
[
name
]
def
pytest_ignore_collect
(
path
config
)
:
    
"
"
"
Skip
App
Engine
tests
in
python
3
or
if
no
SDK
is
available
.
"
"
"
    
if
"
appengine
"
in
str
(
path
)
:
        
if
not
six
.
PY2
:
            
return
True
        
if
not
os
.
environ
.
get
(
"
GAE_SDK_PATH
"
)
:
            
return
True
    
return
False
