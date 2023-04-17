#
coding
:
utf
-
8
"
"
"
Exposes
a
get_spec_tests
(
)
function
for
the
project
'
s
test
harness
.
Creates
a
unittest
.
TestCase
for
the
tests
defined
in
the
mustache
spec
.
"
"
"
FILE_ENCODING
=
'
utf
-
8
'
yaml
=
None
try
:
    
import
yaml
except
ImportError
:
    
try
:
        
import
json
    
except
:
        
try
:
            
import
simplejson
as
json
        
except
ImportError
:
            
from
sys
import
exc_info
            
ex_type
ex_value
tb
=
exc_info
(
)
            
new_ex
=
Exception
(
"
%
s
:
%
s
"
%
(
ex_type
.
__name__
ex_value
)
)
            
raise
new_ex
.
__class__
new_ex
tb
    
file_extension
=
'
json
'
    
parser
=
json
else
:
    
file_extension
=
'
yml
'
    
parser
=
yaml
import
codecs
import
glob
import
os
.
path
import
unittest
import
pystache
from
pystache
import
common
from
pystache
.
renderer
import
Renderer
from
pystache
.
tests
.
common
import
AssertStringMixin
def
get_spec_tests
(
spec_test_dir
)
:
    
"
"
"
    
Return
a
list
of
unittest
.
TestCase
instances
.
    
"
"
"
    
print
"
pystache
:
spec
tests
:
using
%
s
"
%
_get_parser_info
(
)
    
cases
=
[
]
    
spec_test_dir
=
os
.
path
.
abspath
(
spec_test_dir
)
    
spec_paths
=
glob
.
glob
(
os
.
path
.
join
(
spec_test_dir
'
*
.
%
s
'
%
file_extension
)
)
    
for
path
in
spec_paths
:
        
new_cases
=
_read_spec_tests
(
path
)
        
cases
.
extend
(
new_cases
)
    
spec_test_count
=
len
(
cases
)
    
class
CheckSpecTestsFound
(
unittest
.
TestCase
)
:
        
def
runTest
(
self
)
:
            
if
spec_test_count
>
0
:
                
return
            
raise
Exception
(
"
Spec
tests
not
found
-
-
\
n
in
%
s
\
n
"
                
"
Consult
the
README
file
on
how
to
add
the
Mustache
spec
tests
.
"
%
repr
(
spec_test_dir
)
)
    
case
=
CheckSpecTestsFound
(
)
    
cases
.
append
(
case
)
    
return
cases
def
_get_parser_info
(
)
:
    
return
"
%
s
(
version
%
s
)
"
%
(
parser
.
__name__
parser
.
__version__
)
def
_read_spec_tests
(
path
)
:
    
"
"
"
    
Return
a
list
of
unittest
.
TestCase
instances
.
    
"
"
"
    
b
=
common
.
read
(
path
)
    
u
=
unicode
(
b
encoding
=
FILE_ENCODING
)
    
spec_data
=
parse
(
u
)
    
tests
=
spec_data
[
'
tests
'
]
    
cases
=
[
]
    
for
data
in
tests
:
        
case
=
_deserialize_spec_test
(
data
path
)
        
cases
.
append
(
case
)
    
return
cases
def
_convert_children
(
node
)
:
    
"
"
"
    
Recursively
convert
to
functions
all
"
code
strings
"
below
the
node
.
    
This
function
is
needed
only
for
the
json
format
.
    
"
"
"
    
if
not
isinstance
(
node
(
list
dict
)
)
:
        
return
    
if
isinstance
(
node
list
)
:
        
for
child
in
node
:
            
_convert_children
(
child
)
        
return
    
for
key
in
node
.
keys
(
)
:
        
val
=
node
[
key
]
        
if
not
isinstance
(
val
dict
)
or
val
.
get
(
'
__tag__
'
)
!
=
'
code
'
:
            
_convert_children
(
val
)
            
continue
        
val
=
eval
(
val
[
'
python
'
]
)
        
node
[
key
]
=
val
        
continue
def
_deserialize_spec_test
(
data
file_path
)
:
    
"
"
"
    
Return
a
unittest
.
TestCase
instance
representing
a
spec
test
.
    
Arguments
:
      
data
:
the
dictionary
of
attributes
for
a
single
test
.
    
"
"
"
    
context
=
data
[
'
data
'
]
    
description
=
data
[
'
desc
'
]
    
expected
=
unicode
(
data
[
'
expected
'
]
)
    
partials
=
data
.
has_key
(
'
partials
'
)
and
data
[
'
partials
'
]
or
{
}
    
template
=
data
[
'
template
'
]
    
test_name
=
data
[
'
name
'
]
    
_convert_children
(
context
)
    
test_case
=
_make_spec_test
(
expected
template
context
partials
description
test_name
file_path
)
    
return
test_case
def
_make_spec_test
(
expected
template
context
partials
description
test_name
file_path
)
:
    
"
"
"
    
Return
a
unittest
.
TestCase
instance
representing
a
spec
test
.
    
"
"
"
    
file_name
=
os
.
path
.
basename
(
file_path
)
    
test_method_name
=
"
Mustache
spec
(
%
s
)
:
%
s
"
%
(
file_name
repr
(
test_name
)
)
    
class
SpecTest
(
SpecTestBase
)
:
        
pass
    
def
run_test
(
self
)
:
        
self
.
_runTest
(
)
    
setattr
(
SpecTest
test_method_name
run_test
)
    
case
=
SpecTest
(
test_method_name
)
    
case
.
_context
=
context
    
case
.
_description
=
description
    
case
.
_expected
=
expected
    
case
.
_file_path
=
file_path
    
case
.
_partials
=
partials
    
case
.
_template
=
template
    
case
.
_test_name
=
test_name
    
return
case
def
parse
(
u
)
:
    
"
"
"
    
Parse
the
contents
of
a
spec
test
file
and
return
a
dict
.
    
Arguments
:
      
u
:
a
unicode
string
.
    
"
"
"
    
if
yaml
is
None
:
        
return
json
.
loads
(
u
)
    
def
code_constructor
(
loader
node
)
:
        
value
=
loader
.
construct_mapping
(
node
)
        
return
eval
(
value
[
'
python
'
]
{
}
)
    
yaml
.
add_constructor
(
u
'
!
code
'
code_constructor
)
    
return
yaml
.
load
(
u
)
class
SpecTestBase
(
unittest
.
TestCase
AssertStringMixin
)
:
    
def
_runTest
(
self
)
:
        
context
=
self
.
_context
        
description
=
self
.
_description
        
expected
=
self
.
_expected
        
file_path
=
self
.
_file_path
        
partials
=
self
.
_partials
        
template
=
self
.
_template
        
test_name
=
self
.
_test_name
        
renderer
=
Renderer
(
partials
=
partials
)
        
actual
=
renderer
.
render
(
template
context
)
        
def
escape
(
s
)
:
            
return
s
.
replace
(
"
%
"
"
%
%
"
)
        
parser_info
=
_get_parser_info
(
)
        
subs
=
[
repr
(
test_name
)
description
os
.
path
.
abspath
(
file_path
)
                
template
repr
(
context
)
parser_info
]
        
subs
=
tuple
(
[
escape
(
sub
)
for
sub
in
subs
]
)
        
message
=
"
"
"
%
s
:
%
s
  
File
:
%
s
  
Template
:
\
"
"
"
%
s
\
"
"
"
  
Context
:
%
s
  
%
%
s
  
[
using
%
s
]
  
"
"
"
%
subs
        
self
.
assertString
(
actual
expected
format
=
message
)
