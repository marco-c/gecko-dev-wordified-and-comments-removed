from
abc
import
ABC
abstractmethod
from
typing
import
Literal
from
py_serializable
import
ViewType
from
.
import
SchemaVersion
class
BaseSchemaVersion
(
ViewType
ABC
)
:
    
"
"
"
Base
class
for
schema
version
views
.
"
"
"
    
property
    
abstractmethod
    
def
schema_version_enum
(
self
)
-
>
SchemaVersion
:
        
.
.
.
    
def
get_schema_version
(
self
)
-
>
str
:
        
return
self
.
schema_version_enum
.
to_version
(
)
class
SchemaVersion1Dot7
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
7
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_7
]
:
        
return
SchemaVersion
.
V1_7
class
SchemaVersion1Dot6
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
6
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_6
]
:
        
return
SchemaVersion
.
V1_6
class
SchemaVersion1Dot5
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
5
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_5
]
:
        
return
SchemaVersion
.
V1_5
class
SchemaVersion1Dot4
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
4
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_4
]
:
        
return
SchemaVersion
.
V1_4
class
SchemaVersion1Dot3
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
3
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_3
]
:
        
return
SchemaVersion
.
V1_3
class
SchemaVersion1Dot2
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
2
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_2
]
:
        
return
SchemaVersion
.
V1_2
class
SchemaVersion1Dot1
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
1
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_1
]
:
        
return
SchemaVersion
.
V1_1
class
SchemaVersion1Dot0
(
BaseSchemaVersion
)
:
    
"
"
"
Schema
version
views
1
.
0
"
"
"
    
property
    
def
schema_version_enum
(
self
)
-
>
Literal
[
SchemaVersion
.
V1_0
]
:
        
return
SchemaVersion
.
V1_0
SCHEMA_VERSIONS
:
dict
[
SchemaVersion
type
[
BaseSchemaVersion
]
]
=
{
    
SchemaVersion
.
V1_7
:
SchemaVersion1Dot7
    
SchemaVersion
.
V1_6
:
SchemaVersion1Dot6
    
SchemaVersion
.
V1_5
:
SchemaVersion1Dot5
    
SchemaVersion
.
V1_4
:
SchemaVersion1Dot4
    
SchemaVersion
.
V1_3
:
SchemaVersion1Dot3
    
SchemaVersion
.
V1_2
:
SchemaVersion1Dot2
    
SchemaVersion
.
V1_1
:
SchemaVersion1Dot1
    
SchemaVersion
.
V1_0
:
SchemaVersion1Dot0
}
