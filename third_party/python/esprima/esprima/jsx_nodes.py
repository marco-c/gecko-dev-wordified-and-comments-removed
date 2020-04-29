#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
unicode_literals
from
.
nodes
import
Node
from
.
jsx_syntax
import
JSXSyntax
class
JSXClosingElement
(
Node
)
:
    
def
__init__
(
self
name
)
:
        
self
.
type
=
JSXSyntax
.
JSXClosingElement
        
self
.
name
=
name
class
JSXElement
(
Node
)
:
    
def
__init__
(
self
openingElement
children
closingElement
)
:
        
self
.
type
=
JSXSyntax
.
JSXElement
        
self
.
openingElement
=
openingElement
        
self
.
children
=
children
        
self
.
closingElement
=
closingElement
class
JSXEmptyExpression
(
Node
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
type
=
JSXSyntax
.
JSXEmptyExpression
class
JSXExpressionContainer
(
Node
)
:
    
def
__init__
(
self
expression
)
:
        
self
.
type
=
JSXSyntax
.
JSXExpressionContainer
        
self
.
expression
=
expression
class
JSXIdentifier
(
Node
)
:
    
def
__init__
(
self
name
)
:
        
self
.
type
=
JSXSyntax
.
JSXIdentifier
        
self
.
name
=
name
class
JSXMemberExpression
(
Node
)
:
    
def
__init__
(
self
object
property
)
:
        
self
.
type
=
JSXSyntax
.
JSXMemberExpression
        
self
.
object
=
object
        
self
.
property
=
property
class
JSXAttribute
(
Node
)
:
    
def
__init__
(
self
name
value
)
:
        
self
.
type
=
JSXSyntax
.
JSXAttribute
        
self
.
name
=
name
        
self
.
value
=
value
class
JSXNamespacedName
(
Node
)
:
    
def
__init__
(
self
namespace
name
)
:
        
self
.
type
=
JSXSyntax
.
JSXNamespacedName
        
self
.
namespace
=
namespace
        
self
.
name
=
name
class
JSXOpeningElement
(
Node
)
:
    
def
__init__
(
self
name
selfClosing
attributes
)
:
        
self
.
type
=
JSXSyntax
.
JSXOpeningElement
        
self
.
name
=
name
        
self
.
selfClosing
=
selfClosing
        
self
.
attributes
=
attributes
class
JSXSpreadAttribute
(
Node
)
:
    
def
__init__
(
self
argument
)
:
        
self
.
type
=
JSXSyntax
.
JSXSpreadAttribute
        
self
.
argument
=
argument
class
JSXText
(
Node
)
:
    
def
__init__
(
self
value
raw
)
:
        
self
.
type
=
JSXSyntax
.
JSXText
        
self
.
value
=
value
        
self
.
raw
=
raw
