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
from
__future__
import
unicode_literals
absolute_import
from
collections
import
OrderedDict
import
re
import
yaml
from
io
import
StringIO
from
six
.
moves
.
configparser
import
SafeConfigParser
NoOptionError
from
.
regex
import
URL_REGEX
HASH_REGEX
from
.
dependencies
import
DependencyFile
Dependency
from
packaging
.
requirements
import
Requirement
as
PackagingRequirement
InvalidRequirement
from
.
import
filetypes
import
toml
from
packaging
.
specifiers
import
SpecifierSet
import
json
def
setuptools_parse_requirements_backport
(
strs
)
:
    
"
"
"
Yield
Requirement
objects
for
each
specification
in
strs
    
strs
must
be
a
string
or
a
(
possibly
-
nested
)
iterable
thereof
.
    
"
"
"
    
def
yield_lines
(
strs
)
:
        
"
"
"
Yield
non
-
empty
/
non
-
comment
lines
of
a
string
or
sequence
"
"
"
        
if
isinstance
(
strs
str
)
:
            
for
s
in
strs
.
splitlines
(
)
:
                
s
=
s
.
strip
(
)
                
if
s
and
not
s
.
startswith
(
'
#
'
)
:
                    
yield
s
        
else
:
            
for
ss
in
strs
:
                
for
s
in
yield_lines
(
ss
)
:
                    
yield
s
    
lines
=
iter
(
yield_lines
(
strs
)
)
    
for
line
in
lines
:
        
if
'
#
'
in
line
:
            
line
=
line
[
:
line
.
find
(
'
#
'
)
]
        
if
line
.
endswith
(
'
\
\
'
)
:
            
line
=
line
[
:
-
2
]
.
strip
(
)
            
line
+
=
next
(
lines
)
        
yield
PackagingRequirement
(
line
)
class
RequirementsTXTLineParser
(
object
)
:
    
"
"
"
    
"
"
"
    
classmethod
    
def
parse
(
cls
line
)
:
        
"
"
"
        
:
param
line
:
        
:
return
:
        
"
"
"
        
try
:
            
if
"
\
t
#
"
in
line
:
                
parsed
=
setuptools_parse_requirements_backport
(
line
.
replace
(
"
\
t
#
"
"
\
t
#
"
)
)
            
else
:
                
parsed
=
setuptools_parse_requirements_backport
(
line
)
        
except
InvalidRequirement
:
            
return
None
        
dep
=
Dependency
(
            
name
=
parsed
.
name
            
specs
=
parsed
.
specifier
            
line
=
line
            
extras
=
parsed
.
extras
            
dependency_type
=
filetypes
.
requirements_txt
        
)
        
return
dep
class
Parser
(
object
)
:
    
"
"
"
    
"
"
"
    
def
__init__
(
self
obj
)
:
        
"
"
"
        
:
param
obj
:
        
"
"
"
        
self
.
obj
=
obj
        
self
.
_lines
=
None
    
def
iter_lines
(
self
lineno
=
0
)
:
        
"
"
"
        
:
param
lineno
:
        
:
return
:
        
"
"
"
        
for
line
in
self
.
lines
[
lineno
:
]
:
            
yield
line
    
property
    
def
lines
(
self
)
:
        
"
"
"
        
:
return
:
        
"
"
"
        
if
self
.
_lines
is
None
:
            
self
.
_lines
=
self
.
obj
.
content
.
splitlines
(
)
        
return
self
.
_lines
    
property
    
def
is_marked_file
(
self
)
:
        
"
"
"
        
:
return
:
        
"
"
"
        
for
n
line
in
enumerate
(
self
.
iter_lines
(
)
)
:
            
for
marker
in
self
.
obj
.
file_marker
:
                
if
marker
in
line
:
                    
return
True
            
if
n
>
=
2
:
                
break
        
return
False
    
def
is_marked_line
(
self
line
)
:
        
"
"
"
        
:
param
line
:
        
:
return
:
        
"
"
"
        
for
marker
in
self
.
obj
.
line_marker
:
            
if
marker
in
line
:
                
return
True
        
return
False
    
classmethod
    
def
parse_hashes
(
cls
line
)
:
        
"
"
"
        
:
param
line
:
        
:
return
:
        
"
"
"
        
hashes
=
[
]
        
for
match
in
re
.
finditer
(
HASH_REGEX
line
)
:
            
hashes
.
append
(
line
[
match
.
start
(
)
:
match
.
end
(
)
]
)
        
return
re
.
sub
(
HASH_REGEX
"
"
line
)
.
strip
(
)
hashes
    
classmethod
    
def
parse_index_server
(
cls
line
)
:
        
"
"
"
        
:
param
line
:
        
:
return
:
        
"
"
"
        
matches
=
URL_REGEX
.
findall
(
line
)
        
if
matches
:
            
url
=
matches
[
0
]
            
return
url
if
url
.
endswith
(
"
/
"
)
else
url
+
"
/
"
        
return
None
    
classmethod
    
def
resolve_file
(
cls
file_path
line
)
:
        
"
"
"
        
:
param
file_path
:
        
:
param
line
:
        
:
return
:
        
"
"
"
        
line
=
line
.
replace
(
"
-
r
"
"
"
)
.
replace
(
"
-
-
requirement
"
"
"
)
        
parts
=
file_path
.
split
(
"
/
"
)
        
if
"
#
"
in
line
:
            
line
=
line
.
split
(
"
#
"
)
[
0
]
.
strip
(
)
        
if
len
(
parts
)
=
=
1
:
            
return
line
        
return
"
/
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
+
"
/
"
+
line
class
RequirementsTXTParser
(
Parser
)
:
    
"
"
"
    
"
"
"
    
def
parse
(
self
)
:
        
"
"
"
        
Parses
a
requirements
.
txt
-
like
file
        
"
"
"
        
index_server
=
None
        
for
num
line
in
enumerate
(
self
.
iter_lines
(
)
)
:
            
line
=
line
.
rstrip
(
)
            
if
not
line
:
                
continue
            
if
line
.
startswith
(
'
#
'
)
:
                
continue
            
if
line
.
startswith
(
'
-
i
'
)
or
\
                
line
.
startswith
(
'
-
-
index
-
url
'
)
or
\
                
line
.
startswith
(
'
-
-
extra
-
index
-
url
'
)
:
                
index_server
=
self
.
parse_index_server
(
line
)
                
continue
            
elif
self
.
obj
.
path
and
(
line
.
startswith
(
'
-
r
'
)
or
line
.
startswith
(
'
-
-
requirement
'
)
)
:
                
self
.
obj
.
resolved_files
.
append
(
self
.
resolve_file
(
self
.
obj
.
path
line
)
)
            
elif
line
.
startswith
(
'
-
f
'
)
or
line
.
startswith
(
'
-
-
find
-
links
'
)
or
\
                
line
.
startswith
(
'
-
-
no
-
index
'
)
or
line
.
startswith
(
'
-
-
allow
-
external
'
)
or
\
                
line
.
startswith
(
'
-
-
allow
-
unverified
'
)
or
line
.
startswith
(
'
-
Z
'
)
or
\
                
line
.
startswith
(
'
-
-
always
-
unzip
'
)
:
                
continue
            
elif
self
.
is_marked_line
(
line
)
:
                
continue
            
else
:
                
try
:
                    
parseable_line
=
line
                    
if
"
\
\
"
in
line
:
                        
parseable_line
=
line
.
replace
(
"
\
\
"
"
"
)
                        
for
next_line
in
self
.
iter_lines
(
num
+
1
)
:
                            
parseable_line
+
=
next_line
.
strip
(
)
.
replace
(
"
\
\
"
"
"
)
                            
line
+
=
"
\
n
"
+
next_line
                            
if
"
\
\
"
in
next_line
:
                                
continue
                            
break
                        
if
self
.
is_marked_line
(
parseable_line
)
:
                            
continue
                    
hashes
=
[
]
                    
if
"
-
-
hash
"
in
parseable_line
:
                        
parseable_line
hashes
=
Parser
.
parse_hashes
(
parseable_line
)
                    
req
=
RequirementsTXTLineParser
.
parse
(
parseable_line
)
                    
if
req
:
                        
req
.
hashes
=
hashes
                        
req
.
index_server
=
index_server
                        
req
.
line
=
line
                        
self
.
obj
.
dependencies
.
append
(
req
)
                
except
ValueError
:
                    
continue
class
ToxINIParser
(
Parser
)
:
    
"
"
"
    
"
"
"
    
def
parse
(
self
)
:
        
"
"
"
        
:
return
:
        
"
"
"
        
parser
=
SafeConfigParser
(
)
        
parser
.
readfp
(
StringIO
(
self
.
obj
.
content
)
)
        
for
section
in
parser
.
sections
(
)
:
            
try
:
                
content
=
parser
.
get
(
section
=
section
option
=
"
deps
"
)
                
for
n
line
in
enumerate
(
content
.
splitlines
(
)
)
:
                    
if
self
.
is_marked_line
(
line
)
:
                        
continue
                    
if
line
:
                        
req
=
RequirementsTXTLineParser
.
parse
(
line
)
                        
if
req
:
                            
req
.
dependency_type
=
self
.
obj
.
file_type
                            
self
.
obj
.
dependencies
.
append
(
req
)
            
except
NoOptionError
:
                
pass
class
CondaYMLParser
(
Parser
)
:
    
"
"
"
    
"
"
"
    
def
parse
(
self
)
:
        
"
"
"
        
:
return
:
        
"
"
"
        
try
:
            
data
=
yaml
.
safe_load
(
self
.
obj
.
content
)
            
if
data
and
'
dependencies
'
in
data
and
isinstance
(
data
[
'
dependencies
'
]
list
)
:
                
for
dep
in
data
[
'
dependencies
'
]
:
                    
if
isinstance
(
dep
dict
)
and
'
pip
'
in
dep
:
                        
for
n
line
in
enumerate
(
dep
[
'
pip
'
]
)
:
                            
if
self
.
is_marked_line
(
line
)
:
                                
continue
                            
req
=
RequirementsTXTLineParser
.
parse
(
line
)
                            
if
req
:
                                
req
.
dependency_type
=
self
.
obj
.
file_type
                                
self
.
obj
.
dependencies
.
append
(
req
)
        
except
yaml
.
YAMLError
:
            
pass
class
PipfileParser
(
Parser
)
:
    
def
parse
(
self
)
:
        
"
"
"
        
Parse
a
Pipfile
(
as
seen
in
pipenv
)
        
:
return
:
        
"
"
"
        
try
:
            
data
=
toml
.
loads
(
self
.
obj
.
content
_dict
=
OrderedDict
)
            
if
data
:
                
for
package_type
in
[
'
packages
'
'
dev
-
packages
'
]
:
                    
if
package_type
in
data
:
                        
for
name
specs
in
data
[
package_type
]
.
items
(
)
:
                            
if
not
isinstance
(
specs
str
)
:
                                
continue
                            
if
specs
=
=
'
*
'
:
                                
specs
=
'
'
                            
self
.
obj
.
dependencies
.
append
(
                                
Dependency
(
                                    
name
=
name
specs
=
SpecifierSet
(
specs
)
                                    
dependency_type
=
filetypes
.
pipfile
                                    
line
=
'
'
.
join
(
[
name
specs
]
)
                                    
section
=
package_type
                                
)
                            
)
        
except
(
toml
.
TomlDecodeError
IndexError
)
as
e
:
            
pass
class
PipfileLockParser
(
Parser
)
:
    
def
parse
(
self
)
:
        
"
"
"
        
Parse
a
Pipfile
.
lock
(
as
seen
in
pipenv
)
        
:
return
:
        
"
"
"
        
try
:
            
data
=
json
.
loads
(
self
.
obj
.
content
object_pairs_hook
=
OrderedDict
)
            
if
data
:
                
for
package_type
in
[
'
default
'
'
develop
'
]
:
                    
if
package_type
in
data
:
                        
for
name
meta
in
data
[
package_type
]
.
items
(
)
:
                            
if
'
version
'
not
in
meta
:
                                
continue
                            
specs
=
meta
[
'
version
'
]
                            
hashes
=
meta
[
'
hashes
'
]
                            
self
.
obj
.
dependencies
.
append
(
                                
Dependency
(
                                    
name
=
name
specs
=
SpecifierSet
(
specs
)
                                    
dependency_type
=
filetypes
.
pipfile_lock
                                    
hashes
=
hashes
                                    
line
=
'
'
.
join
(
[
name
specs
]
)
                                    
section
=
package_type
                                
)
                            
)
        
except
ValueError
:
            
pass
class
SetupCfgParser
(
Parser
)
:
    
def
parse
(
self
)
:
        
parser
=
SafeConfigParser
(
)
        
parser
.
readfp
(
StringIO
(
self
.
obj
.
content
)
)
        
for
section
in
parser
.
values
(
)
:
            
if
section
.
name
=
=
'
options
'
:
                
options
=
'
install_requires
'
'
setup_requires
'
'
test_require
'
                
for
name
in
options
:
                    
content
=
section
.
get
(
name
)
                    
if
not
content
:
                        
continue
                    
self
.
_parse_content
(
content
)
            
elif
section
.
name
=
=
'
options
.
extras_require
'
:
                
for
content
in
section
.
values
(
)
:
                    
self
.
_parse_content
(
content
)
    
def
_parse_content
(
self
content
)
:
        
for
n
line
in
enumerate
(
content
.
splitlines
(
)
)
:
            
if
self
.
is_marked_line
(
line
)
:
                
continue
            
if
line
:
                
req
=
RequirementsTXTLineParser
.
parse
(
line
)
                
if
req
:
                    
req
.
dependency_type
=
self
.
obj
.
file_type
                    
self
.
obj
.
dependencies
.
append
(
req
)
def
parse
(
content
file_type
=
None
path
=
None
sha
=
None
marker
=
(
(
)
(
)
)
parser
=
None
)
:
    
"
"
"
    
:
param
content
:
    
:
param
file_type
:
    
:
param
path
:
    
:
param
sha
:
    
:
param
marker
:
    
:
param
parser
:
    
:
return
:
    
"
"
"
    
dep_file
=
DependencyFile
(
        
content
=
content
        
path
=
path
        
sha
=
sha
        
marker
=
marker
        
file_type
=
file_type
        
parser
=
parser
    
)
    
return
dep_file
.
parse
(
)
