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
symbolicate_profile_file
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
_profile_archive_paths
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
source_path_mappings
=
None
    
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
source_path_mappings
)
        
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
profile_path
out_path
)
:
        
try
:
            
return
symbolicate_profile_file
(
                
profile_path
                
out_path
                
source_path_mappings
=
self
.
source_path_mappings
            
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
symbolication
.
"
exc_info
=
True
            
)
            
return
False
    
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
tempfile
.
TemporaryDirectory
(
)
as
sym_dir
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
            
symbolicated
=
[
]
            
for
index
profile_info
in
enumerate
(
profiles
)
:
                
profile_path
=
profile_info
[
"
path
"
]
                
if
not
os
.
path
.
exists
(
profile_path
)
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
f
"
Symbolicating
profile
from
{
profile_path
}
"
)
                
sym_path
=
os
.
path
.
join
(
sym_dir
f
"
{
index
}
.
json
"
)
                
archived_path
=
(
                    
sym_path
                    
if
self
.
_symbolicate_profile
(
profile_path
sym_path
)
                    
else
profile_path
                
)
                
symbolicated
.
append
(
(
profile_info
archived_path
)
)
            
archive_paths
=
_profile_archive_paths
(
                
self
.
test_config
                
[
profile_info
for
profile_info
_
in
symbolicated
]
                
[
                    
"
.
json
.
gz
"
if
archived_path
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
                    
for
_
archived_path
in
symbolicated
                
]
            
)
            
for
(
profile_info
archived_path
)
path_in_zip
in
zip
(
                
symbolicated
archive_paths
            
)
:
                
try
:
                    
LOG
.
info
(
                        
f
"
Adding
profile
{
profile_info
[
'
path
'
]
}
to
archive
"
                        
f
"
{
self
.
profile_arcname
}
as
{
path_in_zip
}
"
                    
)
                    
arc
.
write
(
archived_path
path_in_zip
)
                
except
Exception
:
                    
LOG
.
exception
(
                        
f
"
Failed
to
add
symbolicated
profile
{
profile_info
[
'
path
'
]
}
to
"
                        
f
"
archive
{
self
.
profile_arcname
}
"
                    
)
                    
raise
        
os
.
environ
[
"
RAPTOR_LATEST_PROFILE
"
]
=
self
.
profile_arcname
