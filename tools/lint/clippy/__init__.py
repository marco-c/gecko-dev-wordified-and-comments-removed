import
json
import
os
import
signal
import
subprocess
from
mozfile
import
which
from
mozlint
import
result
from
mozlint
.
pathutils
import
get_ancestors_by_name
from
mozprocess
import
ProcessHandler
CLIPPY_NOT_FOUND
=
"
"
"
Could
not
find
clippy
!
Install
clippy
and
try
again
.
    
rustup
component
add
clippy
And
make
sure
that
it
is
in
the
PATH
"
"
"
.
strip
(
)
CARGO_NOT_FOUND
=
"
"
"
Could
not
find
cargo
!
Install
cargo
.
And
make
sure
that
it
is
in
the
PATH
"
"
"
.
strip
(
)
def
parse_issues
(
log
config
issues
path
onlyIn
)
:
    
results
=
[
]
    
for
issue
in
issues
:
        
try
:
            
detail
=
json
.
loads
(
issue
.
decode
(
"
utf
-
8
"
)
)
            
if
"
message
"
in
detail
:
                
p
=
detail
[
'
target
'
]
[
'
src_path
'
]
                
detail
=
detail
[
"
message
"
]
                
if
"
level
"
in
detail
:
                    
if
(
(
detail
[
"
level
"
]
=
=
"
error
"
or
detail
[
"
level
"
]
=
=
"
failure
-
note
"
)
                        
and
not
detail
[
"
code
"
]
)
:
                        
log
.
debug
(
"
Error
outside
of
clippy
.
"
                                  
"
This
means
that
the
build
failed
.
Therefore
skipping
this
"
)
                        
log
.
debug
(
"
File
=
{
}
/
Detail
=
{
}
"
.
format
(
p
detail
)
)
                        
continue
                    
l
=
detail
[
"
spans
"
]
[
0
]
                    
if
onlyIn
and
onlyIn
not
in
p
:
                        
log
.
debug
(
"
{
}
is
not
part
of
the
list
of
files
'
{
}
'
"
.
format
(
p
onlyIn
)
)
                        
continue
                    
res
=
{
                        
"
path
"
:
p
                        
"
level
"
:
detail
[
"
level
"
]
                        
"
lineno
"
:
l
[
"
line_start
"
]
                        
"
column
"
:
l
[
"
column_start
"
]
                        
"
message
"
:
detail
[
"
message
"
]
                        
"
hint
"
:
detail
[
"
rendered
"
]
                        
"
rule
"
:
detail
[
"
code
"
]
[
"
code
"
]
                        
"
lineoffset
"
:
l
[
"
line_end
"
]
-
l
[
"
line_start
"
]
                    
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
json
.
decoder
.
JSONDecodeError
:
            
log
.
debug
(
"
clippy
output
:
{
}
"
.
format
(
issue
)
)
            
continue
    
return
results
def
get_cargo_binary
(
)
:
    
"
"
"
    
Returns
the
path
of
the
first
rustfmt
binary
available
    
if
not
found
returns
None
    
"
"
"
    
cargo_home
=
os
.
environ
.
get
(
"
CARGO_HOME
"
)
    
if
cargo_home
:
        
cargo_bin
=
os
.
path
.
join
(
cargo_home
"
bin
"
"
cargo
"
)
        
if
os
.
path
.
exists
(
cargo_bin
)
:
            
return
cargo_bin
        
else
:
            
return
None
    
return
which
(
"
cargo
"
)
def
is_clippy_installed
(
binary
)
:
    
"
"
"
    
Check
if
we
are
running
the
deprecated
rustfmt
    
"
"
"
    
try
:
        
output
=
subprocess
.
check_output
(
            
[
binary
"
clippy
"
"
-
-
help
"
]
            
stderr
=
subprocess
.
STDOUT
            
universal_newlines
=
True
        
)
    
except
subprocess
.
CalledProcessError
as
e
:
        
output
=
e
.
output
    
if
"
Checks
a
package
"
in
output
:
        
return
True
    
return
False
class
clippyProcess
(
ProcessHandler
)
:
    
def
__init__
(
self
config
*
args
*
*
kwargs
)
:
        
self
.
config
=
config
        
kwargs
[
"
stream
"
]
=
False
        
ProcessHandler
.
__init__
(
self
*
args
*
*
kwargs
)
    
def
run
(
self
*
args
*
*
kwargs
)
:
        
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
        
ProcessHandler
.
run
(
self
*
args
*
*
kwargs
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
def
run_process
(
log
config
cmd
)
:
    
log
.
debug
(
"
Command
:
{
}
"
.
format
(
cmd
)
)
    
proc
=
clippyProcess
(
config
cmd
)
    
proc
.
run
(
)
    
try
:
        
proc
.
wait
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
proc
.
output
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
    
log
=
lintargs
[
"
log
"
]
    
cargo
=
get_cargo_binary
(
)
    
if
not
cargo
:
        
print
(
CARGO_NOT_FOUND
)
        
if
'
MOZ_AUTOMATION
'
in
os
.
environ
:
            
return
1
        
return
[
]
    
if
not
is_clippy_installed
(
cargo
)
:
        
print
(
CLIPPY_NOT_FOUND
)
        
if
'
MOZ_AUTOMATION
'
in
os
.
environ
:
            
return
1
        
return
[
]
    
cmd_args_clean
=
[
cargo
]
    
cmd_args_clean
.
append
(
"
clean
"
)
    
cmd_args_common
=
[
"
-
-
manifest
-
path
"
]
    
cmd_args_clippy
=
[
        
cargo
        
'
clippy
'
        
'
-
-
message
-
format
=
json
'
    
]
    
results
=
[
]
    
for
p
in
paths
:
        
if
p
.
endswith
(
"
Cargo
.
toml
"
)
:
            
print
(
"
Error
:
expects
a
directory
or
a
rs
file
"
)
            
print
(
"
Found
{
}
"
.
format
(
p
)
)
            
return
1
    
for
p
in
paths
:
        
onlyIn
=
[
]
        
path_conf
=
p
        
log
.
debug
(
"
Path
=
{
}
"
.
format
(
p
)
)
        
if
os
.
path
.
isfile
(
p
)
:
            
p
=
os
.
path
.
dirname
(
p
)
            
onlyIn
=
path_conf
        
if
os
.
path
.
isdir
(
p
)
:
            
onlyIn
=
p
        
cargo_files
=
get_ancestors_by_name
(
'
Cargo
.
toml
'
p
lintargs
[
'
root
'
]
)
        
p
=
cargo_files
[
0
]
        
log
.
debug
(
"
Path
translated
to
=
{
}
"
.
format
(
p
)
)
        
clean_command
=
cmd_args_clean
+
cmd_args_common
+
[
p
]
        
run_process
(
log
config
clean_command
)
        
base_command
=
cmd_args_clippy
+
cmd_args_common
+
[
p
]
        
output
=
run_process
(
log
config
base_command
)
        
results
+
=
parse_issues
(
log
config
output
p
onlyIn
)
    
return
sorted
(
results
key
=
lambda
issue
:
issue
.
path
)
