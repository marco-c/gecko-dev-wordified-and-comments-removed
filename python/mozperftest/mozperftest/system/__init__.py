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
android
import
AndroidDevice
from
mozperftest
.
system
.
android_startup
import
AndroidStartUp
from
mozperftest
.
system
.
macos
import
MacosDevice
from
mozperftest
.
system
.
pingserver
import
PingServer
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
proxy
import
ProxyRunner
def
get_layers
(
)
:
    
return
PingServer
Profile
ProxyRunner
AndroidDevice
MacosDevice
AndroidStartUp
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
"
mochitest
"
)
:
        
return
Layers
(
            
env
            
mach_cmd
            
(
                
PingServer
                
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
AndroidStartUp
)
        
)
    
if
flavor
=
=
"
webpagetest
"
:
        
return
Layers
(
env
mach_cmd
(
Profile
)
)
    
raise
NotImplementedError
(
flavor
)
