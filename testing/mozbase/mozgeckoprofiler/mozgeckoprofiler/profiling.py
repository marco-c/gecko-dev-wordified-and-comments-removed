import
os
from
pathlib
import
Path
from
mozlog
import
get_proxy_logger
from
.
symbolication
import
get_extracted_symbols
symbolicate_profile_file
LOG
=
get_proxy_logger
(
"
profiler
"
)
def
symbolicate_profile_json
(
profile_path
symbol_dir
=
None
)
:
    
"
"
"
Symbolicate
a
profile
in
place
.
    
Args
:
        
profile_path
(
path
)
:
The
profile
to
symbolicate
.
Rewritten
in
place
            
keeping
its
original
compression
.
Left
untouched
if
symbolication
            
fails
.
        
symbol_dir
(
path
)
:
Directory
of
Breakpad
symbols
to
use
.
When
omitted
            
it
is
looked
up
with
get_extracted_symbols
(
)
.
    
"
"
"
    
profile_path
=
Path
(
profile_path
)
    
stat
=
profile_path
.
stat
(
)
    
suffix
=
"
.
json
.
gz
"
if
profile_path
.
name
.
endswith
(
"
.
gz
"
)
else
"
.
json
"
    
out_path
=
profile_path
.
with_name
(
f
"
.
{
profile_path
.
name
}
.
sym
{
suffix
}
"
)
    
LOG
.
info
(
f
"
Symbolicating
{
profile_path
.
name
}
(
{
stat
.
st_size
}
bytes
)
.
.
.
"
)
    
try
:
        
if
not
symbolicate_profile_file
(
profile_path
out_path
symbol_dir
)
:
            
LOG
.
warning
(
f
"
Not
replacing
{
profile_path
.
name
}
:
symbolication
failed
.
"
)
            
return
        
sym_size
=
out_path
.
stat
(
)
.
st_size
        
os
.
replace
(
out_path
profile_path
)
        
LOG
.
info
(
            
f
"
Successfully
symbolicated
{
profile_path
.
name
}
:
"
            
f
"
{
stat
.
st_size
}
bytes
-
>
{
sym_size
}
bytes
"
        
)
    
finally
:
        
out_path
.
unlink
(
missing_ok
=
True
)
    
os
.
utime
(
profile_path
(
stat
.
st_atime
stat
.
st_mtime
)
)
def
symbolicate_profiles
(
profile_dir
=
None
symbol_dir
=
None
)
:
    
if
"
MOZ_AUTOMATION
"
in
os
.
environ
:
        
if
profile_dir
is
None
and
os
.
environ
.
get
(
"
MOZ_UPLOAD_DIR
"
)
:
            
profile_dir
=
Path
(
os
.
environ
.
get
(
"
MOZ_UPLOAD_DIR
"
)
)
    
if
profile_dir
is
None
:
        
LOG
.
warning
(
"
No
profile
directory
specified
skipping
symbolication
"
)
        
return
    
profile_files
=
sorted
(
        
profile
        
for
pattern
in
(
"
profile_
*
.
json
"
"
profile_
*
.
json
.
gz
"
)
        
for
profile
in
profile_dir
.
glob
(
pattern
)
        
if
"
resource
-
usage
"
not
in
profile
.
name
    
)
    
if
symbol_dir
is
None
:
        
symbol_dir
=
get_extracted_symbols
(
)
        
if
symbol_dir
is
None
:
            
LOG
.
warning
(
                
"
Symbols
not
found
.
Attempting
to
symbolication
with
remote
symbol
server
.
"
            
)
    
for
profile_file
in
profile_files
:
        
try
:
            
symbolicate_profile_json
(
profile_file
symbol_dir
)
        
except
Exception
as
e
:
            
LOG
.
warning
(
                
f
"
Failed
to
symbolicate
{
profile_file
.
name
}
:
{
e
}
"
                
exc_info
=
True
            
)
