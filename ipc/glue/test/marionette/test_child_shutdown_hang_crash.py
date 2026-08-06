import
glob
import
json
import
os
from
marionette_driver
import
Wait
from
marionette_driver
.
errors
import
TimeoutException
from
marionette_harness
import
MarionetteTestCase
EXPECTED_SIGNATURE
=
"
child
process
hang
at
shutdown
"
class
TestShutdownHangCrash
(
MarionetteTestCase
)
:
    
"
"
"
End
-
to
-
end
test
for
the
deliberate
crash
of
a
child
hanging
at
shutdown
.
    
This
test
exercises
the
~
ProcessChild
hang
path
in
NS_FREE_PERMANENT_DATA
    
builds
.
    
It
verifies
that
the
CrashSignatureOverrideForTesting
annotation
propagates
    
to
the
crashed
child
'
s
report
(
so
these
crashes
group
under
a
single
    
signature
across
platforms
)
.
    
The
crash
reports
that
are
generated
for
the
purpose
of
this
test
must
be
    
flagged
intentional
so
that
they
don
'
t
get
auto
-
reported
as
test
failures
.
    
Therefore
we
also
check
for
the
presence
of
IntentionalCrashForTesting
.
"
"
"
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
)
        
self
.
_previous_env
=
os
.
environ
.
get
(
"
MOZ_TEST_CHILD_EXIT_HANG
"
)
        
os
.
environ
[
"
MOZ_TEST_CHILD_EXIT_HANG
"
]
=
"
40
"
        
self
.
marionette
.
restart
(
clean
=
False
in_app
=
False
)
    
def
tearDown
(
self
)
:
        
if
self
.
_previous_env
is
None
:
            
os
.
environ
.
pop
(
"
MOZ_TEST_CHILD_EXIT_HANG
"
None
)
        
else
:
            
os
.
environ
[
"
MOZ_TEST_CHILD_EXIT_HANG
"
]
=
self
.
_previous_env
        
super
(
)
.
tearDown
(
)
    
def
test_child_shutdown_hang_reported_uniformly
(
self
)
:
        
self
.
marionette
.
navigate
(
"
about
:
blank
"
)
        
self
.
marionette
.
quit
(
)
        
try
:
            
minidump_directory
=
os
.
path
.
join
(
self
.
marionette
.
profile_path
"
minidumps
"
)
            
extra_files
=
Wait
(
None
timeout
=
30
)
.
until
(
                
lambda
_
:
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
minidump_directory
"
*
.
extra
"
)
)
            
)
        
except
TimeoutException
:
            
extra_files
=
[
]
        
self
.
assertTrue
(
            
extra_files
            
"
Expected
at
least
one
crash
report
from
the
deliberately
hung
child
process
"
        
)
        
for
path
in
extra_files
:
            
with
open
(
path
encoding
=
"
utf
-
8
"
)
as
f
:
                
annotations
=
json
.
load
(
f
)
            
self
.
assertEqual
(
                
annotations
.
get
(
"
CrashSignatureOverrideForTesting
"
)
                
EXPECTED_SIGNATURE
                
"
The
parent
'
s
CrashSignatureOverrideForTesting
annotation
must
"
                
"
propagate
to
every
child
crash
report
"
            
)
            
self
.
assertEqual
(
                
annotations
.
get
(
"
IntentionalCrashForTesting
"
)
                
"
1
"
                
"
Every
crashed
child
must
carry
the
IntentionalCrashForTesting
"
                
"
annotation
so
the
deliberate
crash
is
not
reported
as
a
test
"
                
"
failure
"
            
)
