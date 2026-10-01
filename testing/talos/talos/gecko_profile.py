"
"
"
module
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
mozgeckoprofiler
import
symbolicate_profile_json
from
mozlog
import
get_proxy_logger
LOG
=
get_proxy_logger
(
)
class
GeckoProfile
:
    
"
"
"
    
Handle
Gecko
profiling
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
test_config
=
test_config
        
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
"
gecko_profile_interval
"
1
)
        
gecko_profile_entries
=
test_config
.
get
(
            
"
gecko_profile_entries
"
int
(
128
*
1024
*
1024
/
8
)
        
)
        
gecko_profile_features
=
test_config
.
get
(
            
"
gecko_profile_features
"
"
js
stackwalk
screenshots
memory
"
        
)
        
gecko_profile_threads
=
test_config
.
get
(
            
"
gecko_profile_threads
"
"
GeckoMain
Compositor
Renderer
"
        
)
        
gecko_profile_extra_threads
=
test_config
.
get
(
            
"
gecko_profile_extra_threads
"
None
        
)
        
if
gecko_profile_extra_threads
:
            
gecko_profile_threads
+
=
"
"
+
gecko_profile_extra_threads
        
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
test_config
.
get
(
"
suite
"
test_config
[
"
name
"
]
)
)
        
)
        
if
test_config
.
get
(
"
is_first_test
"
False
)
:
            
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
Gecko
Profiling
.
Temp
.
profile
dir
:
"
            
f
"
{
gecko_profile_dir
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
        
self
.
profiling_info
=
{
            
"
gecko_profile_interval
"
:
gecko_profile_interval
            
"
gecko_profile_entries
"
:
gecko_profile_entries
            
"
gecko_profile_dir
"
:
gecko_profile_dir
            
"
gecko_profile_features
"
:
gecko_profile_features
            
"
gecko_profile_threads
"
:
gecko_profile_threads
        
}
    
def
option
(
self
name
)
:
        
return
self
.
profiling_info
[
"
gecko_profile_
"
+
name
]
    
def
update_env
(
self
env
)
:
        
"
"
"
        
update
the
given
env
to
update
some
env
vars
if
required
.
        
"
"
"
        
if
not
self
.
test_config
.
get
(
"
gecko_profile_startup
"
)
:
            
return
        
env
.
update
(
{
            
"
MOZ_PROFILER_STARTUP
"
:
"
1
"
            
"
MOZ_PROFILER_STARTUP_NO_BASE
"
:
"
1
"
            
"
MOZ_PROFILER_STARTUP_INTERVAL
"
:
str
(
self
.
option
(
"
interval
"
)
)
            
"
MOZ_PROFILER_STARTUP_ENTRIES
"
:
str
(
self
.
option
(
"
entries
"
)
)
            
"
MOZ_PROFILER_STARTUP_FEATURES
"
:
str
(
self
.
option
(
"
features
"
)
)
            
"
MOZ_PROFILER_STARTUP_FILTERS
"
:
str
(
self
.
option
(
"
threads
"
)
)
        
}
)
    
def
_save_gecko_profile
(
self
cycle
profile_path
)
:
        
try
:
            
symbolicate_profile_json
(
profile_path
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
                
f
"
symbolication
{
profile_path
}
(
cycle
{
cycle
}
)
"
                
exc_info
=
True
            
)
    
def
symbolicate
(
self
cycle
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
cycle
.
        
:
param
cycle
:
the
number
of
the
cycle
of
the
test
currently
run
.
        
"
"
"
        
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
        
gecko_profile_dir
=
self
.
option
(
"
dir
"
)
        
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
profile_filename
in
os
.
listdir
(
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
gecko_profile_dir
profile_filename
)
                
self
.
_save_gecko_profile
(
cycle
profile_path
)
                
cycle_name
=
f
"
cycle_
{
cycle
}
.
profile
"
                
path_in_zip
=
os
.
path
.
join
(
                    
"
profile_
{
}
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
testname
cycle_name
                
)
                
LOG
.
info
(
                    
f
"
Adding
profile
{
path_in_zip
}
to
archive
{
self
.
profile_arcname
}
"
                
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
                        
f
"
Failed
to
copy
profile
{
profile_path
}
as
{
path_in_zip
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
            
os
.
environ
[
"
TALOS_LATEST_GECKO_PROFILE_ARCHIVE
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
option
(
"
dir
"
)
)
