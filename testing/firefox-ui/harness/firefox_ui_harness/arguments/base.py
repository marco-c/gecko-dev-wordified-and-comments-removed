from
marionette
import
BaseMarionetteArguments
class
FirefoxUIBaseArguments
(
object
)
:
    
name
=
'
Firefox
UI
Tests
'
    
args
=
[
]
class
FirefoxUIArguments
(
BaseMarionetteArguments
)
:
    
def
__init__
(
self
*
*
kwargs
)
:
        
BaseMarionetteArguments
.
__init__
(
self
*
*
kwargs
)
        
self
.
register_argument_container
(
FirefoxUIBaseArguments
(
)
)
