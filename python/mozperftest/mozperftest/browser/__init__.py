from
mozperftest
.
browser
.
browsertime
import
BrowsertimeRunner
def
get_layers
(
)
:
    
return
(
BrowsertimeRunner
)
def
pick_browser
(
env
flavor
mach_cmd
)
:
    
if
flavor
=
=
"
script
"
:
        
return
BrowsertimeRunner
(
env
mach_cmd
)
    
raise
NotImplementedError
(
flavor
)
