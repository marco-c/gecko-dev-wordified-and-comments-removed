import
sys
import
unicodedata
from
mozlint
import
result
from
mozlint
.
pathutils
import
expand_exclusions
results
=
[
]
disallowed
=
set
(
    
chr
(
c
)
for
c
in
range
(
sys
.
maxunicode
)
if
unicodedata
.
category
(
chr
(
c
)
)
=
=
"
Cf
"
)
def
getfiletext
(
config
filename
)
:
    
with
open
(
filename
"
rb
"
)
as
infile
:
        
try
:
            
return
infile
.
read
(
)
.
decode
(
"
utf
-
8
"
)
        
except
Exception
as
e
:
            
res
=
{
                
"
path
"
:
filename
                
"
message
"
:
"
Could
not
open
file
as
utf
-
8
-
maybe
an
encoding
error
:
%
s
"
                
%
e
                
"
level
"
:
"
error
"
            
}
            
results
.
append
(
result
.
from_config
(
config
*
*
res
)
)
            
return
None
    
return
None
def
analyze_text
(
filename
text
disallowed
)
:
    
line
=
0
    
for
t
in
text
.
splitlines
(
)
:
        
line
=
line
+
1
        
subset
=
[
c
for
c
in
t
if
chr
(
ord
(
c
)
)
in
disallowed
]
        
if
subset
:
            
return
(
subset
line
)
    
return
(
"
"
0
)
def
lint
(
paths
config
*
*
lintargs
)
:
    
files
=
list
(
expand_exclusions
(
paths
config
lintargs
[
"
root
"
]
)
)
    
for
f
in
files
:
        
text
=
getfiletext
(
config
f
)
        
if
text
:
            
(
subset
line
)
=
analyze_text
(
f
text
disallowed
)
            
if
subset
:
                
res
=
{
                    
"
path
"
:
f
                    
"
lineno
"
:
line
                    
"
message
"
:
"
disallowed
characters
:
%
s
"
%
subset
                    
"
level
"
:
"
error
"
                
}
                
results
.
append
(
result
.
from_config
(
config
*
*
res
)
)
    
return
{
"
results
"
:
results
"
fixed
"
:
0
}
