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
from
marionette_harness
.
runtests
import
cli
as
mn_cli
def
cli
(
args
=
None
)
:
    
mn_cli
(
        
runner_class
=
FirefoxUITestRunner
        
parser_class
=
FirefoxUIArguments
        
args
=
args
    
)
if
__name__
=
=
"
__main__
"
:
    
cli
(
)
