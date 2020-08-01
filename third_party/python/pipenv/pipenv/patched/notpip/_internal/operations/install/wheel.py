"
"
"
Support
for
installing
and
building
the
"
wheel
"
binary
package
format
.
"
"
"
from
__future__
import
absolute_import
import
collections
import
compileall
import
csv
import
logging
import
os
.
path
import
re
import
shutil
import
stat
import
sys
import
warnings
from
base64
import
urlsafe_b64encode
from
zipfile
import
ZipFile
from
pipenv
.
patched
.
notpip
.
_vendor
import
pkg_resources
from
pipenv
.
patched
.
notpip
.
_vendor
.
distlib
.
scripts
import
ScriptMaker
from
pipenv
.
patched
.
notpip
.
_vendor
.
distlib
.
util
import
get_export_entry
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
import
StringIO
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
locations
import
get_major_minor_version
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
captured_stdout
ensure_dir
hash_file
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
temp_dir
import
TempDirectory
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
unpacking
import
unpack_file
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
wheel
import
parse_wheel
if
MYPY_CHECK_RUNNING
:
    
from
email
.
message
import
Message
    
from
typing
import
(
        
Dict
List
Optional
Sequence
Tuple
IO
Text
Any
        
Iterable
Callable
Set
    
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
models
.
scheme
import
Scheme
    
InstalledCSVRow
=
Tuple
[
str
.
.
.
]
logger
=
logging
.
getLogger
(
__name__
)
def
normpath
(
src
p
)
:
    
return
os
.
path
.
relpath
(
src
p
)
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
def
rehash
(
path
blocksize
=
1
<
<
20
)
:
    
"
"
"
Return
(
encoded_digest
length
)
for
path
using
hashlib
.
sha256
(
)
"
"
"
    
h
length
=
hash_file
(
path
blocksize
)
    
digest
=
'
sha256
=
'
+
urlsafe_b64encode
(
        
h
.
digest
(
)
    
)
.
decode
(
'
latin1
'
)
.
rstrip
(
'
=
'
)
    
return
(
digest
str
(
length
)
)
def
open_for_csv
(
name
mode
)
:
    
if
sys
.
version_info
[
0
]
<
3
:
        
nl
=
{
}
        
bin
=
'
b
'
    
else
:
        
nl
=
{
'
newline
'
:
'
'
}
        
bin
=
'
'
    
return
open
(
name
mode
+
bin
*
*
nl
)
def
fix_script
(
path
)
:
    
"
"
"
Replace
#
!
python
with
#
!
/
path
/
to
/
python
    
Return
True
if
file
was
changed
.
    
"
"
"
    
if
os
.
path
.
isfile
(
path
)
:
        
with
open
(
path
'
rb
'
)
as
script
:
            
firstline
=
script
.
readline
(
)
            
if
not
firstline
.
startswith
(
b
'
#
!
python
'
)
:
                
return
False
            
exename
=
sys
.
executable
.
encode
(
sys
.
getfilesystemencoding
(
)
)
            
firstline
=
b
'
#
!
'
+
exename
+
os
.
linesep
.
encode
(
"
ascii
"
)
            
rest
=
script
.
read
(
)
        
with
open
(
path
'
wb
'
)
as
script
:
            
script
.
write
(
firstline
)
            
script
.
write
(
rest
)
        
return
True
    
return
None
def
wheel_root_is_purelib
(
metadata
)
:
    
return
metadata
.
get
(
"
Root
-
Is
-
Purelib
"
"
"
)
.
lower
(
)
=
=
"
true
"
def
get_entrypoints
(
filename
)
:
    
if
not
os
.
path
.
exists
(
filename
)
:
        
return
{
}
{
}
    
with
open
(
filename
)
as
fp
:
        
data
=
StringIO
(
)
        
for
line
in
fp
:
            
data
.
write
(
line
.
strip
(
)
)
            
data
.
write
(
"
\
n
"
)
        
data
.
seek
(
0
)
    
entry_points
=
pkg_resources
.
EntryPoint
.
parse_map
(
data
)
    
console
=
entry_points
.
get
(
'
console_scripts
'
{
}
)
    
gui
=
entry_points
.
get
(
'
gui_scripts
'
{
}
)
    
def
_split_ep
(
s
)
:
        
"
"
"
get
the
string
representation
of
EntryPoint
        
remove
space
and
split
on
'
=
'
        
"
"
"
        
split_parts
=
str
(
s
)
.
replace
(
"
"
"
"
)
.
split
(
"
=
"
)
        
return
split_parts
[
0
]
split_parts
[
1
]
    
console
=
dict
(
_split_ep
(
v
)
for
v
in
console
.
values
(
)
)
    
gui
=
dict
(
_split_ep
(
v
)
for
v
in
gui
.
values
(
)
)
    
return
console
gui
def
message_about_scripts_not_on_PATH
(
scripts
)
:
    
"
"
"
Determine
if
any
scripts
are
not
on
PATH
and
format
a
warning
.
    
Returns
a
warning
message
if
one
or
more
scripts
are
not
on
PATH
    
otherwise
None
.
    
"
"
"
    
if
not
scripts
:
        
return
None
    
grouped_by_dir
=
collections
.
defaultdict
(
set
)
    
for
destfile
in
scripts
:
        
parent_dir
=
os
.
path
.
dirname
(
destfile
)
        
script_name
=
os
.
path
.
basename
(
destfile
)
        
grouped_by_dir
[
parent_dir
]
.
add
(
script_name
)
    
not_warn_dirs
=
[
        
os
.
path
.
normcase
(
i
)
.
rstrip
(
os
.
sep
)
for
i
in
        
os
.
environ
.
get
(
"
PATH
"
"
"
)
.
split
(
os
.
pathsep
)
    
]
    
not_warn_dirs
.
append
(
os
.
path
.
normcase
(
os
.
path
.
dirname
(
sys
.
executable
)
)
)
    
warn_for
=
{
        
parent_dir
:
scripts
for
parent_dir
scripts
in
grouped_by_dir
.
items
(
)
        
if
os
.
path
.
normcase
(
parent_dir
)
not
in
not_warn_dirs
    
}
    
if
not
warn_for
:
        
return
None
    
msg_lines
=
[
]
    
for
parent_dir
dir_scripts
in
warn_for
.
items
(
)
:
        
sorted_scripts
=
sorted
(
dir_scripts
)
        
if
len
(
sorted_scripts
)
=
=
1
:
            
start_text
=
"
script
{
}
is
"
.
format
(
sorted_scripts
[
0
]
)
        
else
:
            
start_text
=
"
scripts
{
}
are
"
.
format
(
                
"
"
.
join
(
sorted_scripts
[
:
-
1
]
)
+
"
and
"
+
sorted_scripts
[
-
1
]
            
)
        
msg_lines
.
append
(
            
"
The
{
}
installed
in
'
{
}
'
which
is
not
on
PATH
.
"
            
.
format
(
start_text
parent_dir
)
        
)
    
last_line_fmt
=
(
        
"
Consider
adding
{
}
to
PATH
or
if
you
prefer
"
        
"
to
suppress
this
warning
use
-
-
no
-
warn
-
script
-
location
.
"
    
)
    
if
len
(
msg_lines
)
=
=
1
:
        
msg_lines
.
append
(
last_line_fmt
.
format
(
"
this
directory
"
)
)
    
else
:
        
msg_lines
.
append
(
last_line_fmt
.
format
(
"
these
directories
"
)
)
    
warn_for_tilde
=
any
(
        
i
[
0
]
=
=
"
~
"
for
i
in
os
.
environ
.
get
(
"
PATH
"
"
"
)
.
split
(
os
.
pathsep
)
if
i
    
)
    
if
warn_for_tilde
:
        
tilde_warning_msg
=
(
            
"
NOTE
:
The
current
PATH
contains
path
(
s
)
starting
with
~
"
            
"
which
may
not
be
expanded
by
all
applications
.
"
        
)
        
msg_lines
.
append
(
tilde_warning_msg
)
    
return
"
\
n
"
.
join
(
msg_lines
)
def
sorted_outrows
(
outrows
)
:
    
"
"
"
Return
the
given
rows
of
a
RECORD
file
in
sorted
order
.
    
Each
row
is
a
3
-
tuple
(
path
hash
size
)
and
corresponds
to
a
record
of
    
a
RECORD
file
(
see
PEP
376
and
PEP
427
for
details
)
.
For
the
rows
    
passed
to
this
function
the
size
can
be
an
integer
as
an
int
or
string
    
or
the
empty
string
.
    
"
"
"
    
return
sorted
(
outrows
key
=
lambda
row
:
tuple
(
str
(
x
)
for
x
in
row
)
)
def
get_csv_rows_for_installed
(
    
old_csv_rows
    
installed
    
changed
    
generated
    
lib_dir
)
:
    
"
"
"
    
:
param
installed
:
A
map
from
archive
RECORD
path
to
installation
RECORD
        
path
.
    
"
"
"
    
installed_rows
=
[
]
    
for
row
in
old_csv_rows
:
        
if
len
(
row
)
>
3
:
            
logger
.
warning
(
                
'
RECORD
line
has
more
than
three
elements
:
{
}
'
.
format
(
row
)
            
)
        
row
=
list
(
row
)
        
old_path
=
row
[
0
]
        
new_path
=
installed
.
pop
(
old_path
old_path
)
        
row
[
0
]
=
new_path
        
if
new_path
in
changed
:
            
digest
length
=
rehash
(
new_path
)
            
row
[
1
]
=
digest
            
row
[
2
]
=
length
        
installed_rows
.
append
(
tuple
(
row
)
)
    
for
f
in
generated
:
        
digest
length
=
rehash
(
f
)
        
installed_rows
.
append
(
(
normpath
(
f
lib_dir
)
digest
str
(
length
)
)
)
    
for
f
in
installed
:
        
installed_rows
.
append
(
(
installed
[
f
]
'
'
'
'
)
)
    
return
installed_rows
class
MissingCallableSuffix
(
Exception
)
:
    
pass
def
_raise_for_invalid_entrypoint
(
specification
)
:
    
entry
=
get_export_entry
(
specification
)
    
if
entry
is
not
None
and
entry
.
suffix
is
None
:
        
raise
MissingCallableSuffix
(
str
(
entry
)
)
class
PipScriptMaker
(
ScriptMaker
)
:
    
def
make
(
self
specification
options
=
None
)
:
        
_raise_for_invalid_entrypoint
(
specification
)
        
return
super
(
PipScriptMaker
self
)
.
make
(
specification
options
)
def
install_unpacked_wheel
(
    
name
    
wheeldir
    
wheel_zip
    
scheme
    
req_description
    
pycompile
=
True
    
warn_script_location
=
True
)
:
    
"
"
"
Install
a
wheel
.
    
:
param
name
:
Name
of
the
project
to
install
    
:
param
wheeldir
:
Base
directory
of
the
unpacked
wheel
    
:
param
wheel_zip
:
open
ZipFile
for
wheel
being
installed
    
:
param
scheme
:
Distutils
scheme
dictating
the
install
directories
    
:
param
req_description
:
String
used
in
place
of
the
requirement
for
        
logging
    
:
param
pycompile
:
Whether
to
byte
-
compile
installed
Python
files
    
:
param
warn_script_location
:
Whether
to
check
that
scripts
are
installed
        
into
a
directory
on
PATH
    
:
raises
UnsupportedWheel
:
        
*
when
the
directory
holds
an
unpacked
wheel
with
incompatible
          
Wheel
-
Version
        
*
when
the
.
dist
-
info
dir
does
not
match
the
wheel
    
"
"
"
    
source
=
wheeldir
.
rstrip
(
os
.
path
.
sep
)
+
os
.
path
.
sep
    
info_dir
metadata
=
parse_wheel
(
wheel_zip
name
)
    
if
wheel_root_is_purelib
(
metadata
)
:
        
lib_dir
=
scheme
.
purelib
    
else
:
        
lib_dir
=
scheme
.
platlib
    
subdirs
=
os
.
listdir
(
source
)
    
data_dirs
=
[
s
for
s
in
subdirs
if
s
.
endswith
(
'
.
data
'
)
]
    
installed
=
{
}
    
changed
=
set
(
)
    
generated
=
[
]
    
if
pycompile
:
        
with
captured_stdout
(
)
as
stdout
:
            
with
warnings
.
catch_warnings
(
)
:
                
warnings
.
filterwarnings
(
'
ignore
'
)
                
compileall
.
compile_dir
(
source
force
=
True
quiet
=
True
)
        
logger
.
debug
(
stdout
.
getvalue
(
)
)
    
def
record_installed
(
srcfile
destfile
modified
=
False
)
:
        
"
"
"
Map
archive
RECORD
paths
to
installation
RECORD
paths
.
"
"
"
        
oldpath
=
normpath
(
srcfile
wheeldir
)
        
newpath
=
normpath
(
destfile
lib_dir
)
        
installed
[
oldpath
]
=
newpath
        
if
modified
:
            
changed
.
add
(
destfile
)
    
def
clobber
(
            
source
            
dest
            
is_base
            
fixer
=
None
            
filter
=
None
    
)
:
        
ensure_dir
(
dest
)
        
for
dir
subdirs
files
in
os
.
walk
(
source
)
:
            
basedir
=
dir
[
len
(
source
)
:
]
.
lstrip
(
os
.
path
.
sep
)
            
destdir
=
os
.
path
.
join
(
dest
basedir
)
            
if
is_base
and
basedir
=
=
'
'
:
                
subdirs
[
:
]
=
[
s
for
s
in
subdirs
if
not
s
.
endswith
(
'
.
data
'
)
]
            
for
f
in
files
:
                
if
filter
and
filter
(
f
)
:
                    
continue
                
srcfile
=
os
.
path
.
join
(
dir
f
)
                
destfile
=
os
.
path
.
join
(
dest
basedir
f
)
                
ensure_dir
(
destdir
)
                
if
os
.
path
.
exists
(
destfile
)
:
                    
os
.
unlink
(
destfile
)
                
shutil
.
copyfile
(
srcfile
destfile
)
                
st
=
os
.
stat
(
srcfile
)
                
if
hasattr
(
os
"
utime
"
)
:
                    
os
.
utime
(
destfile
(
st
.
st_atime
st
.
st_mtime
)
)
                
if
os
.
access
(
srcfile
os
.
X_OK
)
:
                    
st
=
os
.
stat
(
srcfile
)
                    
permissions
=
(
                        
st
.
st_mode
|
stat
.
S_IXUSR
|
stat
.
S_IXGRP
|
stat
.
S_IXOTH
                    
)
                    
os
.
chmod
(
destfile
permissions
)
                
changed
=
False
                
if
fixer
:
                    
changed
=
fixer
(
destfile
)
                
record_installed
(
srcfile
destfile
changed
)
    
clobber
(
source
lib_dir
True
)
    
dest_info_dir
=
os
.
path
.
join
(
lib_dir
info_dir
)
    
ep_file
=
os
.
path
.
join
(
dest_info_dir
'
entry_points
.
txt
'
)
    
console
gui
=
get_entrypoints
(
ep_file
)
    
def
is_entrypoint_wrapper
(
name
)
:
        
if
name
.
lower
(
)
.
endswith
(
'
.
exe
'
)
:
            
matchname
=
name
[
:
-
4
]
        
elif
name
.
lower
(
)
.
endswith
(
'
-
script
.
py
'
)
:
            
matchname
=
name
[
:
-
10
]
        
elif
name
.
lower
(
)
.
endswith
(
"
.
pya
"
)
:
            
matchname
=
name
[
:
-
4
]
        
else
:
            
matchname
=
name
        
return
(
matchname
in
console
or
matchname
in
gui
)
    
for
datadir
in
data_dirs
:
        
fixer
=
None
        
filter
=
None
        
for
subdir
in
os
.
listdir
(
os
.
path
.
join
(
wheeldir
datadir
)
)
:
            
fixer
=
None
            
if
subdir
=
=
'
scripts
'
:
                
fixer
=
fix_script
                
filter
=
is_entrypoint_wrapper
            
source
=
os
.
path
.
join
(
wheeldir
datadir
subdir
)
            
dest
=
getattr
(
scheme
subdir
)
            
clobber
(
source
dest
False
fixer
=
fixer
filter
=
filter
)
    
maker
=
PipScriptMaker
(
None
scheme
.
scripts
)
    
maker
.
clobber
=
True
    
maker
.
variants
=
{
'
'
}
    
maker
.
set_mode
=
True
    
scripts_to_generate
=
[
]
    
pip_script
=
console
.
pop
(
'
pip
'
None
)
    
if
pip_script
:
        
if
"
ENSUREPIP_OPTIONS
"
not
in
os
.
environ
:
            
scripts_to_generate
.
append
(
'
pip
=
'
+
pip_script
)
        
if
os
.
environ
.
get
(
"
ENSUREPIP_OPTIONS
"
"
"
)
!
=
"
altinstall
"
:
            
scripts_to_generate
.
append
(
                
'
pip
%
s
=
%
s
'
%
(
sys
.
version_info
[
0
]
pip_script
)
            
)
        
scripts_to_generate
.
append
(
            
'
pip
%
s
=
%
s
'
%
(
get_major_minor_version
(
)
pip_script
)
        
)
        
pip_ep
=
[
k
for
k
in
console
if
re
.
match
(
r
'
pip
(
\
d
(
\
.
\
d
)
?
)
?
'
k
)
]
        
for
k
in
pip_ep
:
            
del
console
[
k
]
    
easy_install_script
=
console
.
pop
(
'
easy_install
'
None
)
    
if
easy_install_script
:
        
if
"
ENSUREPIP_OPTIONS
"
not
in
os
.
environ
:
            
scripts_to_generate
.
append
(
                
'
easy_install
=
'
+
easy_install_script
            
)
        
scripts_to_generate
.
append
(
            
'
easy_install
-
%
s
=
%
s
'
%
(
                
get_major_minor_version
(
)
easy_install_script
            
)
        
)
        
easy_install_ep
=
[
            
k
for
k
in
console
if
re
.
match
(
r
'
easy_install
(
-
\
d
\
.
\
d
)
?
'
k
)
        
]
        
for
k
in
easy_install_ep
:
            
del
console
[
k
]
    
scripts_to_generate
.
extend
(
        
'
%
s
=
%
s
'
%
kv
for
kv
in
console
.
items
(
)
    
)
    
gui_scripts_to_generate
=
[
        
'
%
s
=
%
s
'
%
kv
for
kv
in
gui
.
items
(
)
    
]
    
generated_console_scripts
=
[
]
    
try
:
        
generated_console_scripts
=
maker
.
make_multiple
(
scripts_to_generate
)
        
generated
.
extend
(
generated_console_scripts
)
        
generated
.
extend
(
            
maker
.
make_multiple
(
gui_scripts_to_generate
{
'
gui
'
:
True
}
)
        
)
    
except
MissingCallableSuffix
as
e
:
        
entry
=
e
.
args
[
0
]
        
raise
InstallationError
(
            
"
Invalid
script
entry
point
:
{
}
for
req
:
{
}
-
A
callable
"
            
"
suffix
is
required
.
Cf
https
:
/
/
packaging
.
python
.
org
/
"
            
"
specifications
/
entry
-
points
/
#
use
-
for
-
scripts
for
more
"
            
"
information
.
"
.
format
(
entry
req_description
)
        
)
    
if
warn_script_location
:
        
msg
=
message_about_scripts_not_on_PATH
(
generated_console_scripts
)
        
if
msg
is
not
None
:
            
logger
.
warning
(
msg
)
    
installer
=
os
.
path
.
join
(
dest_info_dir
'
INSTALLER
'
)
    
temp_installer
=
os
.
path
.
join
(
dest_info_dir
'
INSTALLER
.
pip
'
)
    
with
open
(
temp_installer
'
wb
'
)
as
installer_file
:
        
installer_file
.
write
(
b
'
pip
\
n
'
)
    
shutil
.
move
(
temp_installer
installer
)
    
generated
.
append
(
installer
)
    
record
=
os
.
path
.
join
(
dest_info_dir
'
RECORD
'
)
    
temp_record
=
os
.
path
.
join
(
dest_info_dir
'
RECORD
.
pip
'
)
    
with
open_for_csv
(
record
'
r
'
)
as
record_in
:
        
with
open_for_csv
(
temp_record
'
w
+
'
)
as
record_out
:
            
reader
=
csv
.
reader
(
record_in
)
            
outrows
=
get_csv_rows_for_installed
(
                
reader
installed
=
installed
changed
=
changed
                
generated
=
generated
lib_dir
=
lib_dir
            
)
            
writer
=
csv
.
writer
(
record_out
)
            
for
row
in
sorted_outrows
(
outrows
)
:
                
writer
.
writerow
(
row
)
    
shutil
.
move
(
temp_record
record
)
def
install_wheel
(
    
name
    
wheel_path
    
scheme
    
req_description
    
pycompile
=
True
    
warn_script_location
=
True
    
_temp_dir_for_testing
=
None
)
:
    
with
TempDirectory
(
        
path
=
_temp_dir_for_testing
kind
=
"
unpacked
-
wheel
"
    
)
as
unpacked_dir
ZipFile
(
wheel_path
allowZip64
=
True
)
as
z
:
        
unpack_file
(
wheel_path
unpacked_dir
.
path
)
        
install_unpacked_wheel
(
            
name
=
name
            
wheeldir
=
unpacked_dir
.
path
            
wheel_zip
=
z
            
scheme
=
scheme
            
req_description
=
req_description
            
pycompile
=
pycompile
            
warn_script_location
=
warn_script_location
        
)
