from
abc
import
ABCMeta
abstractmethod
import
six
six
.
add_metaclass
(
ABCMeta
)
class
Playback
:
    
def
__init__
(
self
config
)
:
        
self
.
config
=
config
        
self
.
host
=
None
        
self
.
port
=
None
    
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
