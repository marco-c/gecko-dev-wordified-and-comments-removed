"
"
"
Tests
for
distutils
.
command
.
check
.
"
"
"
import
os
import
textwrap
from
distutils
.
command
.
check
import
check
from
distutils
.
errors
import
DistutilsSetupError
from
distutils
.
tests
import
support
import
pytest
try
:
    
import
pygments
except
ImportError
:
    
pygments
=
None
HERE
=
os
.
path
.
dirname
(
__file__
)
support
.
combine_markers
class
TestCheck
(
support
.
TempdirManager
)
:
    
def
_run
(
self
metadata
=
None
cwd
=
None
*
*
options
)
:
        
if
metadata
is
None
:
            
metadata
=
{
}
        
if
cwd
is
not
None
:
            
old_dir
=
os
.
getcwd
(
)
            
os
.
chdir
(
cwd
)
        
pkg_info
dist
=
self
.
create_dist
(
*
*
metadata
)
        
cmd
=
check
(
dist
)
        
cmd
.
initialize_options
(
)
        
for
name
value
in
options
.
items
(
)
:
            
setattr
(
cmd
name
value
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
run
(
)
        
if
cwd
is
not
None
:
            
os
.
chdir
(
old_dir
)
        
return
cmd
    
def
test_check_metadata
(
self
)
:
        
cmd
=
self
.
_run
(
)
        
assert
cmd
.
_warnings
=
=
1
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
xxx
'
            
'
author_email
'
:
'
xxx
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
        
}
        
cmd
=
self
.
_run
(
metadata
)
        
assert
cmd
.
_warnings
=
=
0
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
self
.
_run
(
{
}
*
*
{
'
strict
'
:
1
}
)
        
cmd
=
self
.
_run
(
metadata
strict
=
True
)
        
assert
cmd
.
_warnings
=
=
0
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
\
u00c9ric
'
            
'
author_email
'
:
'
xxx
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
            
'
description
'
:
'
Something
about
esszet
\
u00df
'
            
'
long_description
'
:
'
More
things
about
esszet
\
u00df
'
        
}
        
cmd
=
self
.
_run
(
metadata
)
        
assert
cmd
.
_warnings
=
=
0
    
def
test_check_author_maintainer
(
self
)
:
        
for
kind
in
(
"
author
"
"
maintainer
"
)
:
            
metadata
=
{
                
'
url
'
:
'
xxx
'
                
kind
+
'
_email
'
:
'
Name
<
name
email
.
com
>
'
                
'
name
'
:
'
xxx
'
                
'
version
'
:
'
xxx
'
            
}
            
cmd
=
self
.
_run
(
metadata
)
            
assert
cmd
.
_warnings
=
=
0
            
metadata
[
kind
+
'
_email
'
]
=
'
name
email
.
com
'
            
cmd
=
self
.
_run
(
metadata
)
            
assert
cmd
.
_warnings
=
=
0
            
metadata
[
kind
]
=
"
Name
"
            
del
metadata
[
kind
+
'
_email
'
]
            
cmd
=
self
.
_run
(
metadata
)
            
assert
cmd
.
_warnings
=
=
0
    
def
test_check_document
(
self
)
:
        
pytest
.
importorskip
(
'
docutils
'
)
        
pkg_info
dist
=
self
.
create_dist
(
)
        
cmd
=
check
(
dist
)
        
broken_rest
=
'
title
\
n
=
=
=
\
n
\
ntest
'
        
msgs
=
cmd
.
_check_rst_data
(
broken_rest
)
        
assert
len
(
msgs
)
=
=
1
        
rest
=
'
title
\
n
=
=
=
=
=
\
n
\
ntest
'
        
msgs
=
cmd
.
_check_rst_data
(
rest
)
        
assert
len
(
msgs
)
=
=
0
    
def
test_check_restructuredtext
(
self
)
:
        
pytest
.
importorskip
(
'
docutils
'
)
        
broken_rest
=
'
title
\
n
=
=
=
\
n
\
ntest
'
        
pkg_info
dist
=
self
.
create_dist
(
long_description
=
broken_rest
)
        
cmd
=
check
(
dist
)
        
cmd
.
check_restructuredtext
(
)
        
assert
cmd
.
_warnings
=
=
1
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
xxx
'
            
'
author_email
'
:
'
xxx
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
            
'
long_description
'
:
broken_rest
        
}
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
self
.
_run
(
metadata
*
*
{
'
strict
'
:
1
'
restructuredtext
'
:
1
}
)
        
metadata
[
'
long_description
'
]
=
'
title
\
n
=
=
=
=
=
\
n
\
ntest
\
u00df
'
        
cmd
=
self
.
_run
(
metadata
strict
=
True
restructuredtext
=
True
)
        
assert
cmd
.
_warnings
=
=
0
        
metadata
[
'
long_description
'
]
=
'
title
\
n
=
=
=
=
=
\
n
\
n
.
.
include
:
:
includetest
.
rst
'
        
cmd
=
self
.
_run
(
metadata
cwd
=
HERE
strict
=
True
restructuredtext
=
True
)
        
assert
cmd
.
_warnings
=
=
0
    
def
test_check_restructuredtext_with_syntax_highlight
(
self
)
:
        
pytest
.
importorskip
(
'
docutils
'
)
        
example_rst_docs
=
[
            
textwrap
.
dedent
(
                
"
"
"
\
            
Here
'
s
some
code
:
            
.
.
code
:
:
python
                
def
foo
(
)
:
                    
pass
            
"
"
"
            
)
            
textwrap
.
dedent
(
                
"
"
"
\
            
Here
'
s
some
code
:
            
.
.
code
-
block
:
:
python
                
def
foo
(
)
:
                    
pass
            
"
"
"
            
)
        
]
        
for
rest_with_code
in
example_rst_docs
:
            
pkg_info
dist
=
self
.
create_dist
(
long_description
=
rest_with_code
)
            
cmd
=
check
(
dist
)
            
cmd
.
check_restructuredtext
(
)
            
msgs
=
cmd
.
_check_rst_data
(
rest_with_code
)
            
if
pygments
is
not
None
:
                
assert
len
(
msgs
)
=
=
0
            
else
:
                
assert
len
(
msgs
)
=
=
1
                
assert
(
                    
str
(
msgs
[
0
]
[
1
]
)
                    
=
=
'
Cannot
analyze
code
.
Pygments
package
not
found
.
'
                
)
    
def
test_check_all
(
self
)
:
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
self
.
_run
(
{
}
*
*
{
'
strict
'
:
1
'
restructuredtext
'
:
1
}
)
