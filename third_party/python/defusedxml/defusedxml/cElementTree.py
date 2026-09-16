"
"
"
Defused
xml
.
etree
.
cElementTree
"
"
"
from
__future__
import
absolute_import
import
warnings
from
.
common
import
_generate_etree_functions
from
xml
.
etree
.
cElementTree
import
TreeBuilder
as
_TreeBuilder
from
xml
.
etree
.
cElementTree
import
parse
as
_parse
from
xml
.
etree
.
cElementTree
import
tostring
from
xml
.
etree
.
ElementTree
import
iterparse
as
_iterparse
from
.
ElementTree
import
(
    
XML
    
XMLParse
    
XMLParser
    
XMLTreeBuilder
    
fromstring
    
iterparse
    
parse
    
tostring
    
DefusedXMLParser
    
ParseError
)
__origin__
=
"
xml
.
etree
.
cElementTree
"
warnings
.
warn
(
    
"
defusedxml
.
cElementTree
is
deprecated
import
from
defusedxml
.
ElementTree
instead
.
"
    
category
=
DeprecationWarning
    
stacklevel
=
2
)
XMLTreeBuilder
=
XMLParse
=
XMLParser
=
DefusedXMLParser
parse
iterparse
fromstring
=
_generate_etree_functions
(
    
DefusedXMLParser
_TreeBuilder
_parse
_iterparse
)
XML
=
fromstring
__all__
=
[
    
"
ParseError
"
    
"
XML
"
    
"
XMLParse
"
    
"
XMLParser
"
    
"
XMLTreeBuilder
"
    
"
fromstring
"
    
"
iterparse
"
    
"
parse
"
    
"
tostring
"
]
