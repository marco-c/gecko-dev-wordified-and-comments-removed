"
"
"
pytest
:
unit
and
functional
testing
with
Python
.
"
"
"
__all__
=
[
    
'
main
'
    
'
UsageError
'
    
'
cmdline
'
    
'
hookspec
'
    
'
hookimpl
'
    
'
__version__
'
]
if
__name__
=
=
'
__main__
'
:
    
import
pytest
    
raise
SystemExit
(
pytest
.
main
(
)
)
from
_pytest
.
config
import
(
    
main
UsageError
_preloadplugins
cmdline
    
hookspec
hookimpl
)
from
_pytest
import
__version__
_preloadplugins
(
)
