from
marionette_harness
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
UpdateArguments
from
firefox_ui_harness
.
runners
import
UpdateTestRunner
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
UpdateTestRunner
           
parser_class
=
UpdateArguments
           
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
