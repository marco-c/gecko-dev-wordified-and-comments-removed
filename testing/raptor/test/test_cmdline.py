import
os
import
sys
from
unittest
import
mock
import
mozunit
import
pytest
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
raptor_dir
=
os
.
path
.
join
(
os
.
path
.
dirname
(
here
)
"
raptor
"
)
sys
.
path
.
insert
(
0
raptor_dir
)
from
argparse
import
ArgumentParser
Namespace
from
cmdline
import
create_parser
verify_options
def
test_verify_options
(
filedir
)
:
    
args
=
Namespace
(
        
app
=
"
firefox
"
        
binary
=
"
invalid
/
path
"
        
gecko_profile
=
"
False
"
        
page_cycles
=
1
        
page_timeout
=
60000
        
debug
=
"
True
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
parser
=
ArgumentParser
(
)
    
with
pytest
.
raises
(
SystemExit
)
:
        
verify_options
(
parser
args
)
    
args
.
binary
=
os
.
path
.
join
(
filedir
"
fake_binary
.
exe
"
)
    
verify_options
(
parser
args
)
    
args
=
Namespace
(
        
app
=
"
geckoview
"
        
binary
=
"
org
.
mozilla
.
geckoview_example
"
        
activity
=
"
org
.
mozilla
.
geckoview_example
.
GeckoViewActivity
"
        
intent
=
"
android
.
intent
.
action
.
MAIN
"
        
gecko_profile
=
"
False
"
        
is_release_build
=
False
        
host
=
"
sophie
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
verify_options
(
parser
args
)
    
args
=
Namespace
(
        
app
=
"
refbrow
"
        
binary
=
"
org
.
mozilla
.
reference
.
browser
"
        
activity
=
"
org
.
mozilla
.
reference
.
browser
.
BrowserTestActivity
"
        
intent
=
"
android
.
intent
.
action
.
MAIN
"
        
gecko_profile
=
"
False
"
        
is_release_build
=
False
        
host
=
"
sophie
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
verify_options
(
parser
args
)
    
args
=
Namespace
(
        
app
=
"
fenix
"
        
binary
=
"
org
.
mozilla
.
fenix
.
browser
"
        
activity
=
"
org
.
mozilla
.
fenix
.
browser
.
BrowserPerformanceTestActivity
"
        
intent
=
"
android
.
intent
.
action
.
VIEW
"
        
gecko_profile
=
"
False
"
        
is_release_build
=
False
        
host
=
"
sophie
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
verify_options
(
parser
args
)
    
args
=
Namespace
(
        
app
=
"
geckoview
"
        
binary
=
"
org
.
mozilla
.
geckoview_example
"
        
activity
=
"
org
.
mozilla
.
geckoview_example
.
GeckoViewActivity
"
        
intent
=
"
android
.
intent
.
action
.
MAIN
"
        
gecko_profile
=
"
False
"
        
is_release_build
=
False
        
host
=
"
sophie
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
verify_options
(
parser
args
)
    
args
=
Namespace
(
        
app
=
"
refbrow
"
        
binary
=
"
org
.
mozilla
.
reference
.
browser
"
        
activity
=
None
        
intent
=
"
android
.
intent
.
action
.
MAIN
"
        
gecko_profile
=
"
False
"
        
is_release_build
=
False
        
host
=
"
sophie
"
        
chimera
=
False
        
browsertime_video
=
False
        
browsertime_visualmetrics
=
False
        
fission
=
True
        
fission_mobile
=
False
        
test_bytecode_cache
=
False
        
webext
=
False
        
extra_prefs
=
[
]
        
benchmark_repository
=
None
        
benchmark_revision
=
None
        
benchmark_branch
=
None
        
post_startup_delay
=
None
        
power_test
=
False
    
)
    
parser
=
ArgumentParser
(
)
    
verify_options
(
parser
args
)
mock
.
patch
(
"
perftest
.
Perftest
.
build_browser_profile
"
new
=
mock
.
MagicMock
(
)
)
pytest
.
mark
.
parametrize
(
    
"
args
settings_to_check
"
    
[
        
[
            
[
                
"
-
-
test
"
                
"
test
-
page
-
1
"
                
"
-
-
binary
"
                
"
invalid
/
path
"
                
"
-
-
run
-
local
"
            
]
            
[
                
(
"
post_startup_delay
"
30000
)
                
(
"
run_local
"
True
)
                
(
"
debug_mode
"
False
)
            
]
        
]
        
[
            
[
                
"
-
-
test
"
                
"
test
-
page
-
1
"
                
"
-
-
binary
"
                
"
invalid
/
path
"
            
]
            
[
                
(
"
post_startup_delay
"
30000
)
                
(
"
run_local
"
False
)
                
(
"
debug_mode
"
False
)
            
]
        
]
        
[
            
[
                
"
-
-
test
"
                
"
test
-
page
-
1
"
                
"
-
-
binary
"
                
"
invalid
/
path
"
                
"
-
-
debug
-
mode
"
                
"
-
-
run
-
local
"
            
]
            
[
                
(
"
post_startup_delay
"
3000
)
                
(
"
run_local
"
True
)
                
(
"
debug_mode
"
True
)
            
]
        
]
        
[
            
[
                
"
-
-
test
"
                
"
test
-
page
-
1
"
                
"
-
-
binary
"
                
"
invalid
/
path
"
                
"
-
-
debug
-
mode
"
            
]
            
[
                
(
"
post_startup_delay
"
30000
)
                
(
"
run_local
"
False
)
                
(
"
debug_mode
"
False
)
            
]
        
]
    
]
)
def
test_perftest_setup_with_args
(
ConcretePerftest
args
settings_to_check
)
:
    
parser
=
create_parser
(
)
    
args
=
parser
.
parse_args
(
args
)
    
perftest
=
ConcretePerftest
(
*
*
vars
(
args
)
)
    
for
setting
expected
in
settings_to_check
:
        
assert
getattr
(
perftest
setting
)
=
=
expected
pytest
.
mark
.
parametrize
(
    
"
args
expected_failure
"
    
[
        
[
            
{
                
"
app
"
:
"
firefox
"
                
"
binary
"
:
"
org
.
mozilla
.
reference
.
browser
"
                
"
activity
"
:
None
                
"
intent
"
:
"
android
.
intent
.
action
.
MAIN
"
                
"
gecko_profile
"
:
"
False
"
                
"
is_release_build
"
:
False
                
"
host
"
:
"
sophie
"
                
"
chimera
"
:
False
                
"
browsertime_video
"
:
False
                
"
browsertime_visualmetrics
"
:
False
                
"
fission
"
:
True
                
"
fission_mobile
"
:
False
                
"
test_bytecode_cache
"
:
False
                
"
webext
"
:
False
                
"
extra_prefs
"
:
[
]
                
"
benchmark_repository
"
:
None
                
"
benchmark_revision
"
:
None
                
"
benchmark_branch
"
:
None
                
"
post_startup_delay
"
:
None
                
"
power_test
"
:
True
            
}
            
SystemExit
        
]
    
]
)
def
test_verify_options_failure
(
ConcretePerftest
args
expected_failure
)
:
    
args
=
Namespace
(
*
*
args
)
    
parser
=
ArgumentParser
(
)
    
with
pytest
.
raises
(
expected_failure
)
:
        
verify_options
(
parser
args
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
