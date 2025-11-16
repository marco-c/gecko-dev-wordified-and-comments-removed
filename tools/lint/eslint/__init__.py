import
json
import
os
import
signal
import
subprocess
import
sys
sys
.
path
.
append
(
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
"
eslint
"
)
)
from
mozbuild
.
nodeutil
import
check_node_executables_valid
find_node_executable
from
mozlint
import
result
from
eslint
import
prettier_utils
setup_helper
ESLINT_ERROR_MESSAGE
=
"
"
"
An
error
occurred
running
eslint
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
ESLINT_NOT_FOUND_MESSAGE
=
"
"
"
Could
not
find
eslint
!
We
looked
at
the
-
-
binary
option
at
the
ESLINT
environment
variable
and
then
at
your
local
node_modules
path
.
Please
Install
eslint
and
needed
plugins
with
:
mach
eslint
-
-
setup
and
try
again
.
"
"
"
.
strip
(
)
def
setup
(
root
*
*
lintargs
)
:
    
setup_helper
.
set_project_root
(
root
)
    
if
not
check_node_executables_valid
(
)
:
        
return
1
    
return
setup_helper
.
eslint_maybe_setup
(
)
def
lint
(
paths
config
binary
=
None
fix
=
None
rules
=
[
]
setup
=
None
*
*
lintargs
)
:
    
"
"
"
Run
eslint
.
"
"
"
    
log
=
lintargs
[
"
log
"
]
    
setup_helper
.
set_project_root
(
lintargs
[
"
root
"
]
)
    
module_path
=
setup_helper
.
get_project_root
(
)
    
if
not
binary
:
        
binary
_
=
find_node_executable
(
)
    
if
not
binary
:
        
log
.
error
(
ESLINT_NOT_FOUND_MESSAGE
)
        
return
1
    
extra_args
=
lintargs
.
get
(
"
extra_args
"
)
or
[
]
    
result
=
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
    
if
not
lintargs
.
get
(
"
formatonly
"
False
)
:
        
exclude_args
=
[
]
        
for
path
in
config
.
get
(
"
exclude
"
[
]
)
:
            
exclude_args
.
extend
(
                
[
"
-
-
ignore
-
pattern
"
os
.
path
.
relpath
(
path
lintargs
[
"
root
"
]
)
]
            
)
        
for
rule
in
rules
:
            
extra_args
.
extend
(
[
"
-
-
rule
"
rule
]
)
        
cmd_args
=
(
            
[
                
binary
                
os
.
path
.
join
(
module_path
"
node_modules
"
"
eslint
"
"
bin
"
"
eslint
.
js
"
)
                
"
-
-
format
"
                
"
json
"
                
"
-
-
no
-
error
-
on
-
unmatched
-
pattern
"
            
]
            
+
rules
            
+
list
(
filter
(
lambda
x
:
not
x
.
startswith
(
"
-
-
ignore
-
path
"
)
extra_args
)
)
            
+
exclude_args
            
+
paths
        
)
        
if
fix
:
            
cmd_args
.
insert
(
2
"
-
-
fix
"
)
        
log
.
debug
(
"
ESLint
command
:
{
}
"
.
format
(
"
"
.
join
(
cmd_args
)
)
)
        
result
=
run
(
cmd_args
config
)
        
if
result
=
=
1
:
            
return
result
    
ignore_args
=
(
        
[
]
        
if
any
(
a
.
startswith
(
"
-
-
ignore
-
path
"
)
for
a
in
extra_args
)
        
else
[
"
-
-
ignore
-
path
=
.
prettierignore
"
"
-
-
ignore
-
path
=
.
prettierignore
-
css
"
]
    
)
    
cmd_args
=
(
        
[
            
binary
            
os
.
path
.
join
(
                
module_path
"
node_modules
"
"
prettier
"
"
bin
"
"
prettier
.
cjs
"
            
)
            
"
-
-
list
-
different
"
            
"
-
-
no
-
error
-
on
-
unmatched
-
pattern
"
        
]
        
+
list
(
filter
(
lambda
x
:
not
x
.
startswith
(
"
-
-
config
"
)
extra_args
)
)
        
+
ignore_args
        
+
paths
    
)
    
log
.
debug
(
"
Prettier
command
:
{
}
"
.
format
(
"
"
.
join
(
cmd_args
)
)
)
    
if
fix
:
        
cmd_args
.
append
(
"
-
-
write
"
)
    
prettier_result
=
prettier_utils
.
run_prettier
(
cmd_args
config
fix
)
    
if
prettier_result
=
=
1
:
        
return
prettier_result
    
result
[
"
results
"
]
.
extend
(
prettier_result
[
"
results
"
]
)
    
result
[
"
fixed
"
]
=
result
[
"
fixed
"
]
+
prettier_result
[
"
fixed
"
]
    
return
result
def
run
(
cmd_args
config
)
:
    
shell
=
False
    
if
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
        
print
(
ESLINT_ERROR_MESSAGE
.
format
(
errors
)
)
    
if
proc
.
returncode
>
=
2
:
        
return
1
    
if
not
output
:
        
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
    
try
:
        
jsonresult
=
json
.
loads
(
output
)
    
except
ValueError
:
        
print
(
ESLINT_ERROR_MESSAGE
.
format
(
output
)
)
        
return
1
    
results
=
[
]
    
fixed
=
0
    
for
obj
in
jsonresult
:
        
errors
=
obj
[
"
messages
"
]
        
if
"
output
"
in
obj
:
            
fixed
=
fixed
+
1
        
for
err
in
errors
:
            
err
.
update
(
                
{
                    
"
hint
"
:
err
.
get
(
"
fix
"
)
                    
"
level
"
:
"
error
"
if
err
[
"
severity
"
]
=
=
2
else
"
warning
"
                    
"
lineno
"
:
err
.
get
(
"
line
"
)
or
0
                    
"
path
"
:
obj
[
"
filePath
"
]
                    
"
rule
"
:
err
.
get
(
"
ruleId
"
)
                
}
            
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
err
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
