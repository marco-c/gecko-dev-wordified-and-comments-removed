from
geckoprocesstypes
import
process_types
def
main
(
output
)
:
    
output
.
write
(
        
"
"
"
  
processTypes
:
{
"
"
"
    
)
    
for
p
in
process_types
:
        
string_name
=
p
.
string_name
        
if
p
.
string_name
=
=
"
default
"
:
            
string_name
=
"
main
"
        
if
p
.
string_name
=
=
"
tab
"
:
            
string_name
=
"
content
"
        
output
.
write
(
            
"
"
"
    
/
/
A
crash
in
the
%
(
procname
)
s
process
.
    
%
(
proctype
)
d
:
"
%
(
procname
)
s
"
"
"
"
            
%
{
                
"
proctype
"
:
p
.
enum_value
                
"
procname
"
:
string_name
            
}
        
)
    
output
.
write
(
        
"
"
"
  
}
"
"
"
    
)
