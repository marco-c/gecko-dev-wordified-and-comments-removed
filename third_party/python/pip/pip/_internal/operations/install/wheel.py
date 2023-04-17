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
import
collections
import
compileall
import
contextlib
import
csv
import
importlib
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
sys
import
warnings
from
base64
import
urlsafe_b64encode
from
email
.
message
import
Message
from
itertools
import
chain
filterfalse
starmap
from
typing
import
(
    
IO
    
TYPE_CHECKING
    
Any
    
BinaryIO
    
Callable
    
Dict
    
Iterable
    
Iterator
    
List
    
NewType
    
Optional
    
Sequence
    
Set
    
Tuple
    
Union
    
cast
)
from
zipfile
import
ZipFile
ZipInfo
from
pip
.
_vendor
.
distlib
.
scripts
import
ScriptMaker
from
pip
.
_vendor
.
distlib
.
util
import
get_export_entry
from
pip
.
_vendor
.
packaging
.
utils
import
canonicalize_name
from
pip
.
_vendor
.
six
import
ensure_str
ensure_text
reraise
from
pip
.
_internal
.
exceptions
import
InstallationError
from
pip
.
_internal
.
locations
import
get_major_minor_version
from
pip
.
_internal
.
metadata
import
BaseDistribution
get_wheel_distribution
from
pip
.
_internal
.
models
.
direct_url
import
DIRECT_URL_METADATA_NAME
DirectUrl
from
pip
.
_internal
.
models
.
scheme
import
SCHEME_KEYS
Scheme
from
pip
.
_internal
.
utils
.
filesystem
import
adjacent_tmp_file
replace
from
pip
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
partition
from
pip
.
_internal
.
utils
.
unpacking
import
(
    
current_umask
    
is_within_directory
    
set_extracted_file_to_default_mode_plus_executable
    
zip_item_is_executable
)
from
pip
.
_internal
.
utils
.
wheel
import
parse_wheel
if
TYPE_CHECKING
:
    
from
typing
import
Protocol
    
class
File
(
Protocol
)
:
        
src_record_path
=
None
        
dest_path
=
None
        
changed
=
None
        
def
save
(
self
)
:
            
pass
logger
=
logging
.
getLogger
(
__name__
)
RecordPath
=
NewType
(
'
RecordPath
'
str
)
InstalledCSVRow
=
Tuple
[
RecordPath
str
Union
[
int
str
]
]
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
csv_io_kwargs
(
mode
)
:
    
"
"
"
Return
keyword
arguments
to
properly
open
a
CSV
file
    
in
the
given
mode
.
    
"
"
"
    
return
{
'
mode
'
:
mode
'
newline
'
:
'
'
'
encoding
'
:
'
utf
-
8
'
}
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
    
assert
os
.
path
.
isfile
(
path
)
    
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
dist
:
BaseDistribution
)
-
>
Tuple
[
Dict
[
str
str
]
Dict
[
str
str
]
]
:
    
console_scripts
=
{
}
    
gui_scripts
=
{
}
    
for
entry_point
in
dist
.
iter_entry_points
(
)
:
        
if
entry_point
.
group
=
=
"
console_scripts
"
:
            
console_scripts
[
entry_point
.
name
]
=
entry_point
.
value
        
elif
entry_point
.
group
=
=
"
gui_scripts
"
:
            
gui_scripts
[
entry_point
.
name
]
=
entry_point
.
value
    
return
console_scripts
gui_scripts
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
_normalized_outrows
(
outrows
)
:
    
"
"
"
Normalize
the
given
rows
of
a
RECORD
file
.
    
Items
in
each
row
are
converted
into
str
.
Rows
are
then
sorted
to
make
    
the
value
more
predictable
for
tests
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
        
(
ensure_str
(
record_path
encoding
=
'
utf
-
8
'
)
hash_
str
(
size
)
)
        
for
record_path
hash_
size
in
outrows
    
)
def
_record_to_fs_path
(
record_path
)
:
    
return
record_path
def
_fs_to_record_path
(
path
relative_to
=
None
)
:
    
if
relative_to
is
not
None
:
        
if
os
.
path
.
splitdrive
(
path
)
[
0
]
.
lower
(
)
=
=
\
                
os
.
path
.
splitdrive
(
relative_to
)
[
0
]
.
lower
(
)
:
            
path
=
os
.
path
.
relpath
(
path
relative_to
)
    
path
=
path
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
    
return
cast
(
'
RecordPath
'
path
)
def
_parse_record_path
(
record_column
)
:
    
p
=
ensure_text
(
record_column
encoding
=
'
utf
-
8
'
)
    
return
cast
(
'
RecordPath
'
p
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
%
s
'
row
)
        
old_record_path
=
_parse_record_path
(
row
[
0
]
)
        
new_record_path
=
installed
.
pop
(
old_record_path
old_record_path
)
        
if
new_record_path
in
changed
:
            
digest
length
=
rehash
(
_record_to_fs_path
(
new_record_path
)
)
        
else
:
            
digest
=
row
[
1
]
if
len
(
row
)
>
1
else
'
'
            
length
=
row
[
2
]
if
len
(
row
)
>
2
else
'
'
        
installed_rows
.
append
(
(
new_record_path
digest
length
)
)
    
for
f
in
generated
:
        
path
=
_fs_to_record_path
(
f
lib_dir
)
        
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
path
digest
length
)
)
    
for
installed_record_path
in
installed
.
values
(
)
:
        
installed_rows
.
append
(
(
installed_record_path
'
'
'
'
)
)
    
return
installed_rows
def
get_console_script_specs
(
console
)
:
    
"
"
"
    
Given
the
mapping
from
entrypoint
name
to
callable
return
the
relevant
    
console
script
specs
.
    
"
"
"
    
console
=
console
.
copy
(
)
    
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
{
}
=
{
}
'
.
format
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
            
f
'
pip
{
get_major_minor_version
(
)
}
=
{
pip_script
}
'
        
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
{
}
=
{
}
'
.
format
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
starmap
(
'
{
}
=
{
}
'
.
format
console
.
items
(
)
)
)
    
return
scripts_to_generate
class
ZipBackedFile
:
    
def
__init__
(
self
src_record_path
dest_path
zip_file
)
:
        
self
.
src_record_path
=
src_record_path
        
self
.
dest_path
=
dest_path
        
self
.
_zip_file
=
zip_file
        
self
.
changed
=
False
    
def
_getinfo
(
self
)
:
        
return
self
.
_zip_file
.
getinfo
(
self
.
src_record_path
)
    
def
save
(
self
)
:
        
parent_dir
=
os
.
path
.
dirname
(
self
.
dest_path
)
        
ensure_dir
(
parent_dir
)
        
if
os
.
path
.
exists
(
self
.
dest_path
)
:
            
os
.
unlink
(
self
.
dest_path
)
        
zipinfo
=
self
.
_getinfo
(
)
        
with
self
.
_zip_file
.
open
(
zipinfo
)
as
f
:
            
with
open
(
self
.
dest_path
"
wb
"
)
as
dest
:
                
shutil
.
copyfileobj
(
f
dest
)
        
if
zip_item_is_executable
(
zipinfo
)
:
            
set_extracted_file_to_default_mode_plus_executable
(
self
.
dest_path
)
class
ScriptFile
:
    
def
__init__
(
self
file
)
:
        
self
.
_file
=
file
        
self
.
src_record_path
=
self
.
_file
.
src_record_path
        
self
.
dest_path
=
self
.
_file
.
dest_path
        
self
.
changed
=
False
    
def
save
(
self
)
:
        
self
.
_file
.
save
(
)
        
self
.
changed
=
fix_script
(
self
.
dest_path
)
class
MissingCallableSuffix
(
InstallationError
)
:
    
def
__init__
(
self
entry_point
)
:
        
super
(
)
.
__init__
(
            
"
Invalid
script
entry
point
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
entry_point
)
        
)
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
)
.
make
(
specification
options
)
def
_install_wheel
(
    
name
    
wheel_zip
    
wheel_path
    
scheme
    
pycompile
=
True
    
warn_script_location
=
True
    
direct_url
=
None
    
requested
=
False
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
        
newpath
=
_fs_to_record_path
(
destfile
lib_dir
)
        
installed
[
srcfile
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
_fs_to_record_path
(
destfile
)
)
    
def
all_paths
(
)
:
        
names
=
wheel_zip
.
namelist
(
)
        
decoded_names
=
map
(
ensure_text
names
)
        
for
name
in
decoded_names
:
            
yield
cast
(
"
RecordPath
"
name
)
    
def
is_dir_path
(
path
)
:
        
return
path
.
endswith
(
"
/
"
)
    
def
assert_no_path_traversal
(
dest_dir_path
target_path
)
:
        
if
not
is_within_directory
(
dest_dir_path
target_path
)
:
            
message
=
(
                
"
The
wheel
{
!
r
}
has
a
file
{
!
r
}
trying
to
install
"
                
"
outside
the
target
directory
{
!
r
}
"
            
)
            
raise
InstallationError
(
                
message
.
format
(
wheel_path
target_path
dest_dir_path
)
            
)
    
def
root_scheme_file_maker
(
zip_file
dest
)
:
        
def
make_root_scheme_file
(
record_path
)
:
            
normed_path
=
os
.
path
.
normpath
(
record_path
)
            
dest_path
=
os
.
path
.
join
(
dest
normed_path
)
            
assert_no_path_traversal
(
dest
dest_path
)
            
return
ZipBackedFile
(
record_path
dest_path
zip_file
)
        
return
make_root_scheme_file
    
def
data_scheme_file_maker
(
zip_file
scheme
)
:
        
scheme_paths
=
{
}
        
for
key
in
SCHEME_KEYS
:
            
encoded_key
=
ensure_text
(
key
)
            
scheme_paths
[
encoded_key
]
=
ensure_text
(
                
getattr
(
scheme
key
)
encoding
=
sys
.
getfilesystemencoding
(
)
            
)
        
def
make_data_scheme_file
(
record_path
)
:
            
normed_path
=
os
.
path
.
normpath
(
record_path
)
            
try
:
                
_
scheme_key
dest_subpath
=
normed_path
.
split
(
os
.
path
.
sep
2
)
            
except
ValueError
:
                
message
=
(
                    
"
Unexpected
file
in
{
}
:
{
!
r
}
.
.
data
directory
contents
"
                    
"
should
be
named
like
:
'
<
scheme
key
>
/
<
path
>
'
.
"
                
)
.
format
(
wheel_path
record_path
)
                
raise
InstallationError
(
message
)
            
try
:
                
scheme_path
=
scheme_paths
[
scheme_key
]
            
except
KeyError
:
                
valid_scheme_keys
=
"
"
.
join
(
sorted
(
scheme_paths
)
)
                
message
=
(
                    
"
Unknown
scheme
key
used
in
{
}
:
{
}
(
for
file
{
!
r
}
)
.
.
data
"
                    
"
directory
contents
should
be
in
subdirectories
named
"
                    
"
with
a
valid
scheme
key
(
{
}
)
"
                
)
.
format
(
                    
wheel_path
scheme_key
record_path
valid_scheme_keys
                
)
                
raise
InstallationError
(
message
)
            
dest_path
=
os
.
path
.
join
(
scheme_path
dest_subpath
)
            
assert_no_path_traversal
(
scheme_path
dest_path
)
            
return
ZipBackedFile
(
record_path
dest_path
zip_file
)
        
return
make_data_scheme_file
    
def
is_data_scheme_path
(
path
)
:
        
return
path
.
split
(
"
/
"
1
)
[
0
]
.
endswith
(
"
.
data
"
)
    
paths
=
all_paths
(
)
    
file_paths
=
filterfalse
(
is_dir_path
paths
)
    
root_scheme_paths
data_scheme_paths
=
partition
(
        
is_data_scheme_path
file_paths
    
)
    
make_root_scheme_file
=
root_scheme_file_maker
(
        
wheel_zip
        
ensure_text
(
lib_dir
encoding
=
sys
.
getfilesystemencoding
(
)
)
    
)
    
files
=
map
(
make_root_scheme_file
root_scheme_paths
)
    
def
is_script_scheme_path
(
path
)
:
        
parts
=
path
.
split
(
"
/
"
2
)
        
return
(
            
len
(
parts
)
>
2
and
            
parts
[
0
]
.
endswith
(
"
.
data
"
)
and
            
parts
[
1
]
=
=
"
scripts
"
        
)
    
other_scheme_paths
script_scheme_paths
=
partition
(
        
is_script_scheme_path
data_scheme_paths
    
)
    
make_data_scheme_file
=
data_scheme_file_maker
(
wheel_zip
scheme
)
    
other_scheme_files
=
map
(
make_data_scheme_file
other_scheme_paths
)
    
files
=
chain
(
files
other_scheme_files
)
    
distribution
=
get_wheel_distribution
(
wheel_path
canonicalize_name
(
name
)
)
    
console
gui
=
get_entrypoints
(
distribution
)
    
def
is_entrypoint_wrapper
(
file
)
:
        
path
=
file
.
dest_path
        
name
=
os
.
path
.
basename
(
path
)
        
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
    
script_scheme_files
=
map
(
make_data_scheme_file
script_scheme_paths
)
    
script_scheme_files
=
filterfalse
(
        
is_entrypoint_wrapper
script_scheme_files
    
)
    
script_scheme_files
=
map
(
ScriptFile
script_scheme_files
)
    
files
=
chain
(
files
script_scheme_files
)
    
for
file
in
files
:
        
file
.
save
(
)
        
record_installed
(
file
.
src_record_path
file
.
dest_path
file
.
changed
)
    
def
pyc_source_file_paths
(
)
:
        
for
installed_path
in
sorted
(
set
(
installed
.
values
(
)
)
)
:
            
full_installed_path
=
os
.
path
.
join
(
lib_dir
installed_path
)
            
if
not
os
.
path
.
isfile
(
full_installed_path
)
:
                
continue
            
if
not
full_installed_path
.
endswith
(
'
.
py
'
)
:
                
continue
            
yield
full_installed_path
    
def
pyc_output_path
(
path
)
:
        
"
"
"
Return
the
path
the
pyc
file
would
have
been
written
to
.
        
"
"
"
        
return
importlib
.
util
.
cache_from_source
(
path
)
    
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
                
for
path
in
pyc_source_file_paths
(
)
:
                    
path_arg
=
ensure_str
(
                        
path
encoding
=
sys
.
getfilesystemencoding
(
)
                    
)
                    
success
=
compileall
.
compile_file
(
                        
path_arg
force
=
True
quiet
=
True
                    
)
                    
if
success
:
                        
pyc_path
=
pyc_output_path
(
path
)
                        
assert
os
.
path
.
exists
(
pyc_path
)
                        
pyc_record_path
=
cast
(
                            
"
RecordPath
"
pyc_path
.
replace
(
os
.
path
.
sep
"
/
"
)
                        
)
                        
record_installed
(
pyc_record_path
pyc_path
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
get_console_script_specs
(
console
)
    
gui_scripts_to_generate
=
list
(
starmap
(
'
{
}
=
{
}
'
.
format
gui
.
items
(
)
)
)
    
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
    
generated_file_mode
=
0o666
&
~
current_umask
(
)
    
contextlib
.
contextmanager
    
def
_generate_file
(
path
*
*
kwargs
)
:
        
with
adjacent_tmp_file
(
path
*
*
kwargs
)
as
f
:
            
yield
f
        
os
.
chmod
(
f
.
name
generated_file_mode
)
        
replace
(
f
.
name
path
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
    
installer_path
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
    
with
_generate_file
(
installer_path
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
    
generated
.
append
(
installer_path
)
    
if
direct_url
is
not
None
:
        
direct_url_path
=
os
.
path
.
join
(
dest_info_dir
DIRECT_URL_METADATA_NAME
)
        
with
_generate_file
(
direct_url_path
)
as
direct_url_file
:
            
direct_url_file
.
write
(
direct_url
.
to_json
(
)
.
encode
(
"
utf
-
8
"
)
)
        
generated
.
append
(
direct_url_path
)
    
if
requested
:
        
requested_path
=
os
.
path
.
join
(
dest_info_dir
'
REQUESTED
'
)
        
with
open
(
requested_path
"
wb
"
)
:
            
pass
        
generated
.
append
(
requested_path
)
    
record_text
=
distribution
.
read_text
(
'
RECORD
'
)
    
record_rows
=
list
(
csv
.
reader
(
record_text
.
splitlines
(
)
)
)
    
rows
=
get_csv_rows_for_installed
(
        
record_rows
        
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
    
record_path
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
    
with
_generate_file
(
record_path
*
*
csv_io_kwargs
(
'
w
'
)
)
as
record_file
:
        
writer
=
csv
.
writer
(
cast
(
'
IO
[
str
]
'
record_file
)
)
        
writer
.
writerows
(
_normalized_outrows
(
rows
)
)
contextlib
.
contextmanager
def
req_error_context
(
req_description
)
:
    
try
:
        
yield
    
except
InstallationError
as
e
:
        
message
=
"
For
req
:
{
}
.
{
}
"
.
format
(
req_description
e
.
args
[
0
]
)
        
reraise
(
            
InstallationError
InstallationError
(
message
)
sys
.
exc_info
(
)
[
2
]
        
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
    
direct_url
=
None
    
requested
=
False
)
:
    
with
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
        
with
req_error_context
(
req_description
)
:
            
_install_wheel
(
                
name
=
name
                
wheel_zip
=
z
                
wheel_path
=
wheel_path
                
scheme
=
scheme
                
pycompile
=
pycompile
                
warn_script_location
=
warn_script_location
                
direct_url
=
direct_url
                
requested
=
requested
            
)
