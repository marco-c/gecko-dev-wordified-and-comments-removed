from
collections
import
namedtuple
GeckoProcessType
=
namedtuple
(
    
"
GeckoProcessType
"
    
[
        
"
enum_value
"
        
"
enum_name
"
        
"
string_name
"
        
"
proc_typename
"
        
"
process_bin_type
"
        
"
procinfo_typename
"
        
"
webidl_typename
"
        
"
allcaps_name
"
        
"
crash_ping
"
    
]
)
process_types
=
[
    
GeckoProcessType
(
        
0
        
"
Default
"
        
"
default
"
        
"
Parent
"
        
"
Self
"
        
"
Browser
"
        
"
Browser
"
        
"
DEFAULT
"
        
False
    
)
    
GeckoProcessType
(
        
2
        
"
Content
"
        
"
tab
"
        
"
Content
"
        
"
Self
"
        
"
Content
"
        
"
Content
"
        
"
CONTENT
"
        
True
    
)
    
GeckoProcessType
(
        
3
        
"
IPDLUnitTest
"
        
"
ipdlunittest
"
        
"
IPDLUnitTest
"
        
"
PluginContainer
"
        
"
IPDLUnitTest
"
        
"
IpdlUnitTest
"
        
"
IPDLUNITTEST
"
        
False
    
)
    
GeckoProcessType
(
        
4
        
"
GMPlugin
"
        
"
gmplugin
"
        
"
GMPlugin
"
        
"
PluginContainer
"
        
"
GMPlugin
"
        
"
GmpPlugin
"
        
"
GMPLUGIN
"
        
False
    
)
    
GeckoProcessType
(
        
5
        
"
GPU
"
        
"
gpu
"
        
"
GPU
"
        
"
Self
"
        
"
GPU
"
        
"
Gpu
"
        
"
GPU
"
        
True
    
)
    
GeckoProcessType
(
        
6
        
"
VR
"
        
"
vr
"
        
"
VR
"
        
"
Self
"
        
"
VR
"
        
"
Vr
"
        
"
VR
"
        
True
    
)
    
GeckoProcessType
(
        
7
        
"
RDD
"
        
"
rdd
"
        
"
RDD
"
        
"
Self
"
        
"
RDD
"
        
"
Rdd
"
        
"
RDD
"
        
True
    
)
    
GeckoProcessType
(
        
8
        
"
Socket
"
        
"
socket
"
        
"
Socket
"
        
"
Self
"
        
"
Socket
"
        
"
Socket
"
        
"
SOCKET
"
        
True
    
)
    
GeckoProcessType
(
        
9
        
"
RemoteSandboxBroker
"
        
"
sandboxbroker
"
        
"
RemoteSandboxBroker
"
        
"
PluginContainer
"
        
"
RemoteSandboxBroker
"
        
"
RemoteSandboxBroker
"
        
"
REMOTESANDBOXBROKER
"
        
False
    
)
    
GeckoProcessType
(
        
10
        
"
ForkServer
"
        
"
forkserver
"
        
"
ForkServer
"
        
"
Self
"
        
"
ForkServer
"
        
"
ForkServer
"
        
"
FORKSERVER
"
        
False
    
)
    
GeckoProcessType
(
        
11
        
"
Utility
"
        
"
utility
"
        
"
Utility
"
        
"
Self
"
        
"
Utility
"
        
"
Utility
"
        
"
UTILITY
"
        
True
    
)
]
