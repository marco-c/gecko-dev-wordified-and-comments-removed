class
TestServer
:
  
"
"
"
Base
class
for
any
server
that
needs
to
be
set
up
for
the
tests
.
"
"
"
  
def
__init__
(
self
*
args
*
*
kwargs
)
:
    
pass
  
def
SetUp
(
self
)
:
    
raise
NotImplementedError
  
def
Reset
(
self
)
:
    
raise
NotImplementedError
  
def
TearDown
(
self
)
:
    
raise
NotImplementedError
