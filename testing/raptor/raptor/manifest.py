from
__future__
import
absolute_import
import
json
import
os
import
re
from
six
.
moves
.
urllib
.
parse
import
parse_qs
urlsplit
urlunsplit
urlencode
unquote
from
logger
.
logger
import
RaptorLogger
from
manifestparser
import
TestManifest
from
utils
import
bool_from_str
transform_platform
transform_subtest
from
constants
.
raptor_tests_constants
import
YOUTUBE_PLAYBACK_MEASURE
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
raptor_ini
=
os
.
path
.
join
(
here
"
raptor
.
ini
"
)
tests_dir
=
os
.
path
.
join
(
here
"
tests
"
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
manifest
"
)
LIVE_SITE_TIMEOUT_MULTIPLIER
=
1
.
2
required_settings
=
[
    
"
alert_threshold
"
    
"
apps
"
    
"
lower_is_better
"
    
"
measure
"
    
"
page_cycles
"
    
"
test_url
"
    
"
scenario_time
"
    
"
type
"
    
"
unit
"
]
playback_settings
=
[
    
"
playback_pageset_manifest
"
]
def
filter_app
(
tests
values
)
:
    
for
test
in
tests
:
        
if
values
[
"
app
"
]
in
test
[
"
apps
"
]
:
            
yield
test
def
get_browser_test_list
(
browser_app
run_local
)
:
    
LOG
.
info
(
raptor_ini
)
    
test_manifest
=
TestManifest
(
[
raptor_ini
]
strict
=
False
)
    
info
=
{
"
app
"
:
browser_app
"
run_local
"
:
run_local
}
    
return
test_manifest
.
active_tests
(
        
exists
=
False
disabled
=
False
filters
=
[
filter_app
]
*
*
info
    
)
def
validate_test_ini
(
test_details
)
:
    
valid_settings
=
True
    
for
setting
in
required_settings
:
        
if
setting
=
=
"
measure
"
and
test_details
[
"
type
"
]
=
=
"
benchmark
"
:
            
continue
        
if
setting
=
=
"
scenario_time
"
and
test_details
[
"
type
"
]
!
=
"
scenario
"
:
            
continue
        
if
test_details
.
get
(
setting
)
is
None
:
            
if
(
                
setting
=
=
"
page
-
cycles
"
                
and
test_details
.
get
(
"
browser_cycles
"
)
is
not
None
            
)
:
                
continue
            
valid_settings
=
False
            
LOG
.
error
(
                
"
setting
'
%
s
'
is
required
but
not
found
in
%
s
"
                
%
(
setting
test_details
[
"
manifest
"
]
)
            
)
    
test_details
.
setdefault
(
"
page_timeout
"
30000
)
    
if
test_details
.
get
(
"
playback
"
)
is
not
None
:
        
for
setting
in
playback_settings
:
            
if
test_details
.
get
(
setting
)
is
None
:
                
valid_settings
=
False
                
LOG
.
error
(
                    
"
setting
'
%
s
'
is
required
but
not
found
in
%
s
"
                    
%
(
setting
test_details
[
"
manifest
"
]
)
                
)
    
if
test_details
.
get
(
"
alert_on
"
)
is
not
None
:
        
test_details
[
"
alert_on
"
]
=
[
            
_item
.
strip
(
)
for
_item
in
test_details
[
"
alert_on
"
]
.
split
(
"
"
)
        
]
        
valid_alerts
=
[
]
        
if
test_details
.
get
(
            
"
measure
"
        
)
is
None
and
"
youtube
-
playback
"
in
test_details
.
get
(
"
name
"
"
"
)
:
            
test_details
[
"
measure
"
]
=
YOUTUBE_PLAYBACK_MEASURE
        
measure_as_string
=
"
"
.
join
(
test_details
[
"
measure
"
]
)
        
for
alert_on_value
in
test_details
[
"
alert_on
"
]
:
            
alert_on_value_pattern
=
alert_on_value
.
replace
(
"
*
"
"
[
a
-
zA
-
Z0
-
9
.
_
%
]
*
"
)
            
matches
=
re
.
findall
(
alert_on_value_pattern
measure_as_string
)
            
if
len
(
matches
)
=
=
0
:
                
LOG
.
error
(
                    
"
The
'
alert_on
'
value
of
'
%
s
'
is
not
valid
because
"
                    
"
it
doesn
'
t
exist
in
the
'
measure
'
test
setting
!
"
%
alert_on_value
                
)
                
valid_settings
=
False
            
else
:
                
valid_alerts
.
extend
(
matches
)
        
test_details
[
"
alert_on
"
]
=
sorted
(
set
(
valid_alerts
)
)
    
return
valid_settings
def
add_test_url_params
(
url
extra_params
)
:
    
parsed_url
=
urlsplit
(
url
)
    
parsed_query_params
=
parse_qs
(
parsed_url
.
query
)
    
parsed_extra_params
=
parse_qs
(
extra_params
)
    
for
name
value
in
parsed_extra_params
.
items
(
)
:
        
parsed_query_params
[
name
]
=
value
    
final_query_string
=
unquote
(
urlencode
(
parsed_query_params
doseq
=
True
)
)
    
return
urlunsplit
(
        
(
            
parsed_url
.
scheme
            
parsed_url
.
netloc
            
parsed_url
.
path
            
final_query_string
            
parsed_url
.
fragment
        
)
    
)
def
write_test_settings_json
(
args
test_details
oskey
)
:
    
test_url
=
transform_platform
(
test_details
[
"
test_url
"
]
oskey
)
    
test_details
[
"
test_url
"
]
=
test_url
    
test_settings
=
{
        
"
raptor
-
options
"
:
{
            
"
type
"
:
test_details
[
"
type
"
]
            
"
cold
"
:
test_details
[
"
cold
"
]
            
"
test_url
"
:
test_url
            
"
expected_browser_cycles
"
:
test_details
[
"
expected_browser_cycles
"
]
            
"
page_cycles
"
:
int
(
test_details
[
"
page_cycles
"
]
)
            
"
host
"
:
args
.
host
        
}
    
}
    
if
test_details
[
"
type
"
]
=
=
"
pageload
"
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
measure
"
]
=
{
}
        
for
m
in
test_details
[
"
measure
"
]
:
            
test_settings
[
"
raptor
-
options
"
]
[
"
measure
"
]
[
m
]
=
True
            
if
m
=
=
"
hero
"
:
                
test_settings
[
"
raptor
-
options
"
]
[
"
measure
"
]
[
m
]
=
[
                    
h
.
strip
(
)
for
h
in
test_details
[
"
hero
"
]
.
split
(
"
"
)
                
]
        
if
test_details
.
get
(
"
alert_on
"
None
)
is
not
None
:
            
test_settings
[
"
raptor
-
options
"
]
[
"
alert_on
"
]
=
test_details
[
"
alert_on
"
]
    
if
test_details
.
get
(
"
page_timeout
"
None
)
is
not
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
page_timeout
"
]
=
int
(
            
test_details
[
"
page_timeout
"
]
        
)
    
test_settings
[
"
raptor
-
options
"
]
[
"
unit
"
]
=
test_details
.
get
(
"
unit
"
"
ms
"
)
    
test_settings
[
"
raptor
-
options
"
]
[
"
lower_is_better
"
]
=
test_details
.
get
(
        
"
lower_is_better
"
True
    
)
    
val
=
test_details
.
get
(
"
subtest_unit
"
test_settings
[
"
raptor
-
options
"
]
[
"
unit
"
]
)
    
test_settings
[
"
raptor
-
options
"
]
[
"
subtest_unit
"
]
=
val
    
subtest_lower_is_better
=
test_details
.
get
(
"
subtest_lower_is_better
"
)
    
if
subtest_lower_is_better
is
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
subtest_lower_is_better
"
]
=
test_settings
[
            
"
raptor
-
options
"
        
]
[
"
lower_is_better
"
]
    
else
:
        
test_settings
[
"
raptor
-
options
"
]
[
            
"
subtest_lower_is_better
"
        
]
=
subtest_lower_is_better
    
if
test_details
.
get
(
"
alert_change_type
"
None
)
is
not
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
alert_change_type
"
]
=
test_details
[
            
"
alert_change_type
"
        
]
    
if
test_details
.
get
(
"
alert_threshold
"
None
)
is
not
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
alert_threshold
"
]
=
float
(
            
test_details
[
"
alert_threshold
"
]
        
)
    
if
test_details
.
get
(
"
screen_capture
"
None
)
is
not
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
screen_capture
"
]
=
test_details
.
get
(
            
"
screen_capture
"
        
)
    
if
test_details
.
get
(
"
gecko_profile
"
False
)
:
        
threads
=
[
"
GeckoMain
"
"
Compositor
"
]
        
threads
.
extend
(
[
"
Renderer
"
"
WR
"
]
)
        
if
test_details
.
get
(
"
gecko_profile_threads
"
)
:
            
test_threads
=
list
(
                
filter
(
None
test_details
[
"
gecko_profile_threads
"
]
.
split
(
"
"
)
)
            
)
            
threads
.
extend
(
test_threads
)
        
test_settings
[
"
raptor
-
options
"
]
.
update
(
            
{
                
"
gecko_profile
"
:
True
                
"
gecko_profile_entries
"
:
int
(
                    
test_details
.
get
(
"
gecko_profile_entries
"
1000000
)
                
)
                
"
gecko_profile_interval
"
:
int
(
                    
test_details
.
get
(
"
gecko_profile_interval
"
1
)
                
)
                
"
gecko_profile_threads
"
:
"
"
.
join
(
set
(
threads
)
)
            
}
        
)
        
features
=
test_details
.
get
(
"
gecko_profile_features
"
)
        
if
features
:
            
test_settings
[
"
raptor
-
options
"
]
[
"
gecko_profile_features
"
]
=
features
    
if
test_details
.
get
(
"
newtab_per_cycle
"
None
)
is
not
None
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
newtab_per_cycle
"
]
=
bool
(
            
test_details
[
"
newtab_per_cycle
"
]
        
)
    
if
test_details
[
"
type
"
]
=
=
"
scenario
"
:
        
test_settings
[
"
raptor
-
options
"
]
[
"
scenario_time
"
]
=
test_details
[
"
scenario_time
"
]
        
if
"
background_test
"
in
test_details
:
            
test_settings
[
"
raptor
-
options
"
]
[
"
background_test
"
]
=
bool
(
                
test_details
[
"
background_test
"
]
            
)
        
else
:
            
test_settings
[
"
raptor
-
options
"
]
[
"
background_test
"
]
=
False
    
jsons_dir
=
os
.
path
.
join
(
tests_dir
"
json
"
)
    
if
not
os
.
path
.
exists
(
jsons_dir
)
:
        
os
.
mkdir
(
os
.
path
.
join
(
tests_dir
"
json
"
)
)
    
settings_file
=
os
.
path
.
join
(
jsons_dir
test_details
[
"
name
"
]
+
"
.
json
"
)
    
try
:
        
with
open
(
settings_file
"
w
"
)
as
out_file
:
            
json
.
dump
(
test_settings
out_file
indent
=
4
ensure_ascii
=
False
)
            
out_file
.
close
(
)
    
except
IOError
:
        
LOG
.
info
(
"
abort
:
exception
writing
test
settings
json
!
"
)
def
get_raptor_test_list
(
args
oskey
)
:
    
"
"
"
    
A
test
ini
(
i
.
e
.
raptor
-
firefox
-
tp6
.
ini
)
will
have
one
or
more
subtests
inside
    
each
with
it
'
s
own
name
(
[
the
-
ini
-
file
-
test
-
section
]
)
.
    
We
want
the
ability
to
eiter
:
        
-
run
*
all
*
of
the
subtests
listed
inside
the
test
ini
;
-
or
-
        
-
just
run
a
single
one
of
those
subtests
that
are
inside
the
ini
    
A
test
name
is
received
on
the
command
line
.
This
will
either
match
the
name
    
of
a
single
subtest
(
within
an
ini
)
-
or
-
if
there
'
s
no
matching
single
    
subtest
with
that
name
then
the
test
name
provided
might
be
the
name
of
a
    
test
ini
itself
(
i
.
e
.
raptor
-
firefox
-
tp6
)
that
contains
multiple
subtests
.
    
First
look
for
a
single
matching
subtest
name
in
the
list
of
all
availble
tests
    
and
if
it
'
s
found
we
will
just
run
that
single
subtest
.
    
Then
look
at
the
list
of
all
available
tests
-
each
available
test
has
a
manifest
    
name
associated
to
it
-
and
pull
out
all
subtests
whose
manifest
name
matches
    
the
test
name
provided
on
the
command
line
i
.
e
.
run
all
subtests
in
a
specified
ini
.
    
If
no
tests
are
found
at
all
then
the
test
name
is
invalid
.
    
"
"
"
    
tests_to_run
=
[
]
    
available_tests
=
get_browser_test_list
(
args
.
app
args
.
run_local
)
    
for
next_test
in
available_tests
:
        
if
next_test
[
"
name
"
]
=
=
args
.
test
:
            
tests_to_run
.
append
(
next_test
)
            
break
    
if
len
(
tests_to_run
)
=
=
0
:
        
_ini
=
args
.
test
+
"
.
ini
"
        
for
next_test
in
available_tests
:
            
head
tail
=
os
.
path
.
split
(
next_test
[
"
manifest
"
]
)
            
if
tail
=
=
_ini
:
                
tests_to_run
.
append
(
next_test
)
    
if
args
.
collect_perfstats
and
"
chrom
"
not
in
args
.
app
.
lower
(
)
:
        
for
next_test
in
tests_to_run
:
            
next_test
[
"
perfstats
"
]
=
"
true
"
    
if
args
.
live_sites
:
        
for
next_test
in
tests_to_run
:
            
next_test
[
"
use_live_sites
"
]
=
"
true
"
            
next_test
[
"
playback
"
]
=
None
    
for
next_test
in
tests_to_run
:
        
LOG
.
info
(
"
configuring
settings
for
test
%
s
"
%
next_test
[
"
name
"
]
)
        
max_page_cycles
=
int
(
next_test
.
get
(
"
page_cycles
"
1
)
)
        
max_browser_cycles
=
int
(
next_test
.
get
(
"
browser_cycles
"
1
)
)
        
if
next_test
.
get
(
"
playback
"
)
is
not
None
:
            
next_test
[
"
playback_pageset_manifest
"
]
=
transform_subtest
(
                
next_test
[
"
playback_pageset_manifest
"
]
next_test
[
"
name
"
]
            
)
        
if
args
.
gecko_profile
is
True
:
            
next_test
[
"
gecko_profile
"
]
=
True
            
LOG
.
info
(
"
gecko
-
profiling
enabled
"
)
            
max_page_cycles
=
3
            
max_browser_cycles
=
3
            
if
(
                
"
gecko_profile_entries
"
in
args
                
and
args
.
gecko_profile_entries
is
not
None
            
)
:
                
next_test
[
"
gecko_profile_entries
"
]
=
str
(
args
.
gecko_profile_entries
)
                
LOG
.
info
(
                    
"
gecko
-
profiling
entries
set
to
%
s
"
%
args
.
gecko_profile_entries
                
)
            
if
(
                
"
gecko_profile_interval
"
in
args
                
and
args
.
gecko_profile_interval
is
not
None
            
)
:
                
next_test
[
"
gecko_profile_interval
"
]
=
str
(
args
.
gecko_profile_interval
)
                
LOG
.
info
(
                    
"
gecko
-
profiling
interval
set
to
%
s
"
%
args
.
gecko_profile_interval
                
)
            
if
(
                
"
gecko_profile_threads
"
in
args
                
and
args
.
gecko_profile_threads
is
not
None
            
)
:
                
threads
=
list
(
                    
filter
(
None
next_test
.
get
(
"
gecko_profile_threads
"
"
"
)
.
split
(
"
"
)
)
                
)
                
threads
.
extend
(
args
.
gecko_profile_threads
.
split
(
"
"
)
)
                
if
(
                    
"
gecko_profile_extra_threads
"
in
args
                    
and
args
.
gecko_profile_extra_threads
is
not
None
                
)
:
                    
threads
.
extend
(
getattr
(
args
"
gecko_profile_extra_threads
"
[
]
)
)
                
next_test
[
"
gecko_profile_threads
"
]
=
"
"
.
join
(
threads
)
                
LOG
.
info
(
"
gecko
-
profiling
threads
%
s
"
%
args
.
gecko_profile_threads
)
            
if
(
                
"
gecko_profile_features
"
in
args
                
and
args
.
gecko_profile_features
is
not
None
            
)
:
                
next_test
[
"
gecko_profile_features
"
]
=
args
.
gecko_profile_features
                
LOG
.
info
(
"
gecko
-
profiling
features
%
s
"
%
args
.
gecko_profile_features
)
        
else
:
            
next_test
.
pop
(
"
gecko_profile_entries
"
None
)
            
next_test
.
pop
(
"
gecko_profile_interval
"
None
)
            
next_test
.
pop
(
"
gecko_profile_threads
"
None
)
            
next_test
.
pop
(
"
gecko_profile_features
"
None
)
        
if
args
.
debug_mode
is
True
:
            
next_test
[
"
debug_mode
"
]
=
True
            
LOG
.
info
(
"
debug
-
mode
enabled
"
)
            
max_page_cycles
=
2
        
if
args
.
page_cycles
is
not
None
:
            
next_test
[
"
page_cycles
"
]
=
args
.
page_cycles
            
LOG
.
info
(
                
"
setting
page
-
cycles
to
%
d
as
specified
on
cmd
line
"
%
args
.
page_cycles
            
)
        
else
:
            
if
int
(
next_test
.
get
(
"
page_cycles
"
1
)
)
>
max_page_cycles
:
                
next_test
[
"
page_cycles
"
]
=
max_page_cycles
                
LOG
.
info
(
                    
"
setting
page
-
cycles
to
%
d
because
gecko
-
profling
is
enabled
"
                    
%
next_test
[
"
page_cycles
"
]
                
)
        
if
args
.
browser_cycles
is
not
None
:
            
next_test
[
"
browser_cycles
"
]
=
args
.
browser_cycles
            
LOG
.
info
(
                
"
setting
browser
-
cycles
to
%
d
as
specified
on
cmd
line
"
                
%
args
.
browser_cycles
            
)
        
else
:
            
if
int
(
next_test
.
get
(
"
browser_cycles
"
1
)
)
>
max_browser_cycles
:
                
next_test
[
"
browser_cycles
"
]
=
max_browser_cycles
                
LOG
.
info
(
                    
"
setting
browser
-
cycles
to
%
d
because
gecko
-
profilng
is
enabled
"
                    
%
next_test
[
"
browser_cycles
"
]
                
)
        
if
args
.
page_timeout
is
not
None
:
            
LOG
.
info
(
                
"
setting
page
-
timeout
to
%
d
as
specified
on
cmd
line
"
                
%
args
.
page_timeout
            
)
            
next_test
[
"
page_timeout
"
]
=
args
.
page_timeout
        
_running_cold
=
False
        
if
args
.
cold
or
next_test
.
get
(
"
cold
"
)
=
=
"
true
"
:
            
_running_cold
=
True
        
else
:
            
next_test
[
"
browser_cycles
"
]
=
1
        
if
_running_cold
:
            
next_test
[
"
cold
"
]
=
True
            
next_test
[
"
expected_browser_cycles
"
]
=
int
(
next_test
[
"
browser_cycles
"
]
)
            
if
args
.
chimera
:
                
next_test
[
"
page_cycles
"
]
=
2
            
else
:
                
next_test
[
"
page_cycles
"
]
=
1
            
if
"
-
cold
"
not
in
next_test
[
"
name
"
]
and
not
args
.
browsertime
:
                
next_test
[
"
name
"
]
+
=
"
-
cold
"
        
else
:
            
next_test
[
"
cold
"
]
=
False
            
next_test
[
"
expected_browser_cycles
"
]
=
1
        
next_test
[
"
browser_cycle
"
]
=
1
        
if
args
.
test_url_params
is
not
None
:
            
initial_test_url
=
next_test
[
"
test_url
"
]
            
next_test
[
"
test_url
"
]
=
add_test_url_params
(
                
initial_test_url
args
.
test_url_params
            
)
            
LOG
.
info
(
                
"
adding
extra
test_url
params
(
%
s
)
as
specified
on
cmd
line
"
                
"
to
the
current
test_url
(
%
s
)
resulting
:
%
s
"
                
%
(
args
.
test_url_params
initial_test_url
next_test
[
"
test_url
"
]
)
            
)
        
if
next_test
.
get
(
"
use_live_sites
"
"
false
"
)
=
=
"
true
"
:
            
LOG
.
info
(
"
using
live
sites
so
turning
playback
off
!
"
)
            
next_test
[
"
playback
"
]
=
None
            
if
"
raptor
-
youtube
-
playback
"
in
next_test
[
"
name
"
]
:
                
next_test
[
"
name
"
]
=
next_test
[
"
name
"
]
+
"
-
live
"
            
next_test
[
"
page_timeout
"
]
=
(
                
int
(
next_test
[
"
page_timeout
"
]
)
*
LIVE_SITE_TIMEOUT_MULTIPLIER
            
)
            
LOG
.
info
(
                
"
using
live
sites
so
using
page
timeout
of
%
dms
"
                
%
next_test
[
"
page_timeout
"
]
            
)
        
if
not
args
.
browsertime
and
"
browsertime
"
in
next_test
.
get
(
"
manifest
"
"
"
)
:
            
raise
Exception
(
                
"
%
s
test
can
only
be
run
with
-
-
browsertime
"
                
%
next_test
.
get
(
"
name
"
"
Unknown
"
)
            
)
        
if
(
            
args
.
browsertime
            
and
next_test
.
get
(
"
measure
"
)
is
None
            
and
next_test
.
get
(
"
type
"
)
=
=
"
pageload
"
        
)
:
            
next_test
[
"
measure
"
]
=
(
                
"
fnbpaint
fcp
dcf
loadtime
"
                
"
ContentfulSpeedIndex
PerceptualSpeedIndex
"
                
"
SpeedIndex
FirstVisualChange
LastVisualChange
"
            
)
        
if
next_test
.
get
(
"
measure
"
)
is
not
None
:
            
_measures
=
[
]
            
for
measure
in
[
m
.
strip
(
)
for
m
in
next_test
[
"
measure
"
]
.
split
(
"
"
)
]
:
                
_measures
.
append
(
measure
)
            
next_test
[
"
measure
"
]
=
_measures
            
if
(
                
"
hero
"
in
next_test
[
"
measure
"
]
                
and
next_test
.
get
(
"
use_live_sites
"
"
false
"
)
=
=
"
true
"
            
)
:
                
next_test
[
"
measure
"
]
.
remove
(
"
hero
"
)
                
del
next_test
[
"
hero
"
]
        
bool_settings
=
[
            
"
lower_is_better
"
            
"
subtest_lower_is_better
"
            
"
accept_zero_vismet
"
            
"
interactive
"
        
]
        
for
setting
in
bool_settings
:
            
if
next_test
.
get
(
setting
None
)
is
not
None
:
                
next_test
[
setting
]
=
bool_from_str
(
next_test
.
get
(
setting
)
)
    
if
len
(
tests_to_run
)
!
=
0
:
        
for
test
in
tests_to_run
:
            
if
validate_test_ini
(
test
)
:
                
write_test_settings_json
(
args
test
oskey
)
            
else
:
                
LOG
.
info
(
"
test
%
s
is
not
valid
due
to
missing
settings
"
%
test
[
"
name
"
]
)
                
tests_to_run
.
remove
(
test
)
    
return
tests_to_run
