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
def
lint
(
paths
config
fix
=
None
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
    
log
=
lintargs
[
"
log
"
]
    
for
f
in
files
:
        
with
open
(
f
"
rb
"
)
as
open_file
:
            
hasFix
=
False
            
content_to_write
=
[
]
            
try
:
                
lines
=
open_file
.
readlines
(
)
                
if
lines
[
:
]
.
__len__
(
)
!
=
0
and
lines
[
-
1
:
]
[
0
]
.
strip
(
)
.
__len__
(
)
=
=
0
:
                    
open_file
.
seek
(
0
)
                    
if
fix
:
                        
for
i
line
in
reversed
(
list
(
enumerate
(
open_file
)
)
)
:
                            
if
line
.
strip
(
)
!
=
b
"
"
:
                                
with
open
(
f
"
wb
"
)
as
write_file
:
                                    
if
not
lines
[
i
]
.
endswith
(
b
"
\
n
"
)
:
                                        
lines
[
i
]
=
lines
[
i
]
+
b
"
\
n
"
                                    
for
e
in
lines
[
:
i
+
1
]
:
                                        
write_file
.
write
(
e
)
                                
break
                    
else
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
message
"
:
"
Empty
Lines
at
end
of
file
"
                            
"
level
"
:
"
error
"
                            
"
lineno
"
:
open_file
.
readlines
(
)
[
:
]
.
__len__
(
)
                        
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
            
except
Exception
as
ex
:
                
log
.
debug
(
"
Error
:
"
+
str
(
ex
)
+
"
in
file
:
"
+
f
)
            
open_file
.
seek
(
0
)
            
for
i
line
in
enumerate
(
open_file
)
:
                
if
line
.
endswith
(
b
"
\
n
"
)
:
                    
if
fix
:
                        
content_to_write
.
append
(
line
.
rstrip
(
)
+
b
"
\
n
"
)
                        
hasFix
=
True
                    
else
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
message
"
:
"
Trailing
whitespace
"
                            
"
level
"
:
"
error
"
                            
"
lineno
"
:
i
+
1
                        
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
                
else
:
                    
if
fix
:
                        
content_to_write
.
append
(
line
)
            
if
hasFix
:
                
with
open
(
f
"
wb
"
)
as
open_file_to_write
:
                    
open_file_to_write
.
write
(
b
"
"
.
join
(
content_to_write
)
)
            
open_file
.
seek
(
0
)
            
content
=
open_file
.
read
(
)
            
if
b
"
\
r
\
n
"
in
content
:
                
if
fix
:
                    
content
=
content
.
replace
(
b
"
\
r
\
n
"
b
"
\
n
"
)
                    
with
open
(
f
"
wb
"
)
as
open_file_to_write
:
                        
open_file_to_write
.
write
(
content
)
                
else
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
message
"
:
"
Windows
line
return
"
                        
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
results
