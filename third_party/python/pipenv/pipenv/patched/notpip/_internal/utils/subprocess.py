from
__future__
import
absolute_import
import
logging
import
os
import
subprocess
from
pipenv
.
patched
.
notpip
.
_vendor
.
six
.
moves
import
shlex_quote
from
pipenv
.
patched
.
notpip
.
_internal
.
exceptions
import
InstallationError
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
compat
import
console_to_str
str_to_display
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
logging
import
subprocess_logger
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
misc
import
HiddenText
path_to_display
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
ui
import
open_spinner
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
(
        
Any
Callable
Iterable
List
Mapping
Optional
Text
Union
    
)
    
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
ui
import
SpinnerInterface
    
CommandArgs
=
List
[
Union
[
str
HiddenText
]
]
LOG_DIVIDER
=
'
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
'
def
make_command
(
*
args
)
:
    
"
"
"
    
Create
a
CommandArgs
object
.
    
"
"
"
    
command_args
=
[
]
    
for
arg
in
args
:
        
if
isinstance
(
arg
list
)
:
            
command_args
.
extend
(
arg
)
        
else
:
            
command_args
.
append
(
arg
)
    
return
command_args
def
format_command_args
(
args
)
:
    
"
"
"
    
Format
command
arguments
for
display
.
    
"
"
"
    
return
'
'
.
join
(
        
shlex_quote
(
str
(
arg
)
)
if
isinstance
(
arg
HiddenText
)
        
else
shlex_quote
(
arg
)
for
arg
in
args
    
)
def
reveal_command_args
(
args
)
:
    
"
"
"
    
Return
the
arguments
in
their
raw
unredacted
form
.
    
"
"
"
    
return
[
        
arg
.
secret
if
isinstance
(
arg
HiddenText
)
else
arg
for
arg
in
args
    
]
def
make_subprocess_output_error
(
    
cmd_args
    
cwd
    
lines
    
exit_status
)
:
    
"
"
"
    
Create
and
return
the
error
message
to
use
to
log
a
subprocess
error
    
with
command
output
.
    
:
param
lines
:
A
list
of
lines
each
ending
with
a
newline
.
    
"
"
"
    
command
=
format_command_args
(
cmd_args
)
    
command_display
=
str_to_display
(
command
desc
=
'
command
bytes
'
)
    
cwd_display
=
path_to_display
(
cwd
)
    
output
=
'
'
.
join
(
lines
)
    
msg
=
(
        
u
'
Command
errored
out
with
exit
status
{
exit_status
}
:
\
n
'
        
'
command
:
{
command_display
}
\
n
'
        
'
cwd
:
{
cwd_display
}
\
n
'
        
'
Complete
output
(
{
line_count
}
lines
)
:
\
n
{
output
}
{
divider
}
'
    
)
.
format
(
        
exit_status
=
exit_status
        
command_display
=
command_display
        
cwd_display
=
cwd_display
        
line_count
=
len
(
lines
)
        
output
=
output
        
divider
=
LOG_DIVIDER
    
)
    
return
msg
def
call_subprocess
(
    
cmd
    
show_stdout
=
False
    
cwd
=
None
    
on_returncode
=
'
raise
'
    
extra_ok_returncodes
=
None
    
command_desc
=
None
    
extra_environ
=
None
    
unset_environ
=
None
    
spinner
=
None
    
log_failed_cmd
=
True
)
:
    
"
"
"
    
Args
:
      
show_stdout
:
if
true
use
INFO
to
log
the
subprocess
'
s
stderr
and
        
stdout
streams
.
Otherwise
use
DEBUG
.
Defaults
to
False
.
      
extra_ok_returncodes
:
an
iterable
of
integer
return
codes
that
are
        
acceptable
in
addition
to
0
.
Defaults
to
None
which
means
[
]
.
      
unset_environ
:
an
iterable
of
environment
variable
names
to
unset
        
prior
to
calling
subprocess
.
Popen
(
)
.
      
log_failed_cmd
:
if
false
failed
commands
are
not
logged
only
raised
.
    
"
"
"
    
if
extra_ok_returncodes
is
None
:
        
extra_ok_returncodes
=
[
]
    
if
unset_environ
is
None
:
        
unset_environ
=
[
]
    
if
show_stdout
:
        
log_subprocess
=
subprocess_logger
.
info
        
used_level
=
logging
.
INFO
    
else
:
        
log_subprocess
=
subprocess_logger
.
debug
        
used_level
=
logging
.
DEBUG
    
showing_subprocess
=
subprocess_logger
.
getEffectiveLevel
(
)
<
=
used_level
    
use_spinner
=
not
showing_subprocess
and
spinner
is
not
None
    
if
command_desc
is
None
:
        
command_desc
=
format_command_args
(
cmd
)
    
log_subprocess
(
"
Running
command
%
s
"
command_desc
)
    
env
=
os
.
environ
.
copy
(
)
    
if
extra_environ
:
        
env
.
update
(
extra_environ
)
    
for
name
in
unset_environ
:
        
env
.
pop
(
name
None
)
    
try
:
        
proc
=
subprocess
.
Popen
(
            
reveal_command_args
(
cmd
)
            
stderr
=
subprocess
.
STDOUT
stdin
=
subprocess
.
PIPE
            
stdout
=
subprocess
.
PIPE
cwd
=
cwd
env
=
env
        
)
        
proc
.
stdin
.
close
(
)
    
except
Exception
as
exc
:
        
if
log_failed_cmd
:
            
subprocess_logger
.
critical
(
                
"
Error
%
s
while
executing
command
%
s
"
exc
command_desc
            
)
        
raise
    
all_output
=
[
]
    
while
True
:
        
line
=
console_to_str
(
proc
.
stdout
.
readline
(
)
)
        
if
not
line
:
            
break
        
line
=
line
.
rstrip
(
)
        
all_output
.
append
(
line
+
'
\
n
'
)
        
log_subprocess
(
line
)
        
if
use_spinner
:
            
spinner
.
spin
(
)
    
try
:
        
proc
.
wait
(
)
    
finally
:
        
if
proc
.
stdout
:
            
proc
.
stdout
.
close
(
)
    
proc_had_error
=
(
        
proc
.
returncode
and
proc
.
returncode
not
in
extra_ok_returncodes
    
)
    
if
use_spinner
:
        
if
proc_had_error
:
            
spinner
.
finish
(
"
error
"
)
        
else
:
            
spinner
.
finish
(
"
done
"
)
    
if
proc_had_error
:
        
if
on_returncode
=
=
'
raise
'
:
            
if
not
showing_subprocess
and
log_failed_cmd
:
                
msg
=
make_subprocess_output_error
(
                    
cmd_args
=
cmd
                    
cwd
=
cwd
                    
lines
=
all_output
                    
exit_status
=
proc
.
returncode
                
)
                
subprocess_logger
.
error
(
msg
)
            
exc_msg
=
(
                
'
Command
errored
out
with
exit
status
{
}
:
{
}
'
                
'
Check
the
logs
for
full
command
output
.
'
            
)
.
format
(
proc
.
returncode
command_desc
)
            
raise
InstallationError
(
exc_msg
)
        
elif
on_returncode
=
=
'
warn
'
:
            
subprocess_logger
.
warning
(
                
'
Command
"
%
s
"
had
error
code
%
s
in
%
s
'
                
command_desc
proc
.
returncode
cwd
            
)
        
elif
on_returncode
=
=
'
ignore
'
:
            
pass
        
else
:
            
raise
ValueError
(
'
Invalid
value
:
on_returncode
=
%
s
'
%
                             
repr
(
on_returncode
)
)
    
return
'
'
.
join
(
all_output
)
def
runner_with_spinner_message
(
message
)
:
    
"
"
"
Provide
a
subprocess_runner
that
shows
a
spinner
message
.
    
Intended
for
use
with
for
pep517
'
s
Pep517HookCaller
.
Thus
the
runner
has
    
an
API
that
matches
what
'
s
expected
by
Pep517HookCaller
.
subprocess_runner
.
    
"
"
"
    
def
runner
(
        
cmd
        
cwd
=
None
        
extra_environ
=
None
    
)
:
        
with
open_spinner
(
message
)
as
spinner
:
            
call_subprocess
(
                
cmd
                
cwd
=
cwd
                
extra_environ
=
extra_environ
                
spinner
=
spinner
            
)
    
return
runner
