__all__
=
[
'
XmlValidator
'
'
XmlValidationError
'
]
from
abc
import
ABC
from
collections
.
abc
import
Iterable
from
typing
import
TYPE_CHECKING
Literal
Optional
Union
overload
from
.
.
exception
import
MissingOptionalDependencyException
from
.
.
schema
import
OutputFormat
from
.
.
schema
.
_res
import
BOM_XML
as
_S_BOM
from
.
import
BaseSchemabasedValidator
SchemabasedValidator
ValidationError
if
TYPE_CHECKING
:
    
from
.
.
schema
import
SchemaVersion
_missing_deps_error
:
Optional
[
tuple
[
MissingOptionalDependencyException
ImportError
]
]
=
None
try
:
    
from
lxml
.
etree
import
(
        
XMLParser
        
XMLSchema
        
fromstring
as
xml_fromstring
    
)
    
if
TYPE_CHECKING
:
        
from
lxml
.
etree
import
_LogEntry
as
_XmlLogEntry
except
ImportError
as
err
:
    
_missing_deps_error
=
MissingOptionalDependencyException
(
        
'
This
functionality
requires
optional
dependencies
.
\
n
'
        
'
Please
install
cyclonedx
-
python
-
lib
with
the
extra
"
xml
-
validation
"
.
\
n
'
    
)
err
class
XmlValidationError
(
ValidationError
)
:
    
classmethod
    
def
_make_from_xle
(
cls
e
:
'
_XmlLogEntry
'
)
-
>
'
XmlValidationError
'
:
        
"
"
"
This
is
an
internal
API
.
It
is
not
part
of
the
public
interface
and
may
change
without
notice
.
"
"
"
        
return
cls
(
e
)
class
_BaseXmlValidator
(
BaseSchemabasedValidator
ABC
)
:
    
property
    
def
output_format
(
self
)
-
>
Literal
[
OutputFormat
.
XML
]
:
        
return
OutputFormat
.
XML
    
def
__init__
(
self
schema_version
:
'
SchemaVersion
'
)
-
>
None
:
        
super
(
)
.
__init__
(
schema_version
)
    
overload
    
def
validate_str
(
self
data
:
str
*
all_errors
:
Literal
[
False
]
=
.
.
.
)
-
>
Optional
[
XmlValidationError
]
:
        
.
.
.
    
overload
    
def
validate_str
(
self
data
:
str
*
all_errors
:
Literal
[
True
]
)
-
>
Optional
[
Iterable
[
XmlValidationError
]
]
:
        
.
.
.
    
def
validate_str
(
        
self
data
:
str
*
all_errors
:
bool
=
False
    
)
-
>
Union
[
None
XmlValidationError
Iterable
[
XmlValidationError
]
]
:
        
.
.
.
    
if
_missing_deps_error
:
        
__MDERROR
=
_missing_deps_error
        
def
validate_str
(
            
self
data
:
str
*
all_errors
:
bool
=
False
        
)
-
>
Union
[
None
XmlValidationError
Iterable
[
XmlValidationError
]
]
:
            
raise
self
.
__MDERROR
[
0
]
from
self
.
__MDERROR
[
1
]
    
else
:
        
def
validate_str
(
            
self
data
:
str
*
all_errors
:
bool
=
False
        
)
-
>
Union
[
None
XmlValidationError
Iterable
[
XmlValidationError
]
]
:
            
validator
=
self
.
_validator
            
valid
=
validator
.
validate
(
                
xml_fromstring
(
                    
bytes
(
data
encoding
=
'
utf8
'
)
                    
parser
=
self
.
__xml_parser
)
)
            
if
valid
:
                
return
None
            
errors
=
validator
.
error_log
            
return
map
(
XmlValidationError
.
_make_from_xle
errors
)
\
                
if
all_errors
\
                
else
XmlValidationError
.
_make_from_xle
(
errors
.
last_error
)
        
__validator
:
Optional
[
'
XMLSchema
'
]
=
None
        
property
        
def
__xml_parser
(
self
)
-
>
XMLParser
:
            
return
XMLParser
(
                
attribute_defaults
=
False
dtd_validation
=
False
load_dtd
=
False
                
no_network
=
True
                
resolve_entities
=
False
                
huge_tree
=
True
                
compact
=
True
                
recover
=
False
            
)
        
property
        
def
_validator
(
self
)
-
>
'
XMLSchema
'
:
            
if
not
self
.
__validator
:
                
schema_file
=
self
.
_schema_file
                
if
schema_file
is
None
:
                    
raise
NotImplementedError
(
'
missing
schema
file
'
)
                
self
.
__validator
=
XMLSchema
(
file
=
schema_file
)
            
return
self
.
__validator
class
XmlValidator
(
_BaseXmlValidator
BaseSchemabasedValidator
SchemabasedValidator
)
:
    
"
"
"
Validator
for
CycloneDX
documents
in
XML
format
.
"
"
"
    
property
    
def
_schema_file
(
self
)
-
>
Optional
[
str
]
:
        
return
_S_BOM
.
get
(
self
.
schema_version
)
