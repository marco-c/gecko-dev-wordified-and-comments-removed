#
-
*
-
coding
:
utf
-
8
-
*
-
import
sys
import
pytest
pytest
.
fixture
def
stepwise_testdir
(
testdir
)
:
    
testdir
.
makeconftest
(
        
"
"
"
def
pytest_addoption
(
parser
)
:
    
group
=
parser
.
getgroup
(
'
general
'
)
    
group
.
addoption
(
'
-
-
fail
'
action
=
'
store_true
'
dest
=
'
fail
'
)
    
group
.
addoption
(
'
-
-
fail
-
last
'
action
=
'
store_true
'
dest
=
'
fail_last
'
)
"
"
"
    
)
    
testdir
.
makepyfile
(
        
test_a
=
"
"
"
def
test_success_before_fail
(
)
:
    
assert
1
def
test_fail_on_flag
(
request
)
:
    
assert
not
request
.
config
.
getvalue
(
'
fail
'
)
def
test_success_after_fail
(
)
:
    
assert
1
def
test_fail_last_on_flag
(
request
)
:
    
assert
not
request
.
config
.
getvalue
(
'
fail_last
'
)
def
test_success_after_last_fail
(
)
:
    
assert
1
"
"
"
    
)
    
testdir
.
makepyfile
(
        
test_b
=
"
"
"
def
test_success
(
)
:
    
assert
1
"
"
"
    
)
    
testdir
.
makeini
(
        
"
"
"
        
[
pytest
]
        
cache_dir
=
.
cache
    
"
"
"
    
)
    
return
testdir
pytest
.
fixture
def
error_testdir
(
testdir
)
:
    
testdir
.
makepyfile
(
        
test_a
=
"
"
"
def
test_error
(
nonexisting_fixture
)
:
    
assert
1
def
test_success_after_fail
(
)
:
    
assert
1
"
"
"
    
)
    
return
testdir
pytest
.
fixture
def
broken_testdir
(
testdir
)
:
    
testdir
.
makepyfile
(
        
working_testfile
=
"
def
test_proper
(
)
:
assert
1
"
broken_testfile
=
"
foobar
"
    
)
    
return
testdir
def
test_run_without_stepwise
(
stepwise_testdir
)
:
    
result
=
stepwise_testdir
.
runpytest
(
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
fail
"
)
    
result
.
stdout
.
fnmatch_lines
(
[
"
*
test_success_before_fail
PASSED
*
"
]
)
    
result
.
stdout
.
fnmatch_lines
(
[
"
*
test_fail_on_flag
FAILED
*
"
]
)
    
result
.
stdout
.
fnmatch_lines
(
[
"
*
test_success_after_fail
PASSED
*
"
]
)
def
test_fail_and_continue_with_stepwise
(
stepwise_testdir
)
:
    
result
=
stepwise_testdir
.
runpytest
(
        
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
"
-
-
fail
"
    
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_success_before_fail
PASSED
"
in
stdout
    
assert
"
test_fail_on_flag
FAILED
"
in
stdout
    
assert
"
test_success_after_fail
"
not
in
stdout
    
result
=
stepwise_testdir
.
runpytest
(
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_success_before_fail
"
not
in
stdout
    
assert
"
test_fail_on_flag
PASSED
"
in
stdout
    
assert
"
test_success_after_fail
PASSED
"
in
stdout
def
test_run_with_skip_option
(
stepwise_testdir
)
:
    
result
=
stepwise_testdir
.
runpytest
(
        
"
-
v
"
        
"
-
-
strict
-
markers
"
        
"
-
-
stepwise
"
        
"
-
-
stepwise
-
skip
"
        
"
-
-
fail
"
        
"
-
-
fail
-
last
"
    
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_fail_on_flag
FAILED
"
in
stdout
    
assert
"
test_success_after_fail
PASSED
"
in
stdout
    
assert
"
test_fail_last_on_flag
FAILED
"
in
stdout
    
assert
"
test_success_after_last_fail
"
not
in
stdout
def
test_fail_on_errors
(
error_testdir
)
:
    
result
=
error_testdir
.
runpytest
(
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_error
ERROR
"
in
stdout
    
assert
"
test_success_after_fail
"
not
in
stdout
def
test_change_testfile
(
stepwise_testdir
)
:
    
result
=
stepwise_testdir
.
runpytest
(
        
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
"
-
-
fail
"
"
test_a
.
py
"
    
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_fail_on_flag
FAILED
"
in
stdout
    
result
=
stepwise_testdir
.
runpytest
(
        
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
"
test_b
.
py
"
    
)
    
assert
not
result
.
stderr
.
str
(
)
    
stdout
=
result
.
stdout
.
str
(
)
    
assert
"
test_success
PASSED
"
in
stdout
pytest
.
mark
.
parametrize
(
"
broken_first
"
[
True
False
]
)
def
test_stop_on_collection_errors
(
broken_testdir
broken_first
)
:
    
"
"
"
Stop
during
collection
errors
.
Broken
test
first
or
broken
test
last
    
actually
surfaced
a
bug
(
#
5444
)
so
we
test
both
situations
.
"
"
"
    
files
=
[
"
working_testfile
.
py
"
"
broken_testfile
.
py
"
]
    
if
broken_first
:
        
files
.
reverse
(
)
    
result
=
broken_testdir
.
runpytest
(
"
-
v
"
"
-
-
strict
-
markers
"
"
-
-
stepwise
"
*
files
)
    
result
.
stdout
.
fnmatch_lines
(
"
*
errors
during
collection
*
"
)
def
test_xfail_handling
(
testdir
)
:
    
"
"
"
Ensure
normal
xfail
is
ignored
and
strict
xfail
interrupts
the
session
in
sw
mode
    
(
#
5547
)
    
"
"
"
    
contents
=
"
"
"
        
import
pytest
        
def
test_a
(
)
:
pass
        
pytest
.
mark
.
xfail
(
strict
=
{
strict
}
)
        
def
test_b
(
)
:
assert
{
assert_value
}
        
def
test_c
(
)
:
pass
        
def
test_d
(
)
:
pass
    
"
"
"
    
testdir
.
makepyfile
(
contents
.
format
(
assert_value
=
"
0
"
strict
=
"
False
"
)
)
    
result
=
testdir
.
runpytest
(
"
-
-
sw
"
"
-
v
"
)
    
result
.
stdout
.
fnmatch_lines
(
        
[
            
"
*
:
:
test_a
PASSED
*
"
            
"
*
:
:
test_b
XFAIL
*
"
            
"
*
:
:
test_c
PASSED
*
"
            
"
*
:
:
test_d
PASSED
*
"
            
"
*
3
passed
1
xfailed
in
*
"
        
]
    
)
    
testdir
.
makepyfile
(
contents
.
format
(
assert_value
=
"
1
"
strict
=
"
True
"
)
)
    
result
=
testdir
.
runpytest
(
"
-
-
sw
"
"
-
v
"
)
    
result
.
stdout
.
fnmatch_lines
(
        
[
            
"
*
:
:
test_a
PASSED
*
"
            
"
*
:
:
test_b
FAILED
*
"
            
"
*
Interrupted
*
"
            
"
*
1
failed
1
passed
in
*
"
        
]
    
)
    
if
not
sys
.
dont_write_bytecode
:
        
testdir
.
tmpdir
.
join
(
"
__pycache__
"
)
.
remove
(
)
    
testdir
.
makepyfile
(
contents
.
format
(
assert_value
=
"
0
"
strict
=
"
True
"
)
)
    
result
=
testdir
.
runpytest
(
"
-
-
sw
"
"
-
v
"
)
    
result
.
stdout
.
fnmatch_lines
(
        
[
            
"
*
:
:
test_b
XFAIL
*
"
            
"
*
:
:
test_c
PASSED
*
"
            
"
*
:
:
test_d
PASSED
*
"
            
"
*
2
passed
1
deselected
1
xfailed
in
*
"
        
]
    
)
