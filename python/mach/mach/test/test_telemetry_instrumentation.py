import
shutil
import
sys
import
tempfile
import
time
import
unittest
from
pathlib
import
Path
from
unittest
.
mock
import
Mock
from
mach_initialize
import
_finalize_telemetry_glean
from
mach
.
telemetry
import
MACH_METRICS_PATH
report_invocation_metrics
from
mach
.
telemetry_interface
import
GleanTelemetry
TOPSRCDIR
=
Path
(
__file__
)
.
parent
.
parent
.
parent
.
parent
.
parent
BUILD_DIR
=
TOPSRCDIR
/
"
build
"
sys
.
path
.
insert
(
0
str
(
BUILD_DIR
)
)
class
TestMachTelemetryInstrumentation
(
unittest
.
TestCase
)
:
    
"
"
"
Test
suite
for
mach
telemetry
instrumentation
using
Glean
SDK
.
"
"
"
    
def
setUp
(
self
)
:
        
"
"
"
Set
up
test
environment
with
temporary
directories
.
"
"
"
        
self
.
temp_dir
=
tempfile
.
mkdtemp
(
)
        
self
.
data_dir
=
Path
(
self
.
temp_dir
)
/
"
glean
"
        
self
.
data_dir
.
mkdir
(
exist_ok
=
True
)
        
self
.
addCleanup
(
self
.
_cleanup_environment
)
    
def
_cleanup_environment
(
self
)
:
        
"
"
"
Clean
up
temporary
directories
.
"
"
"
        
shutil
.
rmtree
(
self
.
temp_dir
ignore_errors
=
True
)
    
def
test_mach_telemetry_instrumentation
(
self
)
:
        
"
"
"
Test
that
mach
telemetry
properly
records
data
using
the
actual
instrumentation
.
"
"
"
        
try
:
            
from
glean
.
config
import
Configuration
        
except
ImportError
:
            
self
.
skipTest
(
"
Glean
SDK
not
available
for
testing
"
)
        
config
=
Configuration
(
server_endpoint
=
"
http
:
/
/
invalid
.
local
"
)
        
telemetry
=
GleanTelemetry
(
            
upload_enabled
=
True
data_dir
=
self
.
data_dir
configuration
=
config
        
)
        
command_name
=
"
test
-
command
"
        
report_invocation_metrics
(
telemetry
command_name
)
        
time
.
sleep
(
0
.
001
)
        
metrics
=
telemetry
.
metrics
(
MACH_METRICS_PATH
)
        
command_value
=
metrics
.
mach
.
command
.
test_get_value
(
)
        
self
.
assertIsNotNone
(
            
command_value
            
"
Command
should
be
recorded
by
report_invocation_metrics
"
        
)
        
self
.
assertEqual
(
command_name
command_value
)
        
mock_settings
=
Mock
(
)
        
mock_settings
.
mach_telemetry
.
is_employee
=
False
        
original_submit
=
telemetry
.
submit
        
telemetry
.
submit
=
Mock
(
)
        
_finalize_telemetry_glean
(
            
telemetry
=
telemetry
            
is_bootstrap
=
False
            
success
=
True
            
topsrcdir
=
TOPSRCDIR
            
state_dir
=
self
.
data_dir
.
parent
            
settings
=
mock_settings
        
)
        
final_duration
=
metrics
.
mach
.
duration
.
test_get_value
(
)
        
self
.
assertIsNotNone
(
            
final_duration
            
"
Duration
should
be
set
after
_finalize_telemetry_glean
stops
the
timer
"
        
)
        
self
.
assertGreater
(
            
final_duration
            
0
            
"
Duration
should
be
>
0
after
timer
was
stopped
by
_finalize_telemetry_glean
"
        
)
        
success_value
=
metrics
.
mach
.
success
.
test_get_value
(
)
        
self
.
assertTrue
(
            
success_value
"
Success
should
be
set
by
_finalize_telemetry_glean
"
        
)
        
moz_automation_value
=
metrics
.
mach
.
moz_automation
.
test_get_value
(
)
        
self
.
assertIsNotNone
(
moz_automation_value
"
moz_automation
should
be
set
"
)
        
system_metrics
=
metrics
.
mach
.
system
        
distro_value
=
system_metrics
.
distro
.
test_get_value
(
)
        
self
.
assertIsNotNone
(
distro_value
"
System
distro
should
be
detected
"
)
        
distro_version_value
=
system_metrics
.
distro_version
.
test_get_value
(
)
        
self
.
assertIsNotNone
(
            
distro_version_value
"
System
distro
version
should
be
detected
"
        
)
        
telemetry
.
submit
.
assert_called_once_with
(
False
)
        
telemetry
.
submit
=
original_submit
        
ping_submitted
=
False
        
metrics_available_during_submit
=
False
        
def
verify_ping_submission
(
reason
)
:
            
nonlocal
ping_submitted
metrics_available_during_submit
            
cmd_value
=
metrics
.
mach
.
command
.
test_get_value
(
)
            
dur_value
=
metrics
.
mach
.
duration
.
test_get_value
(
)
            
success_value
=
metrics
.
mach
.
success
.
test_get_value
(
)
            
moz_auto_value
=
metrics
.
mach
.
moz_automation
.
test_get_value
(
)
            
ping_submitted
=
True
            
metrics_available_during_submit
=
(
                
cmd_value
is
not
None
                
and
dur_value
is
not
None
                
and
success_value
is
not
None
                
and
moz_auto_value
is
not
None
            
)
        
telemetry
.
_pings
.
usage
.
test_before_next_submit
(
verify_ping_submission
)
        
telemetry
.
submit
(
True
)
        
self
.
assertTrue
(
            
ping_submitted
            
"
Ping
submission
should
have
been
detected
by
test_before_next_submit
"
        
)
        
self
.
assertTrue
(
            
metrics_available_during_submit
            
"
All
metrics
should
be
accessible
during
ping
submission
"
        
)
if
__name__
=
=
"
__main__
"
:
    
unittest
.
main
(
)
