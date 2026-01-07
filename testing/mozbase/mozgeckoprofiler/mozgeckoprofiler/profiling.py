import
os
import
shutil
import
tempfile
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
    
import
json
from
mozlog
import
get_proxy_logger
from
.
symbolication
import
ProfileSymbolicator
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
wb
"
)
as
f
:
        
if
orjson
is
not
None
:
            
f
.
write
(
orjson
.
dumps
(
profile
)
)
        
else
:
            
f
.
write
(
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
)
def
symbolicate_profile_json
(
profile_path
firefox_symbols_path
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
firefox_symbols_path
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
This
could
take
a
couple
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
rb
"
)
as
profile_file
:
            
if
orjson
is
not
None
:
                
profile
=
orjson
.
loads
(
profile_file
.
read
(
)
)
            
else
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
    
shutil
.
rmtree
(
temp_dir
)
