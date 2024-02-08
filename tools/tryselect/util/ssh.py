import
subprocess
def
get_ssh_user
(
host
=
"
hg
.
mozilla
.
org
"
)
:
    
ssh_config
=
subprocess
.
run
(
        
[
"
ssh
"
"
-
G
"
host
]
        
text
=
True
        
check
=
True
        
capture_output
=
True
    
)
.
stdout
    
lines
=
[
l
.
strip
(
)
for
l
in
ssh_config
.
splitlines
(
)
]
    
for
line
in
lines
:
        
if
not
line
:
            
continue
        
key
value
=
line
.
split
(
"
"
1
)
        
if
key
.
lower
(
)
=
=
"
user
"
:
            
return
value
    
raise
Exception
(
f
"
Could
not
detect
ssh
user
for
'
{
host
}
'
!
"
)
