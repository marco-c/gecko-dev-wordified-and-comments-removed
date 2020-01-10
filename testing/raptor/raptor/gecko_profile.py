"
"
"
module
to
handle
Gecko
profilling
.
"
"
"
from
__future__
import
absolute_import
import
json
import
os
import
tempfile
import
zipfile
import
mozfile
from
logger
.
logger
import
RaptorLogger
from
profiler
import
symbolication
profiling
here
=
os
.
path
.
dirname
(
os
.
path
.
realpath
(
__file__
)
)
LOG
=
RaptorLogger
(
component
=
'
raptor
-
gecko
-
profile
'
)
class
GeckoProfile
(
object
)
:
    
"
"
"
    
Handle
Gecko
profilling
.
    
This
allow
to
collect
Gecko
profiling
data
and
to
zip
results
in
one
file
.
    
"
"
"
    
def
__init__
(
self
upload_dir
raptor_config
test_config
)
:
        
self
.
upload_dir
=
upload_dir
        
self
.
raptor_config
self
.
test_config
=
raptor_config
test_config
        
self
.
cleanup
=
True
        
self
.
gecko_profile_dir
=
tempfile
.
mkdtemp
(
)
        
gecko_profile_interval
=
test_config
.
get
(
'
gecko_profile_interval
'
1
)
        
gecko_profile_entries
=
test_config
.
get
(
'
gecko_profile_entries
'
1000000
)
        
cmd_line_interval
=
raptor_config
.
get
(
'
gecko_profile_interval
'
None
)
        
if
cmd_line_interval
is
not
None
:
            
gecko_profile_interval
=
cmd_line_interval
        
cmd_line_entries
=
raptor_config
.
get
(
'
gecko_profile_entries
'
None
)
        
if
cmd_line_entries
is
not
None
:
            
gecko_profile_entries
=
cmd_line_entries
        
if
not
self
.
raptor_config
[
'
symbols_path
'
]
and
\
           
self
.
raptor_config
[
'
run_local
'
]
and
\
           
'
MOZ_DEVELOPER_OBJ_DIR
'
in
os
.
environ
:
            
self
.
raptor_config
[
'
symbols_path
'
]
=
os
.
path
.
join
(
os
.
environ
[
'
MOZ_DEVELOPER_OBJ_DIR
'
]
                                                              
'
dist
'
                                                              
'
crashreporter
-
symbols
'
)
        
os
.
environ
[
'
MOZ_CRASHREPORTER_NO_REPORT
'
]
=
'
1
'
        
if
self
.
raptor_config
[
'
symbols_path
'
]
:
            
os
.
environ
[
'
MOZ_CRASHREPORTER
'
]
=
'
1
'
        
else
:
            
os
.
environ
[
'
MOZ_CRASHREPORTER_DISABLE
'
]
=
'
1
'
        
self
.
profile_arcname
=
os
.
path
.
join
(
            
self
.
upload_dir
            
"
profile_
{
0
}
.
zip
"
.
format
(
test_config
[
'
name
'
]
)
        
)
        
LOG
.
info
(
"
Clearing
archive
{
0
}
"
.
format
(
self
.
profile_arcname
)
)
        
mozfile
.
remove
(
self
.
profile_arcname
)
        
self
.
symbol_paths
=
{
            
'
FIREFOX
'
:
tempfile
.
mkdtemp
(
)
            
'
WINDOWS
'
:
tempfile
.
mkdtemp
(
)
        
}
        
LOG
.
info
(
"
Activating
gecko
profiling
temp
profile
dir
:
"
                 
"
{
0
}
interval
:
{
1
}
entries
:
{
2
}
"
                 
.
format
(
self
.
gecko_profile_dir
                         
gecko_profile_interval
                         
gecko_profile_entries
)
)
    
def
_save_gecko_profile
(
self
symbolicator
missing_symbols_zip
                            
profile_path
)
:
        
try
:
            
with
open
(
profile_path
'
r
'
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
            
profiling
.
save_profile
(
profile
profile_path
)
        
except
MemoryError
:
            
LOG
.
critical
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
                
exc_info
=
True
            
)
        
except
Exception
:
            
LOG
.
critical
(
"
Encountered
an
exception
during
profile
"
                         
"
symbolication
{
0
}
"
                         
.
format
(
profile_path
)
                         
exc_info
=
True
)
    
def
symbolicate
(
self
)
:
        
"
"
"
        
Symbolicate
Gecko
profiling
data
for
one
pagecycle
.
        
"
"
"
        
symbolicator
=
symbolication
.
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
self
.
symbol_paths
        
}
)
        
if
self
.
raptor_config
.
get
(
'
symbols_path
'
None
)
is
not
None
:
            
if
mozfile
.
is_url
(
self
.
raptor_config
[
'
symbols_path
'
]
)
:
                
symbolicator
.
integrate_symbol_zip_from_url
(
                    
self
.
raptor_config
[
'
symbols_path
'
]
                
)
            
elif
os
.
path
.
isfile
(
self
.
raptor_config
[
'
symbols_path
'
]
)
:
                
symbolicator
.
integrate_symbol_zip_from_file
(
                    
self
.
raptor_config
[
'
symbols_path
'
]
                
)
            
elif
os
.
path
.
isdir
(
self
.
raptor_config
[
'
symbols_path
'
]
)
:
                
sym_path
=
self
.
raptor_config
[
'
symbols_path
'
]
                
symbolicator
.
options
[
"
symbolPaths
"
]
[
"
FIREFOX
"
]
=
sym_path
                
self
.
cleanup
=
False
        
missing_symbols_zip
=
os
.
path
.
join
(
self
.
upload_dir
                                           
"
missingsymbols
.
zip
"
)
        
try
:
            
mode
=
zipfile
.
ZIP_DEFLATED
        
except
NameError
:
            
mode
=
zipfile
.
ZIP_STORED
        
with
zipfile
.
ZipFile
(
self
.
profile_arcname
'
a
'
mode
)
as
arc
:
            
for
profile_filename
in
os
.
listdir
(
self
.
gecko_profile_dir
)
:
                
testname
=
profile_filename
                
if
testname
.
endswith
(
"
.
profile
"
)
:
                    
testname
=
testname
[
0
:
-
8
]
                
profile_path
=
os
.
path
.
join
(
self
.
gecko_profile_dir
profile_filename
)
                
self
.
_save_gecko_profile
(
symbolicator
                                         
missing_symbols_zip
                                         
profile_path
)
                
path_in_zip
=
\
                    
os
.
path
.
join
(
                        
"
profile_
{
0
}
"
.
format
(
self
.
test_config
[
'
name
'
]
)
                        
testname
+
"
.
profile
"
)
                
LOG
.
info
(
                    
"
Adding
profile
{
0
}
to
archive
{
1
}
"
                    
.
format
(
path_in_zip
self
.
profile_arcname
)
                
)
                
try
:
                    
arc
.
write
(
profile_path
path_in_zip
)
                
except
Exception
:
                    
LOG
.
exception
(
                        
"
Failed
to
copy
profile
{
0
}
as
{
1
}
to
"
                        
"
archive
{
2
}
"
.
format
(
profile_path
                                              
path_in_zip
                                              
self
.
profile_arcname
)
                    
)
            
os
.
environ
[
'
RAPTOR_LATEST_GECKO_PROFILE_ARCHIVE
'
]
=
self
.
profile_arcname
    
def
clean
(
self
)
:
        
"
"
"
        
Clean
up
temp
folders
created
with
the
instance
creation
.
        
"
"
"
        
mozfile
.
remove
(
self
.
gecko_profile_dir
)
        
if
self
.
cleanup
:
            
for
symbol_path
in
self
.
symbol_paths
.
values
(
)
:
                
mozfile
.
remove
(
symbol_path
)
