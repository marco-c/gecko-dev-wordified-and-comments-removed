from
__future__
import
absolute_import
from
abc
import
ABCMeta
abstractmethod
class
Playback
(
object
)
:
    
__metaclass__
=
ABCMeta
    
def
__init__
(
self
config
android_device
=
None
)
:
        
self
.
config
=
config
        
self
.
android_device
=
android_device
    
abstractmethod
    
def
download
(
self
)
:
        
pass
    
abstractmethod
    
def
setup
(
self
)
:
        
pass
    
abstractmethod
    
def
start
(
self
)
:
        
pass
    
abstractmethod
    
def
stop
(
self
)
:
        
pass
