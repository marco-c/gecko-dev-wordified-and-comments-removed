from
marionette
.
runtests
import
cli
as
mn_cli
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
'
__main__
'
:
    
cli
(
)
