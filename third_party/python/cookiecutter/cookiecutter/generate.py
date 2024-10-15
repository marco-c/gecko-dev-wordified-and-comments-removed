"
"
"
Functions
for
generating
a
project
from
a
project
template
.
"
"
"
import
fnmatch
import
json
import
logging
import
os
import
shutil
import
warnings
from
collections
import
OrderedDict
from
pathlib
import
Path
from
binaryornot
.
check
import
is_binary
from
jinja2
import
Environment
FileSystemLoader
from
jinja2
.
exceptions
import
TemplateSyntaxError
UndefinedError
from
cookiecutter
.
exceptions
import
(
    
ContextDecodingException
    
OutputDirExistsException
    
UndefinedVariableInTemplate
)
from
cookiecutter
.
find
import
find_template
from
cookiecutter
.
hooks
import
run_hook_from_repo_dir
from
cookiecutter
.
utils
import
(
    
create_env_with_context
    
make_sure_path_exists
    
rmtree
    
work_in
)
logger
=
logging
.
getLogger
(
__name__
)
def
is_copy_only_path
(
path
context
)
:
    
"
"
"
Check
whether
the
given
path
should
only
be
copied
and
not
rendered
.
    
Returns
True
if
path
matches
a
pattern
in
the
given
context
dict
    
otherwise
False
.
    
:
param
path
:
A
file
-
system
path
referring
to
a
file
or
dir
that
        
should
be
rendered
or
just
copied
.
    
:
param
context
:
cookiecutter
context
.
    
"
"
"
    
try
:
        
for
dont_render
in
context
[
'
cookiecutter
'
]
[
'
_copy_without_render
'
]
:
            
if
fnmatch
.
fnmatch
(
path
dont_render
)
:
                
return
True
    
except
KeyError
:
        
return
False
    
return
False
def
apply_overwrites_to_context
(
    
context
overwrite_context
*
in_dictionary_variable
=
False
)
:
    
"
"
"
Modify
the
given
context
in
place
based
on
the
overwrite_context
.
"
"
"
    
for
variable
overwrite
in
overwrite_context
.
items
(
)
:
        
if
variable
not
in
context
:
            
if
not
in_dictionary_variable
:
                
continue
            
context
[
variable
]
=
overwrite
        
context_value
=
context
[
variable
]
        
if
isinstance
(
context_value
list
)
:
            
if
in_dictionary_variable
:
                
context
[
variable
]
=
overwrite
                
continue
            
if
isinstance
(
overwrite
list
)
:
                
if
set
(
overwrite
)
.
issubset
(
set
(
context_value
)
)
:
                    
context
[
variable
]
=
overwrite
                
else
:
                    
raise
ValueError
(
                        
f
"
{
overwrite
}
provided
for
multi
-
choice
variable
"
                        
f
"
{
variable
}
but
valid
choices
are
{
context_value
}
"
                    
)
            
else
:
                
if
overwrite
in
context_value
:
                    
context_value
.
remove
(
overwrite
)
                    
context_value
.
insert
(
0
overwrite
)
                
else
:
                    
raise
ValueError
(
                        
f
"
{
overwrite
}
provided
for
choice
variable
"
                        
f
"
{
variable
}
but
the
choices
are
{
context_value
}
.
"
                    
)
        
elif
isinstance
(
context_value
dict
)
and
isinstance
(
overwrite
dict
)
:
            
apply_overwrites_to_context
(
                
context_value
overwrite
in_dictionary_variable
=
True
            
)
            
context
[
variable
]
=
context_value
        
else
:
            
context
[
variable
]
=
overwrite
def
generate_context
(
    
context_file
=
'
cookiecutter
.
json
'
default_context
=
None
extra_context
=
None
)
:
    
"
"
"
Generate
the
context
for
a
Cookiecutter
project
template
.
    
Loads
the
JSON
file
as
a
Python
object
with
key
being
the
JSON
filename
.
    
:
param
context_file
:
JSON
file
containing
key
/
value
pairs
for
populating
        
the
cookiecutter
'
s
variables
.
    
:
param
default_context
:
Dictionary
containing
config
to
take
into
account
.
    
:
param
extra_context
:
Dictionary
containing
configuration
overrides
    
"
"
"
    
context
=
OrderedDict
(
[
]
)
    
try
:
        
with
open
(
context_file
encoding
=
'
utf
-
8
'
)
as
file_handle
:
            
obj
=
json
.
load
(
file_handle
object_pairs_hook
=
OrderedDict
)
    
except
ValueError
as
e
:
        
full_fpath
=
os
.
path
.
abspath
(
context_file
)
        
json_exc_message
=
str
(
e
)
        
our_exc_message
=
(
            
f
"
JSON
decoding
error
while
loading
'
{
full_fpath
}
'
.
"
            
f
"
Decoding
error
details
:
'
{
json_exc_message
}
'
"
        
)
        
raise
ContextDecodingException
(
our_exc_message
)
from
e
    
file_name
=
os
.
path
.
split
(
context_file
)
[
1
]
    
file_stem
=
file_name
.
split
(
'
.
'
)
[
0
]
    
context
[
file_stem
]
=
obj
    
if
default_context
:
        
try
:
            
apply_overwrites_to_context
(
obj
default_context
)
        
except
ValueError
as
error
:
            
warnings
.
warn
(
f
"
Invalid
default
received
:
{
error
}
"
)
    
if
extra_context
:
        
apply_overwrites_to_context
(
obj
extra_context
)
    
logger
.
debug
(
'
Context
generated
is
%
s
'
context
)
    
return
context
def
generate_file
(
project_dir
infile
context
env
skip_if_file_exists
=
False
)
:
    
"
"
"
Render
filename
of
infile
as
name
of
outfile
handle
infile
correctly
.
    
Dealing
with
infile
appropriately
:
        
a
.
If
infile
is
a
binary
file
copy
it
over
without
rendering
.
        
b
.
If
infile
is
a
text
file
render
its
contents
and
write
the
           
rendered
infile
to
outfile
.
    
Precondition
:
        
When
calling
generate_file
(
)
the
root
template
dir
must
be
the
        
current
working
directory
.
Using
utils
.
work_in
(
)
is
the
recommended
        
way
to
perform
this
directory
change
.
    
:
param
project_dir
:
Absolute
path
to
the
resulting
generated
project
.
    
:
param
infile
:
Input
file
to
generate
the
file
from
.
Relative
to
the
root
        
template
dir
.
    
:
param
context
:
Dict
for
populating
the
cookiecutter
'
s
variables
.
    
:
param
env
:
Jinja2
template
execution
environment
.
    
"
"
"
    
logger
.
debug
(
'
Processing
file
%
s
'
infile
)
    
outfile_tmpl
=
env
.
from_string
(
infile
)
    
outfile
=
os
.
path
.
join
(
project_dir
outfile_tmpl
.
render
(
*
*
context
)
)
    
file_name_is_empty
=
os
.
path
.
isdir
(
outfile
)
    
if
file_name_is_empty
:
        
logger
.
debug
(
'
The
resulting
file
name
is
empty
:
%
s
'
outfile
)
        
return
    
if
skip_if_file_exists
and
os
.
path
.
exists
(
outfile
)
:
        
logger
.
debug
(
'
The
resulting
file
already
exists
:
%
s
'
outfile
)
        
return
    
logger
.
debug
(
'
Created
file
at
%
s
'
outfile
)
    
logger
.
debug
(
"
Check
%
s
to
see
if
it
'
s
a
binary
"
infile
)
    
if
is_binary
(
infile
)
:
        
logger
.
debug
(
'
Copying
binary
%
s
to
%
s
without
rendering
'
infile
outfile
)
        
shutil
.
copyfile
(
infile
outfile
)
        
shutil
.
copymode
(
infile
outfile
)
        
return
    
infile_fwd_slashes
=
infile
.
replace
(
os
.
path
.
sep
'
/
'
)
    
try
:
        
tmpl
=
env
.
get_template
(
infile_fwd_slashes
)
    
except
TemplateSyntaxError
as
exception
:
        
exception
.
translated
=
False
        
raise
    
rendered_file
=
tmpl
.
render
(
*
*
context
)
    
if
context
[
'
cookiecutter
'
]
.
get
(
'
_new_lines
'
False
)
:
        
newline
=
context
[
'
cookiecutter
'
]
[
'
_new_lines
'
]
        
logger
.
debug
(
'
Using
configured
newline
character
%
s
'
repr
(
newline
)
)
    
else
:
        
with
open
(
infile
encoding
=
'
utf
-
8
'
)
as
rd
:
            
rd
.
readline
(
)
        
newline
=
rd
.
newlines
[
0
]
if
isinstance
(
rd
.
newlines
tuple
)
else
rd
.
newlines
        
logger
.
debug
(
'
Using
detected
newline
character
%
s
'
repr
(
newline
)
)
    
logger
.
debug
(
'
Writing
contents
to
file
%
s
'
outfile
)
    
with
open
(
outfile
'
w
'
encoding
=
'
utf
-
8
'
newline
=
newline
)
as
fh
:
        
fh
.
write
(
rendered_file
)
    
shutil
.
copymode
(
infile
outfile
)
def
render_and_create_dir
(
    
dirname
:
str
    
context
:
dict
    
output_dir
:
"
os
.
PathLike
[
str
]
"
    
environment
:
Environment
    
overwrite_if_exists
:
bool
=
False
)
:
    
"
"
"
Render
name
of
a
directory
create
the
directory
return
its
path
.
"
"
"
    
name_tmpl
=
environment
.
from_string
(
dirname
)
    
rendered_dirname
=
name_tmpl
.
render
(
*
*
context
)
    
dir_to_create
=
Path
(
output_dir
rendered_dirname
)
    
logger
.
debug
(
        
'
Rendered
dir
%
s
must
exist
in
output_dir
%
s
'
dir_to_create
output_dir
    
)
    
output_dir_exists
=
dir_to_create
.
exists
(
)
    
if
output_dir_exists
:
        
if
overwrite_if_exists
:
            
logger
.
debug
(
                
'
Output
directory
%
s
already
exists
overwriting
it
'
dir_to_create
            
)
        
else
:
            
msg
=
f
'
Error
:
"
{
dir_to_create
}
"
directory
already
exists
'
            
raise
OutputDirExistsException
(
msg
)
    
else
:
        
make_sure_path_exists
(
dir_to_create
)
    
return
dir_to_create
not
output_dir_exists
def
_run_hook_from_repo_dir
(
    
repo_dir
hook_name
project_dir
context
delete_project_on_failure
)
:
    
"
"
"
Run
hook
from
repo
directory
clean
project
directory
if
hook
fails
.
    
:
param
repo_dir
:
Project
template
input
directory
.
    
:
param
hook_name
:
The
hook
to
execute
.
    
:
param
project_dir
:
The
directory
to
execute
the
script
from
.
    
:
param
context
:
Cookiecutter
project
context
.
    
:
param
delete_project_on_failure
:
Delete
the
project
directory
on
hook
        
failure
?
    
"
"
"
    
warnings
.
warn
(
        
"
The
'
_run_hook_from_repo_dir
'
function
is
deprecated
"
        
"
use
'
cookiecutter
.
hooks
.
run_hook_from_repo_dir
'
instead
"
        
DeprecationWarning
        
2
    
)
    
run_hook_from_repo_dir
(
        
repo_dir
hook_name
project_dir
context
delete_project_on_failure
    
)
def
generate_files
(
    
repo_dir
    
context
=
None
    
output_dir
=
'
.
'
    
overwrite_if_exists
=
False
    
skip_if_file_exists
=
False
    
accept_hooks
=
True
    
keep_project_on_failure
=
False
)
:
    
"
"
"
Render
the
templates
and
saves
them
to
files
.
    
:
param
repo_dir
:
Project
template
input
directory
.
    
:
param
context
:
Dict
for
populating
the
template
'
s
variables
.
    
:
param
output_dir
:
Where
to
output
the
generated
project
dir
into
.
    
:
param
overwrite_if_exists
:
Overwrite
the
contents
of
the
output
directory
        
if
it
exists
.
    
:
param
skip_if_file_exists
:
Skip
the
files
in
the
corresponding
directories
        
if
they
already
exist
    
:
param
accept_hooks
:
Accept
pre
and
post
hooks
if
set
to
True
.
    
:
param
keep_project_on_failure
:
If
True
keep
generated
project
directory
even
when
        
generation
fails
    
"
"
"
    
context
=
context
or
OrderedDict
(
[
]
)
    
env
=
create_env_with_context
(
context
)
    
template_dir
=
find_template
(
repo_dir
env
)
    
logger
.
debug
(
'
Generating
project
from
%
s
.
.
.
'
template_dir
)
    
unrendered_dir
=
os
.
path
.
split
(
template_dir
)
[
1
]
    
try
:
        
project_dir
output_directory_created
=
render_and_create_dir
(
            
unrendered_dir
context
output_dir
env
overwrite_if_exists
        
)
    
except
UndefinedError
as
err
:
        
msg
=
f
"
Unable
to
create
project
directory
'
{
unrendered_dir
}
'
"
        
raise
UndefinedVariableInTemplate
(
msg
err
context
)
from
err
    
project_dir
=
os
.
path
.
abspath
(
project_dir
)
    
logger
.
debug
(
'
Project
directory
is
%
s
'
project_dir
)
    
delete_project_on_failure
=
output_directory_created
and
not
keep_project_on_failure
    
if
accept_hooks
:
        
run_hook_from_repo_dir
(
            
repo_dir
'
pre_gen_project
'
project_dir
context
delete_project_on_failure
        
)
    
with
work_in
(
template_dir
)
:
        
env
.
loader
=
FileSystemLoader
(
[
'
.
'
'
.
.
/
templates
'
]
)
        
for
root
dirs
files
in
os
.
walk
(
'
.
'
)
:
            
copy_dirs
=
[
]
            
render_dirs
=
[
]
            
for
d
in
dirs
:
                
d_
=
os
.
path
.
normpath
(
os
.
path
.
join
(
root
d
)
)
                
if
is_copy_only_path
(
d_
context
)
:
                    
logger
.
debug
(
'
Found
copy
only
path
%
s
'
d
)
                    
copy_dirs
.
append
(
d
)
                
else
:
                    
render_dirs
.
append
(
d
)
            
for
copy_dir
in
copy_dirs
:
                
indir
=
os
.
path
.
normpath
(
os
.
path
.
join
(
root
copy_dir
)
)
                
outdir
=
os
.
path
.
normpath
(
os
.
path
.
join
(
project_dir
indir
)
)
                
outdir
=
env
.
from_string
(
outdir
)
.
render
(
*
*
context
)
                
logger
.
debug
(
'
Copying
dir
%
s
to
%
s
without
rendering
'
indir
outdir
)
                
if
os
.
path
.
isdir
(
outdir
)
:
                    
shutil
.
rmtree
(
outdir
)
                
shutil
.
copytree
(
indir
outdir
)
            
dirs
[
:
]
=
render_dirs
            
for
d
in
dirs
:
                
unrendered_dir
=
os
.
path
.
join
(
project_dir
root
d
)
                
try
:
                    
render_and_create_dir
(
                        
unrendered_dir
context
output_dir
env
overwrite_if_exists
                    
)
                
except
UndefinedError
as
err
:
                    
if
delete_project_on_failure
:
                        
rmtree
(
project_dir
)
                    
_dir
=
os
.
path
.
relpath
(
unrendered_dir
output_dir
)
                    
msg
=
f
"
Unable
to
create
directory
'
{
_dir
}
'
"
                    
raise
UndefinedVariableInTemplate
(
msg
err
context
)
from
err
            
for
f
in
files
:
                
infile
=
os
.
path
.
normpath
(
os
.
path
.
join
(
root
f
)
)
                
if
is_copy_only_path
(
infile
context
)
:
                    
outfile_tmpl
=
env
.
from_string
(
infile
)
                    
outfile_rendered
=
outfile_tmpl
.
render
(
*
*
context
)
                    
outfile
=
os
.
path
.
join
(
project_dir
outfile_rendered
)
                    
logger
.
debug
(
                        
'
Copying
file
%
s
to
%
s
without
rendering
'
infile
outfile
                    
)
                    
shutil
.
copyfile
(
infile
outfile
)
                    
shutil
.
copymode
(
infile
outfile
)
                    
continue
                
try
:
                    
generate_file
(
                        
project_dir
infile
context
env
skip_if_file_exists
                    
)
                
except
UndefinedError
as
err
:
                    
if
delete_project_on_failure
:
                        
rmtree
(
project_dir
)
                    
msg
=
f
"
Unable
to
create
file
'
{
infile
}
'
"
                    
raise
UndefinedVariableInTemplate
(
msg
err
context
)
from
err
    
if
accept_hooks
:
        
run_hook_from_repo_dir
(
            
repo_dir
            
'
post_gen_project
'
            
project_dir
            
context
            
delete_project_on_failure
        
)
    
return
project_dir
