from
pylib
.
base
import
output_manager
class
NoopOutputManager
(
output_manager
.
OutputManager
)
:
  
def
__init__
(
self
)
:
    
super
(
NoopOutputManager
self
)
.
__init__
(
)
  
def
_CreateArchivedFile
(
self
out_filename
out_subdir
datatype
)
:
    
del
out_filename
out_subdir
datatype
    
return
NoopArchivedFile
(
)
class
NoopArchivedFile
(
output_manager
.
ArchivedFile
)
:
  
def
__init__
(
self
)
:
    
super
(
NoopArchivedFile
self
)
.
__init__
(
None
None
None
)
  
def
Link
(
self
)
:
    
"
"
"
NoopArchivedFiles
are
not
retained
.
"
"
"
    
return
'
'
  
def
_Link
(
self
)
:
    
pass
  
def
Archive
(
self
)
:
    
"
"
"
NoopArchivedFiles
are
not
retained
.
"
"
"
    
pass
  
def
_Archive
(
self
)
:
    
pass
