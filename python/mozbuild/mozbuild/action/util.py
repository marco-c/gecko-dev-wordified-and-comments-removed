from
__future__
import
absolute_import
print_function
unicode_literals
import
json
import
sys
import
time
def
log_build_task
(
f
*
args
*
*
kwargs
)
:
    
"
"
"
Run
the
given
function
representing
an
entire
build
task
and
log
the
    
BUILDTASK
metadata
row
to
stdout
.
    
"
"
"
    
start
=
time
.
time
(
)
    
try
:
        
return
f
(
*
args
*
*
kwargs
)
    
finally
:
        
end
=
time
.
time
(
)
        
print
(
'
BUILDTASK
%
s
'
%
json
.
dumps
(
{
            
"
argv
"
:
sys
.
argv
            
"
start
"
:
start
            
"
end
"
:
end
            
"
context
"
:
None
        
}
)
)
