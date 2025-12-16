"
"
"
Module
to
handle
Gecko
profiling
.
"
"
"
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
mozgeckoprofiler
import
ProfileSymbolicator
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
"
raptor
-
gecko
-
profile
"
)
from
raptor_profiling
import
RaptorProfiling
class
GeckoProfile
(
RaptorProfiling
)
:
    
"
"
"
    
Handle
Gecko
profiling
.
    
This
allows
us
to
collect
Gecko
profiling
data
and
to
zip
results
into
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
        
super
(
)
.
__init__
(
upload_dir
raptor_config
test_config
)
        
self
.
cleanup
=
True
        
self
.
profile_entry_string
=
"
geckoProfiles
"
        
gecko_profile_interval
=
raptor_config
.
get
(
            
"
gecko_profile_interval
"
None
        
)
or
test_config
.
get
(
"
gecko_profile_interval
"
1
)
        
gecko_profile_entries
=
raptor_config
.
get
(
            
"
gecko_profile_entries
"
None
        
)
or
test_config
.
get
(
"
gecko_profile_entries
"
1000000
)
        
if
(
            
not
self
.
raptor_config
[
"
symbols_path
"
]
            
and
self
.
raptor_config
[
"
run_local
"
]
            
and
"
MOZ_DEVELOPER_OBJ_DIR
"
in
os
.
environ
        
)
:
            
self
.
raptor_config
[
"
symbols_path
"
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
"
MOZ_DEVELOPER_OBJ_DIR
"
]
"
dist
"
"
crashreporter
-
symbols
"
            
)
        
os
.
environ
[
"
MOZ_CRASHREPORTER_NO_REPORT
"
]
=
"
1
"
        
if
self
.
raptor_config
[
"
symbols_path
"
]
:
            
os
.
environ
[
"
MOZ_CRASHREPORTER
"
]
=
"
1
"
        
else
:
            
os
.
environ
[
"
MOZ_CRASHREPORTER_DISABLE
"
]
=
"
1
"
        
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
}
.
zip
"
.
format
(
self
.
test_config
[
"
name
"
]
)
        
)
        
LOG
.
info
(
f
"
Clearing
archive
{
self
.
profile_arcname
}
"
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
            
"
FIREFOX
"
:
tempfile
.
mkdtemp
(
)
            
"
WINDOWS
"
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
            
f
"
{
self
.
temp_profile_dir
}
interval
:
{
gecko_profile_interval
}
entries
:
{
gecko_profile_entries
}
"
        
)
    
property
    
def
_is_extra_profiler_run
(
self
)
:
        
return
self
.
raptor_config
.
get
(
"
extra_profiler_run
"
False
)
    
def
_symbolicate_profile
(
self
profile
missing_symbols_zip
symbolicator
)
:
        
try
:
            
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
            
return
profile
        
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
to
symbolicate
profile
.
"
exc_info
=
True
            
)
            
raise
        
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
symbolication
.
"
exc_info
=
True
            
)
            
return
profile
    
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
        
profiles
=
self
.
collect_profiles
(
)
        
if
len
(
profiles
)
=
=
0
:
            
if
self
.
_is_extra_profiler_run
:
                
LOG
.
info
(
"
No
profiles
collected
in
the
extra
profiler
run
"
)
            
else
:
                
LOG
.
error
(
"
No
profiles
collected
"
)
            
return
        
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
"
symbols_path
"
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
"
symbols_path
"
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
"
symbols_path
"
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
"
symbols_path
"
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
"
symbols_path
"
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
"
symbols_path
"
]
)
:
                
sym_path
=
self
.
raptor_config
[
"
symbols_path
"
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
        
test_type
=
self
.
test_config
.
get
(
"
type
"
"
pageload
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
"
a
"
mode
)
as
arc
:
            
for
profile_info
in
profiles
:
                
profile_path
=
profile_info
[
"
path
"
]
                
LOG
.
info
(
"
Opening
profile
at
%
s
"
%
profile_path
)
                
try
:
                    
profile
=
self
.
_open_profile_file
(
profile_path
)
                
except
FileNotFoundError
:
                    
if
self
.
_is_extra_profiler_run
:
                        
LOG
.
info
(
"
Profile
not
found
on
extra
profiler
run
.
"
)
                    
else
:
                        
LOG
.
error
(
"
Profile
not
found
.
"
)
                    
continue
                
LOG
.
info
(
"
Symbolicating
profile
from
%
s
"
%
profile_path
)
                
symbolicated_profile
=
self
.
_symbolicate_profile
(
                    
profile
missing_symbols_zip
symbolicator
                
)
                
try
:
                    
test_run_type
=
(
                        
"
{
}
-
{
}
"
.
format
(
test_type
profile_info
[
"
type
"
]
)
                        
if
test_type
=
=
"
pageload
"
                        
else
test_type
                    
)
                    
folder_name
=
"
%
s
-
%
s
"
%
(
self
.
test_config
[
"
name
"
]
test_run_type
)
                    
iteration
=
str
(
os
.
path
.
split
(
profile_path
)
[
-
1
]
.
split
(
"
-
"
)
[
-
1
]
)
                    
if
test_type
=
=
"
pageload
"
and
profile_info
[
"
type
"
]
=
=
"
cold
"
:
                        
iteration_type
=
"
browser
-
cycle
"
                    
elif
profile_info
[
"
type
"
]
=
=
"
warm
"
:
                        
iteration_type
=
"
page
-
cycle
"
                    
else
:
                        
iteration_type
=
"
iteration
"
                    
profile_name
=
"
-
"
.
join
(
[
iteration_type
iteration
]
)
                    
path_in_zip
=
os
.
path
.
join
(
folder_name
profile_name
)
                    
LOG
.
info
(
                        
"
Adding
profile
%
s
to
archive
%
s
as
%
s
"
                        
%
(
profile_path
self
.
profile_arcname
path_in_zip
)
                    
)
                    
arc
.
writestr
(
                        
path_in_zip
                        
json
.
dumps
(
symbolicated_profile
ensure_ascii
=
False
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
add
symbolicated
profile
%
s
to
archive
%
s
"
                        
%
(
profile_path
self
.
profile_arcname
)
                    
)
                    
raise
        
os
.
environ
[
"
RAPTOR_LATEST_GECKO_PROFILE_ARCHIVE
"
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
temp_profile_dir
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
