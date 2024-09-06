"
"
"
output
raptor
test
results
"
"
"
import
copy
import
json
import
os
import
warnings
from
abc
import
ABCMeta
abstractmethod
from
collections
.
abc
import
Iterable
import
filters
import
six
from
logger
.
logger
import
RaptorLogger
from
utils
import
flatten
LOG
=
RaptorLogger
(
component
=
"
perftest
-
output
"
)
VISUAL_METRICS
=
[
    
"
SpeedIndex
"
    
"
ContentfulSpeedIndex
"
    
"
PerceptualSpeedIndex
"
    
"
FirstVisualChange
"
    
"
LastVisualChange
"
    
"
VisualReadiness
"
    
"
VisualComplete85
"
    
"
VisualComplete95
"
    
"
VisualComplete99
"
]
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
six
.
add_metaclass
(
ABCMeta
)
class
PerftestOutput
(
object
)
:
    
"
"
"
Abstract
base
class
to
handle
output
of
perftest
results
"
"
"
    
def
__init__
(
        
self
results
supporting_data
subtest_alert_on
app
extra_summary_methods
=
[
]
    
)
:
        
"
"
"
        
-
results
:
list
of
RaptorTestResult
instances
        
"
"
"
        
self
.
app
=
app
        
self
.
results
=
results
        
self
.
summarized_results
=
{
}
        
self
.
supporting_data
=
supporting_data
        
self
.
summarized_supporting_data
=
[
]
        
self
.
summarized_screenshots
=
[
]
        
self
.
subtest_alert_on
=
subtest_alert_on
        
self
.
browser_name
=
None
        
self
.
browser_version
=
None
        
self
.
extra_summary_methods
=
extra_summary_methods
    
abstractmethod
    
def
summarize
(
self
test_names
)
:
        
raise
NotImplementedError
(
)
    
def
set_browser_meta
(
self
browser_name
browser_version
)
:
        
self
.
browser_name
=
browser_name
        
self
.
browser_version
=
browser_version
    
def
summarize_supporting_data
(
self
)
:
        
"
"
"
        
Supporting
data
was
gathered
outside
of
the
main
raptor
test
;
it
will
be
kept
        
separate
from
the
main
raptor
test
results
.
Summarize
it
appropriately
.
        
supporting_data
=
{
            
'
type
'
:
'
data
-
type
'
            
'
test
'
:
'
raptor
-
test
-
ran
-
when
-
data
-
was
-
gathered
'
            
'
unit
'
:
'
unit
that
the
values
are
in
'
            
'
summarize
-
values
'
:
True
/
False
            
'
suite
-
suffix
-
type
'
:
True
/
False
            
'
values
'
:
{
                
'
name
'
:
value_dict
                
'
nameN
'
:
value_dictN
            
}
        
}
        
More
specifically
subtest
supporting
data
will
look
like
this
:
        
supporting_data
=
{
            
'
type
'
:
'
power
'
            
'
test
'
:
'
raptor
-
speedometer
-
geckoview
'
            
'
unit
'
:
'
mAh
'
            
'
values
'
:
{
                
'
cpu
'
:
{
                    
'
values
'
:
val
                    
'
lowerIsBetter
'
:
True
/
False
                    
'
alertThreshold
'
:
2
.
0
                    
'
subtest
-
prefix
-
type
'
:
True
/
False
                    
'
unit
'
:
'
mWh
'
                
}
                
'
wifi
'
:
.
.
.
            
}
        
}
        
We
want
to
treat
each
value
as
a
'
subtest
'
;
and
for
the
overall
aggregated
        
test
result
the
summary
value
is
dependent
on
the
unit
.
An
exception
is
        
raised
in
case
we
don
'
t
know
about
the
specified
unit
.
        
"
"
"
        
if
self
.
supporting_data
is
None
:
            
return
        
self
.
summarized_supporting_data
=
[
]
        
support_data_by_type
=
{
}
        
for
data_set
in
self
.
supporting_data
:
            
data_type
=
data_set
[
"
type
"
]
            
LOG
.
info
(
"
summarizing
%
s
data
"
%
data_type
)
            
if
data_type
not
in
support_data_by_type
:
                
support_data_by_type
[
data_type
]
=
{
                    
"
framework
"
:
{
"
name
"
:
"
raptor
"
}
                    
"
suites
"
:
[
]
                
}
            
vals
=
[
]
            
subtests
=
[
]
            
suite_name
=
data_set
[
"
test
"
]
            
if
data_set
.
get
(
"
suite
-
suffix
-
type
"
True
)
:
                
suite_name
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
data_set
[
"
test
"
]
data_set
[
"
type
"
]
)
            
suite
=
{
                
"
name
"
:
suite_name
                
"
type
"
:
data_set
[
"
type
"
]
                
"
subtests
"
:
subtests
            
}
            
if
data_set
.
get
(
"
summarize
-
values
"
True
)
:
                
suite
.
update
(
                    
{
                        
"
lowerIsBetter
"
:
True
                        
"
unit
"
:
data_set
[
"
unit
"
]
                        
"
alertThreshold
"
:
2
.
0
                    
}
                
)
            
for
result
in
self
.
results
:
                
if
result
[
"
name
"
]
=
=
data_set
[
"
test
"
]
:
                    
suite
[
"
extraOptions
"
]
=
result
[
"
extra_options
"
]
                    
break
            
support_data_by_type
[
data_type
]
[
"
suites
"
]
.
append
(
suite
)
            
for
measurement_name
value_info
in
data_set
[
"
values
"
]
.
items
(
)
:
                
value
=
value_info
                
if
not
isinstance
(
value_info
dict
)
:
                    
value
=
{
"
values
"
:
value_info
}
                
new_subtest
=
{
}
                
if
value
.
get
(
"
subtest
-
prefix
-
type
"
True
)
:
                    
new_subtest
[
"
name
"
]
=
data_type
+
"
-
"
+
measurement_name
                
else
:
                    
new_subtest
[
"
name
"
]
=
measurement_name
                
new_subtest
[
"
value
"
]
=
value
[
"
values
"
]
                
new_subtest
[
"
lowerIsBetter
"
]
=
value
.
get
(
"
lowerIsBetter
"
True
)
                
new_subtest
[
"
alertThreshold
"
]
=
value
.
get
(
"
alertThreshold
"
2
.
0
)
                
new_subtest
[
"
unit
"
]
=
value
.
get
(
"
unit
"
data_set
[
"
unit
"
]
)
                
if
"
shouldAlert
"
in
value
:
                    
new_subtest
[
"
shouldAlert
"
]
=
value
.
get
(
"
shouldAlert
"
)
                
subtests
.
append
(
new_subtest
)
                
vals
.
append
(
[
new_subtest
[
"
value
"
]
new_subtest
[
"
name
"
]
]
)
            
if
len
(
subtests
)
>
=
1
and
data_set
.
get
(
"
summarize
-
values
"
True
)
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
"
supporting_data
"
unit
=
data_set
[
"
unit
"
]
                
)
        
for
data_type
in
support_data_by_type
:
            
data
=
support_data_by_type
[
data_type
]
            
if
self
.
browser_name
:
                
data
[
"
application
"
]
=
{
"
name
"
:
self
.
browser_name
}
                
if
self
.
browser_version
:
                    
data
[
"
application
"
]
[
"
version
"
]
=
self
.
browser_version
            
self
.
summarized_supporting_data
.
append
(
data
)
        
return
    
def
output
(
self
test_names
)
:
        
"
"
"
output
to
file
and
perfherder
data
json
"
"
"
        
if
os
.
getenv
(
"
MOZ_UPLOAD_DIR
"
)
:
            
results_path
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
os
.
environ
[
"
MOZ_UPLOAD_DIR
"
]
)
"
raptor
.
json
"
            
)
            
screenshot_path
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
os
.
environ
[
"
MOZ_UPLOAD_DIR
"
]
)
"
screenshots
.
html
"
            
)
        
else
:
            
results_path
=
os
.
path
.
join
(
os
.
getcwd
(
)
"
raptor
.
json
"
)
            
screenshot_path
=
os
.
path
.
join
(
os
.
getcwd
(
)
"
screenshots
.
html
"
)
        
success
=
True
        
if
self
.
summarized_results
=
=
{
}
:
            
success
=
False
            
LOG
.
error
(
                
"
no
summarized
raptor
results
found
for
any
of
%
s
"
                
%
"
"
.
join
(
test_names
)
            
)
        
else
:
            
for
suite
in
self
.
summarized_results
[
"
suites
"
]
:
                
gecko_profiling_enabled
=
"
gecko
-
profile
"
in
suite
.
get
(
                    
"
extraOptions
"
[
]
                
)
                
if
gecko_profiling_enabled
:
                    
LOG
.
info
(
"
gecko
profiling
enabled
"
)
                    
suite
[
"
shouldAlert
"
]
=
False
                
tname
=
suite
[
"
name
"
]
                
parts
=
tname
.
split
(
"
.
"
)
                
try
:
                    
tname
=
"
.
"
.
join
(
parts
[
:
-
1
]
)
                
except
Exception
as
e
:
                    
LOG
.
info
(
"
no
alias
found
on
test
ignoring
:
%
s
"
%
e
)
                    
pass
                
found
=
False
                
for
test
in
test_names
:
                    
if
tname
in
test
:
                        
found
=
True
                        
break
                
if
not
found
:
                    
success
=
False
                    
LOG
.
error
(
"
no
summarized
raptor
results
found
for
%
s
"
%
(
tname
)
)
            
with
open
(
results_path
"
w
"
)
as
f
:
                
for
result
in
self
.
summarized_results
:
                    
f
.
write
(
"
%
s
\
n
"
%
result
)
        
if
len
(
self
.
summarized_screenshots
)
>
0
:
            
with
open
(
screenshot_path
"
w
"
)
as
f
:
                
for
result
in
self
.
summarized_screenshots
:
                    
f
.
write
(
"
%
s
\
n
"
%
result
)
            
LOG
.
info
(
"
screen
captures
can
be
found
locally
at
:
%
s
"
%
screenshot_path
)
        
if
self
.
summarized_results
=
=
{
}
:
            
return
success
0
        
test_type
=
self
.
summarized_results
[
"
suites
"
]
[
0
]
.
get
(
"
type
"
"
"
)
        
output_perf_data
=
True
        
not_posting
=
"
-
not
posting
regular
test
results
for
perfherder
"
        
if
test_type
=
=
"
scenario
"
:
            
LOG
.
info
(
"
scenario
test
type
was
run
%
s
"
%
not_posting
)
            
output_perf_data
=
False
        
if
self
.
browser_name
:
            
self
.
summarized_results
[
"
application
"
]
=
{
"
name
"
:
self
.
browser_name
}
            
if
self
.
browser_version
:
                
self
.
summarized_results
[
"
application
"
]
[
"
version
"
]
=
self
.
browser_version
        
total_perfdata
=
0
        
if
output_perf_data
:
            
if
len
(
self
.
summarized_supporting_data
)
=
=
0
:
                
LOG
.
info
(
"
PERFHERDER_DATA
:
%
s
"
%
json
.
dumps
(
self
.
summarized_results
)
)
                
total_perfdata
=
1
            
else
:
                
LOG
.
info
(
                    
"
supporting
data
measurements
exist
-
only
posting
those
to
perfherder
"
                
)
        
json
.
dump
(
            
self
.
summarized_results
open
(
results_path
"
w
"
)
indent
=
2
sort_keys
=
True
        
)
        
LOG
.
info
(
"
results
can
also
be
found
locally
at
:
%
s
"
%
results_path
)
        
return
success
total_perfdata
    
def
output_supporting_data
(
self
test_names
)
:
        
"
"
"
        
Supporting
data
was
gathered
outside
of
the
main
raptor
test
;
it
has
already
        
been
summarized
now
output
it
appropriately
.
        
We
want
to
output
supporting
data
in
a
completely
separate
perfherder
json
blob
and
        
in
a
corresponding
file
artifact
.
This
way
supporting
data
can
be
ingested
as
its
own
        
test
suite
in
perfherder
and
alerted
upon
if
desired
;
kept
outside
of
the
test
results
        
from
the
actual
Raptor
test
which
was
run
when
the
supporting
data
was
gathered
.
        
"
"
"
        
if
len
(
self
.
summarized_supporting_data
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
no
summarized
supporting
data
found
for
%
s
"
%
"
"
.
join
(
test_names
)
            
)
            
return
False
0
        
total_perfdata
=
0
        
for
next_data_set
in
self
.
summarized_supporting_data
:
            
data_type
=
next_data_set
[
"
suites
"
]
[
0
]
[
"
type
"
]
            
if
os
.
environ
[
"
MOZ_UPLOAD_DIR
"
]
:
                
results_path
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
os
.
environ
[
"
MOZ_UPLOAD_DIR
"
]
)
                    
"
raptor
-
%
s
.
json
"
%
data_type
                
)
            
else
:
                
results_path
=
os
.
path
.
join
(
os
.
getcwd
(
)
"
raptor
-
%
s
.
json
"
%
data_type
)
            
json
.
dump
(
next_data_set
open
(
results_path
"
w
"
)
indent
=
2
sort_keys
=
True
)
            
LOG
.
info
(
"
PERFHERDER_DATA
:
%
s
"
%
json
.
dumps
(
next_data_set
)
)
            
LOG
.
info
(
                
"
%
s
results
can
also
be
found
locally
at
:
%
s
"
                
%
(
data_type
results_path
)
            
)
            
total_perfdata
+
=
1
        
return
True
total_perfdata
    
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
            
if
len
(
results
)
!
=
380
:
                
raise
Exception
(
                    
"
StyleBench
requires
380
entries
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
75
:
:
76
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
        
if
test
.
get
(
"
custom_data
"
False
)
:
            
test
[
"
measurements
"
]
=
{
test
[
"
name
"
]
:
[
test
[
"
measurements
"
]
]
}
        
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
            
if
not
test
.
get
(
"
custom_data
"
False
)
:
                
flattened_metrics
=
flatten
(
iteration
(
)
)
            
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
parseSpeedometerOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
speedometer
"
]
        
for
page_cycle
in
data
:
            
for
sub
replicates
in
page_cycle
[
0
]
.
items
(
)
:
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
shouldAlert
"
:
True
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
replicates
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
parseAresSixOutput
(
self
test
)
:
        
"
"
"
        
https
:
/
/
browserbench
.
org
/
ARES
-
6
/
        
Every
pagecycle
will
perform
the
tests
from
the
index
page
        
We
have
4
main
tests
per
index
page
:
        
-
Air
Basic
Babylon
ML
        
-
and
from
these
4
above
ares6
generates
the
Overall
results
        
Each
test
has
3
subtests
(
firstIteration
steadyState
averageWorstCase
)
:
        
-
_steadyState
        
-
_firstIteration
        
-
_averageWorstCase
        
Each
index
page
will
run
5
cycles
this
is
set
in
glue
.
js
        
{
            
'
expected_browser_cycles
'
:
1
            
'
subtest_unit
'
:
'
ms
'
            
'
name
'
:
'
raptor
-
ares6
-
firefox
'
            
'
lower_is_better
'
:
False
            
'
browser_cycle
'
:
'
1
'
            
'
subtest_lower_is_better
'
:
True
            
'
cold
'
:
False
            
'
browser
'
:
'
Firefox
69
.
0a1
20190531035909
'
            
'
type
'
:
'
benchmark
'
            
'
page
'
:
'
http
:
/
/
127
.
0
.
0
.
1
:
35369
/
ARES
-
6
/
index
.
html
?
raptor
'
            
'
unit
'
:
'
ms
'
            
'
alert_threshold
'
:
2
            
'
measurements
'
:
{
                
'
ares6
'
:
[
[
{
                    
'
Babylon_firstIteration
'
:
[
                        
123
.
68
                        
168
.
21999999999997
                        
127
.
34000000000003
                        
113
.
56
                        
128
.
78
                        
169
.
44000000000003
                    
]
                    
'
Air_steadyState
'
:
[
                        
21
.
184723618090434
                        
22
.
906331658291457
                        
19
.
939396984924624
                        
20
.
572462311557775
                        
20
.
790452261306534
                        
18
.
378693467336696
                    
]
                    
etc
.
                
}
]
]
            
}
        
}
        
Details
on
how
/
ARES6
/
index
.
html
is
showing
the
mean
on
subsequent
test
results
:
        
I
selected
just
a
small
part
from
the
metrics
just
to
be
easier
to
explain
        
what
is
going
on
.
        
After
the
raptor
GeckoView
test
finishes
we
have
these
results
in
the
logs
:
        
Extracted
from
"
INFO
-
raptor
-
control
-
server
Info
:
received
webext_results
:
"
        
'
Air_firstIteration
'
:
[
660
.
8000000000002
626
.
4599999999999
655
.
6199999999999
        
635
.
9000000000001
636
.
4000000000001
]
        
Extracted
from
"
INFO
-
raptor
-
output
Info
:
PERFHERDER_DATA
:
"
        
{
"
name
"
:
"
Air_firstIteration
"
"
lowerIsBetter
"
:
true
"
alertThreshold
"
:
2
.
0
        
"
replicates
"
:
[
660
.
8
626
.
46
655
.
62
635
.
9
636
.
4
]
"
value
"
:
636
.
4
"
unit
"
:
"
ms
"
}
        
On
GeckoView
'
s
/
ARES6
/
index
.
html
this
is
what
we
see
for
Air
-
First
Iteration
:
        
-
on
1st
test
cycle
:
660
.
80
(
rounded
from
660
.
8000000000002
)
        
-
on
2nd
test
cycle
:
643
.
63
this
is
coming
from
          
(
660
.
8000000000002
+
626
.
4599999999999
)
/
2
          
then
rounded
up
to
a
precision
of
2
decimals
        
-
on
3rd
test
cycle
:
647
.
63
this
is
coming
from
          
(
660
.
8000000000002
+
626
.
4599999999999
+
655
.
6199999999999
)
/
3
          
then
rounded
up
to
a
precision
of
2
decimals
        
-
and
so
on
        
"
"
"
        
_subtests
=
{
}
        
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
ares6
"
]
        
for
page_cycle
in
data
:
            
for
sub
replicates
in
page_cycle
[
0
]
.
items
(
)
:
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
float
(
round
(
x
3
)
)
for
x
in
replicates
]
                
)
        
vals
=
[
]
        
for
name
test
in
_subtests
.
items
(
)
:
            
test
[
"
value
"
]
=
filters
.
mean
(
test
[
"
replicates
"
]
)
            
vals
.
append
(
[
test
[
"
value
"
]
name
]
)
        
return
list
(
_subtests
.
values
(
)
)
sorted
(
vals
reverse
=
True
)
    
def
parseMotionmarkOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
motionmark
"
]
        
for
page_cycle
in
data
:
            
page_cycle_results
=
page_cycle
[
0
]
            
suite
=
list
(
page_cycle_results
)
[
0
]
            
for
sub
in
page_cycle_results
[
suite
]
.
keys
(
)
:
                
try
:
                    
replicate
=
round
(
                        
float
(
                            
page_cycle_results
[
suite
]
[
sub
]
[
"
complexity
"
]
[
"
bootstrap
"
]
[
                                
"
median
"
                            
]
                            
if
"
ramp
"
in
test
[
"
name
"
]
                            
else
page_cycle_results
[
suite
]
[
sub
]
[
"
frameLength
"
]
[
                                
"
average
"
                            
]
                        
)
                        
3
                    
)
                
except
TypeError
as
e
:
                    
LOG
.
warning
(
                        
"
[
{
}
]
[
{
}
]
:
{
}
-
{
}
"
.
format
(
suite
sub
e
.
__class__
.
__name__
e
)
                    
)
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
replicate
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
        
failed_tests
=
[
]
        
for
pagecycle
in
data
:
            
for
_sub
_value
in
six
.
iteritems
(
pagecycle
[
0
]
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
                    
"
{
}
_decoded_frames
"
.
format
(
_sub
)
                    
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
                    
"
{
}
_dropped_frames
"
.
format
(
_sub
)
_value
[
"
droppedFrames
"
]
                
)
                
create_subtest_entry
(
                    
"
{
}
_
%
_dropped_frames
"
.
format
(
_sub
)
percent_dropped
                
)
        
if
len
(
failed_tests
)
>
0
:
            
[
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
for
test
in
failed_tests
]
            
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
parseUnityWebGLOutput
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
raptor
-
unity
-
webgl
-
firefox
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
unity
-
webgl
'
:
[
                
[
                    
'
[
{
"
benchmark
"
:
"
Mandelbrot
GPU
"
"
result
"
:
1035361
}
.
.
.
}
]
'
                
]
            
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
        
_subtests
=
{
}
        
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
unity
-
webgl
"
]
        
for
page_cycle
in
data
:
            
data
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
item
in
data
:
                
sub
=
item
[
"
benchmark
"
]
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
]
[
"
replicates
"
]
.
append
(
item
[
"
result
"
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
parseWebaudioOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
webaudio
"
]
        
for
page_cycle
in
data
:
            
data
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
item
in
data
:
                
sub
=
item
[
"
name
"
]
                
replicates
=
[
item
[
"
duration
"
]
]
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
float
(
round
(
x
3
)
)
for
x
in
replicates
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
        
print
(
subtests
)
        
return
subtests
vals
    
def
parseWASMGodotOutput
(
self
test
)
:
        
"
"
"
        
{
u
'
wasm
-
godot
'
:
[
            
{
              
"
name
"
:
"
wasm
-
instantiate
"
              
"
time
"
:
349
            
}
{
              
"
name
"
:
"
engine
-
instantiate
"
              
"
time
"
:
1263
            
.
.
.
            
}
]
}
        
"
"
"
        
_subtests
=
{
}
        
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
wasm
-
godot
"
]
        
print
(
data
)
        
for
page_cycle
in
data
:
            
for
item
in
page_cycle
[
0
]
:
                
sub
=
item
[
"
name
"
]
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
]
[
"
replicates
"
]
.
append
(
item
[
"
time
"
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
parseSunspiderOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
sunspider
"
]
        
for
page_cycle
in
data
:
            
for
sub
replicates
in
page_cycle
[
0
]
.
items
(
)
:
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
float
(
round
(
x
3
)
)
for
x
in
replicates
]
                
)
        
subtests
=
[
]
        
vals
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
filters
.
mean
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
parseAssortedDomOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
assorted
-
dom
"
]
        
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
_sub
not
in
_subtests
:
                    
_subtests
[
_sub
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
_sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
_sub
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
_value
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
float
(
                
round
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
2
)
            
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
=
=
"
total
"
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
parseJetstreamTwoOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
jetstream2
"
]
        
for
page_cycle
in
data
:
            
for
sub
replicates
in
page_cycle
[
0
]
.
items
(
)
:
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
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
float
(
round
(
x
3
)
)
for
x
in
replicates
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
filters
.
mean
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
parseWASMMiscOutput
(
self
test
)
:
        
"
"
"
        
{
u
'
wasm
-
misc
'
:
[
          
[
[
{
u
'
name
'
:
u
'
validate
'
u
'
time
'
:
163
.
44000000000005
}
            
.
.
.
            
{
u
'
name
'
:
u
'
__total__
'
u
'
time
'
:
63308
.
434904788155
}
]
]
          
.
.
.
          
[
[
{
u
'
name
'
:
u
'
validate
'
u
'
time
'
:
129
.
42000000000002
}
            
{
u
'
name
'
:
u
'
__total__
'
u
'
time
'
:
63181
.
24089257814
}
]
]
         
]
}
        
"
"
"
        
_subtests
=
{
}
        
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
wasm
-
misc
"
]
        
for
page_cycle
in
data
:
            
for
item
in
page_cycle
[
0
]
:
                
sub
=
item
[
"
name
"
]
                
if
sub
not
in
_subtests
:
                    
_subtests
[
sub
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
_subtests
[
sub
]
[
"
replicates
"
]
.
append
(
item
[
"
time
"
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
parseMatrixReactBenchOutput
(
self
test
)
:
        
_subtests
=
{
}
        
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
matrix
-
react
-
bench
"
]
        
for
page_cycle
in
data
:
            
for
iteration
val
in
page_cycle
:
                
sub
=
f
"
{
iteration
}
-
iterations
"
                
_subtests
.
setdefault
(
                    
sub
                    
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
sub
                        
"
replicates
"
:
[
]
                    
}
                
)
                
_subtests
[
sub
]
[
"
replicates
"
]
.
append
(
val
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
filters
.
mean
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
parseTwitchAnimationOutput
(
self
test
)
:
        
_subtests
=
{
}
        
for
metric_name
data
in
test
[
"
measurements
"
]
.
items
(
)
:
            
if
"
perfstat
-
"
not
in
metric_name
and
metric_name
!
=
"
twitch
-
animation
"
:
                
continue
            
if
metric_name
=
=
"
twitch
-
animation
"
:
                
metric
=
"
run
"
            
else
:
                
metric
=
metric_name
            
for
polymorphic_page_cycle
in
data
:
                
if
not
isinstance
(
polymorphic_page_cycle
list
)
:
                    
page_cycle
=
[
polymorphic_page_cycle
]
                
else
:
                    
page_cycle
=
polymorphic_page_cycle
                
for
val
in
page_cycle
:
                    
_subtests
.
setdefault
(
                        
metric
                        
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
                    
)
                    
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
append
(
val
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
filters
.
mean
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
class
RaptorOutput
(
PerftestOutput
)
:
    
"
"
"
class
for
raptor
output
"
"
"
    
def
summarize
(
self
test_names
)
:
        
suites
=
[
]
        
test_results
=
{
"
framework
"
:
{
"
name
"
:
"
raptor
"
}
"
suites
"
:
suites
}
        
if
len
(
self
.
results
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
no
raptor
test
results
found
for
%
s
"
%
"
"
.
join
(
test_names
)
)
            
return
        
for
test
in
self
.
results
:
            
vals
=
[
]
            
subtests
=
[
]
            
suite
=
{
                
"
name
"
:
test
[
"
name
"
]
                
"
type
"
:
test
[
"
type
"
]
                
"
tags
"
:
test
.
get
(
"
tags
"
[
]
)
                
"
extraOptions
"
:
test
[
"
extra_options
"
]
                
"
subtests
"
:
subtests
                
"
lowerIsBetter
"
:
test
[
"
lower_is_better
"
]
                
"
unit
"
:
test
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
            
}
            
if
hasattr
(
test
"
alert_change_type
"
)
:
                
suite
[
"
alertChangeType
"
]
=
test
[
"
alert_change_type
"
]
            
if
test
[
"
cold
"
]
is
True
:
                
suite
[
"
cold
"
]
=
True
                
suite
[
"
browser_cycle
"
]
=
int
(
test
[
"
browser_cycle
"
]
)
                
suite
[
"
expected_browser_cycles
"
]
=
int
(
test
[
"
expected_browser_cycles
"
]
)
                
suite
[
"
tags
"
]
.
append
(
"
cold
"
)
            
else
:
                
suite
[
"
tags
"
]
.
append
(
"
warm
"
)
            
suites
.
append
(
suite
)
            
if
test
[
"
type
"
]
in
(
"
pageload
"
"
scenario
"
)
:
                
for
measurement_name
replicates
in
test
[
"
measurements
"
]
.
items
(
)
:
                    
new_subtest
=
{
}
                    
new_subtest
[
"
name
"
]
=
measurement_name
                    
new_subtest
[
"
replicates
"
]
=
replicates
                    
new_subtest
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
                    
new_subtest
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
                    
new_subtest
[
"
value
"
]
=
0
                    
new_subtest
[
"
unit
"
]
=
test
[
"
subtest_unit
"
]
                    
if
test
[
"
cold
"
]
is
False
:
                        
LOG
.
info
(
                            
"
ignoring
the
first
%
s
value
due
to
initial
pageload
noise
"
                            
%
measurement_name
                        
)
                        
filtered_values
=
filters
.
ignore_first
(
                            
new_subtest
[
"
replicates
"
]
1
                        
)
                    
else
:
                        
filtered_values
=
new_subtest
[
"
replicates
"
]
                    
if
measurement_name
=
=
"
ttfi
"
:
                        
filtered_values
=
filters
.
ignore_negative
(
filtered_values
)
                        
if
len
(
filtered_values
)
<
1
:
                            
continue
                    
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
                            
new_subtest
[
"
shouldAlert
"
]
=
True
                        
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
                            
new_subtest
[
"
shouldAlert
"
]
=
False
                    
new_subtest
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
filtered_values
)
                    
vals
.
append
(
[
new_subtest
[
"
value
"
]
new_subtest
[
"
name
"
]
]
)
                    
subtests
.
append
(
new_subtest
)
            
elif
test
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
                
if
any
(
                    
[
                        
"
youtube
-
playback
"
in
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
                    
]
                
)
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
assorted
-
dom
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseAssortedDomOutput
(
test
)
                
elif
"
ares6
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseAresSixOutput
(
test
)
                
elif
"
jetstream2
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseJetstreamTwoOutput
(
test
)
                
elif
"
motionmark
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseMotionmarkOutput
(
test
)
                
elif
"
speedometer
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseSpeedometerOutput
(
test
)
                
elif
"
sunspider
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseSunspiderOutput
(
test
)
                
elif
"
unity
-
webgl
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseUnityWebGLOutput
(
test
)
                
elif
"
wasm
-
godot
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWASMGodotOutput
(
test
)
                
elif
"
wasm
-
misc
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWASMMiscOutput
(
test
)
                
elif
"
webaudio
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWebaudioOutput
(
test
)
                
else
:
                    
subtests
vals
in
self
.
parseUnknown
(
test
)
                
suite
[
"
subtests
"
]
=
subtests
            
else
:
                
LOG
.
error
(
                    
"
output
.
summarize
received
unsupported
test
results
type
for
%
s
"
                    
%
test
[
"
name
"
]
                
)
                
return
            
suite
[
"
tags
"
]
.
append
(
test
[
"
type
"
]
)
            
if
len
(
subtests
)
>
1
and
test
[
"
type
"
]
!
=
"
pageload
"
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
            
suite
[
"
tags
"
]
.
sort
(
)
        
suites
.
sort
(
key
=
lambda
suite
:
suite
[
"
name
"
]
)
        
self
.
summarized_results
=
test_results
    
def
combine_browser_cycles
(
self
)
:
        
"
"
"
        
At
this
point
the
results
have
been
summarized
;
however
there
may
have
been
multiple
        
browser
cycles
(
i
.
e
.
cold
load
)
.
In
which
case
the
results
have
one
entry
for
each
        
test
for
each
browser
cycle
.
For
each
test
we
need
to
combine
the
results
for
all
        
browser
cycles
into
one
results
entry
.
        
For
example
this
is
what
the
summarized
results
suites
list
looks
like
from
a
test
that
        
was
run
with
multiple
(
two
)
browser
cycles
:
        
[
{
'
expected_browser_cycles
'
:
2
'
extraOptions
'
:
[
]
            
'
name
'
:
u
'
raptor
-
tp6m
-
amazon
-
geckoview
-
cold
'
'
lowerIsBetter
'
:
True
            
'
alertThreshold
'
:
2
.
0
'
value
'
:
1776
.
94
'
browser_cycle
'
:
1
            
'
subtests
'
:
[
{
'
name
'
:
u
'
dcf
'
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
                
'
value
'
:
818
'
replicates
'
:
[
818
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
fcp
'
                
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
'
value
'
:
1131
'
shouldAlert
'
:
True
                
'
replicates
'
:
[
1131
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
fnbpaint
'
'
lowerIsBetter
'
:
True
                
'
alertThreshold
'
:
2
.
0
'
value
'
:
1056
'
replicates
'
:
[
1056
]
'
unit
'
:
u
'
ms
'
}
                
{
'
name
'
:
u
'
ttfi
'
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
'
value
'
:
18074
                
'
replicates
'
:
[
18074
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
loadtime
'
'
lowerIsBetter
'
:
True
                
'
alertThreshold
'
:
2
.
0
'
value
'
:
1002
'
shouldAlert
'
:
True
'
replicates
'
:
[
1002
]
                
'
unit
'
:
u
'
ms
'
}
]
            
'
cold
'
:
True
'
type
'
:
u
'
pageload
'
'
unit
'
:
u
'
ms
'
}
        
{
'
expected_browser_cycles
'
:
2
'
extraOptions
'
:
[
]
            
'
name
'
:
u
'
raptor
-
tp6m
-
amazon
-
geckoview
-
cold
'
'
lowerIsBetter
'
:
True
            
'
alertThreshold
'
:
2
.
0
'
value
'
:
840
.
25
'
browser_cycle
'
:
2
            
'
subtests
'
:
[
{
'
name
'
:
u
'
dcf
'
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
                
'
value
'
:
462
'
replicates
'
:
[
462
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
fcp
'
                
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
'
value
'
:
718
'
shouldAlert
'
:
True
                
'
replicates
'
:
[
718
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
fnbpaint
'
'
lowerIsBetter
'
:
True
                
'
alertThreshold
'
:
2
.
0
'
value
'
:
676
'
replicates
'
:
[
676
]
'
unit
'
:
u
'
ms
'
}
                
{
'
name
'
:
u
'
ttfi
'
'
lowerIsBetter
'
:
True
'
alertThreshold
'
:
2
.
0
'
value
'
:
3084
                
'
replicates
'
:
[
3084
]
'
unit
'
:
u
'
ms
'
}
{
'
name
'
:
u
'
loadtime
'
'
lowerIsBetter
'
:
True
                
'
alertThreshold
'
:
2
.
0
'
value
'
:
605
'
shouldAlert
'
:
True
'
replicates
'
:
[
605
]
                
'
unit
'
:
u
'
ms
'
}
]
            
'
cold
'
:
True
'
type
'
:
u
'
pageload
'
'
unit
'
:
u
'
ms
'
}
]
        
Need
to
combine
those
into
a
single
entry
.
        
"
"
"
        
if
len
(
self
.
results
)
=
=
0
:
            
LOG
.
info
(
                
"
error
:
no
raptor
test
results
found
so
no
need
to
combine
browser
cycles
"
            
)
            
return
        
suites_to_be_combined
=
[
]
        
combined_suites
=
[
]
        
for
_index
suite
in
enumerate
(
self
.
summarized_results
.
get
(
"
suites
"
[
]
)
)
:
            
if
suite
.
get
(
"
cold
"
)
is
None
:
                
continue
            
if
suite
[
"
expected_browser_cycles
"
]
>
1
:
                
_name
=
suite
[
"
name
"
]
                
_details
=
suite
.
copy
(
)
                
suites_to_be_combined
.
append
(
{
"
name
"
:
_name
"
details
"
:
_details
}
)
                
suite
[
"
to_be_deleted
"
]
=
True
        
combined_suites
=
{
}
        
for
next_suite
in
suites_to_be_combined
:
            
suite_name
=
next_suite
[
"
details
"
]
[
"
name
"
]
            
browser_cycle
=
next_suite
[
"
details
"
]
[
"
browser_cycle
"
]
            
LOG
.
info
(
                
"
combining
results
from
browser
cycle
%
d
for
%
s
"
                
%
(
browser_cycle
suite_name
)
            
)
            
if
suite_name
not
in
combined_suites
:
                
combined_suites
[
suite_name
]
=
next_suite
[
"
details
"
]
                
LOG
.
info
(
"
created
new
combined
result
with
intial
cycle
replicates
"
)
                
del
combined_suites
[
suite_name
]
[
"
cold
"
]
                
del
combined_suites
[
suite_name
]
[
"
browser_cycle
"
]
                
del
combined_suites
[
suite_name
]
[
"
expected_browser_cycles
"
]
            
else
:
                
for
next_subtest
in
next_suite
[
"
details
"
]
[
"
subtests
"
]
:
                    
found_subtest
=
False
                    
for
combined_subtest
in
combined_suites
[
suite_name
]
[
"
subtests
"
]
:
                        
if
combined_subtest
[
"
name
"
]
=
=
next_subtest
[
"
name
"
]
:
                            
LOG
.
info
(
"
adding
replicates
for
%
s
"
%
next_subtest
[
"
name
"
]
)
                            
combined_subtest
[
"
replicates
"
]
.
extend
(
                                
next_subtest
[
"
replicates
"
]
                            
)
                            
found_subtest
=
True
                    
if
not
found_subtest
:
                        
LOG
.
info
(
"
adding
replicates
for
%
s
"
%
next_subtest
[
"
name
"
]
)
                        
combined_suites
[
next_suite
[
"
details
"
]
[
"
name
"
]
]
[
                            
"
subtests
"
                        
]
.
append
(
next_subtest
)
        
for
i
name
in
enumerate
(
combined_suites
)
:
            
vals
=
[
]
            
for
next_sub
in
combined_suites
[
name
]
[
"
subtests
"
]
:
                
next_sub
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
next_sub
[
"
replicates
"
]
)
                
vals
.
append
(
[
next_sub
[
"
value
"
]
next_sub
[
"
name
"
]
]
)
            
if
len
(
combined_suites
[
name
]
[
"
subtests
"
]
)
>
1
:
                
combined_suites
[
name
]
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
name
                
)
            
self
.
summarized_results
[
"
suites
"
]
.
append
(
combined_suites
[
name
]
)
        
self
.
summarized_results
[
"
suites
"
]
=
[
            
item
            
for
item
in
self
.
summarized_results
[
"
suites
"
]
            
if
item
.
get
(
"
to_be_deleted
"
)
is
not
True
        
]
    
def
summarize_screenshots
(
self
screenshots
)
:
        
if
len
(
screenshots
)
=
=
0
:
            
return
        
self
.
summarized_screenshots
.
append
(
            
"
"
"
<
!
DOCTYPE
html
>
        
<
head
>
        
<
style
>
            
table
th
td
{
              
border
:
1px
solid
black
;
              
border
-
collapse
:
collapse
;
            
}
        
<
/
style
>
        
<
/
head
>
        
<
html
>
<
body
>
        
<
h1
>
Captured
screenshots
!
<
/
h1
>
        
<
table
style
=
"
width
:
100
%
"
>
          
<
tr
>
            
<
th
>
Test
Name
<
/
th
>
            
<
th
>
Pagecycle
<
/
th
>
            
<
th
>
Screenshot
<
/
th
>
          
<
/
tr
>
"
"
"
        
)
        
for
screenshot
in
screenshots
:
            
self
.
summarized_screenshots
.
append
(
                
"
"
"
<
tr
>
            
<
th
>
%
s
<
/
th
>
            
<
th
>
%
s
<
/
th
>
            
<
th
>
                
<
img
src
=
"
%
s
"
alt
=
"
%
s
%
s
"
width
=
"
320
"
height
=
"
240
"
>
            
<
/
th
>
            
<
/
tr
>
"
"
"
                
%
(
                    
screenshot
[
"
test_name
"
]
                    
screenshot
[
"
page_cycle
"
]
                    
screenshot
[
"
screenshot
"
]
                    
screenshot
[
"
test_name
"
]
                    
screenshot
[
"
page_cycle
"
]
                
)
            
)
        
self
.
summarized_screenshots
.
append
(
"
"
"
<
/
table
>
<
/
body
>
<
/
html
>
"
"
"
)
class
BrowsertimeOutput
(
PerftestOutput
)
:
    
"
"
"
class
for
browsertime
output
"
"
"
    
def
summarize
(
self
test_names
)
:
        
"
"
"
        
Summarize
the
parsed
browsertime
test
output
and
format
accordingly
so
the
output
can
        
be
ingested
by
Perfherder
.
        
At
this
point
each
entry
in
self
.
results
for
browsertime
-
pageload
tests
is
in
this
format
:
        
{
'
statistics
'
:
{
'
fcp
'
:
{
u
'
p99
'
:
932
u
'
mdev
'
:
10
.
0941
u
'
min
'
:
712
u
'
p90
'
:
810
u
'
max
'
:
        
932
u
'
median
'
:
758
u
'
p10
'
:
728
u
'
stddev
'
:
50
u
'
mean
'
:
769
}
'
dcf
'
:
{
u
'
p99
'
:
864
        
u
'
mdev
'
:
11
.
6768
u
'
min
'
:
614
u
'
p90
'
:
738
u
'
max
'
:
864
u
'
median
'
:
670
u
'
p10
'
:
632
        
u
'
stddev
'
:
58
u
'
mean
'
:
684
}
'
fnbpaint
'
:
{
u
'
p99
'
:
830
u
'
mdev
'
:
9
.
6851
u
'
min
'
:
616
        
u
'
p90
'
:
719
u
'
max
'
:
830
u
'
median
'
:
668
u
'
p10
'
:
642
u
'
stddev
'
:
48
u
'
mean
'
:
680
}
        
'
loadtime
'
:
{
u
'
p99
'
:
5818
u
'
mdev
'
:
111
.
7028
u
'
min
'
:
3220
u
'
p90
'
:
4450
u
'
max
'
:
5818
        
u
'
median
'
:
3476
u
'
p10
'
:
3241
u
'
stddev
'
:
559
u
'
mean
'
:
3642
}
}
'
name
'
:
        
'
raptor
-
tp6
-
guardian
-
firefox
'
'
url
'
:
'
https
:
/
/
www
.
theguardian
.
co
.
uk
'
'
lower_is_better
'
:
        
True
'
measurements
'
:
{
'
fcp
'
:
[
932
744
744
810
712
775
759
744
777
739
809
906
        
734
742
760
758
728
792
757
759
742
759
775
726
730
]
'
dcf
'
:
[
864
679
637
        
662
652
651
710
679
646
689
686
845
670
694
632
703
670
738
633
703
614
        
703
650
622
670
]
'
fnbpaint
'
:
[
830
648
666
704
616
683
678
650
685
651
719
        
820
634
664
681
664
642
703
668
670
669
668
681
652
642
]
'
loadtime
'
:
[
4450
        
3592
3770
3345
3453
3220
3434
3621
3511
3416
3430
5818
4729
3406
3506
3588
        
3245
3381
3707
3241
3595
3483
3236
3390
3476
]
}
'
subtest_unit
'
:
'
ms
'
'
bt_ver
'
:
        
'
4
.
9
.
2
-
android
'
'
alert_threshold
'
:
2
'
cold
'
:
True
'
type
'
:
'
browsertime
-
pageload
'
        
'
unit
'
:
'
ms
'
'
browser
'
:
"
{
u
'
userAgent
'
:
u
'
Mozilla
/
5
.
0
(
Macintosh
;
Intel
Mac
OS
X
10
.
13
;
        
rv
:
70
.
0
)
Gecko
/
20100101
Firefox
/
70
.
0
'
u
'
windowSize
'
:
u
'
1366x694
'
}
"
}
        
Now
we
must
process
this
further
and
prepare
the
result
for
output
suitable
for
perfherder
        
ingestion
.
        
Note
:
For
the
overall
subtest
values
/
results
(
i
.
e
.
for
each
measurement
type
)
we
will
use
        
the
Browsertime
-
provided
statistics
instead
of
calcuating
our
own
geomeans
from
the
        
replicates
.
        
"
"
"
        
def
_filter_data
(
data
method
subtest_name
)
:
            
import
numpy
as
np
            
from
scipy
.
cluster
.
vq
import
kmeans2
whiten
            
"
"
"
            
Take
the
kmeans
of
the
data
and
attempt
to
filter
this
way
.
            
We
'
ll
use
hard
-
coded
values
to
get
rid
of
data
that
is
2x
            
smaller
/
larger
than
the
majority
of
the
data
.
If
the
data
approaches
            
a
35
%
/
65
%
split
then
it
won
'
t
be
filtered
as
we
can
'
t
figure
            
out
which
one
is
the
right
mean
to
take
.
            
The
way
that
this
will
work
for
multi
-
modal
data
(
more
than
2
modes
)
            
is
that
the
majority
of
the
modes
will
end
up
in
either
one
bin
or
            
the
other
.
Taking
the
group
with
the
most
points
lets
us
            
consistently
remove
very
large
outliers
out
of
the
data
and
target
the
            
modes
with
the
largest
prominence
.
            
TODO
:
The
seed
exists
because
using
a
randomized
one
often
gives
us
            
multiple
results
on
the
same
dataset
.
This
should
keep
things
more
            
consistent
from
one
task
to
the
next
.
We
should
also
look
into
playing
            
with
iterations
but
that
comes
at
the
cost
of
processing
time
(
this
            
might
not
be
a
valid
concern
)
.
            
"
"
"
            
data
=
np
.
asarray
(
data
)
            
with
warnings
.
catch_warnings
(
)
:
                
warnings
.
simplefilter
(
"
ignore
"
)
                
kmeans
result
=
kmeans2
(
                    
whiten
(
np
.
asarray
(
[
float
(
d
)
for
d
in
data
]
)
)
2
seed
=
1000
                
)
            
if
len
(
kmeans
)
<
2
:
                
summary_method
=
np
.
mean
                
if
method
=
=
"
geomean
"
:
                    
filters
.
geometric_mean
                
data
=
data
[
                    
np
.
where
(
data
>
summary_method
(
data
)
-
(
np
.
std
(
data
)
*
2
)
)
[
0
]
                
]
                
data
=
list
(
                    
data
[
np
.
where
(
data
<
summary_method
(
data
)
+
(
np
.
std
(
data
)
*
2
)
)
[
0
]
]
                
)
            
else
:
                
first_group
=
data
[
np
.
where
(
result
=
=
0
)
]
                
secnd_group
=
data
[
np
.
where
(
result
=
=
1
)
]
                
total_len
=
len
(
data
)
                
first_len
=
len
(
first_group
)
                
secnd_len
=
len
(
secnd_group
)
                
ratio
=
np
.
ceil
(
(
min
(
first_len
secnd_len
)
/
total_len
)
*
100
)
                
if
ratio
<
=
35
:
                    
max_mean
=
max
(
kmeans
)
                    
min_mean
=
min
(
kmeans
)
                    
if
abs
(
max_mean
/
min_mean
)
>
2
:
                        
major_group
=
first_group
                        
major_mean
=
np
.
mean
(
first_group
)
if
first_len
>
0
else
0
                        
minor_mean
=
np
.
mean
(
secnd_group
)
if
secnd_len
>
0
else
0
                        
if
first_len
<
secnd_len
:
                            
major_group
=
secnd_group
                            
tmp
=
major_mean
                            
major_mean
=
minor_mean
                            
minor_mean
=
tmp
                        
LOG
.
info
(
                            
f
"
{
subtest_name
}
:
Filtering
out
{
total_len
-
len
(
major_group
)
}
"
                            
f
"
data
points
found
in
minor_group
of
data
with
"
                            
f
"
mean
{
minor_mean
}
vs
.
{
major_mean
}
in
major
group
"
                        
)
                        
data
=
major_group
            
return
data
        
def
_process_geomean
(
subtest
)
:
            
data
=
subtest
[
"
replicates
"
]
            
subtest
[
"
value
"
]
=
round
(
filters
.
geometric_mean
(
data
)
1
)
        
def
_process_alt_method
(
subtest
alternative_method
)
:
            
data
=
subtest
[
"
replicates
"
]
            
if
alternative_method
=
=
"
median
"
:
                
subtest
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
data
)
        
def
_process
(
subtest
method
=
"
geomean
"
)
:
            
if
test
[
"
type
"
]
=
=
"
power
"
:
                
subtest
[
"
value
"
]
=
filters
.
mean
(
subtest
[
"
replicates
"
]
)
            
elif
method
=
=
"
geomean
"
:
                
_process_geomean
(
subtest
)
            
else
:
                
_process_alt_method
(
subtest
method
)
            
return
subtest
        
def
_process_suite
(
suite
)
:
            
suite
[
"
subtests
"
]
=
[
                
_process
(
subtest
)
                
for
subtest
in
suite
[
"
subtests
"
]
.
values
(
)
                
if
subtest
[
"
replicates
"
]
            
]
            
if
self
.
extra_summary_methods
:
                
new_subtests
=
[
]
                
for
subtest
in
suite
[
"
subtests
"
]
:
                    
try
:
                        
for
alternative_method
in
self
.
extra_summary_methods
:
                            
new_subtest
=
copy
.
deepcopy
(
subtest
)
                            
new_subtest
[
                                
"
name
"
                            
]
=
f
"
{
new_subtest
[
'
name
'
]
}
(
{
alternative_method
}
)
"
                            
_process
(
new_subtest
alternative_method
)
                            
new_subtests
.
append
(
new_subtest
)
                    
except
Exception
as
e
:
                        
LOG
.
info
(
f
"
Failed
to
summarize
with
alternative
methods
:
{
e
}
"
)
                        
pass
                
suite
[
"
subtests
"
]
.
extend
(
new_subtests
)
            
suite
[
"
subtests
"
]
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
            
if
len
(
suite
[
"
subtests
"
]
)
>
1
and
suite
[
"
type
"
]
!
=
"
pageload
"
:
                
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
suite
[
"
subtests
"
]
                
]
                
testname
=
suite
[
"
name
"
]
                
if
suite
[
"
type
"
]
=
=
"
power
"
:
                    
testname
=
"
supporting_data
"
                
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
testname
)
            
return
suite
        
LOG
.
info
(
"
preparing
browsertime
results
for
output
"
)
        
if
len
(
self
.
results
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
no
browsertime
test
results
found
for
%
s
"
%
"
"
.
join
(
test_names
)
            
)
            
return
        
test_results
=
{
"
framework
"
:
{
"
name
"
:
"
browsertime
"
}
}
        
suites
=
{
}
        
for
test
in
self
.
results
:
            
test_name
=
test
[
"
name
"
]
            
extra_options
=
test
[
"
extra_options
"
]
            
prev_name
=
test_name
            
while
(
                
test_name
in
suites
                
and
suites
[
test_name
]
[
"
extraOptions
"
]
!
=
extra_options
            
)
:
                
missing
=
set
(
extra_options
)
-
set
(
suites
[
test_name
]
[
"
extraOptions
"
]
)
                
if
len
(
missing
)
=
=
0
:
                    
missing
=
set
(
suites
[
test_name
]
[
"
extraOptions
"
]
)
-
set
(
                        
extra_options
                    
)
                
test_name
=
test_name
+
"
-
"
.
join
(
list
(
missing
)
)
                
if
prev_name
=
=
test_name
:
                    
break
                
else
:
                    
prev_name
=
test_name
            
suite
=
suites
.
setdefault
(
                
test_name
                
{
                    
"
name
"
:
test
[
"
name
"
]
                    
"
type
"
:
test
[
"
type
"
]
                    
"
extraOptions
"
:
extra_options
                    
"
tags
"
:
test
.
get
(
"
tags
"
[
]
)
+
extra_options
                    
"
lowerIsBetter
"
:
test
[
"
lower_is_better
"
]
                    
"
unit
"
:
test
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
subtests
"
:
{
}
                
}
            
)
            
for
alert_option
schema_name
in
(
                
(
"
min_back_window
"
"
minBackWindow
"
)
                
(
"
max_back_window
"
"
maxBackWindow
"
)
                
(
"
fore_window
"
"
foreWindow
"
)
            
)
:
                
if
test
.
get
(
alert_option
None
)
is
not
None
:
                    
suite
[
schema_name
]
=
int
(
test
[
alert_option
]
)
            
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
                
suite
[
"
shouldAlert
"
]
=
False
            
if
(
                
test
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
                
and
"
alertChangeType
"
not
in
suite
            
)
:
                
suite
[
"
alertChangeType
"
]
=
test
[
"
alert_change_type
"
]
            
def
_process_measurements
(
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
                
if
measurement_name
=
=
"
cpuTime
"
:
                    
subtest
[
"
unit
"
]
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
                    
subtest
[
"
unit
"
]
=
"
uWh
"
                
else
:
                    
subtest
[
"
unit
"
]
=
test
[
"
subtest_unit
"
]
                
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
            
if
test
.
get
(
"
support_class
"
)
:
                
test
.
get
(
"
support_class
"
)
.
summarize_test
(
test
suite
)
            
elif
test
[
"
type
"
]
in
[
"
pageload
"
"
scenario
"
"
power
"
]
:
                
LOG
.
warning
(
                    
"
This
test
is
using
a
soon
-
to
-
be
deprecated
method
for
summarizing
"
                    
"
output
.
A
subclass
of
browsertime_pageload
.
py
should
be
built
for
"
                    
"
this
instead
.
Output
handling
is
already
built
there
and
the
results
"
                    
"
parsing
will
need
to
be
added
for
this
specific
test
.
"
                
)
                
for
measurement_name
replicates
in
test
[
"
measurements
"
]
.
items
(
)
:
                    
new_subtest
=
_process_measurements
(
measurement_name
replicates
)
                    
if
measurement_name
not
in
suite
[
"
subtests
"
]
:
                        
suite
[
"
subtests
"
]
[
measurement_name
]
=
new_subtest
                    
else
:
                        
suite
[
"
subtests
"
]
[
measurement_name
]
[
"
replicates
"
]
.
extend
(
                            
new_subtest
[
"
replicates
"
]
                        
)
            
elif
"
benchmark
"
in
test
[
"
type
"
]
:
                
subtests
=
None
                
if
"
speedometer
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseSpeedometerOutput
(
test
)
                
elif
"
ares6
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
parseAresSixOutput
(
test
)
                
elif
"
motionmark
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseMotionmarkOutput
(
test
)
                
elif
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
unity
-
webgl
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
parseUnityWebGLOutput
(
test
)
                
elif
"
webaudio
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWebaudioOutput
(
test
)
                
elif
"
wasm
-
godot
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWASMGodotOutput
(
test
)
                
elif
"
wasm
-
misc
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseWASMMiscOutput
(
test
)
                
elif
"
sunspider
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseSunspiderOutput
(
test
)
                
elif
"
assorted
-
dom
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseAssortedDomOutput
(
test
)
                
elif
"
jetstream2
"
in
test
[
"
measurements
"
]
:
                    
subtests
vals
=
self
.
parseJetstreamTwoOutput
(
test
)
                
elif
"
matrix
-
react
-
bench
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
parseMatrixReactBenchOutput
(
test
)
                
elif
"
twitch
-
animation
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
parseTwitchAnimationOutput
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
                
if
"
cpuTime
"
in
test
[
"
measurements
"
]
and
test
.
get
(
                    
"
gather_cpuTime
"
None
                
)
:
                    
replicates
=
test
[
"
measurements
"
]
[
"
cpuTime
"
]
                    
cpu_subtest
=
_process_measurements
(
"
cpuTime
"
replicates
)
                    
_process
(
cpu_subtest
)
                    
suite
[
"
subtests
"
]
.
append
(
cpu_subtest
)
                
if
"
powerUsage
"
in
test
[
"
measurements
"
]
:
                    
replicates
=
test
[
"
measurements
"
]
[
"
powerUsage
"
]
                    
power_subtest
=
_process_measurements
(
"
powerUsage
"
replicates
)
                    
power_subtest
[
"
value
"
]
=
round
(
filters
.
mean
(
replicates
)
2
)
                    
suite
[
"
subtests
"
]
.
append
(
power_subtest
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
        
suites
=
[
            
s
            
if
(
"
benchmark
"
in
s
[
"
type
"
]
or
test
.
get
(
"
support_class
"
)
)
            
else
_process_suite
(
s
)
            
for
s
in
suites
.
values
(
)
        
]
        
if
test
.
get
(
"
support_class
"
)
:
            
test
.
get
(
"
support_class
"
)
.
summarize_suites
(
suites
)
        
suites
.
sort
(
key
=
lambda
suite
:
suite
[
"
name
"
]
)
        
test_results
[
"
suites
"
]
=
suites
        
self
.
summarized_results
=
test_results
