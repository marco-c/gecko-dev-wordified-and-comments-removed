"
"
"
Run
Error
Prone
.
"
"
"
import
argparse
import
sys
import
compile_java
from
util
import
server_utils
ERRORPRONE_CHECKS_TO_APPLY
=
[
]
TESTONLY_ERRORPRONE_WARNINGS_TO_DISABLE
=
[
    
'
UnusedVariable
'
    
'
NoStreams
'
]
ERRORPRONE_WARNINGS_TO_DISABLE
=
[
    
'
InlineMeInliner
'
    
'
InlineMeSuggester
'
    
'
HidingField
'
    
'
AlreadyChecked
'
    
'
DirectInvocationOnMock
'
    
'
MockNotUsedInProduction
'
    
'
JdkObsolete
'
    
'
ReturnValueIgnored
'
    
'
StaticAssignmentInConstructor
'
    
'
InvalidBlockTag
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
MalformedInlineTag
'
    
'
MissingSummary
'
    
'
UnescapedEntity
'
    
'
UnrecognisedJavadocTag
'
    
'
MutablePublicArray
'
    
'
NonCanonicalType
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
StaticMockMember
'
    
'
StaticAssignmentOfThrowable
'
    
'
CatchAndPrintStackTrace
'
    
'
TypeParameterUnusedInFormals
'
    
'
DefaultCharset
'
    
'
FutureReturnValueIgnored
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
ThreadLocalUsage
'
    
'
EqualsHashCode
'
    
'
OverrideThrowableToString
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
SameNameButDifferent
'
    
'
UnnecessaryLambda
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
RefersToDaggerCodegen
'
    
'
RemoveUnusedImports
'
    
'
UnicodeEscape
'
    
'
NonApiType
'
    
'
StringCharset
'
    
'
StringCaseLocaleUsage
'
    
'
RedundantControlFlow
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
    
'
NoStreams
'
]
def
main
(
)
:
  
parser
=
argparse
.
ArgumentParser
(
)
  
parser
.
add_argument
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
add_argument
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
add_argument
(
'
-
-
testonly
'
                      
action
=
'
store_true
'
                      
help
=
'
Disable
some
Error
Prone
checks
'
)
  
parser
.
add_argument
(
'
-
-
enable
-
nullaway
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
NullAway
(
requires
-
-
enable
-
errorprone
)
'
)
  
parser
.
add_argument
(
'
-
-
stamp
'
                      
required
=
True
                      
help
=
'
Path
of
output
.
stamp
file
'
)
  
options
compile_java_argv
=
parser
.
parse_known_args
(
)
  
compile_java_argv
+
=
[
'
-
-
jar
-
path
'
options
.
stamp
]
  
if
not
options
.
skip_build_server
and
(
server_utils
.
MaybeRunCommand
(
      
name
=
options
.
stamp
      
argv
=
sys
.
argv
      
stamp_file
=
options
.
stamp
      
use_build_server
=
options
.
use_build_server
)
)
:
    
compile_java
.
main
(
compile_java_argv
write_depfile_only
=
True
)
    
return
  
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
  
if
options
.
enable_nullaway
:
    
errorprone_flags
+
=
[
'
-
XepOpt
:
NullAway
:
OnlyNullMarked
'
]
    
errorprone_flags
+
=
[
        
'
-
XepOpt
:
NullAway
:
CustomContractAnnotations
=
'
        
'
org
.
chromium
.
build
.
annotations
.
Contract
'
        
'
org
.
chromium
.
support_lib_boundary
.
util
.
Contract
'
    
]
    
errorprone_flags
+
=
[
(
'
-
XepOpt
:
NullAway
:
CastToNonNullMethod
=
'
                          
'
org
.
chromium
.
build
.
NullUtil
.
assumeNonNull
'
)
]
    
errorprone_flags
+
=
[
'
-
XepOpt
:
NullAway
:
AssertsEnabled
=
true
'
]
    
errorprone_flags
+
=
[
        
'
-
XepOpt
:
NullAway
:
AcknowledgeRestrictiveAnnotations
=
true
'
    
]
    
errorprone_flags
+
=
[
'
-
XepOpt
:
Nullaway
:
AcknowledgeAndroidRecent
=
true
'
]
    
errorprone_flags
+
=
[
'
-
XepOpt
:
NullAway
:
JSpecifyMode
=
true
'
]
    
init_methods
=
[
        
'
android
.
app
.
Application
.
onCreate
'
        
'
android
.
app
.
Activity
.
onCreate
'
        
'
android
.
app
.
Service
.
onCreate
'
        
'
android
.
app
.
backup
.
BackupAgent
.
onCreate
'
        
'
android
.
content
.
ContentProvider
.
attachInfo
'
        
'
android
.
content
.
ContentProvider
.
onCreate
'
        
'
android
.
content
.
ContextWrapper
.
attachBaseContext
'
    
]
    
errorprone_flags
+
=
[
        
'
-
XepOpt
:
NullAway
:
KnownInitializers
=
'
+
'
'
.
join
(
init_methods
)
    
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
options
.
testonly
:
    
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
TESTONLY_ERRORPRONE_WARNINGS_TO_DISABLE
)
  
if
ERRORPRONE_CHECKS_TO_APPLY
:
    
to_apply
=
list
(
ERRORPRONE_CHECKS_TO_APPLY
)
    
if
options
.
testonly
:
      
to_apply
=
[
          
x
for
x
in
to_apply
          
if
x
not
in
TESTONLY_ERRORPRONE_WARNINGS_TO_DISABLE
      
]
    
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
to_apply
)
    
]
  
javac_args
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
ifError
=
FLOW
'
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
  
compile_java
.
main
(
compile_java_argv
                    
extra_javac_args
=
javac_args
                    
use_errorprone
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
  
main
(
)
