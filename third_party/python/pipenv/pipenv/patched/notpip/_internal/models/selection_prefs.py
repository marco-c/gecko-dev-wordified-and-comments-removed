from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Optional
    
from
pipenv
.
patched
.
notpip
.
_internal
.
models
.
format_control
import
FormatControl
class
SelectionPreferences
(
object
)
:
    
"
"
"
    
Encapsulates
the
candidate
selection
preferences
for
downloading
    
and
installing
files
.
    
"
"
"
    
def
__init__
(
        
self
        
allow_yanked
        
allow_all_prereleases
=
False
        
format_control
=
None
        
prefer_binary
=
False
        
ignore_requires_python
=
None
    
)
:
        
"
"
"
Create
a
SelectionPreferences
object
.
        
:
param
allow_yanked
:
Whether
files
marked
as
yanked
(
in
the
sense
            
of
PEP
592
)
are
permitted
to
be
candidates
for
install
.
        
:
param
format_control
:
A
FormatControl
object
or
None
.
Used
to
control
            
the
selection
of
source
packages
/
binary
packages
when
consulting
            
the
index
and
links
.
        
:
param
prefer_binary
:
Whether
to
prefer
an
old
but
valid
binary
            
dist
over
a
new
source
dist
.
        
:
param
ignore_requires_python
:
Whether
to
ignore
incompatible
            
"
Requires
-
Python
"
values
in
links
.
Defaults
to
False
.
        
"
"
"
        
if
ignore_requires_python
is
None
:
            
ignore_requires_python
=
False
        
self
.
allow_yanked
=
allow_yanked
        
self
.
allow_all_prereleases
=
allow_all_prereleases
        
self
.
format_control
=
format_control
        
self
.
prefer_binary
=
prefer_binary
        
self
.
ignore_requires_python
=
ignore_requires_python
