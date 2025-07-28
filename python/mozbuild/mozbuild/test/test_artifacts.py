from
unittest
import
TestCase
mock
import
buildconfig
import
mozunit
from
mozbuild
.
artifacts
import
(
    
ArtifactJob
    
GeckoJobConfiguration
    
ThunderbirdJobConfiguration
)
class
FakeArtifactJob
(
ArtifactJob
)
:
    
package_re
=
r
"
"
    
job_configuration
=
GeckoJobConfiguration
class
TestArtifactJob
(
TestCase
)
:
    
def
_assert_candidate_trees
(
self
version_display
expected_trees
)
:
        
with
mock
.
patch
.
object
(
            
buildconfig
"
substs
"
{
"
MOZ_APP_VERSION_DISPLAY
"
:
version_display
}
        
)
:
            
job
=
FakeArtifactJob
(
)
            
self
.
assertGreater
(
len
(
job
.
candidate_trees
)
0
)
            
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
    
def
test_candidate_trees_with_empty_file
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
"
            
expected_trees
=
GeckoJobConfiguration
.
default_candidate_trees
        
)
    
def
test_candidate_trees_with_beta_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
92
.
1b2
"
            
expected_trees
=
GeckoJobConfiguration
.
beta_candidate_trees
        
)
    
def
test_candidate_trees_with_esr_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
91
.
3
.
0esr
"
            
expected_trees
=
GeckoJobConfiguration
.
esr_candidate_trees
        
)
    
def
test_candidate_trees_with_nightly_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
95
.
0a1
"
            
expected_trees
=
GeckoJobConfiguration
.
nightly_candidate_trees
        
)
    
def
test_candidate_trees_with_release_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
93
.
0
.
1
"
            
expected_trees
=
GeckoJobConfiguration
.
default_candidate_trees
        
)
    
def
test_candidate_trees_with_newline_before_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
\
n
\
n91
.
3
.
0esr
"
            
expected_trees
=
GeckoJobConfiguration
.
esr_candidate_trees
        
)
    
def
test_property_is_cached
(
self
)
:
        
job
=
FakeArtifactJob
(
)
        
expected_trees
=
GeckoJobConfiguration
.
esr_candidate_trees
        
buildconfig
.
substs
[
"
MOZ_APP_VERSION_DISPLAY
"
]
=
"
91
.
3
.
0
.
esr
"
        
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
        
buildconfig
.
substs
[
"
MOZ_APP_VERSION_DISPLAY
"
]
=
"
"
        
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
class
TestThunderbirdMixin
(
TestCase
)
:
    
def
_assert_candidate_trees
(
self
version_display
source_repo
expected_trees
)
:
        
with
mock
.
patch
.
object
(
            
buildconfig
            
"
substs
"
            
{
                
"
MOZ_APP_VERSION_DISPLAY
"
:
version_display
                
"
MOZ_SOURCE_REPO
"
:
source_repo
            
}
        
)
:
            
job
=
FakeArtifactJob
(
                
override_job_configuration
=
ThunderbirdJobConfiguration
            
)
            
self
.
assertGreater
(
len
(
job
.
candidate_trees
)
0
)
            
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
    
def
test_candidate_trees_with_beta_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
92
.
1b2
"
            
source_repo
=
"
https
:
/
/
hg
.
mozilla
.
org
/
releases
/
comm
-
beta
"
            
expected_trees
=
ThunderbirdJobConfiguration
.
beta_candidate_trees
        
)
    
def
test_candidate_trees_with_esr_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
91
.
3
.
0esr
"
            
source_repo
=
"
https
:
/
/
hg
.
mozilla
.
org
/
releases
/
comm
-
esr91
"
            
expected_trees
=
ThunderbirdJobConfiguration
.
esr_candidate_trees
        
)
    
def
test_candidate_trees_with_nightly_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
95
.
0a1
"
            
source_repo
=
"
https
:
/
/
hg
.
mozilla
.
org
/
comm
-
central
"
            
expected_trees
=
ThunderbirdJobConfiguration
.
nightly_candidate_trees
        
)
    
def
test_candidate_trees_with_release_version
(
self
)
:
        
self
.
_assert_candidate_trees
(
            
version_display
=
"
93
.
0
.
1
"
            
source_repo
=
"
https
:
/
/
hg
.
mozilla
.
org
/
releases
/
comm
-
release
"
            
expected_trees
=
ThunderbirdJobConfiguration
.
default_candidate_trees
        
)
    
def
test_property_is_cached
(
self
)
:
        
job
=
FakeArtifactJob
(
override_job_configuration
=
ThunderbirdJobConfiguration
)
        
expected_trees
=
ThunderbirdJobConfiguration
.
esr_candidate_trees
        
buildconfig
.
substs
[
"
MOZ_APP_VERSION_DISPLAY
"
]
=
"
91
.
3
.
0
.
esr
"
        
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
        
buildconfig
.
substs
[
"
MOZ_APP_VERSION_DISPLAY
"
]
=
"
"
        
self
.
assertEqual
(
job
.
candidate_trees
expected_trees
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
