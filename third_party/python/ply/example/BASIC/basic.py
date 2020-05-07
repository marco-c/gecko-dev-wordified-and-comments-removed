import
sys
sys
.
path
.
insert
(
0
"
.
.
/
.
.
"
)
if
sys
.
version_info
[
0
]
>
=
3
:
    
raw_input
=
input
import
basiclex
import
basparse
import
basinterp
if
len
(
sys
.
argv
)
=
=
2
:
    
data
=
open
(
sys
.
argv
[
1
]
)
.
read
(
)
    
prog
=
basparse
.
parse
(
data
)
    
if
not
prog
:
        
raise
SystemExit
    
b
=
basinterp
.
BasicInterpreter
(
prog
)
    
try
:
        
b
.
run
(
)
        
raise
SystemExit
    
except
RuntimeError
:
        
pass
else
:
    
b
=
basinterp
.
BasicInterpreter
(
{
}
)
while
1
:
    
try
:
        
line
=
raw_input
(
"
[
BASIC
]
"
)
    
except
EOFError
:
        
raise
SystemExit
    
if
not
line
:
        
continue
    
line
+
=
"
\
n
"
    
prog
=
basparse
.
parse
(
line
)
    
if
not
prog
:
        
continue
    
keys
=
list
(
prog
)
    
if
keys
[
0
]
>
0
:
        
b
.
add_statements
(
prog
)
    
else
:
        
stat
=
prog
[
keys
[
0
]
]
        
if
stat
[
0
]
=
=
'
RUN
'
:
            
try
:
                
b
.
run
(
)
            
except
RuntimeError
:
                
pass
        
elif
stat
[
0
]
=
=
'
LIST
'
:
            
b
.
list
(
)
        
elif
stat
[
0
]
=
=
'
BLANK
'
:
            
b
.
del_line
(
stat
[
1
]
)
        
elif
stat
[
0
]
=
=
'
NEW
'
:
            
b
.
new
(
)
