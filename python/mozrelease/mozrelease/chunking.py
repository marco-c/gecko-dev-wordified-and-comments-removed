from
__future__
import
absolute_import
from
copy
import
copy
class
ChunkingError
(
Exception
)
:
    
pass
def
getChunk
(
things
chunks
thisChunk
)
:
    
if
thisChunk
>
chunks
:
        
raise
ChunkingError
(
"
thisChunk
(
%
d
)
is
greater
than
total
chunks
(
%
d
)
"
%
                           
(
thisChunk
chunks
)
)
    
possibleThings
=
copy
(
things
)
    
nThings
=
len
(
possibleThings
)
    
for
c
in
range
(
1
chunks
+
1
)
:
        
n
=
nThings
/
chunks
        
if
c
<
=
(
nThings
%
chunks
)
:
            
n
+
=
1
        
if
c
=
=
thisChunk
:
            
return
possibleThings
[
0
:
n
]
        
del
possibleThings
[
0
:
n
]
