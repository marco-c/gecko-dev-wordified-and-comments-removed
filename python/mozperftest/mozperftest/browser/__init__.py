from
mozperftest
.
browser
.
browsertime
import
BrowsertimeRunner
def
pick_browser
(
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
mach_cmd
)
    
raise
NotImplementedError
(
flavor
)
