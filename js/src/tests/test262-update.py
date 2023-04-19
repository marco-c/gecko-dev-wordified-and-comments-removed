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
print_function
import
contextlib
import
io
import
os
import
tempfile
import
shutil
import
sys
from
functools
import
partial
from
itertools
import
chain
from
operator
import
itemgetter
UNSUPPORTED_FEATURES
=
set
(
    
[
        
"
tail
-
call
-
optimization
"
        
"
Intl
.
DateTimeFormat
-
quarter
"
        
"
Intl
.
Segmenter
"
        
"
Intl
.
Locale
-
info
"
        
"
Intl
.
DurationFormat
"
        
"
Atomics
.
waitAsync
"
        
"
legacy
-
regexp
"
        
"
json
-
modules
"
        
"
resizable
-
arraybuffer
"
        
"
Temporal
"
        
"
regexp
-
v
-
flag
"
        
"
decorators
"
        
"
regexp
-
duplicate
-
named
-
groups
"
    
]
)
FEATURE_CHECK_NEEDED
=
{
    
"
Atomics
"
:
"
!
this
.
hasOwnProperty
(
'
Atomics
'
)
"
    
"
FinalizationRegistry
"
:
"
!
this
.
hasOwnProperty
(
'
FinalizationRegistry
'
)
"
    
"
SharedArrayBuffer
"
:
"
!
this
.
hasOwnProperty
(
'
SharedArrayBuffer
'
)
"
    
"
WeakRef
"
:
"
!
this
.
hasOwnProperty
(
'
WeakRef
'
)
"
    
"
array
-
grouping
"
:
"
!
Array
.
prototype
.
group
"
    
"
change
-
array
-
by
-
copy
"
:
"
!
Array
.
prototype
.
with
"
}
RELEASE_OR_BETA
=
set
(
    
[
        
"
Intl
.
NumberFormat
-
v3
"
    
]
)
SHELL_OPTIONS
=
{
    
"
import
-
assertions
"
:
"
-
-
enable
-
import
-
assertions
"
    
"
ShadowRealm
"
:
"
-
-
enable
-
shadow
-
realms
"
    
"
array
-
grouping
"
:
"
-
-
enable
-
array
-
grouping
"
    
"
change
-
array
-
by
-
copy
"
:
"
-
-
enable
-
change
-
array
-
by
-
copy
"
}
contextlib
.
contextmanager
def
TemporaryDirectory
(
)
:
    
tmpDir
=
tempfile
.
mkdtemp
(
)
    
try
:
        
yield
tmpDir
    
finally
:
        
shutil
.
rmtree
(
tmpDir
)
def
loadTest262Parser
(
test262Dir
)
:
    
"
"
"
    
Loads
the
test262
test
record
parser
.
    
"
"
"
    
import
imp
    
fileObj
=
None
    
try
:
        
moduleName
=
"
parseTestRecord
"
        
packagingDir
=
os
.
path
.
join
(
test262Dir
"
tools
"
"
packaging
"
)
        
(
fileObj
pathName
description
)
=
imp
.
find_module
(
moduleName
[
packagingDir
]
)
        
return
imp
.
load_module
(
moduleName
fileObj
pathName
description
)
    
finally
:
        
if
fileObj
:
            
fileObj
.
close
(
)
def
tryParseTestFile
(
test262parser
source
testName
)
:
    
"
"
"
    
Returns
the
result
of
test262parser
.
parseTestRecord
(
)
or
None
if
a
parser
    
error
occured
.
    
See
<
https
:
/
/
github
.
com
/
tc39
/
test262
/
blob
/
main
/
INTERPRETING
.
md
>
for
an
    
overview
of
the
returned
test
attributes
.
    
"
"
"
    
try
:
        
return
test262parser
.
parseTestRecord
(
source
testName
)
    
except
Exception
as
err
:
        
print
(
"
Error
'
%
s
'
in
file
:
%
s
"
%
(
err
testName
)
file
=
sys
.
stderr
)
        
print
(
"
Please
report
this
error
to
the
test262
GitHub
repository
!
"
)
        
return
None
def
createRefTestEntry
(
options
skip
skipIf
error
isModule
isAsync
)
:
    
"
"
"
    
Returns
the
|
reftest
|
tuple
(
terms
comments
)
from
the
input
arguments
.
Or
a
    
tuple
of
empty
strings
if
no
reftest
entry
is
required
.
    
"
"
"
    
terms
=
[
]
    
comments
=
[
]
    
if
options
:
        
terms
.
extend
(
options
)
    
if
skip
:
        
terms
.
append
(
"
skip
"
)
        
comments
.
extend
(
skip
)
    
if
skipIf
:
        
terms
.
append
(
"
skip
-
if
(
"
+
"
|
|
"
.
join
(
[
cond
for
(
cond
_
)
in
skipIf
]
)
+
"
)
"
)
        
comments
.
extend
(
[
comment
for
(
_
comment
)
in
skipIf
]
)
    
if
error
:
        
terms
.
append
(
"
error
:
"
+
error
)
    
if
isModule
:
        
terms
.
append
(
"
module
"
)
    
if
isAsync
:
        
terms
.
append
(
"
async
"
)
    
return
(
"
"
.
join
(
terms
)
"
"
.
join
(
comments
)
)
def
createRefTestLine
(
terms
comments
)
:
    
"
"
"
    
Creates
the
|
reftest
|
line
using
the
given
terms
and
comments
.
    
"
"
"
    
refTest
=
terms
    
if
comments
:
        
refTest
+
=
"
-
-
"
+
comments
    
return
refTest
def
createSource
(
testSource
refTest
prologue
epilogue
)
:
    
"
"
"
    
Returns
the
post
-
processed
source
for
|
testSource
|
.
    
"
"
"
    
source
=
[
]
    
if
refTest
:
        
source
.
append
(
b
"
/
/
|
reftest
|
"
+
refTest
.
encode
(
"
utf
-
8
"
)
)
    
if
prologue
:
        
source
.
append
(
prologue
.
encode
(
"
utf
-
8
"
)
)
    
source
.
append
(
testSource
)
    
if
epilogue
:
        
source
.
append
(
epilogue
.
encode
(
"
utf
-
8
"
)
)
        
source
.
append
(
b
"
"
)
    
return
b
"
\
n
"
.
join
(
source
)
def
writeTestFile
(
test262OutDir
testFileName
source
)
:
    
"
"
"
    
Writes
the
test
source
to
|
test262OutDir
|
.
    
"
"
"
    
with
io
.
open
(
os
.
path
.
join
(
test262OutDir
testFileName
)
"
wb
"
)
as
output
:
        
output
.
write
(
source
)
def
addSuffixToFileName
(
fileName
suffix
)
:
    
(
filePath
ext
)
=
os
.
path
.
splitext
(
fileName
)
    
return
filePath
+
suffix
+
ext
def
writeShellAndBrowserFiles
(
    
test262OutDir
harnessDir
includesMap
localIncludesMap
relPath
)
:
    
"
"
"
    
Generate
the
shell
.
js
and
browser
.
js
files
for
the
test
harness
.
    
"
"
"
    
def
findParentIncludes
(
)
:
        
parentIncludes
=
set
(
)
        
current
=
relPath
        
while
current
:
            
(
parent
child
)
=
os
.
path
.
split
(
current
)
            
if
parent
in
includesMap
:
                
parentIncludes
.
update
(
includesMap
[
parent
]
)
            
current
=
parent
        
return
parentIncludes
    
def
findIncludes
(
)
:
        
parentIncludes
=
findParentIncludes
(
)
        
for
include
in
includesMap
[
relPath
]
:
            
if
include
not
in
parentIncludes
:
                
yield
include
    
def
readIncludeFile
(
filePath
)
:
        
with
io
.
open
(
filePath
"
rb
"
)
as
includeFile
:
            
return
b
"
/
/
file
:
%
s
\
n
%
s
"
%
(
                
os
.
path
.
basename
(
filePath
)
.
encode
(
"
utf
-
8
"
)
                
includeFile
.
read
(
)
            
)
    
localIncludes
=
localIncludesMap
[
relPath
]
if
relPath
in
localIncludesMap
else
[
]
    
includeSource
=
b
"
\
n
"
.
join
(
        
map
(
            
readIncludeFile
            
chain
(
                
map
(
partial
(
os
.
path
.
join
harnessDir
)
sorted
(
findIncludes
(
)
)
)
                
map
(
partial
(
os
.
path
.
join
os
.
getcwd
(
)
)
sorted
(
localIncludes
)
)
            
)
        
)
    
)
    
with
io
.
open
(
os
.
path
.
join
(
test262OutDir
relPath
"
shell
.
js
"
)
"
wb
"
)
as
shellFile
:
        
if
includeSource
:
            
shellFile
.
write
(
b
"
/
/
GENERATED
DO
NOT
EDIT
\
n
"
)
            
shellFile
.
write
(
includeSource
)
    
with
io
.
open
(
        
os
.
path
.
join
(
test262OutDir
relPath
"
browser
.
js
"
)
"
wb
"
    
)
as
browserFile
:
        
browserFile
.
write
(
b
"
"
)
def
pathStartsWith
(
path
*
args
)
:
    
prefix
=
os
.
path
.
join
(
*
args
)
    
return
os
.
path
.
commonprefix
(
[
path
prefix
]
)
=
=
prefix
def
convertTestFile
(
test262parser
testSource
testName
includeSet
strictTests
)
:
    
"
"
"
    
Convert
a
test262
test
to
a
compatible
jstests
test
file
.
    
"
"
"
    
testRec
=
tryParseTestFile
(
test262parser
testSource
.
decode
(
"
utf
-
8
"
)
testName
)
    
refTestOptions
=
[
]
    
refTestSkip
=
[
]
    
refTestSkipIf
=
[
]
    
if
testRec
is
None
:
        
refTestSkip
.
append
(
"
has
YAML
errors
"
)
        
testRec
=
dict
(
)
    
onlyStrict
=
"
onlyStrict
"
in
testRec
    
noStrict
=
"
noStrict
"
in
testRec
    
raw
=
"
raw
"
in
testRec
    
isNegative
=
"
negative
"
in
testRec
    
assert
not
isNegative
or
type
(
testRec
[
"
negative
"
]
)
=
=
dict
    
errorType
=
testRec
[
"
negative
"
]
[
"
type
"
]
if
isNegative
else
None
    
isAsync
=
"
async
"
in
testRec
    
assert
not
(
isNegative
and
isAsync
)
(
        
"
Can
'
t
have
both
async
and
negative
attributes
:
%
s
"
%
testName
    
)
    
assert
b
"
DONE
"
not
in
testSource
or
isAsync
or
isNegative
(
        
"
Missing
async
attribute
in
:
%
s
"
%
testName
    
)
    
isModule
=
"
module
"
in
testRec
    
if
"
CanBlockIsFalse
"
in
testRec
:
        
refTestSkipIf
.
append
(
(
"
xulRuntime
.
shell
"
"
shell
can
block
main
thread
"
)
)
    
if
"
CanBlockIsTrue
"
in
testRec
:
        
refTestSkipIf
.
append
(
(
"
!
xulRuntime
.
shell
"
"
browser
cannot
block
main
thread
"
)
)
    
if
"
features
"
in
testRec
:
        
unsupported
=
[
f
for
f
in
testRec
[
"
features
"
]
if
f
in
UNSUPPORTED_FEATURES
]
        
if
unsupported
:
            
refTestSkip
.
append
(
"
%
s
is
not
supported
"
%
"
"
.
join
(
unsupported
)
)
        
else
:
            
releaseOrBeta
=
[
f
for
f
in
testRec
[
"
features
"
]
if
f
in
RELEASE_OR_BETA
]
            
if
releaseOrBeta
:
                
refTestSkipIf
.
append
(
                    
(
                        
"
release_or_beta
"
                        
"
%
s
is
not
released
yet
"
%
"
"
.
join
(
releaseOrBeta
)
                    
)
                
)
            
featureCheckNeeded
=
[
                
f
for
f
in
testRec
[
"
features
"
]
if
f
in
FEATURE_CHECK_NEEDED
            
]
            
if
featureCheckNeeded
:
                
refTestSkipIf
.
append
(
                    
(
                        
"
|
|
"
.
join
(
                            
[
FEATURE_CHECK_NEEDED
[
f
]
for
f
in
featureCheckNeeded
]
                        
)
                        
"
%
s
is
not
enabled
unconditionally
"
                        
%
"
"
.
join
(
featureCheckNeeded
)
                    
)
                
)
            
if
(
                
"
Atomics
"
in
testRec
[
"
features
"
]
                
and
"
SharedArrayBuffer
"
in
testRec
[
"
features
"
]
            
)
:
                
refTestSkipIf
.
append
(
                    
(
                        
"
(
this
.
hasOwnProperty
(
'
getBuildConfiguration
'
)
"
                        
"
&
&
getBuildConfiguration
(
)
[
'
arm64
-
simulator
'
]
)
"
                        
"
ARM64
Simulator
cannot
emulate
atomics
"
                    
)
                
)
            
shellOptions
=
{
                
SHELL_OPTIONS
[
f
]
for
f
in
testRec
[
"
features
"
]
if
f
in
SHELL_OPTIONS
            
}
            
if
shellOptions
:
                
refTestSkipIf
.
append
(
(
"
!
xulRuntime
.
shell
"
"
requires
shell
-
options
"
)
)
                
refTestOptions
.
extend
(
                    
(
"
shell
-
option
(
{
}
)
"
.
format
(
opt
)
for
opt
in
sorted
(
shellOptions
)
)
                
)
    
if
"
includes
"
in
testRec
:
        
assert
not
raw
"
Raw
test
with
includes
:
%
s
"
%
testName
        
includeSet
.
update
(
testRec
[
"
includes
"
]
)
    
if
not
isNegative
and
not
isAsync
:
        
testEpilogue
=
"
reportCompare
(
0
0
)
;
"
    
else
:
        
testEpilogue
=
"
"
    
if
raw
:
        
refTestOptions
.
append
(
"
test262
-
raw
"
)
    
(
terms
comments
)
=
createRefTestEntry
(
        
refTestOptions
refTestSkip
refTestSkipIf
errorType
isModule
isAsync
    
)
    
if
raw
:
        
refTest
=
"
"
        
externRefTest
=
(
terms
comments
)
    
else
:
        
refTest
=
createRefTestLine
(
terms
comments
)
        
externRefTest
=
None
    
noStrictVariant
=
raw
or
isModule
    
assert
not
(
noStrictVariant
and
(
onlyStrict
or
noStrict
)
)
(
        
"
Unexpected
onlyStrict
or
noStrict
attribute
:
%
s
"
%
testName
    
)
    
if
noStrictVariant
or
noStrict
or
not
onlyStrict
:
        
testPrologue
=
"
"
        
nonStrictSource
=
createSource
(
testSource
refTest
testPrologue
testEpilogue
)
        
testFileName
=
testName
        
yield
(
testFileName
nonStrictSource
externRefTest
)
    
if
not
noStrictVariant
and
(
onlyStrict
or
(
not
noStrict
and
strictTests
)
)
:
        
testPrologue
=
"
'
use
strict
'
;
"
        
strictSource
=
createSource
(
testSource
refTest
testPrologue
testEpilogue
)
        
testFileName
=
testName
        
if
not
noStrict
:
            
testFileName
=
addSuffixToFileName
(
testFileName
"
-
strict
"
)
        
yield
(
testFileName
strictSource
externRefTest
)
def
convertFixtureFile
(
fixtureSource
fixtureName
)
:
    
"
"
"
    
Convert
a
test262
fixture
file
to
a
compatible
jstests
test
file
.
    
"
"
"
    
refTestOptions
=
[
]
    
refTestSkip
=
[
"
not
a
test
file
"
]
    
refTestSkipIf
=
[
]
    
errorType
=
None
    
isModule
=
False
    
isAsync
=
False
    
(
terms
comments
)
=
createRefTestEntry
(
        
refTestOptions
refTestSkip
refTestSkipIf
errorType
isModule
isAsync
    
)
    
refTest
=
createRefTestLine
(
terms
comments
)
    
source
=
createSource
(
fixtureSource
refTest
"
"
"
"
)
    
externRefTest
=
None
    
yield
(
fixtureName
source
externRefTest
)
def
process_test262
(
test262Dir
test262OutDir
strictTests
externManifests
)
:
    
"
"
"
    
Process
all
test262
files
and
converts
them
into
jstests
compatible
tests
.
    
"
"
"
    
harnessDir
=
os
.
path
.
join
(
test262Dir
"
harness
"
)
    
testDir
=
os
.
path
.
join
(
test262Dir
"
test
"
)
    
test262parser
=
loadTest262Parser
(
test262Dir
)
    
includesMap
=
{
}
    
localIncludesMap
=
{
}
    
includesMap
[
"
"
]
=
set
(
[
"
sta
.
js
"
"
assert
.
js
"
]
)
    
localIncludesMap
[
"
"
]
=
[
"
test262
-
host
.
js
"
]
    
includesMap
[
"
"
]
.
update
(
[
"
propertyHelper
.
js
"
"
compareArray
.
js
"
]
)
    
writeShellAndBrowserFiles
(
        
test262OutDir
harnessDir
includesMap
localIncludesMap
"
"
    
)
    
explicitIncludes
=
{
}
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
Atomics
"
)
]
=
[
        
"
testAtomics
.
js
"
        
"
testTypedArray
.
js
"
    
]
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
DataView
"
)
]
=
[
        
"
byteConversionValues
.
js
"
    
]
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
Promise
"
)
]
=
[
"
promiseHelper
.
js
"
]
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
Temporal
"
)
]
=
[
"
temporalHelpers
.
js
"
]
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
TypedArray
"
)
]
=
[
        
"
byteConversionValues
.
js
"
        
"
detachArrayBuffer
.
js
"
        
"
nans
.
js
"
    
]
    
explicitIncludes
[
os
.
path
.
join
(
"
built
-
ins
"
"
TypedArrays
"
)
]
=
[
        
"
detachArrayBuffer
.
js
"
    
]
    
for
(
dirPath
dirNames
fileNames
)
in
os
.
walk
(
testDir
)
:
        
relPath
=
os
.
path
.
relpath
(
dirPath
testDir
)
        
if
relPath
=
=
"
.
"
:
            
continue
        
if
relPath
not
in
(
"
prs
"
"
local
"
)
and
not
os
.
path
.
exists
(
            
os
.
path
.
join
(
test262OutDir
relPath
)
        
)
:
            
os
.
makedirs
(
os
.
path
.
join
(
test262OutDir
relPath
)
)
        
includeSet
=
set
(
)
        
includesMap
[
relPath
]
=
includeSet
        
if
relPath
in
explicitIncludes
:
            
includeSet
.
update
(
explicitIncludes
[
relPath
]
)
        
for
fileName
in
fileNames
:
            
filePath
=
os
.
path
.
join
(
dirPath
fileName
)
            
testName
=
os
.
path
.
relpath
(
filePath
testDir
)
            
(
_
fileExt
)
=
os
.
path
.
splitext
(
fileName
)
            
if
fileExt
!
=
"
.
js
"
:
                
shutil
.
copyfile
(
filePath
os
.
path
.
join
(
test262OutDir
testName
)
)
                
continue
            
isFixtureFile
=
fileName
.
endswith
(
"
_FIXTURE
.
js
"
)
            
with
io
.
open
(
filePath
"
rb
"
)
as
testFile
:
                
testSource
=
testFile
.
read
(
)
            
if
isFixtureFile
:
                
convert
=
convertFixtureFile
(
testSource
testName
)
            
else
:
                
convert
=
convertTestFile
(
                    
test262parser
testSource
testName
includeSet
strictTests
                
)
            
for
(
newFileName
newSource
externRefTest
)
in
convert
:
                
writeTestFile
(
test262OutDir
newFileName
newSource
)
                
if
externRefTest
is
not
None
:
                    
externManifests
.
append
(
                        
{
                            
"
name
"
:
newFileName
                            
"
reftest
"
:
externRefTest
                        
}
                    
)
        
writeShellAndBrowserFiles
(
            
test262OutDir
harnessDir
includesMap
localIncludesMap
relPath
        
)
def
fetch_local_changes
(
inDir
outDir
srcDir
strictTests
)
:
    
"
"
"
    
Fetch
the
changes
from
a
local
clone
of
Test262
.
    
1
.
Get
the
list
of
file
changes
made
by
the
current
branch
used
on
Test262
(
srcDir
)
.
    
2
.
Copy
only
the
(
A
)
dded
(
C
)
opied
(
M
)
odified
and
(
R
)
enamed
files
to
inDir
.
    
3
.
inDir
is
treated
like
a
Test262
checkout
where
files
will
be
converted
.
    
4
.
Fetches
the
current
branch
name
to
set
the
outDir
.
    
5
.
Processed
files
will
be
added
to
<
outDir
>
/
local
/
<
branchName
>
.
    
"
"
"
    
import
subprocess
    
status
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
status
-
-
porcelain
"
%
srcDir
)
.
split
(
"
"
)
    
)
    
if
status
.
strip
(
)
:
        
raise
RuntimeError
(
            
"
Please
commit
files
and
cleanup
the
local
test262
folder
before
importing
files
.
\
n
"
            
"
Current
status
:
\
n
%
s
"
%
status
        
)
    
branchName
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
rev
-
parse
-
-
abbrev
-
ref
HEAD
"
%
srcDir
)
.
split
(
"
"
)
    
)
.
split
(
"
\
n
"
)
[
0
]
    
files
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
diff
main
-
-
diff
-
filter
=
ACMR
-
-
name
-
only
"
%
srcDir
)
.
split
(
"
"
)
    
)
    
deletedFiles
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
diff
main
-
-
diff
-
filter
=
D
-
-
name
-
only
"
%
srcDir
)
.
split
(
"
"
)
    
)
    
modifiedFiles
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
diff
main
-
-
diff
-
filter
=
M
-
-
name
-
only
"
%
srcDir
)
.
split
(
"
"
)
    
)
    
renamedFiles
=
subprocess
.
check_output
(
        
(
"
git
-
C
%
s
diff
main
-
-
diff
-
filter
=
R
-
-
summary
"
%
srcDir
)
.
split
(
"
"
)
    
)
    
print
(
"
From
the
branch
%
s
in
%
s
\
n
"
%
(
branchName
srcDir
)
)
    
print
(
"
Files
being
copied
to
the
local
folder
:
\
n
%
s
"
%
files
)
    
if
deletedFiles
:
        
print
(
            
"
Deleted
files
(
use
this
list
to
update
the
skip
list
)
:
\
n
%
s
"
%
deletedFiles
        
)
    
if
modifiedFiles
:
        
print
(
            
"
Modified
files
(
use
this
list
to
update
the
skip
list
)
:
\
n
%
s
"
            
%
modifiedFiles
        
)
    
if
renamedFiles
:
        
print
(
"
Renamed
files
(
already
added
with
the
new
names
)
:
\
n
%
s
"
%
renamedFiles
)
    
for
f
in
files
.
splitlines
(
)
:
        
fileTree
=
os
.
path
.
join
(
inDir
os
.
path
.
dirname
(
f
)
)
        
if
not
os
.
path
.
exists
(
fileTree
)
:
            
os
.
makedirs
(
fileTree
)
        
shutil
.
copyfile
(
            
os
.
path
.
join
(
srcDir
f
)
os
.
path
.
join
(
fileTree
os
.
path
.
basename
(
f
)
)
        
)
    
shutil
.
copytree
(
os
.
path
.
join
(
srcDir
"
tools
"
)
os
.
path
.
join
(
inDir
"
tools
"
)
)
    
shutil
.
copytree
(
os
.
path
.
join
(
srcDir
"
harness
"
)
os
.
path
.
join
(
inDir
"
harness
"
)
)
    
outDir
=
os
.
path
.
join
(
outDir
"
local
"
branchName
)
    
if
os
.
path
.
isdir
(
outDir
)
:
        
shutil
.
rmtree
(
outDir
)
    
os
.
makedirs
(
outDir
)
    
process_test262
(
inDir
outDir
strictTests
[
]
)
def
fetch_pr_files
(
inDir
outDir
prNumber
strictTests
)
:
    
import
requests
    
prTestsOutDir
=
os
.
path
.
join
(
outDir
"
prs
"
prNumber
)
    
if
os
.
path
.
isdir
(
prTestsOutDir
)
:
        
print
(
"
Removing
folder
%
s
"
%
prTestsOutDir
)
        
shutil
.
rmtree
(
prTestsOutDir
)
    
os
.
makedirs
(
prTestsOutDir
)
    
shutil
.
rmtree
(
os
.
path
.
join
(
inDir
"
test
"
)
)
    
prRequest
=
requests
.
get
(
        
"
https
:
/
/
api
.
github
.
com
/
repos
/
tc39
/
test262
/
pulls
/
%
s
"
%
prNumber
    
)
    
prRequest
.
raise_for_status
(
)
    
pr
=
prRequest
.
json
(
)
    
if
pr
[
"
state
"
]
!
=
"
open
"
:
        
return
print
(
"
PR
%
s
is
closed
"
%
prNumber
)
    
url
=
"
https
:
/
/
api
.
github
.
com
/
repos
/
tc39
/
test262
/
pulls
/
%
s
/
files
"
%
prNumber
    
hasNext
=
True
    
while
hasNext
:
        
files
=
requests
.
get
(
url
)
        
files
.
raise_for_status
(
)
        
for
item
in
files
.
json
(
)
:
            
if
not
item
[
"
filename
"
]
.
startswith
(
"
test
/
"
)
:
                
continue
            
filename
=
item
[
"
filename
"
]
            
fileStatus
=
item
[
"
status
"
]
            
print
(
"
%
s
%
s
"
%
(
fileStatus
filename
)
)
            
if
fileStatus
=
=
"
removed
"
:
                
continue
            
contents
=
requests
.
get
(
item
[
"
raw_url
"
]
)
            
contents
.
raise_for_status
(
)
            
fileText
=
contents
.
text
            
filePathDirs
=
os
.
path
.
join
(
inDir
*
filename
.
split
(
"
/
"
)
[
:
-
1
]
)
            
if
not
os
.
path
.
isdir
(
filePathDirs
)
:
                
os
.
makedirs
(
filePathDirs
)
            
with
io
.
open
(
                
os
.
path
.
join
(
inDir
*
filename
.
split
(
"
/
"
)
)
"
wb
"
            
)
as
output_file
:
                
output_file
.
write
(
fileText
.
encode
(
"
utf8
"
)
)
        
hasNext
=
False
        
if
"
link
"
in
files
.
headers
:
            
link
=
files
.
headers
[
"
link
"
]
            
for
pages
in
link
.
split
(
"
"
)
:
                
(
pageUrl
rel
)
=
pages
.
split
(
"
;
"
)
                
assert
pageUrl
[
0
]
=
=
"
<
"
                
assert
pageUrl
[
-
1
]
=
=
"
>
"
                
pageUrl
=
pageUrl
[
1
:
-
1
]
                
assert
pageUrl
.
startswith
(
"
https
:
/
/
api
.
github
.
com
/
"
)
                
assert
(
                    
rel
=
=
'
rel
=
"
prev
"
'
                    
or
rel
=
=
'
rel
=
"
next
"
'
                    
or
rel
=
=
'
rel
=
"
first
"
'
                    
or
rel
=
=
'
rel
=
"
last
"
'
                
)
                
if
rel
=
=
'
rel
=
"
next
"
'
:
                    
url
=
pageUrl
                    
hasNext
=
True
    
process_test262
(
inDir
prTestsOutDir
strictTests
[
]
)
def
general_update
(
inDir
outDir
strictTests
)
:
    
import
subprocess
    
restoreLocalTestsDir
=
False
    
restorePrsTestsDir
=
False
    
localTestsOutDir
=
os
.
path
.
join
(
outDir
"
local
"
)
    
prsTestsOutDir
=
os
.
path
.
join
(
outDir
"
prs
"
)
    
if
os
.
path
.
isdir
(
localTestsOutDir
)
:
        
shutil
.
move
(
localTestsOutDir
inDir
)
        
restoreLocalTestsDir
=
True
    
if
os
.
path
.
isdir
(
prsTestsOutDir
)
:
        
shutil
.
move
(
prsTestsOutDir
inDir
)
        
restorePrsTestsDir
=
True
    
if
os
.
path
.
isdir
(
outDir
)
:
        
shutil
.
rmtree
(
outDir
)
    
os
.
makedirs
(
outDir
)
    
shutil
.
copyfile
(
os
.
path
.
join
(
inDir
"
LICENSE
"
)
os
.
path
.
join
(
outDir
"
LICENSE
"
)
)
    
with
io
.
open
(
os
.
path
.
join
(
outDir
"
GIT
-
INFO
"
)
"
w
"
encoding
=
"
utf
-
8
"
)
as
info
:
        
subprocess
.
check_call
(
[
"
git
"
"
-
C
"
inDir
"
log
"
"
-
1
"
]
stdout
=
info
)
    
externManifests
=
[
]
    
process_test262
(
inDir
outDir
strictTests
externManifests
)
    
with
io
.
open
(
os
.
path
.
join
(
outDir
"
jstests
.
list
"
)
"
wb
"
)
as
manifestFile
:
        
manifestFile
.
write
(
b
"
#
GENERATED
DO
NOT
EDIT
\
n
\
n
"
)
        
for
externManifest
in
sorted
(
externManifests
key
=
itemgetter
(
"
name
"
)
)
:
            
(
terms
comments
)
=
externManifest
[
"
reftest
"
]
            
if
terms
:
                
entry
=
"
%
s
script
%
s
%
s
\
n
"
%
(
                    
terms
                    
externManifest
[
"
name
"
]
                    
(
"
#
%
s
"
%
comments
)
if
comments
else
"
"
                
)
                
manifestFile
.
write
(
entry
.
encode
(
"
utf
-
8
"
)
)
    
if
restoreLocalTestsDir
:
        
shutil
.
move
(
os
.
path
.
join
(
inDir
"
local
"
)
outDir
)
    
if
restorePrsTestsDir
:
        
shutil
.
move
(
os
.
path
.
join
(
inDir
"
prs
"
)
outDir
)
def
update_test262
(
args
)
:
    
import
subprocess
    
url
=
args
.
url
    
branch
=
args
.
branch
    
revision
=
args
.
revision
    
outDir
=
args
.
out
    
prNumber
=
args
.
pull
    
srcDir
=
args
.
local
    
if
not
os
.
path
.
isabs
(
outDir
)
:
        
outDir
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
outDir
)
    
strictTests
=
args
.
strict
    
with
TemporaryDirectory
(
)
as
inDir
:
        
if
srcDir
:
            
return
fetch_local_changes
(
inDir
outDir
srcDir
strictTests
)
        
if
revision
=
=
"
HEAD
"
:
            
subprocess
.
check_call
(
                
[
"
git
"
"
clone
"
"
-
-
depth
=
1
"
"
-
-
branch
=
%
s
"
%
branch
url
inDir
]
            
)
        
else
:
            
subprocess
.
check_call
(
                
[
"
git
"
"
clone
"
"
-
-
single
-
branch
"
"
-
-
branch
=
%
s
"
%
branch
url
inDir
]
            
)
            
subprocess
.
check_call
(
[
"
git
"
"
-
C
"
inDir
"
reset
"
"
-
-
hard
"
revision
]
)
        
if
prNumber
:
            
return
fetch_pr_files
(
inDir
outDir
prNumber
strictTests
)
        
general_update
(
inDir
outDir
strictTests
)
if
__name__
=
=
"
__main__
"
:
    
import
argparse
    
if
"
/
"
.
join
(
os
.
path
.
normpath
(
os
.
getcwd
(
)
)
.
split
(
os
.
sep
)
[
-
3
:
]
)
!
=
"
js
/
src
/
tests
"
:
        
raise
RuntimeError
(
"
%
s
must
be
run
from
js
/
src
/
tests
"
%
sys
.
argv
[
0
]
)
    
parser
=
argparse
.
ArgumentParser
(
description
=
"
Update
the
test262
test
suite
.
"
)
    
parser
.
add_argument
(
        
"
-
-
url
"
        
default
=
"
https
:
/
/
github
.
com
/
tc39
/
test262
.
git
"
        
help
=
"
URL
to
git
repository
(
default
:
%
(
default
)
s
)
"
    
)
    
parser
.
add_argument
(
        
"
-
-
branch
"
default
=
"
main
"
help
=
"
Git
branch
(
default
:
%
(
default
)
s
)
"
    
)
    
parser
.
add_argument
(
        
"
-
-
revision
"
default
=
"
HEAD
"
help
=
"
Git
revision
(
default
:
%
(
default
)
s
)
"
    
)
    
parser
.
add_argument
(
        
"
-
-
out
"
        
default
=
"
test262
"
        
help
=
"
Output
directory
.
Any
existing
directory
will
be
removed
!
"
        
"
(
default
:
%
(
default
)
s
)
"
    
)
    
parser
.
add_argument
(
        
"
-
-
pull
"
help
=
"
Import
contents
from
a
Pull
Request
specified
by
its
number
"
    
)
    
parser
.
add_argument
(
        
"
-
-
local
"
        
help
=
"
Import
new
and
modified
contents
from
a
local
folder
a
new
folder
"
        
"
will
be
created
on
local
/
branch_name
"
    
)
    
parser
.
add_argument
(
        
"
-
-
strict
"
        
default
=
False
        
action
=
"
store_true
"
        
help
=
"
Generate
additional
strict
mode
tests
.
Not
enabled
by
default
.
"
    
)
    
parser
.
set_defaults
(
func
=
update_test262
)
    
args
=
parser
.
parse_args
(
)
    
args
.
func
(
args
)
