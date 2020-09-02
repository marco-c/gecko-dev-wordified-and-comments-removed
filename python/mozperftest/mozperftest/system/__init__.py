from
mozperftest
.
layers
import
Layers
from
mozperftest
.
system
.
proxy
import
ProxyRunner
from
mozperftest
.
system
.
android
import
AndroidDevice
from
mozperftest
.
system
.
profile
import
Profile
from
mozperftest
.
system
.
macos
import
MacosDevice
def
get_layers
(
)
:
    
return
Profile
ProxyRunner
AndroidDevice
MacosDevice
def
pick_system
(
env
flavor
mach_cmd
)
:
    
if
flavor
in
(
"
desktop
-
browser
"
"
xpcshell
"
)
:
        
return
Layers
(
            
env
            
mach_cmd
            
(
                
MacosDevice
                
Profile
                
ProxyRunner
            
)
        
)
    
if
flavor
=
=
"
mobile
-
browser
"
:
        
return
Layers
(
env
mach_cmd
(
Profile
ProxyRunner
AndroidDevice
)
)
    
raise
NotImplementedError
(
flavor
)
