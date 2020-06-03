"
"
"
Bytecode
manipulation
for
coverage
.
py
"
"
"
import
types
def
code_objects
(
code
)
:
    
"
"
"
Iterate
over
all
the
code
objects
in
code
.
"
"
"
    
stack
=
[
code
]
    
while
stack
:
        
code
=
stack
.
pop
(
)
        
for
c
in
code
.
co_consts
:
            
if
isinstance
(
c
types
.
CodeType
)
:
                
stack
.
append
(
c
)
        
yield
code
