import
json
import
pathlib
import
sys
from
collections
.
abc
import
Iterable
import
filters
sys
.
path
.
insert
(
0
str
(
pathlib
.
Path
(
__file__
)
.
parent
)
)
from
browsertime_pageload
import
PageloadSupport
from
logger
.
logger
import
RaptorLogger
LOG
=
RaptorLogger
(
component
=
"
perftest
-
support
-
class
"
)
METRIC_BLOCKLIST
=
[
    
"
mean
"
    
"
median
"
    
"
geomean
"
]
class
MissingBenchmarkResultsError
(
Exception
)
:
    
"
"
"
    
This
error
is
raised
when
the
benchmark
results
from
a
test
    
run
do
not
contain
the
browsertime_benchmark
entry
in
the
dict
    
of
extra
data
.
    
"
"
"
    
pass
class
BenchmarkSupport
(
PageloadSupport
)
:
    
def
__init__
(
self
*
*
kwargs
)
:
        
super
(
)
.
__init__
(
*
*
kwargs
)
        
self
.
failed_tests
=
[
]
        
self
.
youtube_playback_failure
=
False
    
def
setup_test
(
self
next_test
args
)
:
        
super
(
)
.
setup_test
(
next_test
args
)
        
if
next_test
.
get
(
"
custom_data
"
False
)
=
=
"
true
"
:
            
raise
ValueError
(
                
"
Cannot
use
BenchmarkSupport
class
for
custom
data
a
"
                
"
new
support
class
should
be
built
for
that
use
case
.
"
            
)
    
def
modify_command
(
self
cmd
test
)
:
        
cmd
.
extend
(
[
            
"
-
-
browsertime
.
cpuTime_test
"
            
"
true
"
            
"
-
-
browsertime
.
wallclock_tracking_test
"
            
"
true
"
        
]
)
    
def
handle_result
(
self
bt_result
raw_result
*
*
kwargs
)
:
        
"
"
"
Parse
a
result
for
the
required
results
.
        
See
base_python_support
.
py
for
what
'
s
expected
from
this
method
.
        
"
"
"
        
for
custom_types
in
raw_result
[
"
extras
"
]
:
            
browsertime_benchmark_results
=
custom_types
.
get
(
"
browsertime_benchmark
"
)
            
if
not
browsertime_benchmark_results
:
                
raise
MissingBenchmarkResultsError
(
                    
"
Could
not
find
browsertime_benchmark
entry
"
                    
"
in
the
browsertime
extra
results
"
                
)
            
for
metric
values
in
browsertime_benchmark_results
.
items
(
)
:
                
bt_result
[
"
measurements
"
]
.
setdefault
(
metric
[
]
)
.
append
(
values
)
        
if
self
.
perfstats
:
            
for
cycle
in
raw_result
[
"
geckoPerfStats
"
]
:
                
for
metric
in
cycle
:
                    
bt_result
[
"
measurements
"
]
.
setdefault
(
                        
"
perfstat
-
"
+
metric
[
]
                    
)
.
append
(
cycle
[
metric
]
)
    
def
parseYoutubePlaybackPerformanceOutput
(
self
test
)
:
        
"
"
"
Parse
the
metrics
for
the
Youtube
playback
performance
test
.
        
For
each
video
measured
values
for
dropped
and
decoded
frames
will
be
        
available
from
the
benchmark
site
.
        
{
u
'
PlaybackPerf
.
VP9
.
2160p60
2X
'
:
{
u
'
droppedFrames
'
:
1
u
'
decodedFrames
'
:
796
}
        
With
each
page
cycle
/
iteration
of
the
test
multiple
values
can
be
present
.
        
Raptor
will
calculate
the
percentage
of
dropped
frames
to
decoded
frames
.
        
All
those
three
values
will
then
be
emitted
as
separate
sub
tests
.
        
"
"
"
        
_subtests
=
{
}
        
test_name
=
[
            
measurement
            
for
measurement
in
test
[
"
measurements
"
]
.
keys
(
)
            
if
"
youtube
-
playback
"
in
measurement
        
]
        
if
len
(
test_name
)
>
0
:
            
data
=
test
[
"
measurements
"
]
.
get
(
test_name
[
0
]
)
        
else
:
            
raise
Exception
(
"
No
measurements
found
for
youtube
test
!
"
)
        
def
create_subtest_entry
(
            
name
            
value
            
unit
=
test
[
"
subtest_unit
"
]
            
lower_is_better
=
test
[
"
subtest_lower_is_better
"
]
        
)
:
            
if
name
not
in
_subtests
:
                
_subtests
[
name
]
=
{
                    
"
name
"
:
name
                    
"
unit
"
:
unit
                    
"
lowerIsBetter
"
:
lower_is_better
                    
"
replicates
"
:
[
]
                
}
            
_subtests
[
name
]
[
"
replicates
"
]
.
append
(
value
)
            
if
self
.
subtest_alert_on
is
not
None
:
                
if
name
in
self
.
subtest_alert_on
:
                    
LOG
.
info
(
                        
"
turning
on
subtest
alerting
for
measurement
type
:
%
s
"
%
name
                    
)
                    
_subtests
[
name
]
[
"
shouldAlert
"
]
=
True
        
for
pagecycle
in
data
:
            
for
_sub
_value
in
pagecycle
[
0
]
.
items
(
)
:
                
if
_value
[
"
decodedFrames
"
]
=
=
0
:
                    
self
.
failed_tests
.
append
(
                        
"
%
s
test
Failed
.
decodedFrames
%
s
droppedFrames
%
s
.
"
                        
%
(
_sub
_value
[
"
decodedFrames
"
]
_value
[
"
droppedFrames
"
]
)
                    
)
                
try
:
                    
percent_dropped
=
(
                        
float
(
_value
[
"
droppedFrames
"
]
)
/
_value
[
"
decodedFrames
"
]
*
100
.
0
                    
)
                
except
ZeroDivisionError
:
                    
percent_dropped
=
100
.
0
                
_sub
=
_sub
.
split
(
"
PlaybackPerf
"
1
)
[
-
1
]
                
if
_sub
.
startswith
(
"
.
"
)
:
                    
_sub
=
_sub
[
1
:
]
                
create_subtest_entry
(
                    
f
"
{
_sub
}
_decoded_frames
"
                    
_value
[
"
decodedFrames
"
]
                    
lower_is_better
=
False
                
)
                
create_subtest_entry
(
f
"
{
_sub
}
_dropped_frames
"
_value
[
"
droppedFrames
"
]
)
                
create_subtest_entry
(
f
"
{
_sub
}
_
%
_dropped_frames
"
percent_dropped
)
        
if
len
(
self
.
failed_tests
)
>
0
:
            
self
.
youtube_playback_failure
=
True
        
vals
=
[
]
        
subtests
=
[
]
        
names
=
list
(
_subtests
)
        
names
.
sort
(
reverse
=
True
)
        
for
name
in
names
:
            
_subtests
[
name
]
[
"
value
"
]
=
round
(
                
float
(
filters
.
median
(
_subtests
[
name
]
[
"
replicates
"
]
)
)
2
            
)
            
subtests
.
append
(
_subtests
[
name
]
)
            
if
name
.
endswith
(
"
X_dropped_frames
"
)
:
                
vals
.
append
(
[
_subtests
[
name
]
[
"
value
"
]
name
]
)
        
return
subtests
vals
    
def
parseWebCodecsOutput
(
self
test
)
:
        
"
"
"
        
Example
output
(
this
is
one
page
cycle
)
:
        
{
            
'
name
'
:
'
webcodecs
'
            
'
type
'
:
'
benchmark
'
            
'
measurements
'
:
{
            
'
webcodecs
'
:
[
                
[
'
{
                    
"
vp8
realtime
encode
"
:
{
                        
"
frame
-
to
-
frame
mean
(
key
)
"
:
{
"
value
"
:
5
.
222857
"
unit
"
:
"
ms
"
}
                        
"
frame
-
to
-
frame
cv
(
key
)
"
:
{
"
value
"
:
27
.
052957
"
unit
"
:
"
%
"
}
                        
"
frame
-
dropping
rate
(
key
)
"
:
{
"
value
"
:
0
"
unit
"
:
"
%
"
}
                        
"
frame
-
to
-
frame
mean
(
non
key
)
"
:
{
"
value
"
:
1
.
460678
"
unit
"
:
"
ms
"
}
                        
"
frame
-
to
-
frame
cv
(
non
key
)
"
:
{
"
value
"
:
65
.
4360136
"
unit
"
:
"
%
"
}
                        
"
frame
-
dropping
rate
(
non
key
)
"
:
{
"
value
"
:
0
"
unit
"
:
"
%
"
}
                    
}
                
}
'
]
                
.
.
.
            
]
            
}
            
'
lower_is_better
'
:
False
            
'
unit
'
:
'
score
'
        
}
        
"
"
"
        
data
=
test
[
"
measurements
"
]
[
"
webcodecs
"
]
        
results
=
{
}
        
for
page_cycle
in
data
:
            
d
=
json
.
loads
(
page_cycle
[
0
]
)
            
for
test_name
test_data
in
d
.
items
(
)
:
                
results
.
setdefault
(
test_name
[
]
)
.
append
(
test_data
)
        
_subtests
=
{
}
        
for
test_name
in
results
:
            
for
result
in
results
[
test_name
]
:
                
for
subtest_name
subtest_result
in
result
.
items
(
)
:
                    
subtest_result_name
=
f
"
{
test_name
}
-
{
subtest_name
}
"
                    
_subtests
.
setdefault
(
                        
subtest_result_name
                        
{
                            
"
unit
"
:
subtest_result
[
"
unit
"
]
                            
"
alertThreshold
"
:
float
(
test
[
"
alert_threshold
"
]
)
                            
"
lowerIsBetter
"
:
test
[
"
subtest_lower_is_better
"
]
                            
"
name
"
:
subtest_result_name
                            
"
replicates
"
:
[
]
                            
"
shouldAlert
"
:
True
                        
}
                    
)
[
"
replicates
"
]
.
append
(
subtest_result
[
"
value
"
]
)
            
for
subtest_name
in
results
[
test_name
]
:
                
for
subtest_name
in
result
:
                    
subtest_result_name
=
f
"
{
test_name
}
-
{
subtest_name
}
"
                    
_subtests
[
subtest_result_name
]
[
"
value
"
]
=
filters
.
median
(
                        
_subtests
[
subtest_result_name
]
[
"
replicates
"
]
                    
)
        
subtests
=
sorted
(
_subtests
.
values
(
)
key
=
lambda
x
:
x
[
"
name
"
]
reverse
=
True
)
        
for
subtest
in
subtests
:
            
if
isinstance
(
subtest
[
"
value
"
]
float
)
:
                
subtest
[
"
value
"
]
=
round
(
subtest
[
"
value
"
]
3
)
        
vals
=
[
[
subtest
[
"
value
"
]
subtest
[
"
name
"
]
]
for
subtest
in
subtests
]
        
return
subtests
vals
    
def
parseUnknown
(
self
test
)
:
        
_subtests
=
{
}
        
if
not
isinstance
(
test
[
"
measurements
"
]
dict
)
:
            
raise
Exception
(
                
"
Expected
a
dictionary
with
a
single
entry
as
the
name
of
the
test
.
"
                
"
The
value
of
this
key
should
be
the
data
.
"
            
)
        
for
iteration
in
test
[
"
measurements
"
]
[
list
(
test
[
"
measurements
"
]
.
keys
(
)
)
[
0
]
]
:
            
flattened_metrics
=
None
            
for
metric
value
in
(
flattened_metrics
or
iteration
)
.
items
(
)
:
                
if
metric
in
METRIC_BLOCKLIST
:
                    
continue
                
if
metric
not
in
_subtests
:
                    
_subtests
[
metric
]
=
{
                        
"
unit
"
:
test
[
"
subtest_unit
"
]
                        
"
alertThreshold
"
:
float
(
test
[
"
alert_threshold
"
]
)
                        
"
lowerIsBetter
"
:
test
[
"
subtest_lower_is_better
"
]
                        
"
name
"
:
metric
                        
"
replicates
"
:
[
]
                    
}
                
updated_metric
=
value
                
if
not
isinstance
(
value
Iterable
)
:
                    
updated_metric
=
[
value
]
                
_subtests
[
metric
]
[
"
replicates
"
]
.
extend
(
[
                    
round
(
x
3
)
for
x
in
updated_metric
                
]
)
        
vals
=
[
]
        
subtests
=
[
]
        
names
=
list
(
_subtests
)
        
names
.
sort
(
reverse
=
True
)
        
summaries
=
{
            
"
median
"
:
filters
.
median
            
"
mean
"
:
filters
.
mean
            
"
geomean
"
:
filters
.
geometric_mean
        
}
        
for
name
in
names
:
            
summary_method
=
test
.
get
(
"
submetric_summary_method
"
"
median
"
)
            
_subtests
[
name
]
[
"
value
"
]
=
round
(
                
summaries
[
summary_method
]
(
_subtests
[
name
]
[
"
replicates
"
]
)
3
            
)
            
subtests
.
append
(
_subtests
[
name
]
)
            
vals
.
append
(
[
_subtests
[
name
]
[
"
value
"
]
name
]
)
        
return
subtests
vals
    
def
construct_summary
(
self
vals
testname
unit
=
None
)
:
        
def
_filter
(
vals
value
=
None
)
:
            
if
value
is
None
:
                
return
[
i
for
i
j
in
vals
]
            
return
[
i
for
i
j
in
vals
if
j
=
=
value
]
        
if
testname
.
startswith
(
"
raptor
-
v8_7
"
)
:
            
return
100
*
filters
.
geometric_mean
(
_filter
(
vals
)
)
        
if
testname
=
=
"
speedometer3
"
:
            
score
=
None
            
for
val
name
in
vals
:
                
if
name
=
=
"
score
"
:
                    
score
=
val
            
if
score
is
None
:
                
raise
Exception
(
"
Unable
to
find
score
for
Speedometer
3
"
)
            
return
score
        
if
"
speedometer
"
in
testname
:
            
correctionFactor
=
3
            
results
=
_filter
(
vals
)
            
if
len
(
results
)
!
=
160
:
                
raise
Exception
(
                    
"
Speedometer
has
160
subtests
found
:
%
s
instead
"
%
len
(
results
)
                
)
            
results
=
results
[
9
:
:
10
]
            
score
=
60
*
1000
/
filters
.
geometric_mean
(
results
)
/
correctionFactor
            
return
score
        
if
"
stylebench
"
in
testname
:
            
correctionFactor
=
3
            
results
=
_filter
(
vals
)
            
EXPECTED_ENTRIES
=
380
+
166
            
if
len
(
results
)
!
=
EXPECTED_ENTRIES
:
                
raise
Exception
(
                    
f
"
StyleBench
requires
{
EXPECTED_ENTRIES
}
entries
found
:
{
len
(
results
)
}
instead
"
                
)
            
results
=
results
[
:
380
]
[
75
:
:
76
]
+
[
results
[
-
1
]
]
            
return
60
*
1000
/
filters
.
geometric_mean
(
results
)
/
correctionFactor
        
if
testname
.
startswith
(
"
raptor
-
kraken
"
)
or
"
sunspider
"
in
testname
:
            
return
sum
(
_filter
(
vals
)
)
        
if
"
unity
-
webgl
"
in
testname
or
"
webaudio
"
in
testname
:
            
return
filters
.
mean
(
_filter
(
vals
"
Geometric
Mean
"
)
)
        
if
"
assorted
-
dom
"
in
testname
:
            
return
round
(
filters
.
geometric_mean
(
_filter
(
vals
)
)
2
)
        
if
"
wasm
-
misc
"
in
testname
:
            
return
filters
.
mean
(
_filter
(
vals
"
__total__
"
)
)
        
if
"
wasm
-
godot
"
in
testname
:
            
return
filters
.
mean
(
_filter
(
vals
"
first
-
interactive
"
)
)
        
if
"
youtube
-
playback
"
in
testname
:
            
return
round
(
filters
.
mean
(
_filter
(
vals
)
)
2
)
        
if
"
twitch
-
animation
"
in
testname
:
            
return
round
(
filters
.
geometric_mean
(
_filter
(
vals
"
run
"
)
)
2
)
        
if
"
ve
"
in
testname
:
            
if
"
rt
"
in
testname
:
                
means
=
[
i
for
i
j
in
vals
if
"
mean
"
in
j
]
                
if
len
(
means
)
>
0
:
                    
return
round
(
filters
.
geometric_mean
(
means
)
2
)
                
return
-
1
            
if
"
q
"
in
testname
:
                
if
len
(
vals
)
>
0
:
                    
return
round
(
filters
.
mean
(
_filter
(
vals
)
)
2
)
                
return
-
1
            
raise
NotImplementedError
(
"
Summary
for
%
s
is
not
implemented
"
%
testname
)
        
if
testname
.
startswith
(
"
supporting_data
"
)
:
            
if
not
unit
:
                
return
sum
(
_filter
(
vals
)
)
            
if
unit
=
=
"
%
"
:
                
return
filters
.
mean
(
_filter
(
vals
)
)
            
if
unit
in
(
"
W
"
"
MHz
"
)
:
                
allavgs
=
[
]
                
for
val
subtest
in
vals
:
                    
if
"
avg
"
in
subtest
:
                        
allavgs
.
append
(
val
)
                
if
allavgs
:
                    
return
sum
(
allavgs
)
                
raise
Exception
(
                    
"
No
average
measurements
found
for
supporting
data
with
W
or
MHz
unit
.
"
                
)
            
if
unit
in
[
"
KB
"
"
mAh
"
"
mWh
"
]
:
                
return
sum
(
_filter
(
vals
)
)
            
raise
NotImplementedError
(
"
Unit
%
s
not
suported
"
%
unit
)
        
if
len
(
vals
)
>
1
:
            
return
round
(
filters
.
geometric_mean
(
_filter
(
vals
)
)
2
)
        
return
round
(
filters
.
mean
(
_filter
(
vals
)
)
2
)
    
def
_process_measurements
(
self
suite
test
measurement_name
replicates
)
:
        
subtest
=
{
}
        
subtest
[
"
name
"
]
=
measurement_name
        
subtest
[
"
lowerIsBetter
"
]
=
test
[
"
subtest_lower_is_better
"
]
        
subtest
[
"
alertThreshold
"
]
=
float
(
test
[
"
alert_threshold
"
]
)
        
unit
=
test
[
"
subtest_unit
"
]
        
if
measurement_name
=
=
"
cpuTime
"
:
            
unit
=
"
ms
"
        
elif
measurement_name
=
=
"
powerUsage
"
:
            
unit
=
"
uWh
"
        
subtest
[
"
unit
"
]
=
unit
        
for
schema_name
in
(
            
"
minBackWindow
"
            
"
maxBackWindow
"
            
"
foreWindow
"
        
)
:
            
if
suite
.
get
(
schema_name
None
)
is
not
None
:
                
subtest
[
schema_name
]
=
suite
[
schema_name
]
        
if
self
.
subtest_alert_on
is
not
None
:
            
if
measurement_name
in
self
.
subtest_alert_on
:
                
LOG
.
info
(
                    
"
turning
on
subtest
alerting
for
measurement
type
:
%
s
"
                    
%
measurement_name
                
)
                
subtest
[
"
shouldAlert
"
]
=
True
                
if
self
.
app
in
(
                    
"
chrome
"
                    
"
chrome
-
m
"
                    
"
custom
-
car
"
                    
"
cstm
-
car
-
m
"
                
)
:
                    
subtest
[
"
shouldAlert
"
]
=
False
            
else
:
                
LOG
.
info
(
                    
"
turning
off
subtest
alerting
for
measurement
type
:
%
s
"
                    
%
measurement_name
                
)
                
subtest
[
"
shouldAlert
"
]
=
False
        
if
self
.
power_test
and
measurement_name
=
=
"
powerUsage
"
:
            
subtest
[
"
shouldAlert
"
]
=
True
        
subtest
[
"
replicates
"
]
=
replicates
        
return
subtest
    
def
summarize_test
(
self
test
suite
*
*
kwargs
)
:
        
subtests
=
None
        
if
"
youtube
-
playback
"
in
test
[
"
name
"
]
:
            
subtests
vals
=
self
.
parseYoutubePlaybackPerformanceOutput
(
test
)
        
elif
"
ve
"
in
test
[
"
name
"
]
:
            
subtests
vals
=
self
.
parseWebCodecsOutput
(
test
)
        
else
:
            
subtests
vals
=
self
.
parseUnknown
(
test
)
        
if
subtests
is
None
:
            
raise
Exception
(
"
No
benchmark
metrics
found
in
browsertime
results
"
)
        
suite
[
"
subtests
"
]
=
subtests
        
self
.
add_additional_metrics
(
test
suite
)
        
if
len
(
subtests
)
>
1
:
            
suite
[
"
value
"
]
=
self
.
construct_summary
(
vals
testname
=
test
[
"
name
"
]
)
        
subtests
.
sort
(
key
=
lambda
subtest
:
subtest
[
"
name
"
]
)
    
def
summarize_suites
(
self
suites
)
:
        
pass
    
def
report_test_success
(
self
)
:
        
if
len
(
self
.
failed_tests
)
>
0
:
            
LOG
.
warning
(
"
Some
tests
failed
.
"
)
            
if
self
.
youtube_playback_failure
:
                
for
test
in
self
.
failed_tests
:
                    
LOG
.
warning
(
"
Youtube
sub
-
test
FAILED
:
%
s
"
%
test
)
                
LOG
.
warning
(
                    
"
Youtube
playback
sub
-
tests
failed
!
!
!
"
                    
"
Not
submitting
results
to
perfherder
!
"
                
)
            
return
False
        
return
True
