"
"
"
Echo
path
simulation
factory
module
.
"
"
"
import
numpy
as
np
from
.
import
echo_path_simulation
class
EchoPathSimulatorFactory
(
object
)
:
    
_LINEAR_ECHO_IMPULSE_RESPONSE
=
np
.
array
(
[
0
.
0
]
*
(
20
*
48
)
+
[
0
.
15
]
)
    
def
__init__
(
self
)
:
        
pass
    
classmethod
    
def
GetInstance
(
cls
echo_path_simulator_class
render_input_filepath
)
:
        
"
"
"
Creates
an
EchoPathSimulator
instance
given
a
class
object
.
    
Args
:
      
echo_path_simulator_class
:
EchoPathSimulator
class
object
(
not
an
                                 
instance
)
.
      
render_input_filepath
:
Path
to
the
render
audio
track
file
.
    
Returns
:
      
An
EchoPathSimulator
instance
.
    
"
"
"
        
assert
render_input_filepath
is
not
None
or
(
            
echo_path_simulator_class
=
=
            
echo_path_simulation
.
NoEchoPathSimulator
)
        
if
echo_path_simulator_class
=
=
echo_path_simulation
.
NoEchoPathSimulator
:
            
return
echo_path_simulation
.
NoEchoPathSimulator
(
)
        
elif
echo_path_simulator_class
=
=
(
                
echo_path_simulation
.
LinearEchoPathSimulator
)
:
            
return
echo_path_simulation
.
LinearEchoPathSimulator
(
                
render_input_filepath
cls
.
_LINEAR_ECHO_IMPULSE_RESPONSE
)
        
else
:
            
return
echo_path_simulator_class
(
render_input_filepath
)
