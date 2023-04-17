from
__future__
import
absolute_import
from
.
_compat
import
ABC
FileNotFoundError
from
abc
import
abstractmethod
try
:
    
from
typing
import
BinaryIO
Iterable
Text
except
ImportError
:
    
pass
class
ResourceReader
(
ABC
)
:
    
"
"
"
Abstract
base
class
for
loaders
to
provide
resource
reading
support
.
"
"
"
    
abstractmethod
    
def
open_resource
(
self
resource
)
:
        
"
"
"
Return
an
opened
file
-
like
object
for
binary
reading
.
        
The
'
resource
'
argument
is
expected
to
represent
only
a
file
name
.
        
If
the
resource
cannot
be
found
FileNotFoundError
is
raised
.
        
"
"
"
        
raise
FileNotFoundError
    
abstractmethod
    
def
resource_path
(
self
resource
)
:
        
"
"
"
Return
the
file
system
path
to
the
specified
resource
.
        
The
'
resource
'
argument
is
expected
to
represent
only
a
file
name
.
        
If
the
resource
does
not
exist
on
the
file
system
raise
        
FileNotFoundError
.
        
"
"
"
        
raise
FileNotFoundError
    
abstractmethod
    
def
is_resource
(
self
path
)
:
        
"
"
"
Return
True
if
the
named
'
path
'
is
a
resource
.
        
Files
are
resources
directories
are
not
.
        
"
"
"
        
raise
FileNotFoundError
    
abstractmethod
    
def
contents
(
self
)
:
        
"
"
"
Return
an
iterable
of
entries
in
package
.
"
"
"
        
raise
FileNotFoundError
