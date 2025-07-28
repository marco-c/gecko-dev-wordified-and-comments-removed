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
  
def
_Archive
(
self
)
:
    
pass
