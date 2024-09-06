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
binarysetup
import
BinarySetup
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
from
mozperftest
.
system
.
versionproducer
import
VersionProducer
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
    
desktop_layers
=
[
        
PingServer
        
BinarySetup
        
MacosDevice
        
Profile
        
ProxyRunner
        
VersionProducer
    
]
    
mobile_layers
=
[
        
Profile
        
ProxyRunner
        
BinarySetup
        
AndroidDevice
        
VersionProducer
        
AndroidStartUp
    
]
    
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
            
desktop_layers
        
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
mobile_layers
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
    
if
flavor
=
=
"
custom
-
script
"
:
        
layers
=
[
            
PingServer
            
Profile
            
ProxyRunner
            
BinarySetup
            
AndroidDevice
            
MacosDevice
            
AndroidStartUp
            
VersionProducer
        
]
        
return
Layers
(
env
mach_cmd
layers
)
    
if
flavor
=
=
"
alert
"
:
        
return
Layers
(
env
mach_cmd
[
]
)
    
raise
NotImplementedError
(
flavor
)
