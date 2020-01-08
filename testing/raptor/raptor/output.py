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
from
__future__
import
absolute_import
import
filter
import
json
import
os
from
mozlog
import
get_proxy_logger
LOG
=
get_proxy_logger
(
component
=
"
raptor
-
output
"
)
class
Output
(
object
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
__init__
(
self
results
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
results
=
results
        
self
.
summarized_results
=
{
}
    
def
summarize
(
self
)
:
        
suites
=
[
]
        
test_results
=
{
            
'
framework
'
:
{
                
'
name
'
:
'
raptor
'
            
}
            
'
suites
'
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
error
:
no
raptor
test
results
found
!
"
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
                
'
name
'
:
test
.
name
                
'
type
'
:
test
.
type
                
'
extraOptions
'
:
test
.
extra_options
                
'
subtests
'
:
subtests
                
'
lowerIsBetter
'
:
test
.
lower_is_better
                
'
unit
'
:
test
.
unit
                
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
            
}
            
suites
.
append
(
suite
)
            
if
test
.
type
=
=
"
pageload
"
:
                
for
measurement_name
replicates
in
test
.
measurements
.
iteritems
(
)
:
                    
new_subtest
=
{
}
                    
new_subtest
[
'
name
'
]
=
test
.
name
+
"
-
"
+
measurement_name
                    
new_subtest
[
'
replicates
'
]
=
replicates
                    
new_subtest
[
'
lowerIsBetter
'
]
=
test
.
subtest_lower_is_better
                    
new_subtest
[
'
alertThreshold
'
]
=
float
(
test
.
alert_threshold
)
                    
new_subtest
[
'
value
'
]
=
0
                    
new_subtest
[
'
unit
'
]
=
test
.
subtest_unit
                    
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
filter
.
ignore_first
(
new_subtest
[
'
replicates
'
]
1
)
                    
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
filter
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
                    
new_subtest
[
'
value
'
]
=
filter
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
'
value
'
]
new_subtest
[
'
name
'
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
.
type
=
=
"
benchmark
"
:
                
if
'
speedometer
'
in
test
.
measurements
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
'
motionmark
'
in
test
.
measurements
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
'
sunspider
'
in
test
.
measurements
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
'
webaudio
'
in
test
.
measurements
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
'
unity
-
webgl
'
in
test
.
measurements
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
'
assorted
-
dom
'
in
test
.
measurements
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
'
wasm
-
misc
'
in
test
.
measurements
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
                
suite
[
'
subtests
'
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
"
)
                
return
            
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
'
value
'
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
.
name
)
        
self
.
summarized_results
=
test_results
    
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
.
measurements
[
'
speedometer
'
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
iteritems
(
)
:
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
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
        
'
'
'
          
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
        
'
'
'
        
_subtests
=
{
}
        
data
=
test
.
measurements
[
'
wasm
-
misc
'
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
'
name
'
]
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
]
.
append
(
item
[
'
time
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
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
.
measurements
[
'
webaudio
'
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
'
name
'
]
                
replicates
=
[
item
[
'
duration
'
]
]
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
]
name
]
)
        
print
subtests
        
return
subtests
vals
    
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
.
measurements
[
'
motionmark
'
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
page_cycle_results
.
keys
(
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
                
replicate
=
round
(
page_cycle_results
[
suite
]
[
sub
]
[
'
frameLength
'
]
[
'
average
'
]
3
)
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
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
.
measurements
[
'
sunspider
'
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
iteritems
(
)
:
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
mean
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
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
.
measurements
[
'
unity
-
webgl
'
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
'
benchmark
'
]
                
if
sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                      
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                      
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                      
'
name
'
:
sub
                                      
'
replicates
'
:
[
]
}
                
_subtests
[
sub
]
[
'
replicates
'
]
.
append
(
item
[
'
result
'
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
_subtests
.
keys
(
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
'
value
'
]
=
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
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
'
value
'
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
.
measurements
[
'
assorted
-
dom
'
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
iteritems
(
)
:
                
if
_sub
not
in
_subtests
.
keys
(
)
:
                    
_subtests
[
_sub
]
=
{
'
unit
'
:
test
.
subtest_unit
                                       
'
alertThreshold
'
:
float
(
test
.
alert_threshold
)
                                       
'
lowerIsBetter
'
:
test
.
subtest_lower_is_better
                                       
'
name
'
:
_sub
                                       
'
replicates
'
:
[
]
}
                
_subtests
[
_sub
]
[
'
replicates
'
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
_subtests
.
keys
(
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
'
value
'
]
=
round
(
filter
.
median
(
_subtests
[
name
]
[
'
replicates
'
]
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
=
=
'
total
'
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
'
value
'
]
name
]
)
        
return
subtests
vals
    
def
output
(
self
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
self
.
summarized_results
=
=
{
}
:
            
LOG
.
error
(
"
error
:
no
summarized
raptor
results
found
!
"
)
            
return
False
        
if
os
.
environ
[
'
MOZ_UPLOAD_DIR
'
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
'
MOZ_UPLOAD_DIR
'
]
)
                                        
'
raptor
.
json
'
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
'
raptor
.
json
'
)
        
with
open
(
results_path
'
w
'
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
        
extra_opts
=
self
.
summarized_results
[
'
suites
'
]
[
0
]
.
get
(
'
extraOptions
'
[
]
)
        
if
'
geckoProfile
'
not
in
extra_opts
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
'
w
'
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
True
    
classmethod
    
def
v8_Metric
(
cls
val_list
)
:
        
results
=
[
i
for
i
j
in
val_list
]
        
score
=
100
*
filter
.
geometric_mean
(
results
)
        
return
score
    
classmethod
    
def
JS_Metric
(
cls
val_list
)
:
        
"
"
"
v8
benchmark
score
"
"
"
        
results
=
[
i
for
i
j
in
val_list
]
        
return
sum
(
results
)
    
classmethod
    
def
speedometer_score
(
cls
val_list
)
:
        
"
"
"
        
speedometer_score
:
https
:
/
/
bug
-
172968
-
attachments
.
webkit
.
org
/
attachment
.
cgi
?
id
=
319888
        
"
"
"
        
correctionFactor
=
3
        
results
=
[
i
for
i
j
in
val_list
]
        
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
filter
.
geometric_mean
(
results
)
/
correctionFactor
        
return
score
    
classmethod
    
def
benchmark_score
(
cls
val_list
)
:
        
"
"
"
        
benchmark_score
:
ares6
/
jetstream
self
reported
as
'
geomean
'
        
"
"
"
        
results
=
[
i
for
i
j
in
val_list
if
j
=
=
'
geomean
'
]
        
return
filter
.
mean
(
results
)
    
classmethod
    
def
webaudio_score
(
cls
val_list
)
:
        
"
"
"
        
webaudio_score
:
self
reported
as
'
Geometric
Mean
'
        
"
"
"
        
results
=
[
i
for
i
j
in
val_list
if
j
=
=
'
Geometric
Mean
'
]
        
return
filter
.
mean
(
results
)
    
classmethod
    
def
unity_webgl_score
(
cls
val_list
)
:
        
"
"
"
        
unity_webgl_score
:
self
reported
as
'
Geometric
Mean
'
        
"
"
"
        
results
=
[
i
for
i
j
in
val_list
if
j
=
=
'
Geometric
Mean
'
]
        
return
filter
.
mean
(
results
)
    
classmethod
    
def
wasm_misc_score
(
cls
val_list
)
:
        
"
"
"
        
wasm_misc_score
:
self
reported
as
'
__total__
'
        
"
"
"
        
results
=
[
i
for
i
j
in
val_list
if
j
=
=
'
__total__
'
]
        
return
filter
.
mean
(
results
)
    
classmethod
    
def
stylebench_score
(
cls
val_list
)
:
        
"
"
"
        
stylebench_score
:
https
:
/
/
bug
-
172968
-
attachments
.
webkit
.
org
/
attachment
.
cgi
?
id
=
319888
        
"
"
"
        
correctionFactor
=
3
        
results
=
[
i
for
i
j
in
val_list
]
        
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
has
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
        
score
=
60
*
1000
/
filter
.
geometric_mean
(
results
)
/
correctionFactor
        
return
score
    
classmethod
    
def
sunspider_score
(
cls
val_list
)
:
        
results
=
[
i
for
i
j
in
val_list
]
        
return
sum
(
results
)
    
classmethod
    
def
assorted_dom_score
(
cls
val_list
)
:
        
results
=
[
i
for
i
j
in
val_list
]
        
return
round
(
filter
.
geometric_mean
(
results
)
2
)
    
def
construct_summary
(
self
vals
testname
)
:
        
if
testname
.
startswith
(
'
raptor
-
v8_7
'
)
:
            
return
self
.
v8_Metric
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
kraken
'
)
:
            
return
self
.
JS_Metric
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
jetstream
'
)
:
            
return
self
.
benchmark_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
speedometer
'
)
:
            
return
self
.
speedometer_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
stylebench
'
)
:
            
return
self
.
stylebench_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
sunspider
'
)
:
            
return
self
.
sunspider_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
unity
-
webgl
'
)
:
            
return
self
.
unity_webgl_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
webaudio
'
)
:
            
return
self
.
webaudio_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
assorted
-
dom
'
)
:
            
return
self
.
assorted_dom_score
(
vals
)
        
elif
testname
.
startswith
(
'
raptor
-
wasm
-
misc
'
)
:
            
return
self
.
wasm_misc_score
(
vals
)
        
elif
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
filter
.
geometric_mean
(
[
i
for
i
j
in
vals
]
)
2
)
        
else
:
            
return
round
(
filter
.
mean
(
[
i
for
i
j
in
vals
]
)
2
)
