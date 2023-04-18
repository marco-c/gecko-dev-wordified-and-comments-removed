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
    
)
]
