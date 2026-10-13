import
gzip
import
os
import
shutil
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
MAX_SYMBOLICATABLE_PROFILE_SIZE
=
2
*
*
29
-
24
def
_gzip_file
(
in_path
out_path
)
:
    
with
open
(
in_path
"
rb
"
)
as
f_in
gzip
.
open
(
out_path
"
wb
"
)
as
f_out
:
        
shutil
.
copyfileobj
(
f_in
f_out
1024
*
1024
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
replacing
it
with
a
gzipped
symbolicated
profile
.
    
Symbolicated
profiles
are
always
gzipped
whatever
the
input
'
s
compression
    
so
the
result
is
named
"
.
json
.
gz
"
.
The
profile
therefore
moves
when
it
was
    
not
already
named
that
way
and
callers
should
use
the
returned
path
.
The
    
move
happens
even
when
symbolication
fails
in
which
case
the
unsymbolicated
    
profile
is
gzipped
instead
so
that
harnesses
can
name
the
artifact
before
    
symbolication
has
run
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
    
Returns
:
        
Path
:
Where
the
profile
ended
up
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
:
        
final_path
=
profile_path
    
else
:
        
final_path
=
profile_path
.
with_name
(
profile_path
.
name
+
"
.
gz
"
)
        
if
final_path
.
exists
(
)
:
            
LOG
.
warning
(
                
f
"
Not
renaming
{
profile_path
.
name
}
to
{
final_path
.
name
}
:
"
                
"
a
profile
of
that
name
already
exists
.
"
            
)
            
final_path
=
profile_path
    
out_path
=
final_path
.
with_name
(
f
"
.
{
final_path
.
name
}
.
sym
.
json
.
gz
"
)
    
try
:
        
if
stat
.
st_size
>
MAX_SYMBOLICATABLE_PROFILE_SIZE
:
            
LOG
.
warning
(
                
f
"
Not
symbolicating
{
profile_path
.
name
}
:
its
{
stat
.
st_size
}
bytes
"
                
"
are
too
large
for
profiler
-
edit
.
"
            
)
            
symbolicated
=
False
        
else
:
            
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
            
symbolicated
=
symbolicate_profile_file
(
profile_path
out_path
symbol_dir
)
        
if
symbolicated
:
            
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
final_path
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
-
>
{
final_path
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
        
elif
final_path
!
=
profile_path
:
            
LOG
.
warning
(
                
f
"
Gzipping
{
profile_path
.
name
}
unsymbolicated
as
{
final_path
.
name
}
.
"
            
)
            
_gzip_file
(
profile_path
out_path
)
            
os
.
replace
(
out_path
final_path
)
        
else
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
profile_path
        
if
final_path
!
=
profile_path
:
            
profile_path
.
unlink
(
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
final_path
(
stat
.
st_atime
stat
.
st_mtime
)
)
    
return
final_path
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
not
profile_files
:
        
return
    
if
symbol_dir
is
not
None
and
not
Path
(
symbol_dir
)
.
is_dir
(
)
:
        
symbol_dir
=
None
    
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
