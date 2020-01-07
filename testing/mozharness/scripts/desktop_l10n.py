"
"
"
desktop_l10n
.
py
This
script
manages
Desktop
repacks
for
nightly
builds
.
"
"
"
import
os
import
glob
import
re
import
sys
import
shlex
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
sys
.
path
[
0
]
)
)
from
mozharness
.
base
.
errors
import
MakefileErrorList
from
mozharness
.
base
.
script
import
BaseScript
from
mozharness
.
base
.
vcs
.
vcsbase
import
VCSMixin
from
mozharness
.
mozilla
.
automation
import
AutomationMixin
from
mozharness
.
mozilla
.
building
.
buildbase
import
(
    
MakeUploadOutputParser
    
get_mozconfig_path
)
from
mozharness
.
mozilla
.
l10n
.
locales
import
LocalesMixin
from
mozharness
.
mozilla
.
mar
import
MarMixin
try
:
    
import
simplejson
as
json
    
assert
json
except
ImportError
:
    
import
json
SUCCESS
=
0
FAILURE
=
1
SUCCESS_STR
=
"
Success
"
FAILURE_STR
=
"
Failed
"
configuration_tokens
=
(
'
branch
'
'
update_channel
'
)
runtime_config_tokens
=
(
'
version
'
'
locale
'
'
abs_objdir
'
'
revision
'
                         
'
en_us_installer_binary_url
'
)
class
DesktopSingleLocale
(
LocalesMixin
AutomationMixin
                          
VCSMixin
BaseScript
MarMixin
)
:
    
"
"
"
Manages
desktop
repacks
"
"
"
    
config_options
=
[
[
        
[
'
-
-
locale
'
]
        
{
"
action
"
:
"
extend
"
         
"
dest
"
:
"
locales
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Specify
the
locale
(
s
)
to
sign
and
update
.
Optionally
pass
"
                 
"
revision
separated
by
colon
en
-
GB
:
default
.
"
}
    
]
[
        
[
'
-
-
tag
-
override
'
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
tag_override
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Override
the
tags
set
for
all
repos
"
}
    
]
[
        
[
'
-
-
revision
'
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
revision
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Override
the
gecko
revision
to
use
(
otherwise
use
automation
supplied
"
                 
"
value
or
en
-
US
revision
)
"
}
    
]
[
        
[
'
-
-
en
-
us
-
installer
-
url
'
]
        
{
"
action
"
:
"
store
"
         
"
dest
"
:
"
en_us_installer_url
"
         
"
type
"
:
"
string
"
         
"
help
"
:
"
Specify
the
url
of
the
en
-
us
binary
"
}
    
]
[
        
[
'
-
-
scm
-
level
'
]
{
         
"
action
"
:
"
store
"
         
"
type
"
:
"
int
"
         
"
dest
"
:
"
scm_level
"
         
"
default
"
:
1
         
"
help
"
:
"
This
sets
the
SCM
level
for
the
branch
being
built
.
"
                 
"
See
https
:
/
/
www
.
mozilla
.
org
/
en
-
US
/
about
/
"
                 
"
governance
/
policies
/
commit
/
access
-
policy
/
"
}
    
]
]
    
def
__init__
(
self
require_config_file
=
True
)
:
        
buildscript_kwargs
=
{
            
'
all_actions
'
:
[
                
"
clone
-
locales
"
                
"
list
-
locales
"
                
"
setup
"
                
"
repack
"
                
"
summary
"
            
]
            
'
config
'
:
{
                
"
ignore_locales
"
:
[
"
en
-
US
"
]
                
"
locales_dir
"
:
"
browser
/
locales
"
                
"
log_name
"
:
"
single_locale
"
            
}
        
}
        
LocalesMixin
.
__init__
(
self
)
        
BaseScript
.
__init__
(
            
self
            
config_options
=
self
.
config_options
            
require_config_file
=
require_config_file
            
*
*
buildscript_kwargs
        
)
        
self
.
bootstrap_env
=
None
        
self
.
upload_env
=
None
        
self
.
revision
=
None
        
self
.
version
=
None
        
self
.
upload_urls
=
{
}
        
self
.
locales_property
=
{
}
        
self
.
pushdate
=
None
        
self
.
upload_files
=
{
}
    
def
_pre_config_lock
(
self
rw_config
)
:
        
"
"
"
replaces
'
configuration_tokens
'
with
their
values
before
the
           
configuration
gets
locked
.
If
some
of
the
configuration_tokens
           
are
not
present
stops
the
execution
of
the
script
"
"
"
        
for
token
in
configuration_tokens
:
            
if
token
not
in
self
.
config
:
                
self
.
fatal
(
'
No
%
s
in
configuration
!
'
%
token
)
        
for
token
in
configuration_tokens
:
            
token_string
=
'
'
.
join
(
(
'
%
(
'
token
'
)
s
'
)
)
            
token_value
=
self
.
config
[
token
]
            
for
element
in
self
.
config
:
                
old_value
=
self
.
config
[
element
]
                
new_value
=
self
.
__detokenise_element
(
self
.
config
[
element
]
                                                      
token_string
                                                      
token_value
)
                
if
new_value
and
new_value
!
=
old_value
:
                    
msg
=
"
%
s
:
replacing
%
s
with
%
s
"
%
(
element
                                                        
old_value
                                                        
new_value
)
                    
self
.
debug
(
msg
)
                    
self
.
config
[
element
]
=
new_value
        
tokens_left
=
set
(
self
.
_get_configuration_tokens
(
self
.
config
)
)
        
unknown_tokens
=
set
(
tokens_left
)
-
set
(
runtime_config_tokens
)
        
if
unknown_tokens
:
            
msg
=
[
'
unknown
tokens
in
configuration
:
'
]
            
for
t
in
unknown_tokens
:
                
msg
.
append
(
t
)
            
self
.
fatal
(
'
'
.
join
(
msg
)
)
        
self
.
info
(
'
configuration
looks
ok
'
)
        
return
    
def
_get_configuration_tokens
(
self
iterable
)
:
        
"
"
"
gets
a
list
of
tokens
in
iterable
"
"
"
        
regex
=
re
.
compile
(
'
%
\
(
\
w
+
\
)
s
'
)
        
results
=
[
]
        
try
:
            
for
element
in
iterable
:
                
if
isinstance
(
iterable
str
)
:
                    
tokens
=
re
.
findall
(
regex
iterable
)
                    
for
token
in
tokens
:
                        
token_name
=
token
.
partition
(
'
%
(
'
)
[
2
]
                        
token_name
=
token_name
.
partition
(
'
)
s
'
)
[
0
]
                        
results
.
append
(
token_name
)
                    
break
                
elif
isinstance
(
iterable
(
list
tuple
)
)
:
                    
results
.
extend
(
self
.
_get_configuration_tokens
(
element
)
)
                
elif
isinstance
(
iterable
dict
)
:
                    
results
.
extend
(
self
.
_get_configuration_tokens
(
iterable
[
element
]
)
)
        
except
TypeError
:
            
pass
        
return
list
(
set
(
results
)
)
    
def
__detokenise_element
(
self
config_option
token
value
)
:
        
"
"
"
reads
config_options
and
returns
a
version
of
the
same
config_option
           
replacing
token
with
value
recursively
"
"
"
        
if
isinstance
(
config_option
str
)
:
            
return
config_option
.
replace
(
token
value
)
        
elif
isinstance
(
config_option
dict
)
:
            
for
element
in
config_option
:
                
config_option
[
element
]
=
self
.
__detokenise_element
(
                    
config_option
[
element
]
token
value
)
            
return
config_option
        
elif
isinstance
(
config_option
list
)
:
            
new_list
=
[
]
            
for
element
in
config_option
:
                
new_list
.
append
(
self
.
__detokenise_element
(
element
token
value
)
)
            
return
new_list
        
elif
isinstance
(
config_option
tuple
)
:
            
new_list
=
[
]
            
for
element
in
config_option
:
                
new_list
.
append
(
self
.
__detokenise_element
(
element
token
value
)
)
            
return
tuple
(
new_list
)
        
else
:
            
return
config_option
    
def
query_bootstrap_env
(
self
)
:
        
"
"
"
returns
the
env
for
repacks
"
"
"
        
if
self
.
bootstrap_env
:
            
return
self
.
bootstrap_env
        
config
=
self
.
config
        
replace_dict
=
self
.
query_abs_dirs
(
)
        
bootstrap_env
=
self
.
query_env
(
partial_env
=
config
.
get
(
"
bootstrap_env
"
)
                                       
replace_dict
=
replace_dict
)
        
for
binary
in
self
.
_mar_binaries
(
)
:
            
name
=
binary
.
replace
(
'
.
exe
'
'
'
)
            
name
=
name
.
upper
(
)
            
binary_path
=
os
.
path
.
join
(
self
.
_mar_tool_dir
(
)
binary
)
            
if
binary
.
endswith
(
'
.
exe
'
)
:
                
binary_path
=
binary_path
.
replace
(
'
\
\
'
'
\
\
\
\
\
\
\
\
'
)
            
bootstrap_env
[
name
]
=
binary_path
        
if
self
.
query_is_nightly
(
)
:
            
bootstrap_env
[
"
IS_NIGHTLY
"
]
=
"
yes
"
        
self
.
bootstrap_env
=
bootstrap_env
        
return
self
.
bootstrap_env
    
def
_query_upload_env
(
self
)
:
        
"
"
"
returns
the
environment
used
for
the
upload
step
"
"
"
        
if
self
.
upload_env
:
            
return
self
.
upload_env
        
config
=
self
.
config
        
upload_env
=
self
.
query_env
(
partial_env
=
config
.
get
(
"
upload_env
"
)
)
        
if
'
upload_env_extra
'
in
config
:
            
for
extra
in
config
[
'
upload_env_extra
'
]
:
                
upload_env
[
extra
]
=
config
[
'
upload_env_extra
'
]
[
extra
]
        
self
.
upload_env
=
upload_env
        
return
self
.
upload_env
    
def
query_l10n_env
(
self
)
:
        
l10n_env
=
self
.
_query_upload_env
(
)
.
copy
(
)
        
l10n_env
.
update
(
self
.
query_bootstrap_env
(
)
)
        
return
l10n_env
    
def
_query_revision
(
self
)
:
        
"
"
"
Get
the
gecko
revision
in
this
order
of
precedence
              
*
cached
value
              
*
command
line
arg
-
-
revision
(
development
taskcluster
)
              
*
from
the
en
-
US
build
(
m
-
c
&
m
-
a
)
        
This
will
fail
the
last
case
if
the
build
hasn
'
t
been
pulled
yet
.
        
"
"
"
        
if
self
.
revision
:
            
return
self
.
revision
        
config
=
self
.
config
        
revision
=
None
        
if
config
.
get
(
"
revision
"
)
:
            
revision
=
config
[
"
revision
"
]
        
if
not
revision
:
            
self
.
fatal
(
"
Can
'
t
determine
revision
!
"
)
        
self
.
revision
=
str
(
revision
)
        
return
self
.
revision
    
def
_query_make_variable
(
self
variable
make_args
=
None
)
:
        
"
"
"
returns
the
value
of
make
echo
-
variable
-
<
variable
>
           
it
accepts
extra
make
arguements
(
make_args
)
        
"
"
"
        
dirs
=
self
.
query_abs_dirs
(
)
        
make_args
=
make_args
or
[
]
        
target
=
[
"
echo
-
variable
-
%
s
"
%
variable
]
+
make_args
        
cwd
=
dirs
[
'
abs_locales_dir
'
]
        
raw_output
=
self
.
_get_output_from_make
(
target
cwd
=
cwd
                                                
env
=
self
.
query_bootstrap_env
(
)
)
        
output
=
[
]
        
for
line
in
raw_output
.
split
(
"
\
n
"
)
:
            
output
.
append
(
line
.
strip
(
)
)
        
output
=
"
"
.
join
(
output
)
.
strip
(
)
        
self
.
info
(
'
echo
-
variable
-
%
s
:
%
s
'
%
(
variable
output
)
)
        
return
output
    
def
query_version
(
self
)
:
        
"
"
"
Gets
the
version
from
the
objdir
.
        
Only
valid
after
setup
is
run
.
"
"
"
        
if
self
.
version
:
            
return
self
.
version
        
self
.
version
=
self
.
_query_make_variable
(
"
MOZ_APP_VERSION
"
)
        
return
self
.
version
    
def
_map
(
self
func
items
)
:
        
"
"
"
runs
func
for
any
item
in
items
calls
the
add_failure
(
)
for
each
           
error
.
It
assumes
that
function
returns
0
when
successful
.
           
returns
a
two
element
tuple
with
(
success_count
total_count
)
"
"
"
        
success_count
=
0
        
total_count
=
len
(
items
)
        
name
=
func
.
__name__
        
for
item
in
items
:
            
result
=
func
(
item
)
            
if
result
=
=
SUCCESS
:
                
success_count
+
=
1
            
else
:
                
message
=
'
failure
:
%
s
(
%
s
)
'
%
(
name
item
)
                
self
.
_add_failure
(
item
message
)
        
return
(
success_count
total_count
)
    
def
_add_failure
(
self
locale
message
*
*
kwargs
)
:
        
"
"
"
marks
current
step
as
failed
"
"
"
        
self
.
locales_property
[
locale
]
=
FAILURE_STR
        
prop_key
=
"
%
s_failure
"
%
locale
        
prop_value
=
self
.
query_property
(
prop_key
)
        
if
prop_value
:
            
prop_value
=
"
%
s
%
s
"
%
(
prop_value
message
)
        
else
:
            
prop_value
=
message
        
self
.
set_property
(
prop_key
prop_value
)
        
BaseScript
.
add_failure
(
self
locale
message
=
message
                               
increment_return_code
=
False
*
*
kwargs
)
    
def
query_failed_locales
(
self
)
:
        
return
[
l
for
l
res
in
self
.
locales_property
.
items
(
)
if
                
res
=
=
FAILURE_STR
]
    
def
summary
(
self
)
:
        
"
"
"
generates
a
summary
"
"
"
        
BaseScript
.
summary
(
self
)
        
locales
=
self
.
query_locales
(
)
        
for
locale
in
locales
:
            
self
.
locales_property
.
setdefault
(
locale
SUCCESS_STR
)
        
self
.
set_property
(
"
locales
"
json
.
dumps
(
self
.
locales_property
)
)
    
def
clone_locales
(
self
)
:
        
self
.
pull_locale_source
(
)
    
def
setup
(
self
)
:
        
"
"
"
setup
step
"
"
"
        
self
.
_run_tooltool
(
)
        
self
.
_copy_mozconfig
(
)
        
self
.
_mach_configure
(
)
        
self
.
_run_make_in_config_dir
(
)
        
self
.
make_wget_en_US
(
)
        
self
.
make_unpack_en_US
(
)
        
self
.
download_mar_tools
(
)
    
def
_run_make_in_config_dir
(
self
)
:
        
"
"
"
this
step
creates
nsinstall
needed
my
make_wget_en_US
(
)
        
"
"
"
        
dirs
=
self
.
query_abs_dirs
(
)
        
config_dir
=
os
.
path
.
join
(
dirs
[
'
abs_objdir
'
]
'
config
'
)
        
env
=
self
.
query_bootstrap_env
(
)
        
return
self
.
_make
(
target
=
[
'
export
'
]
cwd
=
config_dir
env
=
env
)
    
def
_copy_mozconfig
(
self
)
:
        
"
"
"
copies
the
mozconfig
file
into
abs_mozilla_dir
/
.
mozconfig
           
and
logs
the
content
        
"
"
"
        
config
=
self
.
config
        
dirs
=
self
.
query_abs_dirs
(
)
        
src
=
get_mozconfig_path
(
self
config
dirs
)
        
dst
=
os
.
path
.
join
(
dirs
[
'
abs_mozilla_dir
'
]
'
.
mozconfig
'
)
        
self
.
copyfile
(
src
dst
)
        
self
.
read_from_file
(
dst
verbose
=
True
)
    
def
_mach
(
self
target
env
halt_on_failure
=
True
output_parser
=
None
)
:
        
dirs
=
self
.
query_abs_dirs
(
)
        
mach
=
self
.
_get_mach_executable
(
)
        
return
self
.
run_command
(
mach
+
target
                                
halt_on_failure
=
True
                                
env
=
env
                                
cwd
=
dirs
[
'
abs_mozilla_dir
'
]
                                
output_parser
=
None
)
    
def
_mach_configure
(
self
)
:
        
"
"
"
calls
mach
configure
"
"
"
        
env
=
self
.
query_bootstrap_env
(
)
        
target
=
[
"
configure
"
]
        
return
self
.
_mach
(
target
=
target
env
=
env
)
    
def
_get_mach_executable
(
self
)
:
        
return
[
sys
.
executable
'
mach
'
]
    
def
_get_make_executable
(
self
)
:
        
config
=
self
.
config
        
dirs
=
self
.
query_abs_dirs
(
)
        
if
config
.
get
(
'
enable_mozmake
'
)
:
            
make
=
r
"
/
"
.
join
(
[
dirs
[
'
abs_mozilla_dir
'
]
'
mozmake
.
exe
'
]
)
            
make
=
make
.
replace
(
'
\
\
'
'
/
'
)
            
make
=
[
make
]
        
else
:
            
make
=
[
'
make
'
]
        
return
make
    
def
_make
(
self
target
cwd
env
error_list
=
MakefileErrorList
              
halt_on_failure
=
True
output_parser
=
None
)
:
        
"
"
"
Runs
make
.
Returns
the
exit
code
"
"
"
        
make
=
self
.
_get_make_executable
(
)
        
if
target
:
            
make
=
make
+
target
        
return
self
.
run_command
(
make
                                
cwd
=
cwd
                                
env
=
env
                                
error_list
=
error_list
                                
halt_on_failure
=
halt_on_failure
                                
output_parser
=
output_parser
)
    
def
_get_output_from_make
(
self
target
cwd
env
halt_on_failure
=
True
ignore_errors
=
False
)
:
        
"
"
"
runs
make
and
returns
the
output
of
the
command
"
"
"
        
make
=
self
.
_get_make_executable
(
)
        
return
self
.
get_output_from_command
(
make
+
target
                                            
cwd
=
cwd
                                            
env
=
env
                                            
silent
=
True
                                            
halt_on_failure
=
halt_on_failure
                                            
ignore_errors
=
ignore_errors
)
    
def
make_unpack_en_US
(
self
)
:
        
"
"
"
wrapper
for
make
unpack
"
"
"
        
config
=
self
.
config
        
dirs
=
self
.
query_abs_dirs
(
)
        
env
=
self
.
query_bootstrap_env
(
)
        
cwd
=
os
.
path
.
join
(
dirs
[
'
abs_objdir
'
]
config
[
'
locales_dir
'
]
)
        
return
self
.
_make
(
target
=
[
"
unpack
"
]
cwd
=
cwd
env
=
env
)
    
def
make_wget_en_US
(
self
)
:
        
"
"
"
wrapper
for
make
wget
-
en
-
US
"
"
"
        
env
=
self
.
query_bootstrap_env
(
)
        
dirs
=
self
.
query_abs_dirs
(
)
        
cwd
=
dirs
[
'
abs_locales_dir
'
]
        
return
self
.
_make
(
target
=
[
"
wget
-
en
-
US
"
]
cwd
=
cwd
env
=
env
)
    
def
make_upload
(
self
locale
)
:
        
"
"
"
wrapper
for
make
upload
command
"
"
"
        
env
=
self
.
query_l10n_env
(
)
        
dirs
=
self
.
query_abs_dirs
(
)
        
target
=
[
'
upload
'
'
AB_CD
=
%
s
'
%
(
locale
)
]
        
cwd
=
dirs
[
'
abs_locales_dir
'
]
        
parser
=
MakeUploadOutputParser
(
config
=
self
.
config
                                        
log_obj
=
self
.
log_obj
)
        
retval
=
self
.
_make
(
target
=
target
cwd
=
cwd
env
=
env
                            
halt_on_failure
=
False
output_parser
=
parser
)
        
if
retval
=
=
SUCCESS
:
            
self
.
info
(
'
Upload
successful
(
%
s
)
'
%
locale
)
            
ret
=
SUCCESS
        
else
:
            
self
.
error
(
'
failed
to
upload
%
s
'
%
locale
)
            
ret
=
FAILURE
        
if
ret
=
=
FAILURE
:
            
return
ret
        
if
self
.
config
.
get
(
"
simple_name_move
"
)
:
            
upload_target
=
self
.
config
[
"
upload_env
"
]
[
"
UPLOAD_PATH
"
]
            
target_path
=
os
.
path
.
join
(
upload_target
locale
)
            
self
.
mkdir_p
(
target_path
)
            
glob_name
=
"
*
.
%
s
.
*
"
%
locale
            
matches
=
(
glob
.
glob
(
os
.
path
.
join
(
upload_target
glob_name
)
)
+
                       
glob
.
glob
(
os
.
path
.
join
(
upload_target
'
update
'
glob_name
)
)
+
                       
glob
.
glob
(
os
.
path
.
join
(
upload_target
'
*
'
'
xpi
'
glob_name
)
)
+
                       
glob
.
glob
(
os
.
path
.
join
(
upload_target
'
install
'
'
sea
'
glob_name
)
)
+
                       
glob
.
glob
(
os
.
path
.
join
(
upload_target
'
setup
.
exe
'
)
)
+
                       
glob
.
glob
(
os
.
path
.
join
(
upload_target
'
setup
-
stub
.
exe
'
)
)
)
            
targets_exts
=
[
"
tar
.
bz2
"
"
dmg
"
"
langpack
.
xpi
"
                            
"
complete
.
mar
"
"
checksums
"
"
zip
"
                            
"
installer
.
exe
"
"
installer
-
stub
.
exe
"
]
            
targets
=
[
(
"
.
%
s
"
%
(
ext
)
"
target
.
%
s
"
%
(
ext
)
)
for
ext
in
targets_exts
]
            
targets
.
extend
(
[
(
f
f
)
for
f
in
'
setup
.
exe
'
'
setup
-
stub
.
exe
'
]
)
            
for
f
in
matches
:
                
possible_targets
=
[
                    
(
tail
target_file
)
                    
for
(
tail
target_file
)
in
targets
                    
if
f
.
endswith
(
tail
)
                
]
                
if
len
(
possible_targets
)
=
=
1
:
                    
_
target_file
=
possible_targets
[
0
]
                    
targets
.
remove
(
possible_targets
[
0
]
)
                
else
:
                    
raise
RuntimeError
(
"
Unexpected
matching
file
name
encountered
:
%
s
"
                                       
%
f
)
                
self
.
move
(
os
.
path
.
join
(
f
)
                          
os
.
path
.
join
(
target_path
target_file
)
)
            
self
.
log
(
"
Converted
uploads
for
%
s
to
simple
names
"
%
locale
)
        
return
ret
    
def
set_upload_files
(
self
locale
)
:
        
env
=
self
.
query_l10n_env
(
)
        
target
=
[
'
echo
-
variable
-
UPLOAD_FILES
'
'
echo
-
variable
-
CHECKSUM_FILES
'
                  
'
AB_CD
=
%
s
'
%
locale
]
        
dirs
=
self
.
query_abs_dirs
(
)
        
cwd
=
dirs
[
'
abs_locales_dir
'
]
        
output
=
self
.
_get_output_from_make
(
target
=
target
cwd
=
cwd
env
=
env
                                            
ignore_errors
=
True
)
        
self
.
info
(
'
UPLOAD_FILES
is
"
%
s
"
'
%
output
)
        
files
=
shlex
.
split
(
output
)
        
if
not
files
:
            
self
.
error
(
'
failed
to
get
upload
file
list
for
locale
%
s
'
%
locale
)
            
return
FAILURE
        
self
.
upload_files
[
locale
]
=
[
            
os
.
path
.
abspath
(
os
.
path
.
join
(
cwd
f
)
)
for
f
in
files
        
]
        
return
SUCCESS
    
def
make_installers
(
self
locale
)
:
        
"
"
"
wrapper
for
make
installers
-
(
locale
)
"
"
"
        
env
=
self
.
query_l10n_env
(
)
        
self
.
_copy_mozconfig
(
)
        
dirs
=
self
.
query_abs_dirs
(
)
        
cwd
=
os
.
path
.
join
(
dirs
[
'
abs_locales_dir
'
]
)
        
target
=
[
"
installers
-
%
s
"
%
locale
]
        
return
self
.
_make
(
target
=
target
cwd
=
cwd
                          
env
=
env
halt_on_failure
=
False
)
    
def
repack_locale
(
self
locale
)
:
        
"
"
"
wraps
the
logic
for
make
installers
and
generating
           
complete
updates
.
"
"
"
        
if
self
.
make_installers
(
locale
)
!
=
SUCCESS
:
            
self
.
error
(
"
make
installers
-
%
s
failed
"
%
(
locale
)
)
            
return
FAILURE
        
if
self
.
make_upload
(
locale
)
:
            
self
.
error
(
"
make
upload
for
locale
%
s
failed
!
"
%
(
locale
)
)
            
return
FAILURE
        
if
self
.
set_upload_files
(
locale
)
:
            
self
.
error
(
"
failed
to
get
list
of
files
to
upload
for
locale
%
s
"
%
locale
)
            
return
FAILURE
        
return
SUCCESS
    
def
repack
(
self
)
:
        
"
"
"
creates
the
repacks
and
udpates
"
"
"
        
self
.
_map
(
self
.
repack_locale
self
.
query_locales
(
)
)
    
def
_query_objdir
(
self
)
:
        
"
"
"
returns
objdir
name
from
configuration
"
"
"
        
return
self
.
config
[
'
objdir
'
]
    
def
query_abs_dirs
(
self
)
:
        
if
self
.
abs_dirs
:
            
return
self
.
abs_dirs
        
abs_dirs
=
super
(
DesktopSingleLocale
self
)
.
query_abs_dirs
(
)
        
for
directory
in
abs_dirs
:
            
value
=
abs_dirs
[
directory
]
            
abs_dirs
[
directory
]
=
value
        
dirs
=
{
}
        
dirs
[
'
abs_tools_dir
'
]
=
os
.
path
.
join
(
abs_dirs
[
'
abs_work_dir
'
]
'
tools
'
)
        
dirs
[
'
abs_src_dir
'
]
=
os
.
path
.
join
(
abs_dirs
[
'
abs_work_dir
'
]
'
src
'
)
        
for
key
in
dirs
.
keys
(
)
:
            
if
key
not
in
abs_dirs
:
                
abs_dirs
[
key
]
=
dirs
[
key
]
        
self
.
abs_dirs
=
abs_dirs
        
return
self
.
abs_dirs
    
def
_mar_binaries
(
self
)
:
        
"
"
"
returns
a
tuple
with
mar
and
mbsdiff
paths
"
"
"
        
config
=
self
.
config
        
return
(
config
[
'
mar
'
]
config
[
'
mbsdiff
'
]
)
    
def
_get_tooltool_auth_file
(
self
)
:
        
if
'
tooltool_authentication_file
'
in
self
.
config
:
            
fn
=
self
.
config
[
'
tooltool_authentication_file
'
]
        
elif
self
.
_is_windows
(
)
:
            
fn
=
r
'
c
:
\
builds
\
relengapi
.
tok
'
        
else
:
            
fn
=
'
/
builds
/
relengapi
.
tok
'
        
if
os
.
path
.
exists
(
fn
)
:
            
return
fn
    
def
_run_tooltool
(
self
)
:
        
env
=
self
.
query_bootstrap_env
(
)
        
config
=
self
.
config
        
dirs
=
self
.
query_abs_dirs
(
)
        
toolchains
=
os
.
environ
.
get
(
'
MOZ_TOOLCHAINS
'
)
        
manifest_src
=
os
.
environ
.
get
(
'
TOOLTOOL_MANIFEST
'
)
        
if
not
manifest_src
:
            
manifest_src
=
config
.
get
(
'
tooltool_manifest_src
'
)
        
if
not
manifest_src
and
not
toolchains
:
            
return
        
python
=
sys
.
executable
        
cmd
=
[
            
python
'
-
u
'
            
os
.
path
.
join
(
dirs
[
'
abs_mozilla_dir
'
]
'
mach
'
)
            
'
artifact
'
            
'
toolchain
'
            
'
-
v
'
            
'
-
-
retry
'
'
4
'
            
'
-
-
artifact
-
manifest
'
            
os
.
path
.
join
(
dirs
[
'
abs_mozilla_dir
'
]
'
toolchains
.
json
'
)
        
]
        
if
manifest_src
:
            
cmd
.
extend
(
[
                
'
-
-
tooltool
-
manifest
'
                
os
.
path
.
join
(
dirs
[
'
abs_mozilla_dir
'
]
manifest_src
)
                
'
-
-
tooltool
-
url
'
                
config
[
'
tooltool_url
'
]
            
]
)
            
auth_file
=
self
.
_get_tooltool_auth_file
(
)
            
if
auth_file
and
os
.
path
.
exists
(
auth_file
)
:
                
cmd
.
extend
(
[
'
-
-
authentication
-
file
'
auth_file
]
)
        
cache
=
config
[
'
bootstrap_env
'
]
.
get
(
'
TOOLTOOL_CACHE
'
)
        
if
cache
:
            
cmd
.
extend
(
[
'
-
-
cache
-
dir
'
cache
]
)
        
if
toolchains
:
            
cmd
.
extend
(
toolchains
.
split
(
)
)
        
self
.
info
(
str
(
cmd
)
)
        
self
.
run_command
(
cmd
cwd
=
dirs
[
'
abs_mozilla_dir
'
]
halt_on_failure
=
True
                         
env
=
env
)
if
__name__
=
=
'
__main__
'
:
    
single_locale
=
DesktopSingleLocale
(
)
    
single_locale
.
run_and_exit
(
)
