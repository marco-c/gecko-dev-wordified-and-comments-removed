import
gzip
import
json
import
os
import
shutil
import
tempfile
from
pathlib
import
Path
try
:
    
import
orjson
except
ImportError
:
    
orjson
=
None
from
mozlog
import
get_proxy_logger
from
.
symbolication
import
ProfileSymbolicator
get_extracted_symbols
LOG
=
get_proxy_logger
(
"
profiler
"
)
def
save_gecko_profile
(
profile
filename
gzip_compress
=
False
)
:
    
LOG
.
info
(
        
f
"
Saving
profile
to
{
filename
}
{
'
with
gzip
compression
'
if
gzip_compress
else
'
'
}
"
    
)
    
if
orjson
is
not
None
:
        
try
:
            
data
=
orjson
.
dumps
(
profile
)
        
except
Exception
:
            
data
=
json
.
dumps
(
profile
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
    
else
:
        
data
=
json
.
dumps
(
profile
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
    
if
gzip_compress
:
        
with
gzip
.
open
(
filename
"
wb
"
)
as
f
:
            
f
.
write
(
data
)
    
else
:
        
with
open
(
filename
"
wb
"
)
as
f
:
            
f
.
write
(
data
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
single
JSON
profile
.
    
"
"
"
    
stat
=
Path
(
profile_path
)
.
stat
(
)
    
original_atime
=
stat
.
st_atime
    
original_mtime
=
stat
.
st_mtime
    
with
tempfile
.
TemporaryDirectory
(
)
as
work_dir
:
        
if
symbol_dir
is
None
:
            
symbol_dir
=
get_extracted_symbols
(
work_dir
)
        
temp_dir
=
tempfile
.
mkdtemp
(
)
        
windows_symbol_path
=
os
.
path
.
join
(
temp_dir
"
windows
"
)
        
os
.
mkdir
(
windows_symbol_path
)
        
symbol_paths
=
{
"
FIREFOX
"
:
symbol_dir
"
WINDOWS
"
:
windows_symbol_path
}
        
try
:
            
symbolicator
=
ProfileSymbolicator
(
{
                
"
enableTracing
"
:
0
                
"
remoteSymbolServer
"
:
"
https
:
/
/
symbolication
.
services
.
mozilla
.
com
/
symbolicate
/
v4
"
                
"
maxCacheEntries
"
:
2000000
                
"
prefetchInterval
"
:
12
                
"
prefetchThreshold
"
:
48
                
"
prefetchMaxSymbolsPerLib
"
:
3
                
"
defaultApp
"
:
"
FIREFOX
"
                
"
defaultOs
"
:
"
WINDOWS
"
                
"
symbolPaths
"
:
symbol_paths
            
}
)
            
LOG
.
info
(
"
Symbolicating
the
performance
profile
.
.
.
"
)
            
try
:
                
gzipped
=
False
                
with
open
(
profile_path
"
rb
"
)
as
profile_file
:
                    
data
=
profile_file
.
read
(
)
                    
LOG
.
info
(
f
"
Profile
file
size
:
{
len
(
data
)
}
bytes
"
)
                    
gzip_magic_number
=
b
"
\
x1f
\
x8b
"
                    
if
data
[
:
2
]
=
=
gzip_magic_number
:
                        
gzipped
=
True
                        
data
=
gzip
.
decompress
(
data
)
                        
LOG
.
info
(
f
"
Decompressed
profile
size
:
{
len
(
data
)
}
bytes
"
)
                    
else
:
                        
LOG
.
debug
(
"
Profile
was
not
gzipped
treating
as
regular
JSON
"
)
                    
if
orjson
is
not
None
:
                        
try
:
                            
profile
=
orjson
.
loads
(
data
)
                        
except
Exception
:
                            
profile
=
json
.
loads
(
data
)
                    
else
:
                        
profile
=
json
.
loads
(
data
)
                
symbolicator
.
symbolicate_profile
(
profile
symbol_dir
)
                
save_gecko_profile
(
profile
profile_path
gzip_compress
=
gzipped
)
            
except
MemoryError
:
                
LOG
.
error
(
                    
f
"
Ran
out
of
memory
while
trying
to
symbolicate
profile
{
profile_path
}
"
                
)
            
except
Exception
as
e
:
                
LOG
.
error
(
"
Encountered
an
exception
during
profile
symbolication
"
)
                
LOG
.
error
(
e
)
        
finally
:
            
shutil
.
rmtree
(
temp_dir
)
    
os
.
utime
(
profile_path
(
original_atime
original_mtime
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
profile
in
profile_dir
.
glob
(
"
profile_
*
.
json
"
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
    
with
tempfile
.
TemporaryDirectory
(
)
as
work_dir
:
        
if
symbol_dir
is
None
:
            
symbol_dir
=
get_extracted_symbols
(
work_dir
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
        
with
tempfile
.
TemporaryDirectory
(
)
as
temp_dir
:
            
for
profile_file
in
profile_files
:
                
stat
=
profile_file
.
stat
(
)
                
unsym_size
=
stat
.
st_size
                
unsym_mod_time
=
stat
.
st_mtime
                
unsym_access_time
=
stat
.
st_atime
                
LOG
.
info
(
f
"
Symbolicating
{
profile_file
.
name
}
(
{
unsym_size
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
                    
temp_path
=
Path
(
temp_dir
)
/
profile_file
.
name
                    
shutil
.
copy
(
profile_file
temp_path
)
                    
symbolicate_profile_json
(
str
(
temp_path
)
symbol_dir
)
                    
if
temp_path
.
is_file
(
)
:
                        
sym_size
=
temp_path
.
stat
(
)
.
st_size
                        
LOG
.
info
(
                            
f
"
Successfully
symbolicated
{
profile_file
.
name
}
:
"
                            
f
"
{
unsym_size
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
                        
try
:
                            
os
.
replace
(
str
(
temp_path
)
str
(
profile_file
)
)
                            
LOG
.
info
(
                                
f
"
Successfully
moved
{
profile_file
.
name
}
using
os
.
replace
"
                            
)
                        
except
Exception
:
                            
shutil
.
move
(
str
(
temp_path
)
str
(
profile_file
)
)
                            
LOG
.
info
(
                                
f
"
Successfully
moved
{
profile_file
.
name
}
using
shutil
.
move
"
                            
)
                        
os
.
utime
(
profile_file
(
unsym_access_time
unsym_mod_time
)
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
