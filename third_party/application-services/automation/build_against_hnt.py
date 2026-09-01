import
argparse
import
subprocess
import
os
import
signal
import
tempfile
import
sys
from
pathlib
import
Path
from
shared
import
(
    
find_app_services_root
    
step_msg
    
err_msg
    
run_cmd_is_successful
    
dir_file_sanity_check
)
DEFAULT_MOZ_CONFIG_LOCATION
=
"
mozconfig_desktop
"
DEFAULT_MOZ_CONFIG
=
"
"
"
ac_add_options
-
-
enable
-
project
=
browser
"
"
"
MOZILLA_FF_GRADLE_PROPERTIES_PATH
=
"
gradle
.
properties
"
COMPONENTS_FOLDER_AS_SUBPATH
=
"
components
"
COMPONENTS_FOLDER_MC_SUBPATH
=
"
third_party
/
application
-
services
/
components
"
COMPONENTS_FOLDER_MC_SUBPATH_TMP
=
"
third_party
/
application
-
services
/
components_tmp
"
def
safe_exit
(
firefox_repo_path
)
:
    
step_msg
(
"
Exit
signal
caught
gracefully
exiting
.
.
.
"
)
    
clean_up_func
(
firefox_repo_path
)
    
step_msg
(
"
Exiting
.
.
.
"
)
    
sys
.
exit
(
0
)
def
clean_up_func
(
firefox_repo_path
)
:
    
symlink_src
=
firefox_repo_path
/
COMPONENTS_FOLDER_MC_SUBPATH
    
components_tmp_dir
=
firefox_repo_path
/
COMPONENTS_FOLDER_MC_SUBPATH_TMP
    
step_msg
(
"
Cleaning
up
restoring
symlinks
.
.
.
"
)
    
try
:
        
if
os
.
path
.
islink
(
symlink_src
)
and
os
.
path
.
isdir
(
components_tmp_dir
)
:
            
os
.
unlink
(
symlink_src
)
        
if
os
.
path
.
isdir
(
components_tmp_dir
)
:
            
os
.
rename
(
components_tmp_dir
symlink_src
)
    
except
OSError
:
        
err_msg
(
            
"
Failed
to
restore
the
m
-
c
state
.
Please
remove
the
symlink
and
return
the
'
components
'
directory
to
it
'
s
intended
spot
.
"
        
)
        
return
False
    
return
True
def
build_against_hnt
(
    
firefox_dir
    
moz_config_location
    
clean_up
    
hnt_test
    
verbose
    
action
)
:
    
firefox_repo_path
=
Path
(
firefox_dir
)
    
clean_up_func
(
firefox_repo_path
)
    
signal
.
signal
(
signal
.
SIGINT
lambda
_s
_h
:
safe_exit
(
firefox_repo_path
)
)
    
step_msg
(
"
Registered
sigint
trap
.
.
.
"
)
    
success
=
build_against_hnt_inner
(
        
firefox_dir
        
moz_config_location
        
hnt_test
        
verbose
        
action
    
)
    
if
success
:
        
step_msg
(
"
Finished
running
against
HNT
.
"
)
    
else
:
        
err_msg
(
"
Building
against
HNT
failed
.
"
)
    
if
clean_up
:
        
step_msg
(
"
Cleaning
up
.
.
.
"
)
        
clean_up_func
(
firefox_repo_path
)
    
else
:
        
step_msg
(
            
"
Skipping
cleanup
step
.
Rerunning
the
command
will
cleanup
before
recompiling
.
"
        
)
    
return
success
def
build_against_hnt_inner
(
    
firefox_dir
    
moz_config_location
    
hnt_test
    
verbose
    
action
)
:
    
subprocess_stdout
=
None
if
verbose
else
subprocess
.
DEVNULL
    
subprocess_stderr
=
None
if
verbose
else
subprocess
.
DEVNULL
    
if
action
is
None
:
        
action
=
"
run
-
tests
"
    
firefox_repo_path
=
Path
(
firefox_dir
)
    
tmp_dir_path
=
Path
(
tempfile
.
mkdtemp
(
suffix
=
"
-
test
-
hnt
"
)
)
    
app_services_path
=
find_app_services_root
(
)
    
step_msg
(
"
Checking
for
sanity
of
application
-
services
repository
.
.
.
"
)
    
if
not
dir_file_sanity_check
(
        
app_services_path
"
application
-
services
"
[
"
megazords
"
"
components
"
]
    
)
:
        
return
False
    
if
moz_config_location
is
None
:
        
moz_config_location
=
os
.
path
.
abspath
(
            
tmp_dir_path
/
DEFAULT_MOZ_CONFIG_LOCATION
        
)
        
with
open
(
moz_config_location
"
w
"
)
as
file
:
            
file
.
write
(
DEFAULT_MOZ_CONFIG
)
    
if
not
os
.
path
.
isabs
(
moz_config_location
)
:
        
err_msg
(
            
f
"
mozconfig
path
passed
:
{
moz_config_location
}
must
be
an
absolute
path
.
"
        
)
        
return
False
    
if
not
os
.
path
.
isfile
(
moz_config_location
)
:
        
err_msg
(
f
"
mozconfig
path
passed
:
{
moz_config_location
}
could
not
be
found
.
"
)
        
return
False
    
step_msg
(
f
"
Using
mozconfig
path
:
{
moz_config_location
}
.
Displaying
:
"
)
    
with
open
(
moz_config_location
)
as
f
:
        
print
(
f
.
read
(
)
)
    
step_msg
(
"
Checking
for
sanity
of
firefox
repository
.
.
.
"
)
    
if
not
dir_file_sanity_check
(
        
firefox_repo_path
        
"
mozilla
-
central
"
        
[
"
mach
"
"
CLOBBER
"
"
gradlew
"
"
Cargo
.
toml
"
"
local
.
properties
"
]
    
)
:
        
return
False
    
step_msg
(
"
Verifying
Desktop
environment
.
.
.
"
)
    
if
not
run_cmd_is_successful
(
        
"
.
/
libs
/
verify
-
desktop
-
environment
.
sh
"
        
cwd
=
app_services_path
        
shell
=
True
        
stdout
=
subprocess_stdout
        
stderr
=
subprocess_stderr
    
)
:
        
err_msg
(
            
"
Failed
to
run
.
/
libs
/
verify
-
android
-
environment
.
sh
in
app
-
services
environment
.
Run
this
script
and
follow
any
instructions
given
until
it
succeeds
then
try
again
.
"
        
)
        
return
False
    
symlink_dest
=
app_services_path
/
COMPONENTS_FOLDER_AS_SUBPATH
    
symlink_src
=
firefox_repo_path
/
COMPONENTS_FOLDER_MC_SUBPATH
    
components_tmp_dir
=
firefox_repo_path
/
COMPONENTS_FOLDER_MC_SUBPATH_TMP
    
step_msg
(
f
"
Creating
symlink
in
{
firefox_repo_path
}
to
link
to
local
appservices
"
)
    
os
.
rename
(
symlink_src
components_tmp_dir
)
    
os
.
symlink
(
symlink_dest
symlink_src
)
    
step_msg
(
"
Regenerating
uniffi
bindings
(
mozconfig
=
{
moz_config_location
}
)
.
.
.
"
)
    
if
not
run_cmd_is_successful
(
        
"
.
/
mach
uniffi
generate
"
        
cwd
=
firefox_repo_path
        
shell
=
True
        
stdout
=
subprocess_stdout
    
)
:
        
err_msg
(
"
Failed
to
generate
uniffi
bindings
with
:
.
/
mach
uniffi
generate
/
"
)
        
return
False
    
step_msg
(
        
f
"
Compiling
firefox
with
.
/
mach
build
(
mozconfig
=
{
moz_config_location
}
)
.
.
.
"
    
)
    
if
not
run_cmd_is_successful
(
        
f
"
MOZCONFIG
=
{
moz_config_location
}
.
/
mach
build
"
        
cwd
=
firefox_repo_path
        
shell
=
True
        
stdout
=
subprocess_stdout
    
)
:
        
err_msg
(
"
Failed
to
compile
firefox
with
.
/
mach
build
.
"
)
        
return
False
    
if
action
=
=
"
run
-
tests
"
:
        
step_msg
(
            
f
"
Compiling
firefox
with
mozconfig
with
.
/
mach
test
(
mozconfig
=
{
moz_config_location
}
)
.
.
.
"
        
)
        
test_string
=
hnt_test
if
hnt_test
is
not
None
else
"
-
-
auto
"
        
step_msg
(
f
"
Running
test
command
.
/
mach
test
{
test_string
}
"
)
        
if
not
run_cmd_is_successful
(
            
f
"
MOZCONFIG
=
{
moz_config_location
}
.
/
mach
test
{
test_string
}
"
            
cwd
=
firefox_repo_path
            
shell
=
True
            
stdout
=
subprocess_stdout
        
)
:
            
err_msg
(
f
"
Failed
to
run
tests
against
firefox
with
.
/
mach
test
{
test_string
}
.
"
)
            
return
False
    
elif
action
=
=
"
run
"
:
        
step_msg
(
            
f
"
Running
firefox
with
mozconfig
with
.
/
mach
run
(
mozconfig
=
{
moz_config_location
}
)
.
.
.
"
        
)
        
if
not
run_cmd_is_successful
(
            
f
"
MOZCONFIG
=
{
moz_config_location
}
.
/
mach
run
"
            
cwd
=
firefox_repo_path
            
shell
=
True
            
stdout
=
subprocess_stdout
        
)
:
            
err_msg
(
"
Failed
to
run
tests
against
firefox
with
.
/
mach
run
.
"
)
            
return
False
    
step_msg
(
"
Successfully
built
against
HNT
!
"
)
    
return
True
if
__name__
=
=
"
__main__
"
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Run
Firefox
HNT
tests
against
this
application
-
services
working
tree
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
verbose
"
        
help
=
"
Display
subprocess
logs
for
compilation
processes
(
off
by
default
)
.
"
        
action
=
argparse
.
BooleanOptionalAction
    
)
    
parser
.
add_argument
(
        
"
-
-
action
"
        
choices
=
[
"
run
"
"
run
-
tests
"
"
build
-
without
-
testing
"
]
        
help
=
"
Whether
to
run
tests
after
the
build
step
is
complete
.
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
firefox
-
dir
"
        
required
=
True
        
help
=
"
Path
to
existing
bootstrapped
mozilla
-
central
directory
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
mozconfig
"
        
help
=
"
Absolute
path
to
the
desired
mozconfig
file
.
This
affects
the
build
destination
ensure
it
specifies
android
if
you
override
it
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
hnt
-
test
"
        
help
=
"
Name
of
the
test
file
to
run
as
if
you
were
running
.
/
mach
test
ARG
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
clean
-
up
"
        
help
=
"
Skip
the
on
-
success
cleanup
step
done
at
the
end
of
a
successful
build
.
This
does
not
skip
the
cleanup
step
if
there
is
an
error
or
graceful
exit
(
such
as
with
-
-
action
run
)
.
"
        
action
=
argparse
.
BooleanOptionalAction
        
default
=
True
    
)
    
args
=
parser
.
parse_args
(
)
    
firefox_dir
=
args
.
firefox_dir
    
verbose
=
args
.
verbose
    
moz_config_location
=
args
.
mozconfig
    
action
=
args
.
action
    
clean_up
=
args
.
clean_up
    
hnt_test
=
args
.
hnt_test
    
build_against_hnt
(
firefox_dir
moz_config_location
clean_up
hnt_test
verbose
action
)
