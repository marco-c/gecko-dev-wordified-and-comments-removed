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
supporting_data
subtest_alert_on
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
'
shouldAlert
'
]
=
True
                    
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
                
elif
'
wasm
-
godot
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
parseWASMGodotOutput
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
summarize_supporting_data
(
self
)
:
        
'
'
'
        
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
values
'
:
{
                               
'
name
'
:
value
                               
'
nameN
'
:
valueN
}
}
        
More
specifically
power
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
cpu
                               
'
wifi
'
:
wifi
                               
'
screen
'
:
screen
                               
'
proportional
'
:
proportional
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
we
will
add
all
of
these
subtest
values
togther
.
        
'
'
'
        
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
        
for
data_set
in
self
.
supporting_data
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
            
data_type
=
data_set
[
'
type
'
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
data_set
[
'
test
'
]
+
"
-
"
+
data_set
[
'
type
'
]
                
'
type
'
:
data_set
[
'
type
'
]
                
'
subtests
'
:
subtests
                
'
lowerIsBetter
'
:
True
                
'
unit
'
:
data_set
[
'
unit
'
]
                
'
alertThreshold
'
:
2
.
0
            
}
            
suites
.
append
(
suite
)
            
for
measurement_name
value
in
data_set
[
'
values
'
]
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
data_set
[
'
test
'
]
+
"
-
"
+
data_type
+
"
-
"
+
measurement_name
                
new_subtest
[
'
value
'
]
=
value
                
new_subtest
[
'
lowerIsBetter
'
]
=
True
                
new_subtest
[
'
alertThreshold
'
]
=
2
.
0
                
new_subtest
[
'
unit
'
]
=
data_set
[
'
unit
'
]
                
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
"
supporting_data
"
)
            
self
.
summarized_supporting_data
.
append
(
test_results
)
        
return
    
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
parseWASMGodotOutput
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
godot
'
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
'
test_name
'
]
                        
screenshot
[
'
page_cycle
'
]
                        
screenshot
[
'
screenshot
'
]
                        
screenshot
[
'
test_name
'
]
                        
screenshot
[
'
page_cycle
'
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
'
MOZ_UPLOAD_DIR
'
]
)
                                           
'
screenshots
.
html
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
'
screenshots
.
html
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
gecko_profile
'
not
in
extra_opts
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
        
else
:
            
LOG
.
info
(
"
gecko
profiling
enabled
-
not
posting
results
for
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
    
def
output_supporting_data
(
self
)
:
        
'
'
'
        
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
it
'
s
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
.
Kept
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
that
was
ran
when
the
supporting
data
was
gathered
.
        
'
'
'
        
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
error
:
no
summarized
supporting
data
found
!
"
)
            
return
False
        
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
'
suites
'
]
[
0
]
[
'
type
'
]
            
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
-
%
s
.
json
'
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
'
raptor
-
%
s
.
json
'
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
wasm_godot_score
(
cls
val_list
)
:
        
"
"
"
        
wasm_godot_score
:
first
-
interactive
mean
        
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
first
-
interactive
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
    
classmethod
    
def
supporting_data_total
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
testname
.
startswith
(
'
raptor
-
wasm
-
godot
'
)
:
            
return
self
.
wasm_godot_score
(
vals
)
        
elif
testname
.
startswith
(
'
supporting_data
'
)
:
            
return
self
.
supporting_data_total
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
