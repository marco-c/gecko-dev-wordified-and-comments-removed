from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
unittest
from
mozunit
import
main
from
buildconfig
import
(
    
topobjdir
    
topsrcdir
)
from
mozbuild
.
configure
.
lint
import
LintSandbox
import
six
test_path
=
os
.
path
.
abspath
(
__file__
)
class
LintMeta
(
type
)
:
    
def
__new__
(
mcs
name
bases
attrs
)
:
        
def
create_test
(
project
func
)
:
            
def
test
(
self
)
:
                
return
func
(
self
project
)
            
return
test
        
for
project
in
(
            
"
browser
"
            
"
extensions
"
            
"
js
"
            
"
memory
"
            
"
mobile
/
android
"
            
"
tools
/
update
-
programs
"
        
)
:
            
attrs
[
"
test_
%
s
"
%
project
.
replace
(
"
/
"
"
_
"
)
]
=
create_test
(
                
project
attrs
[
"
lint
"
]
            
)
        
return
type
.
__new__
(
mcs
name
bases
attrs
)
six
.
add_metaclass
(
LintMeta
)
class
Lint
(
unittest
.
TestCase
)
:
    
def
setUp
(
self
)
:
        
self
.
_curdir
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
topobjdir
)
    
def
tearDown
(
self
)
:
        
os
.
chdir
(
self
.
_curdir
)
    
def
lint
(
self
project
)
:
        
sandbox
=
LintSandbox
(
            
{
                
"
OLD_CONFIGURE
"
:
os
.
path
.
join
(
topsrcdir
"
old
-
configure
"
)
                
"
MOZCONFIG
"
:
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
test_path
)
"
data
"
"
empty_mozconfig
"
                
)
            
}
            
[
"
configure
"
"
-
-
enable
-
project
=
%
s
"
%
project
"
-
-
help
"
]
        
)
        
sandbox
.
run
(
os
.
path
.
join
(
topsrcdir
"
moz
.
configure
"
)
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
