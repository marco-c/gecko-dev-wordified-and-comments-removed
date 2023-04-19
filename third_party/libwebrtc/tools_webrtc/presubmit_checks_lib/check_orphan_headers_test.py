import
os
import
sys
import
unittest
import
check_orphan_headers
def
_GetRootBasedOnPlatform
(
)
:
    
if
sys
.
platform
.
startswith
(
'
win
'
)
:
        
return
'
C
:
\
\
'
    
else
:
        
return
'
/
'
def
_GetPath
(
*
path_chunks
)
:
    
return
os
.
path
.
join
(
_GetRootBasedOnPlatform
(
)
*
path_chunks
)
class
GetBuildGnPathFromFilePathTest
(
unittest
.
TestCase
)
:
    
def
testGetBuildGnFromSameDirectory
(
self
)
:
        
file_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
'
base
'
'
foo
.
h
'
)
        
expected_build_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
'
base
'
                                       
'
BUILD
.
gn
'
)
        
file_exists
=
lambda
p
:
p
=
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
                                              
'
base
'
'
BUILD
.
gn
'
)
        
src_dir_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
)
        
self
.
assertEqual
(
            
expected_build_path
            
check_orphan_headers
.
GetBuildGnPathFromFilePath
(
                
file_path
file_exists
src_dir_path
)
)
    
def
testGetBuildPathFromParentDirectory
(
self
)
:
        
file_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
'
base
'
'
foo
.
h
'
)
        
expected_build_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
                                       
'
BUILD
.
gn
'
)
        
file_exists
=
lambda
p
:
p
=
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
                                              
'
BUILD
.
gn
'
)
        
src_dir_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
)
        
self
.
assertEqual
(
            
expected_build_path
            
check_orphan_headers
.
GetBuildGnPathFromFilePath
(
                
file_path
file_exists
src_dir_path
)
)
    
def
testExceptionIfNoBuildGnFilesAreFound
(
self
)
:
        
with
self
.
assertRaises
(
check_orphan_headers
.
NoBuildGnFoundError
)
:
            
file_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
'
base
'
'
foo
.
h
'
)
            
file_exists
=
lambda
p
:
False
            
src_dir_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
)
            
check_orphan_headers
.
GetBuildGnPathFromFilePath
(
                
file_path
file_exists
src_dir_path
)
    
def
testExceptionIfFilePathIsNotAnHeader
(
self
)
:
        
with
self
.
assertRaises
(
check_orphan_headers
.
WrongFileTypeError
)
:
            
file_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
'
base
'
                                 
'
foo
.
cc
'
)
            
file_exists
=
lambda
p
:
False
            
src_dir_path
=
_GetPath
(
'
home
'
'
projects
'
'
webrtc
'
)
            
check_orphan_headers
.
GetBuildGnPathFromFilePath
(
                
file_path
file_exists
src_dir_path
)
class
GetHeadersInBuildGnFileSourcesTest
(
unittest
.
TestCase
)
:
    
def
testEmptyFileReturnsEmptySet
(
self
)
:
        
self
.
assertEqual
(
            
set
(
[
]
)
            
check_orphan_headers
.
GetHeadersInBuildGnFileSources
(
'
'
'
/
a
/
b
'
)
)
    
def
testReturnsSetOfHeadersFromFileContent
(
self
)
:
        
file_content
=
"
"
"
    
#
Some
comments
    
if
(
is_android
)
{
      
import
(
"
/
/
a
/
b
/
c
.
gni
"
)
      
import
(
"
/
/
d
/
e
/
f
.
gni
"
)
    
}
    
source_set
(
"
foo
"
)
{
      
sources
=
[
"
foo
.
h
"
]
      
deps
=
[
"
:
bar
"
]
    
}
    
rtc_static_library
(
"
bar
"
)
{
      
#
Public
headers
should
also
be
included
.
      
public
=
[
        
"
public_foo
.
h
"
      
]
      
sources
=
[
        
"
bar
.
h
"
        
"
bar
.
cc
"
      
]
      
deps
=
[
"
:
bar
"
]
    
}
    
source_set
(
"
baz_foo
"
)
{
      
sources
=
[
"
baz
/
foo
.
h
"
]
    
}
    
"
"
"
        
target_abs_path
=
_GetPath
(
'
a
'
'
b
'
)
        
self
.
assertEqual
(
            
set
(
[
                
_GetPath
(
'
a
'
'
b
'
'
foo
.
h
'
)
                
_GetPath
(
'
a
'
'
b
'
'
bar
.
h
'
)
                
_GetPath
(
'
a
'
'
b
'
'
public_foo
.
h
'
)
                
_GetPath
(
'
a
'
'
b
'
'
baz
'
'
foo
.
h
'
)
            
]
)
            
check_orphan_headers
.
GetHeadersInBuildGnFileSources
(
                
file_content
target_abs_path
)
)
if
__name__
=
=
'
__main__
'
:
    
unittest
.
main
(
)
