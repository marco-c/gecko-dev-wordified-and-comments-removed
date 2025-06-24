try
:
    
from
typing
import
TYPE_CHECKING
except
ImportError
:
    
TYPE_CHECKING
=
False
MYPY
=
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
collections
.
abc
import
MutableMapping
    
from
datetime
import
datetime
    
from
types
import
TracebackType
    
from
typing
import
Any
    
from
typing
import
Callable
    
from
typing
import
Dict
    
from
typing
import
List
    
from
typing
import
Mapping
    
from
typing
import
Optional
    
from
typing
import
Tuple
    
from
typing
import
Type
    
from
typing
import
Union
    
from
typing_extensions
import
Literal
TypedDict
    
LogLevelStr
=
Literal
[
"
fatal
"
"
critical
"
"
error
"
"
warning
"
"
info
"
"
debug
"
]
    
Event
=
TypedDict
(
        
"
Event
"
        
{
            
"
breadcrumbs
"
:
dict
[
                
Literal
[
"
values
"
]
list
[
dict
[
str
Any
]
]
            
]
            
"
check_in_id
"
:
str
            
"
contexts
"
:
dict
[
str
dict
[
str
object
]
]
            
"
dist
"
:
str
            
"
duration
"
:
Optional
[
float
]
            
"
environment
"
:
str
            
"
errors
"
:
list
[
dict
[
str
Any
]
]
            
"
event_id
"
:
str
            
"
exception
"
:
dict
[
                
Literal
[
"
values
"
]
list
[
dict
[
str
Any
]
]
            
]
            
"
extra
"
:
MutableMapping
[
str
object
]
            
"
fingerprint
"
:
list
[
str
]
            
"
level
"
:
LogLevelStr
            
"
logentry
"
:
Mapping
[
str
object
]
            
"
logger
"
:
str
            
"
measurements
"
:
dict
[
str
object
]
            
"
message
"
:
str
            
"
modules
"
:
dict
[
str
str
]
            
"
monitor_config
"
:
Mapping
[
str
object
]
            
"
monitor_slug
"
:
Optional
[
str
]
            
"
platform
"
:
Literal
[
"
python
"
]
            
"
profile
"
:
object
            
"
release
"
:
str
            
"
request
"
:
dict
[
str
object
]
            
"
sdk
"
:
Mapping
[
str
object
]
            
"
server_name
"
:
str
            
"
spans
"
:
list
[
dict
[
str
object
]
]
            
"
stacktrace
"
:
dict
[
                
str
object
            
]
            
"
start_timestamp
"
:
datetime
            
"
status
"
:
Optional
[
str
]
            
"
tags
"
:
MutableMapping
[
                
str
str
            
]
            
"
threads
"
:
dict
[
                
Literal
[
"
values
"
]
list
[
dict
[
str
Any
]
]
            
]
            
"
timestamp
"
:
Optional
[
datetime
]
            
"
transaction
"
:
str
            
"
transaction_info
"
:
Mapping
[
str
Any
]
            
"
type
"
:
Literal
[
"
check_in
"
"
transaction
"
]
            
"
user
"
:
dict
[
str
object
]
            
"
_metrics_summary
"
:
dict
[
str
object
]
        
}
        
total
=
False
    
)
    
ExcInfo
=
Tuple
[
        
Optional
[
Type
[
BaseException
]
]
Optional
[
BaseException
]
Optional
[
TracebackType
]
    
]
    
Hint
=
Dict
[
str
Any
]
    
Breadcrumb
=
Dict
[
str
Any
]
    
BreadcrumbHint
=
Dict
[
str
Any
]
    
SamplingContext
=
Dict
[
str
Any
]
    
EventProcessor
=
Callable
[
[
Event
Hint
]
Optional
[
Event
]
]
    
ErrorProcessor
=
Callable
[
[
Event
ExcInfo
]
Optional
[
Event
]
]
    
BreadcrumbProcessor
=
Callable
[
[
Breadcrumb
BreadcrumbHint
]
Optional
[
Breadcrumb
]
]
    
TransactionProcessor
=
Callable
[
[
Event
Hint
]
Optional
[
Event
]
]
    
TracesSampler
=
Callable
[
[
SamplingContext
]
Union
[
float
int
bool
]
]
    
NotImplementedType
=
Any
    
EventDataCategory
=
Literal
[
        
"
default
"
        
"
error
"
        
"
crash
"
        
"
transaction
"
        
"
security
"
        
"
attachment
"
        
"
session
"
        
"
internal
"
        
"
profile
"
        
"
metric_bucket
"
        
"
monitor
"
    
]
    
SessionStatus
=
Literal
[
"
ok
"
"
exited
"
"
crashed
"
"
abnormal
"
]
    
EndpointType
=
Literal
[
"
store
"
"
envelope
"
]
    
DurationUnit
=
Literal
[
        
"
nanosecond
"
        
"
microsecond
"
        
"
millisecond
"
        
"
second
"
        
"
minute
"
        
"
hour
"
        
"
day
"
        
"
week
"
    
]
    
InformationUnit
=
Literal
[
        
"
bit
"
        
"
byte
"
        
"
kilobyte
"
        
"
kibibyte
"
        
"
megabyte
"
        
"
mebibyte
"
        
"
gigabyte
"
        
"
gibibyte
"
        
"
terabyte
"
        
"
tebibyte
"
        
"
petabyte
"
        
"
pebibyte
"
        
"
exabyte
"
        
"
exbibyte
"
    
]
    
FractionUnit
=
Literal
[
"
ratio
"
"
percent
"
]
    
MeasurementUnit
=
Union
[
DurationUnit
InformationUnit
FractionUnit
str
]
    
ProfilerMode
=
Literal
[
"
sleep
"
"
thread
"
"
gevent
"
"
unknown
"
]
    
MetricType
=
Literal
[
"
d
"
"
s
"
"
g
"
"
c
"
]
    
MetricValue
=
Union
[
int
float
str
]
    
MetricTagsInternal
=
Tuple
[
Tuple
[
str
str
]
.
.
.
]
    
MetricTagValue
=
Union
[
        
str
        
int
        
float
        
None
        
List
[
Union
[
int
str
float
None
]
]
        
Tuple
[
Union
[
int
str
float
None
]
.
.
.
]
    
]
    
MetricTags
=
Mapping
[
str
MetricTagValue
]
    
FlushedMetricValue
=
Union
[
int
float
]
    
BucketKey
=
Tuple
[
MetricType
str
MeasurementUnit
MetricTagsInternal
]
    
MetricMetaKey
=
Tuple
[
MetricType
str
MeasurementUnit
]
    
MonitorConfigScheduleType
=
Literal
[
"
crontab
"
"
interval
"
]
    
MonitorConfigScheduleUnit
=
Literal
[
        
"
year
"
        
"
month
"
        
"
week
"
        
"
day
"
        
"
hour
"
        
"
minute
"
        
"
second
"
    
]
    
MonitorConfigSchedule
=
TypedDict
(
        
"
MonitorConfigSchedule
"
        
{
            
"
type
"
:
MonitorConfigScheduleType
            
"
value
"
:
Union
[
int
str
]
            
"
unit
"
:
MonitorConfigScheduleUnit
        
}
        
total
=
False
    
)
    
MonitorConfig
=
TypedDict
(
        
"
MonitorConfig
"
        
{
            
"
schedule
"
:
MonitorConfigSchedule
            
"
timezone
"
:
str
            
"
checkin_margin
"
:
int
            
"
max_runtime
"
:
int
            
"
failure_issue_threshold
"
:
int
            
"
recovery_threshold
"
:
int
        
}
        
total
=
False
    
)
