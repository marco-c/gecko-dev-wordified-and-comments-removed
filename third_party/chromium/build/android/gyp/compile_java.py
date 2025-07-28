import
functools
import
logging
import
multiprocessing
import
optparse
import
os
import
re
import
shutil
import
sys
import
time
import
zipfile
import
javac_output_processor
from
util
import
build_utils
from
util
import
md5_check
from
util
import
jar_info_utils
from
util
import
server_utils
import
action_helpers
import
zip_helpers
_JAVAC_EXTRACTOR
=
os
.
path
.
join
(
build_utils
.
DIR_SOURCE_ROOT
'
third_party
'
                                
'
android_prebuilts
'
'
build_tools
'
'
common
'
                                
'
framework
'
'
javac_extractor
.
jar
'
)
ERRORPRONE_CHECKS_TO_APPLY
=
[
]
ERRORPRONE_WARNINGS_TO_DISABLE
=
[
    
'
InlineMeInliner
'
    
'
InvalidParam
'
    
'
InvalidLink
'
    
'
InvalidInlineTag
'
    
'
EmptyBlockTag
'
    
'
PublicConstructorForAbstractClass
'
    
'
InvalidBlockTag
'
    
'
StaticAssignmentInConstructor
'
    
'
MutablePublicArray
'
    
'
UnescapedEntity
'
    
'
NonCanonicalType
'
    
'
AlmostJavadoc
'
    
'
ReturnValueIgnored
'
    
'
InlineMeSuggester
'
    
'
DoNotClaimAnnotations
'
    
'
JavaUtilDate
'
    
'
IdentityHashMapUsage
'
    
'
UnnecessaryMethodReference
'
    
'
LongFloatConversion
'
    
'
CharacterGetNumericValue
'
    
'
ErroneousThreadPoolConstructorChecker
'
    
'
StaticMockMember
'
    
'
MissingSuperCall
'
    
'
ToStringReturnsNull
'
    
'
MalformedInlineTag
'
    
'
DoubleBraceInitialization
'
    
'
CatchAndPrintStackTrace
'
    
'
SynchronizeOnNonFinalField
'
    
'
TypeParameterUnusedInFormals
'
    
'
CatchFail
'
    
'
JUnitAmbiguousTestClass
'
    
'
DefaultCharset
'
    
'
UnrecognisedJavadocTag
'
    
'
JdkObsolete
'
    
'
FunctionalInterfaceClash
'
    
'
FutureReturnValueIgnored
'
    
'
OperatorPrecedence
'
    
'
ThreadJoinLoop
'
    
'
StringSplitter
'
    
'
ClassNewInstance
'
    
'
ClassCanBeStatic
'
    
'
FloatCast
'
    
'
ThreadLocalUsage
'
    
'
Finally
'
    
'
FragmentNotInstantiable
'
    
'
HidingField
'
    
'
IntLongMath
'
    
'
BadComparable
'
    
'
EqualsHashCode
'
    
'
TypeParameterShadowing
'
    
'
ImmutableEnumChecker
'
    
'
InputStreamSlowMultibyteRead
'
    
'
BoxedPrimitiveConstructor
'
    
'
OverrideThrowableToString
'
    
'
CollectionToArraySafeParameter
'
    
'
ObjectToString
'
    
'
UnusedMethod
'
    
'
UnusedVariable
'
    
'
UnsafeReflectiveConstructionCast
'
    
'
MixedMutabilityReturnType
'
    
'
EqualsGetClass
'
    
'
UndefinedEquals
'
    
'
ExtendingJUnitAssert
'
    
'
SystemExitOutsideMain
'
    
'
TypeParameterNaming
'
    
'
UnusedException
'
    
'
UngroupedOverloads
'
    
'
FunctionalInterfaceClash
'
    
'
InconsistentOverloads
'
    
'
SameNameButDifferent
'
    
'
UnnecessaryLambda
'
    
'
UnnecessaryAnonymousClass
'
    
'
LiteProtoToString
'
    
'
MissingSummary
'
    
'
ReturnFromVoid
'
    
'
EmptyCatch
'
    
'
BadImport
'
    
'
UseCorrectAssertInTests
'
    
'
InlineFormatString
'
    
'
DefaultPackage
'
    
'
RefersToDaggerCodegen
'
    
'
RemoveUnusedImports
'
    
'
UnnecessaryParentheses
'
    
'
UnicodeEscape
'
    
'
AlreadyChecked
'
]
ERRORPRONE_WARNINGS_TO_ENABLE
=
[
    
'
BinderIdentityRestoredDangerously
'
    
'
EmptyIf
'
    
'
EqualsBrokenForNull
'
    
'
InvalidThrows
'
    
'
LongLiteralLowerCaseSuffix
'
    
'
MultiVariableDeclaration
'
    
'
RedundantOverride
'
    
'
StaticQualifiedUsingExpression
'
    
'
StringEquality
'
    
'
TimeUnitMismatch
'
    
'
UnnecessaryStaticImport
'
    
'
UseBinds
'
    
'
WildcardImport
'
]
def
ProcessJavacOutput
(
output
target_name
)
:
  
deprecated_re
=
re
.
compile
(
r
'
Note
:
.
*
uses
?
or
overrides
?
a
deprecated
API
'
)
  
unchecked_re
=
re
.
compile
(
      
r
'
(
Note
:
.
*
uses
?
unchecked
or
unsafe
operations
.
)
'
)
  
recompile_re
=
re
.
compile
(
r
'
(
Note
:
Recompile
with
-
Xlint
:
.
*
for
details
.
)
'
)
  
def
ApplyFilters
(
line
)
:
    
return
not
(
deprecated_re
.
match
(
line
)
or
unchecked_re
.
match
(
line
)
                
or
recompile_re
.
match
(
line
)
)
  
output
=
build_utils
.
FilterReflectiveAccessJavaWarnings
(
output
)
  
if
'
Unsafe
is
internal
proprietary
API
'
in
output
:
    
output
=
re
.
sub
(
r
'
.
*
?
Unsafe
is
internal
proprietary
API
[
\
s
\
S
]
*
?
\
^
\
n
'
'
'
                    
output
)
    
output
=
re
.
sub
(
r
'
\
d
+
warnings
\
n
'
'
'
output
)
  
lines
=
(
l
for
l
in
output
.
split
(
'
\
n
'
)
if
ApplyFilters
(
l
)
)
  
output_processor
=
javac_output_processor
.
JavacOutputProcessor
(
target_name
)
  
lines
=
output_processor
.
Process
(
lines
)
  
return
'
\
n
'
.
join
(
lines
)
def
CreateJarFile
(
jar_path
                  
classes_dir
                  
service_provider_configuration_dir
=
None
                  
additional_jar_files
=
None
                  
extra_classes_jar
=
None
)
:
  
"
"
"
Zips
files
from
compilation
into
a
single
jar
.
"
"
"
  
logging
.
info
(
'
Start
creating
jar
file
:
%
s
'
jar_path
)
  
with
action_helpers
.
atomic_output
(
jar_path
)
as
f
:
    
with
zipfile
.
ZipFile
(
f
.
name
'
w
'
)
as
z
:
      
zip_helpers
.
zip_directory
(
z
classes_dir
)
      
if
service_provider_configuration_dir
:
        
config_files
=
build_utils
.
FindInDirectory
(
            
service_provider_configuration_dir
)
        
for
config_file
in
config_files
:
          
zip_path
=
os
.
path
.
relpath
(
config_file
                                     
service_provider_configuration_dir
)
          
zip_helpers
.
add_to_zip_hermetic
(
z
zip_path
src_path
=
config_file
)
      
if
additional_jar_files
:
        
for
src_path
zip_path
in
additional_jar_files
:
          
zip_helpers
.
add_to_zip_hermetic
(
z
zip_path
src_path
=
src_path
)
      
if
extra_classes_jar
:
        
path_transform
=
lambda
p
:
p
if
p
.
endswith
(
'
.
class
'
)
else
None
        
zip_helpers
.
merge_zips
(
z
[
extra_classes_jar
]
                               
path_transform
=
path_transform
)
  
logging
.
info
(
'
Completed
jar
file
:
%
s
'
jar_path
)
def
_ParsePackageAndClassNames
(
source_file
)
:
  
"
"
"
This
should
support
both
Java
and
Kotlin
files
.
"
"
"
  
package_name
=
'
'
  
class_names
=
[
]
  
with
open
(
source_file
)
as
f
:
    
for
l
in
f
:
      
l
=
re
.
sub
(
r
'
^
(
?
:
/
/
.
*
|
/
?
\
*
.
*
?
(
?
:
\
*
/
\
s
*
|
)
)
'
'
'
l
)
      
l
=
re
.
sub
(
'
(
?
:
"
.
*
?
"
)
'
'
'
l
)
      
m
=
re
.
match
(
r
'
package
\
s
+
(
.
*
?
)
(
;
|
\
s
*
)
'
l
)
      
if
m
and
not
package_name
:
        
package_name
=
m
.
group
(
1
)
      
m
=
re
.
match
(
r
'
(
?
:
\
S
.
*
?
)
?
(
?
:
class
|
?
interface
|
enum
)
\
s
+
(
.
+
?
)
\
b
'
l
)
      
if
m
:
        
class_names
.
append
(
m
.
group
(
1
)
)
  
return
package_name
class_names
def
_ProcessSourceFileForInfo
(
source_file
)
:
  
package_name
class_names
=
_ParsePackageAndClassNames
(
source_file
)
  
return
source_file
package_name
class_names
class
_InfoFileContext
:
  
"
"
"
Manages
the
creation
of
the
class
-
>
source
file
.
info
file
.
"
"
"
  
def
__init__
(
self
chromium_code
excluded_globs
)
:
    
self
.
_chromium_code
=
chromium_code
    
self
.
_excluded_globs
=
excluded_globs
    
self
.
_srcjar_files
=
{
}
    
self
.
_results
=
[
]
    
self
.
_pool
=
None
  
def
AddSrcJarSources
(
self
srcjar_path
extracted_paths
parent_dir
)
:
    
for
path
in
extracted_paths
:
      
self
.
_srcjar_files
[
path
]
=
'
{
}
/
{
}
'
.
format
(
          
srcjar_path
os
.
path
.
relpath
(
path
parent_dir
)
)
  
def
SubmitFiles
(
self
source_files
)
:
    
if
not
source_files
:
      
return
    
if
self
.
_pool
is
None
:
      
self
.
_pool
=
multiprocessing
.
Pool
(
1
)
    
logging
.
info
(
'
Submitting
%
d
files
for
info
'
len
(
source_files
)
)
    
self
.
_results
.
append
(
        
self
.
_pool
.
imap_unordered
(
_ProcessSourceFileForInfo
                                  
source_files
                                  
chunksize
=
1000
)
)
  
def
_CheckPathMatchesClassName
(
self
source_file
package_name
class_name
)
:
    
if
source_file
.
endswith
(
'
.
java
'
)
:
      
parts
=
package_name
.
split
(
'
.
'
)
+
[
class_name
+
'
.
java
'
]
    
else
:
      
parts
=
package_name
.
split
(
'
.
'
)
+
[
class_name
+
'
.
kt
'
]
    
expected_suffix
=
os
.
path
.
sep
.
join
(
parts
)
    
if
not
source_file
.
endswith
(
expected_suffix
)
:
      
raise
Exception
(
(
'
Source
package
+
class
name
do
not
match
its
path
.
\
n
'
                       
'
Actual
path
:
%
s
\
nExpected
path
:
%
s
'
)
%
                      
(
source_file
expected_suffix
)
)
  
def
_ProcessInfo
(
self
java_file
package_name
class_names
source
)
:
    
for
class_name
in
class_names
:
      
yield
'
{
}
.
{
}
'
.
format
(
package_name
class_name
)
      
if
'
_aidl
.
srcjar
'
in
source
:
        
continue
      
assert
not
self
.
_chromium_code
or
len
(
class_names
)
=
=
1
(
          
'
Chromium
java
files
must
only
have
one
class
:
{
}
'
.
format
(
source
)
)
      
if
self
.
_chromium_code
:
        
self
.
_CheckPathMatchesClassName
(
java_file
package_name
class_names
[
0
]
)
  
def
_ShouldIncludeInJarInfo
(
self
fully_qualified_name
)
:
    
name_as_class_glob
=
fully_qualified_name
.
replace
(
'
.
'
'
/
'
)
+
'
.
class
'
    
return
not
build_utils
.
MatchesGlob
(
name_as_class_glob
self
.
_excluded_globs
)
  
def
_Collect
(
self
)
:
    
if
self
.
_pool
is
None
:
      
return
{
}
    
ret
=
{
}
    
for
result
in
self
.
_results
:
      
for
java_file
package_name
class_names
in
result
:
        
source
=
self
.
_srcjar_files
.
get
(
java_file
java_file
)
        
for
fully_qualified_name
in
self
.
_ProcessInfo
(
java_file
package_name
                                                      
class_names
source
)
:
          
if
self
.
_ShouldIncludeInJarInfo
(
fully_qualified_name
)
:
            
ret
[
fully_qualified_name
]
=
java_file
    
return
ret
  
def
Close
(
self
)
:
    
if
self
.
_pool
is
not
None
:
      
logging
.
info
(
'
Joining
multiprocessing
.
Pool
'
)
      
self
.
_pool
.
terminate
(
)
      
self
.
_pool
.
join
(
)
      
logging
.
info
(
'
Done
.
'
)
  
def
Commit
(
self
output_path
)
:
    
"
"
"
Writes
a
.
jar
.
info
file
.
    
Maps
fully
qualified
names
for
classes
to
either
the
java
file
that
they
    
are
defined
in
or
the
path
of
the
srcjar
that
they
came
from
.
    
"
"
"
    
logging
.
info
(
'
Collecting
info
file
entries
'
)
    
entries
=
self
.
_Collect
(
)
    
logging
.
info
(
'
Writing
info
file
:
%
s
'
output_path
)
    
with
action_helpers
.
atomic_output
(
output_path
mode
=
'
wb
'
)
as
f
:
      
jar_info_utils
.
WriteJarInfoFile
(
f
entries
self
.
_srcjar_files
)
    
logging
.
info
(
'
Completed
info
file
:
%
s
'
output_path
)
def
_OnStaleMd5
(
changes
options
javac_cmd
javac_args
java_files
kt_files
)
:
  
logging
.
info
(
'
Starting
_OnStaleMd5
'
)
  
if
(
options
.
enable_errorprone
and
not
options
.
skip_build_server
      
and
server_utils
.
MaybeRunCommand
(
name
=
options
.
target_name
                                       
argv
=
sys
.
argv
                                       
stamp_file
=
options
.
jar_path
                                       
force
=
options
.
use_build_server
)
)
:
    
return
  
if
options
.
enable_kythe_annotations
:
    
if
not
os
.
environ
.
get
(
'
KYTHE_ROOT_DIRECTORY
'
)
or
\
        
not
os
.
environ
.
get
(
'
KYTHE_OUTPUT_DIRECTORY
'
)
:
      
raise
Exception
(
'
-
-
enable
-
kythe
-
annotations
requires
'
                      
'
KYTHE_ROOT_DIRECTORY
and
KYTHE_OUTPUT_DIRECTORY
'
                      
'
environment
variables
to
be
set
.
'
)
    
javac_extractor_cmd
=
build_utils
.
JavaCmd
(
)
+
[
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
api
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
code
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
file
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
util
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
main
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
tree
=
ALL
-
UNNAMED
'
        
'
-
-
add
-
exports
=
jdk
.
internal
.
opt
/
jdk
.
internal
.
opt
=
ALL
-
UNNAMED
'
        
'
-
jar
'
        
_JAVAC_EXTRACTOR
    
]
    
try
:
      
_RunCompiler
(
changes
                   
options
                   
javac_extractor_cmd
+
javac_args
                   
java_files
                   
options
.
jar_path
+
'
.
javac_extractor
'
                   
enable_partial_javac
=
False
)
    
except
build_utils
.
CalledProcessError
as
e
:
      
logging
.
error
(
'
Could
not
generate
kzip
:
%
s
'
e
)
  
intermediates_out_dir
=
None
  
jar_info_path
=
None
  
if
not
options
.
enable_errorprone
:
    
shutil
.
rmtree
(
options
.
generated_dir
True
)
    
intermediates_out_dir
=
options
.
generated_dir
    
jar_info_path
=
options
.
jar_path
+
'
.
info
'
  
try
:
    
_RunCompiler
(
changes
                 
options
                 
javac_cmd
+
javac_args
                 
java_files
                 
options
.
jar_path
                 
kt_files
=
kt_files
                 
jar_info_path
=
jar_info_path
                 
intermediates_out_dir
=
intermediates_out_dir
                 
enable_partial_javac
=
True
)
  
except
build_utils
.
CalledProcessError
as
e
:
    
sys
.
stderr
.
write
(
e
.
output
)
    
sys
.
exit
(
1
)
  
logging
.
info
(
'
Completed
all
steps
in
_OnStaleMd5
'
)
def
_RunCompiler
(
changes
                 
options
                 
javac_cmd
                 
java_files
                 
jar_path
                 
kt_files
=
None
                 
jar_info_path
=
None
                 
intermediates_out_dir
=
None
                 
enable_partial_javac
=
False
)
:
  
"
"
"
Runs
java
compiler
.
  
Args
:
    
changes
:
md5_check
.
Changes
object
.
    
options
:
Object
with
command
line
flags
.
    
javac_cmd
:
Command
to
execute
.
    
java_files
:
List
of
java
files
passed
from
command
line
.
    
jar_path
:
Path
of
output
jar
file
.
    
kt_files
:
List
of
Kotlin
files
passed
from
command
line
if
any
.
    
jar_info_path
:
Path
of
the
.
info
file
to
generate
.
        
If
None
.
info
file
will
not
be
generated
.
    
intermediates_out_dir
:
Directory
for
saving
intermediate
outputs
.
        
If
None
a
temporary
directory
is
used
.
    
enable_partial_javac
:
Enables
compiling
only
Java
files
which
have
changed
        
in
the
special
case
that
no
method
signatures
have
changed
.
This
is
        
useful
for
large
GN
targets
.
        
Not
supported
if
compiling
generates
outputs
other
than
|
jar_path
|
and
        
|
jar_info_path
|
.
  
"
"
"
  
logging
.
info
(
'
Starting
_RunCompiler
'
)
  
java_files
=
java_files
.
copy
(
)
  
java_srcjars
=
options
.
java_srcjars
  
save_info_file
=
jar_info_path
is
not
None
  
temp_dir
=
jar_path
+
'
.
staging
'
  
build_utils
.
DeleteDirectory
(
temp_dir
)
  
os
.
makedirs
(
temp_dir
)
  
info_file_context
=
None
  
try
:
    
classes_dir
=
os
.
path
.
join
(
temp_dir
'
classes
'
)
    
service_provider_configuration
=
os
.
path
.
join
(
        
temp_dir
'
service_provider_configuration
'
)
    
if
java_files
:
      
os
.
makedirs
(
classes_dir
)
      
if
enable_partial_javac
:
        
all_changed_paths_are_java
=
all
(
            
p
.
endswith
(
"
.
java
"
)
for
p
in
changes
.
IterChangedPaths
(
)
)
        
if
(
all_changed_paths_are_java
and
not
changes
.
HasStringChanges
(
)
            
and
os
.
path
.
exists
(
jar_path
)
            
and
(
jar_info_path
is
None
or
os
.
path
.
exists
(
jar_info_path
)
)
)
:
          
logging
.
info
(
'
Using
partial
javac
optimization
for
%
s
compile
'
%
                       
(
jar_path
)
)
          
java_files
=
list
(
changes
.
IterChangedPaths
(
)
)
          
java_srcjars
=
None
          
save_info_file
=
False
          
build_utils
.
ExtractAll
(
jar_path
classes_dir
pattern
=
'
*
.
class
'
)
    
if
save_info_file
:
      
info_file_context
=
_InfoFileContext
(
options
.
chromium_code
                                           
options
.
jar_info_exclude_globs
)
    
if
intermediates_out_dir
is
None
:
      
intermediates_out_dir
=
temp_dir
    
input_srcjars_dir
=
os
.
path
.
join
(
intermediates_out_dir
'
input_srcjars
'
)
    
if
java_srcjars
:
      
logging
.
info
(
'
Extracting
srcjars
to
%
s
'
input_srcjars_dir
)
      
build_utils
.
MakeDirectory
(
input_srcjars_dir
)
      
for
srcjar
in
options
.
java_srcjars
:
        
extracted_files
=
build_utils
.
ExtractAll
(
            
srcjar
no_clobber
=
True
path
=
input_srcjars_dir
pattern
=
'
*
.
java
'
)
        
java_files
.
extend
(
extracted_files
)
        
if
save_info_file
:
          
info_file_context
.
AddSrcJarSources
(
srcjar
extracted_files
                                             
input_srcjars_dir
)
      
logging
.
info
(
'
Done
extracting
srcjars
'
)
    
if
options
.
header_jar
:
      
logging
.
info
(
'
Extracting
service
provider
configs
'
)
      
build_utils
.
ExtractAll
(
options
.
header_jar
                             
no_clobber
=
True
                             
path
=
service_provider_configuration
                             
pattern
=
'
META
-
INF
/
services
/
*
'
)
      
logging
.
info
(
'
Done
extracting
service
provider
configs
'
)
    
if
save_info_file
and
java_files
:
      
info_file_context
.
SubmitFiles
(
java_files
)
      
info_file_context
.
SubmitFiles
(
kt_files
)
    
if
java_files
:
      
cmd
=
list
(
javac_cmd
)
      
cmd
+
=
[
'
-
d
'
classes_dir
]
      
if
options
.
classpath
:
        
cmd
+
=
[
'
-
classpath
'
'
:
'
.
join
(
options
.
classpath
)
]
      
java_files_rsp_path
=
os
.
path
.
join
(
temp_dir
'
files_list
.
txt
'
)
      
with
open
(
java_files_rsp_path
'
w
'
)
as
f
:
        
f
.
write
(
'
'
.
join
(
java_files
)
)
      
cmd
+
=
[
'
'
+
java_files_rsp_path
]
      
process_javac_output_partial
=
functools
.
partial
(
          
ProcessJavacOutput
target_name
=
options
.
target_name
)
      
logging
.
debug
(
'
Build
command
%
s
'
cmd
)
      
start
=
time
.
time
(
)
      
build_utils
.
CheckOutput
(
cmd
                              
print_stdout
=
options
.
chromium_code
                              
stdout_filter
=
process_javac_output_partial
                              
stderr_filter
=
process_javac_output_partial
                              
fail_on_output
=
options
.
warnings_as_errors
)
      
end
=
time
.
time
(
)
-
start
      
logging
.
info
(
'
Java
compilation
took
%
ss
'
end
)
    
CreateJarFile
(
jar_path
classes_dir
service_provider_configuration
                  
options
.
additional_jar_files
options
.
kotlin_jar_path
)
    
for
root
_
files
in
os
.
walk
(
intermediates_out_dir
)
:
      
for
subpath
in
files
:
        
p
=
os
.
path
.
join
(
root
subpath
)
        
if
'
_jni_java
/
'
in
p
and
not
p
.
endswith
(
'
Jni
.
java
'
)
:
          
os
.
unlink
(
p
)
    
if
save_info_file
:
      
info_file_context
.
Commit
(
jar_info_path
)
    
logging
.
info
(
'
Completed
all
steps
in
_RunCompiler
'
)
  
finally
:
    
if
info_file_context
:
      
info_file_context
.
Close
(
)
    
shutil
.
rmtree
(
temp_dir
)
def
_ParseOptions
(
argv
)
:
  
parser
=
optparse
.
OptionParser
(
)
  
action_helpers
.
add_depfile_arg
(
parser
)
  
parser
.
add_option
(
'
-
-
target
-
name
'
help
=
'
Fully
qualified
GN
target
name
.
'
)
  
parser
.
add_option
(
'
-
-
skip
-
build
-
server
'
                    
action
=
'
store_true
'
                    
help
=
'
Avoid
using
the
build
server
.
'
)
  
parser
.
add_option
(
'
-
-
use
-
build
-
server
'
                    
action
=
'
store_true
'
                    
help
=
'
Always
use
the
build
server
.
'
)
  
parser
.
add_option
(
      
'
-
-
java
-
srcjars
'
      
action
=
'
append
'
      
default
=
[
]
      
help
=
'
List
of
srcjars
to
include
in
compilation
.
'
)
  
parser
.
add_option
(
      
'
-
-
generated
-
dir
'
      
help
=
'
Subdirectory
within
target_gen_dir
to
place
extracted
srcjars
and
'
      
'
annotation
processor
output
for
codesearch
to
find
.
'
)
  
parser
.
add_option
(
'
-
-
classpath
'
action
=
'
append
'
help
=
'
Classpath
to
use
.
'
)
  
parser
.
add_option
(
      
'
-
-
processorpath
'
      
action
=
'
append
'
      
help
=
'
GN
list
of
jars
that
comprise
the
classpath
used
for
Annotation
'
      
'
Processors
.
'
)
  
parser
.
add_option
(
      
'
-
-
processor
-
arg
'
      
dest
=
'
processor_args
'
      
action
=
'
append
'
      
help
=
'
key
=
value
arguments
for
the
annotation
processors
.
'
)
  
parser
.
add_option
(
      
'
-
-
additional
-
jar
-
file
'
      
dest
=
'
additional_jar_files
'
      
action
=
'
append
'
      
help
=
'
Additional
files
to
package
into
jar
.
By
default
only
Java
.
class
'
      
'
files
are
packaged
into
the
jar
.
Files
should
be
specified
in
'
      
'
format
<
filename
>
:
<
path
to
be
placed
in
jar
>
.
'
)
  
parser
.
add_option
(
      
'
-
-
jar
-
info
-
exclude
-
globs
'
      
help
=
'
GN
list
of
exclude
globs
to
filter
from
generated
.
info
files
.
'
)
  
parser
.
add_option
(
      
'
-
-
chromium
-
code
'
      
type
=
'
int
'
      
help
=
'
Whether
code
being
compiled
should
be
built
with
stricter
'
      
'
warnings
for
chromium
code
.
'
)
  
parser
.
add_option
(
      
'
-
-
errorprone
-
path
'
help
=
'
Use
the
Errorprone
compiler
at
this
path
.
'
)
  
parser
.
add_option
(
      
'
-
-
enable
-
errorprone
'
      
action
=
'
store_true
'
      
help
=
'
Enable
errorprone
checks
'
)
  
parser
.
add_option
(
      
'
-
-
warnings
-
as
-
errors
'
      
action
=
'
store_true
'
      
help
=
'
Treat
all
warnings
as
errors
.
'
)
  
parser
.
add_option
(
'
-
-
jar
-
path
'
help
=
'
Jar
output
path
.
'
)
  
parser
.
add_option
(
      
'
-
-
javac
-
arg
'
      
action
=
'
append
'
      
default
=
[
]
      
help
=
'
Additional
arguments
to
pass
to
javac
.
'
)
  
parser
.
add_option
(
      
'
-
-
enable
-
kythe
-
annotations
'
      
action
=
'
store_true
'
      
help
=
'
Enable
generation
of
Kythe
kzip
used
for
codesearch
.
Ensure
'
      
'
proper
environment
variables
are
set
before
using
this
flag
.
'
)
  
parser
.
add_option
(
      
'
-
-
header
-
jar
'
      
help
=
'
This
is
the
header
jar
for
the
current
target
that
contains
'
      
'
META
-
INF
/
services
/
*
files
to
be
included
in
the
output
jar
.
'
)
  
parser
.
add_option
(
      
'
-
-
kotlin
-
jar
-
path
'
      
help
=
'
Kotlin
jar
to
be
merged
into
the
output
jar
.
This
contains
the
'
      
"
.
class
files
from
this
target
'
s
.
kt
files
.
"
)
  
options
args
=
parser
.
parse_args
(
argv
)
  
build_utils
.
CheckOptions
(
options
parser
required
=
(
'
jar_path
'
)
)
  
options
.
classpath
=
action_helpers
.
parse_gn_list
(
options
.
classpath
)
  
options
.
processorpath
=
action_helpers
.
parse_gn_list
(
options
.
processorpath
)
  
options
.
java_srcjars
=
action_helpers
.
parse_gn_list
(
options
.
java_srcjars
)
  
options
.
jar_info_exclude_globs
=
action_helpers
.
parse_gn_list
(
      
options
.
jar_info_exclude_globs
)
  
additional_jar_files
=
[
]
  
for
arg
in
options
.
additional_jar_files
or
[
]
:
    
filepath
jar_filepath
=
arg
.
split
(
'
:
'
)
    
additional_jar_files
.
append
(
(
filepath
jar_filepath
)
)
  
options
.
additional_jar_files
=
additional_jar_files
  
files
=
[
]
  
for
arg
in
args
:
    
if
arg
.
startswith
(
'
'
)
:
      
files
.
extend
(
build_utils
.
ReadSourcesList
(
arg
[
1
:
]
)
)
    
else
:
      
files
.
append
(
arg
)
  
java_files
=
[
f
for
f
in
files
if
f
.
endswith
(
'
.
java
'
)
]
  
kt_files
=
[
f
for
f
in
files
if
f
.
endswith
(
'
.
kt
'
)
]
  
return
options
java_files
kt_files
def
main
(
argv
)
:
  
build_utils
.
InitLogging
(
'
JAVAC_DEBUG
'
)
  
argv
=
build_utils
.
ExpandFileArgs
(
argv
)
  
options
java_files
kt_files
=
_ParseOptions
(
argv
)
  
javac_cmd
=
[
build_utils
.
JAVAC_PATH
]
  
javac_args
=
[
      
'
-
g
'
      
'
-
-
release
'
      
'
17
'
      
'
-
encoding
'
      
'
UTF
-
8
'
      
'
-
sourcepath
'
      
'
:
'
      
'
-
Xlint
:
-
dep
-
ann
'
      
'
-
Xlint
:
-
removal
'
      
'
-
J
-
XX
:
+
PerfDisableSharedMem
'
  
]
  
if
options
.
enable_errorprone
:
    
errorprone_flags
=
[
'
-
Xplugin
:
ErrorProne
'
]
    
errorprone_flags
+
=
[
'
-
XepAllErrorsAsWarnings
'
]
    
errorprone_flags
+
=
[
'
-
XepDisableWarningsInGeneratedCode
'
]
    
errorprone_flags
.
extend
(
'
-
Xep
:
{
}
:
OFF
'
.
format
(
x
)
                            
for
x
in
ERRORPRONE_WARNINGS_TO_DISABLE
)
    
errorprone_flags
.
extend
(
'
-
Xep
:
{
}
:
WARN
'
.
format
(
x
)
                            
for
x
in
ERRORPRONE_WARNINGS_TO_ENABLE
)
    
if
ERRORPRONE_CHECKS_TO_APPLY
:
      
errorprone_flags
+
=
[
          
'
-
XepPatchLocation
:
IN_PLACE
'
          
'
-
XepPatchChecks
:
'
+
'
'
.
join
(
ERRORPRONE_CHECKS_TO_APPLY
)
      
]
    
javac_args
+
=
[
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
api
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
file
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
main
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
model
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
parser
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
processing
=
'
        
'
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
tree
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
exports
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
util
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
opens
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
code
=
ALL
-
UNNAMED
'
        
'
-
J
-
-
add
-
opens
=
jdk
.
compiler
/
com
.
sun
.
tools
.
javac
.
comp
=
ALL
-
UNNAMED
'
    
]
    
javac_args
+
=
[
'
-
XDcompilePolicy
=
simple
'
'
'
.
join
(
errorprone_flags
)
]
    
if
not
ERRORPRONE_CHECKS_TO_APPLY
:
      
javac_args
+
=
[
'
-
XDshould
-
stop
.
ifNoError
=
FLOW
'
]
  
javac_args
.
extend
(
[
'
-
proc
:
none
'
]
)
  
if
options
.
processorpath
:
    
javac_args
.
extend
(
[
'
-
processorpath
'
'
:
'
.
join
(
options
.
processorpath
)
]
)
  
if
options
.
processor_args
:
    
for
arg
in
options
.
processor_args
:
      
javac_args
.
extend
(
[
'
-
A
%
s
'
%
arg
]
)
  
javac_args
.
extend
(
options
.
javac_arg
)
  
classpath_inputs
=
options
.
classpath
+
options
.
processorpath
  
depfile_deps
=
classpath_inputs
  
input_paths
=
(
[
build_utils
.
JAVAC_PATH
]
+
depfile_deps
+
                 
options
.
java_srcjars
+
java_files
+
kt_files
)
  
if
options
.
header_jar
:
    
input_paths
.
append
(
options
.
header_jar
)
  
input_paths
+
=
[
x
[
0
]
for
x
in
options
.
additional_jar_files
]
  
output_paths
=
[
options
.
jar_path
]
  
if
not
options
.
enable_errorprone
:
    
output_paths
+
=
[
options
.
jar_path
+
'
.
info
'
]
  
input_strings
=
(
javac_cmd
+
javac_args
+
options
.
classpath
+
java_files
+
                   
kt_files
+
                   
[
options
.
warnings_as_errors
options
.
jar_info_exclude_globs
]
)
  
md5_check
.
CallAndWriteDepfileIfStale
(
lambda
changes
:
_OnStaleMd5
(
      
changes
options
javac_cmd
javac_args
java_files
kt_files
)
                                       
options
                                       
depfile_deps
=
depfile_deps
                                       
input_paths
=
input_paths
                                       
input_strings
=
input_strings
                                       
output_paths
=
output_paths
                                       
pass_changes
=
True
)
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
sys
.
argv
[
1
:
]
)
)
