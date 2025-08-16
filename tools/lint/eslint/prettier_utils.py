import
os
import
signal
import
subprocess
from
mozlint
import
result
PRETTIER_ERROR_MESSAGE
=
"
"
"
An
error
occurred
running
prettier
.
Please
check
the
following
error
messages
:
{
}
"
"
"
.
strip
(
)
PRETTIER_FORMATTING_MESSAGE
=
(
    
"
This
file
needs
formatting
with
Prettier
(
use
'
mach
lint
-
-
fix
<
path
>
'
)
.
"
)
def
run_prettier
(
cmd_args
config
fix
)
:
    
shell
=
False
    
if
is_windows
(
)
:
        
shell
=
True
    
encoding
=
"
utf
-
8
"
    
orig
=
signal
.
signal
(
signal
.
SIGINT
signal
.
SIG_IGN
)
    
proc
=
subprocess
.
Popen
(
        
cmd_args
shell
=
shell
stdout
=
subprocess
.
PIPE
stderr
=
subprocess
.
PIPE
    
)
    
signal
.
signal
(
signal
.
SIGINT
orig
)
    
try
:
        
output
errors
=
proc
.
communicate
(
)
    
except
KeyboardInterrupt
:
        
proc
.
kill
(
)
        
return
{
"
results
"
:
[
]
"
fixed
"
:
0
}
    
results
=
[
]
    
if
errors
:
        
errors
=
errors
.
decode
(
encoding
"
replace
"
)
.
strip
(
)
.
split
(
"
\
n
"
)
        
errors
=
[
            
error
            
for
error
in
errors
            
if
not
(
"
Ignored
unknown
option
"
in
error
)
        
]
        
if
errors
:
            
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
{
                        
"
name
"
:
"
eslint
"
                        
"
path
"
:
os
.
path
.
abspath
(
"
.
"
)
                        
"
message
"
:
PRETTIER_ERROR_MESSAGE
.
format
(
"
\
n
"
.
join
(
errors
)
)
                        
"
level
"
:
"
error
"
                        
"
rule
"
:
"
prettier
"
                        
"
lineno
"
:
0
                        
"
column
"
:
0
                    
}
                
)
            
)
    
if
not
output
:
        
if
errors
and
errors
:
            
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
        
return
{
"
results
"
:
[
]
"
fixed
"
:
0
}
    
output
=
output
.
decode
(
encoding
"
replace
"
)
.
splitlines
(
)
    
fixed
=
0
    
if
fix
:
        
fixed
=
len
(
output
)
    
else
:
        
for
file
in
output
:
            
if
not
file
:
                
continue
            
file
=
os
.
path
.
abspath
(
file
)
            
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
{
                        
"
name
"
:
"
eslint
"
                        
"
path
"
:
file
                        
"
message
"
:
PRETTIER_FORMATTING_MESSAGE
                        
"
level
"
:
"
error
"
                        
"
rule
"
:
"
prettier
"
                        
"
lineno
"
:
0
                        
"
column
"
:
0
                    
}
                
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
fixed
}
def
is_windows
(
)
:
    
return
(
        
os
.
environ
.
get
(
"
MSYSTEM
"
)
in
(
"
MINGW32
"
"
MINGW64
"
)
        
or
"
MOZILLABUILD
"
in
os
.
environ
    
)
