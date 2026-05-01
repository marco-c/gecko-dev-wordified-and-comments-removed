import
pytest
from
fml
import
FmlClient
pytest
.
fixture
def
fml_client
(
)
:
    
def
_client
(
path
channel
)
:
        
return
FmlClient
(
            
"
.
/
megazords
/
cirrus
/
tests
/
python
-
tests
/
resources
/
"
+
path
channel
        
)
    
return
_client
