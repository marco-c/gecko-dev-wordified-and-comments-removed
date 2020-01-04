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
UpdateArguments
from
firefox_ui_harness
.
runners
import
UpdateTestRunner
def
cli_update
(
)
:
    
cli
(
runner_class
=
UpdateTestRunner
        
parser_class
=
UpdateArguments
        
)
if
__name__
=
=
'
__main__
'
:
    
cli_update
(
)
