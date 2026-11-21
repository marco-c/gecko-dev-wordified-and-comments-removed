import
statistics
DEFAULT_COMPARISON
=
"
mean
"
DEFAULT_THRESHOLD
=
3
MAD_SCALE
=
1
.
4826
ZERO_SPREAD_PERCENTAGE
=
50
ZERO_VALUE_THRESHOLD
=
12
HISTORICAL_MIN_NUMS
=
15
class
UnknownComparisonError
(
Exception
)
:
    
pass
class
Comparisons
:
    
"
"
"
Registry
of
the
comparisons
.
"
"
"
    
_methods
=
{
}
    
classmethod
    
def
add
(
cls
name
)
:
        
"
"
"
Decorator
registering
a
comparison
function
under
name
.
"
"
"
        
def
decorator
(
func
)
:
            
cls
.
_methods
[
name
]
=
func
            
return
func
        
return
decorator
    
classmethod
    
def
get
(
cls
name
)
:
        
"
"
"
Return
the
comparison
registered
under
name
.
"
"
"
        
if
name
not
in
cls
.
_methods
:
            
raise
UnknownComparisonError
(
f
"
Unknown
comparison
:
{
name
}
"
)
        
return
cls
.
_methods
[
name
]
def
median_absolute_deviation
(
values
)
:
    
"
"
"
Return
the
median
absolute
deviation
of
values
.
"
"
"
    
median
=
statistics
.
median
(
values
)
    
return
MAD_SCALE
*
statistics
.
median
(
abs
(
value
-
median
)
for
value
in
values
)
def
_compare_statistic
(
    
name
    
statistic
    
spread_name
    
spread
    
new_values
    
historical_values
    
threshold
    
lower_is_better
)
:
    
historical_values
=
list
(
historical_values
or
[
]
)
    
new
=
statistic
(
new_values
)
    
historical
=
statistic
(
historical_values
)
if
historical_values
else
None
    
difference
=
new
-
historical
if
historical
is
not
None
else
None
    
percentage
=
100
*
difference
/
abs
(
historical
)
if
historical
else
None
    
historical_spread
=
(
        
spread
(
historical_values
)
        
if
len
(
historical_values
)
>
=
HISTORICAL_MIN_NUMS
        
else
None
    
)
    
limit
=
None
    
if
threshold
is
not
None
and
historical_spread
is
not
None
:
        
if
historical_spread
:
            
limit
=
threshold
*
historical_spread
        
elif
historical
:
            
limit
=
abs
(
historical
)
*
ZERO_SPREAD_PERCENTAGE
/
100
        
else
:
            
limit
=
ZERO_VALUE_THRESHOLD
    
exceeds_variance
=
None
    
if
limit
is
not
None
:
        
if
lower_is_better
:
            
exceeds_variance
=
difference
>
limit
        
else
:
            
exceeds_variance
=
difference
<
-
limit
    
return
{
        
f
"
new_
{
name
}
"
:
new
        
f
"
historical_
{
name
}
"
:
historical
        
f
"
historical_
{
spread_name
}
"
:
historical_spread
        
"
difference
"
:
difference
        
"
percentage
"
:
percentage
        
"
exceeds_variance
"
:
exceeds_variance
    
}
Comparisons
.
add
(
"
mean
"
)
def
compare_to_mean
(
    
new_values
historical_values
threshold
=
DEFAULT_THRESHOLD
lower_is_better
=
True
)
:
    
"
"
"
Compare
the
means
.
Uses
standard
deviation
for
the
threshold
.
"
"
"
    
return
_compare_statistic
(
        
"
mean
"
        
statistics
.
mean
        
"
stdev
"
        
statistics
.
stdev
        
new_values
        
historical_values
        
threshold
        
lower_is_better
    
)
Comparisons
.
add
(
"
median
"
)
def
compare_to_median
(
    
new_values
historical_values
threshold
=
DEFAULT_THRESHOLD
lower_is_better
=
True
)
:
    
"
"
"
Compare
the
medians
.
Uses
MAD
for
the
threshold
.
"
"
"
    
return
_compare_statistic
(
        
"
median
"
        
statistics
.
median
        
"
mad
"
        
median_absolute_deviation
        
new_values
        
historical_values
        
threshold
        
lower_is_better
    
)
