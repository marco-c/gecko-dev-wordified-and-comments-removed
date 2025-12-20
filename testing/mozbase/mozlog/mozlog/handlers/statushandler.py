from
collections
import
defaultdict
namedtuple
RunSummary
=
namedtuple
(
    
"
RunSummary
"
    
(
        
"
unexpected_statuses
"
        
"
expected_statuses
"
        
"
known_intermittent_statuses
"
        
"
log_level_counts
"
        
"
action_counts
"
    
)
)
class
StatusHandler
:
    
"
"
"
A
handler
used
to
determine
an
overall
status
for
a
test
run
according
    
to
a
sequence
of
log
messages
.
"
"
"
    
def
__init__
(
self
)
:
        
self
.
unexpected_statuses
=
defaultdict
(
int
)
        
self
.
expected_statuses
=
defaultdict
(
int
)
        
self
.
known_intermittent_statuses
=
defaultdict
(
int
)
        
self
.
action_counts
=
defaultdict
(
int
)
        
self
.
log_level_counts
=
defaultdict
(
int
)
        
self
.
no_tests_run_count
=
0
        
self
.
tests_with_counted_crash
=
set
(
)
    
def
__call__
(
self
data
)
:
        
action
=
data
[
"
action
"
]
        
known_intermittent
=
data
.
get
(
"
known_intermittent
"
[
]
)
        
if
action
=
=
"
crash
"
:
            
test_name
=
data
.
get
(
"
test
"
)
            
if
test_name
is
None
or
test_name
not
in
self
.
tests_with_counted_crash
:
                
self
.
action_counts
[
"
crash
"
]
+
=
1
                
if
test_name
is
not
None
:
                    
self
.
tests_with_counted_crash
.
add
(
test_name
)
        
else
:
            
self
.
action_counts
[
action
]
+
=
1
        
if
action
=
=
"
log
"
:
            
if
data
[
"
level
"
]
=
=
"
ERROR
"
and
data
[
"
message
"
]
=
=
"
No
tests
ran
"
:
                
self
.
no_tests_run_count
+
=
1
            
self
.
log_level_counts
[
data
[
"
level
"
]
]
+
=
1
        
if
action
in
(
"
test_status
"
"
test_end
"
)
:
            
status
=
data
[
"
status
"
]
            
if
"
expected
"
in
data
and
status
not
in
known_intermittent
:
                
self
.
unexpected_statuses
[
status
]
+
=
1
            
else
:
                
self
.
expected_statuses
[
status
]
+
=
1
                
if
status
in
known_intermittent
:
                    
self
.
known_intermittent_statuses
[
status
]
+
=
1
        
if
action
=
=
"
test_end
"
:
            
self
.
tests_with_counted_crash
.
discard
(
data
.
get
(
"
test
"
)
)
        
if
action
=
=
"
assertion_count
"
:
            
if
data
[
"
count
"
]
<
data
[
"
min_expected
"
]
:
                
self
.
unexpected_statuses
[
"
PASS
"
]
+
=
1
            
elif
data
[
"
count
"
]
>
data
[
"
max_expected
"
]
:
                
self
.
unexpected_statuses
[
"
FAIL
"
]
+
=
1
            
elif
data
[
"
count
"
]
:
                
self
.
expected_statuses
[
"
FAIL
"
]
+
=
1
            
else
:
                
self
.
expected_statuses
[
"
PASS
"
]
+
=
1
        
if
action
=
=
"
lsan_leak
"
:
            
if
not
data
.
get
(
"
allowed_match
"
)
:
                
self
.
unexpected_statuses
[
"
FAIL
"
]
+
=
1
        
if
action
=
=
"
lsan_summary
"
:
            
if
not
data
.
get
(
"
allowed
"
False
)
:
                
self
.
unexpected_statuses
[
"
FAIL
"
]
+
=
1
        
if
action
=
=
"
mozleak_total
"
:
            
if
data
[
"
bytes
"
]
is
not
None
and
data
[
"
bytes
"
]
>
data
.
get
(
"
threshold
"
0
)
:
                
self
.
unexpected_statuses
[
"
FAIL
"
]
+
=
1
    
def
summarize
(
self
)
:
        
return
RunSummary
(
            
dict
(
self
.
unexpected_statuses
)
            
dict
(
self
.
expected_statuses
)
            
dict
(
self
.
known_intermittent_statuses
)
            
dict
(
self
.
log_level_counts
)
            
dict
(
self
.
action_counts
)
        
)
