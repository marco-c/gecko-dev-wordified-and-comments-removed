class
FrameClass
:
    
def
__init__
(
self
cls
)
:
        
self
.
cls
=
cls
class
Frame
(
FrameClass
)
:
    
def
__init__
(
self
cls
ty
flags
)
:
        
FrameClass
.
__init__
(
self
cls
)
        
self
.
ty
=
ty
        
self
.
flags
=
flags
        
self
.
is_concrete
=
True
class
AbstractFrame
(
FrameClass
)
:
    
def
__init__
(
self
cls
)
:
        
FrameClass
.
__init__
(
self
cls
)
        
self
.
is_concrete
=
False
