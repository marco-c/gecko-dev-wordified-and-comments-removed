from
marionette
.
runtests
import
cli
from
firefox_ui_harness
.
arguments
import
FirefoxUIArguments
from
firefox_ui_harness
.
runners
import
FirefoxUITestRunner
def
cli_functional
(
)
:
    
cli
(
runner_class
=
FirefoxUITestRunner
        
parser_class
=
FirefoxUIArguments
        
)
if
__name__
=
=
'
__main__
'
:
    
cli_functional
(
)
