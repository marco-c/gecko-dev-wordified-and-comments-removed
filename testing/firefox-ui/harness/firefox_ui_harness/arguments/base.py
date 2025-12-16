from
marionette_harness
import
BaseMarionetteArguments
class
FirefoxUIBaseArguments
:
    
name
=
"
Firefox
UI
Tests
"
    
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
        
super
(
)
.
__init__
(
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
