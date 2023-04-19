from
__future__
import
absolute_import
import
json
import
tempfile
import
shutil
import
os
from
.
symbolication
import
ProfileSymbolicator
from
mozlog
import
get_proxy_logger
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
)
:
    
with
open
(
filename
"
w
"
)
as
f
:
        
json
.
dump
(
profile
f
)
def
symbolicate_profile_json
(
profile_path
objdir_path
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
    
temp_dir
=
tempfile
.
mkdtemp
(
)
    
missing_symbols_zip
=
os
.
path
.
join
(
temp_dir
"
missingsymbols
.
zip
"
)
    
firefox_symbol_path
=
os
.
path
.
join
(
objdir_path
"
dist
"
"
crashreporter
-
symbols
"
)
    
if
not
os
.
path
.
isdir
(
firefox_symbol_path
)
:
        
os
.
mkdir
(
firefox_symbol_path
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
firefox_symbol_path
"
WINDOWS
"
:
windows_symbol_path
}
    
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
symbols
.
mozilla
.
org
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
This
could
take
a
couple
"
        
"
of
minutes
.
"
    
)
    
try
:
        
with
open
(
profile_path
"
r
"
encoding
=
"
utf
-
8
"
)
as
profile_file
:
            
profile
=
json
.
load
(
profile_file
)
        
symbolicator
.
dump_and_integrate_missing_symbols
(
profile
missing_symbols_zip
)
        
symbolicator
.
symbolicate_profile
(
profile
)
        
save_gecko_profile
(
profile
profile_path
)
    
except
MemoryError
:
        
LOG
.
error
(
            
"
Ran
out
of
memory
while
trying
"
            
"
to
symbolicate
profile
{
0
}
"
.
format
(
profile_path
)
        
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
    
shutil
.
rmtree
(
temp_dir
)
