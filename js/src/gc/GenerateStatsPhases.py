import
re
import
collections
class
PhaseKind
:
    
def
__init__
(
self
name
descr
bucket
children
=
[
]
)
:
        
self
.
name
=
name
        
self
.
descr
=
descr
        
self
.
bucket
=
bucket
        
self
.
children
=
children
AllPhaseKinds
=
[
]
PhaseKindsByName
=
dict
(
)
def
addPhaseKind
(
name
descr
bucket
children
=
[
]
)
:
    
assert
name
not
in
PhaseKindsByName
    
phaseKind
=
PhaseKind
(
name
descr
bucket
children
)
    
AllPhaseKinds
.
append
(
phaseKind
)
    
PhaseKindsByName
[
name
]
=
phaseKind
    
return
phaseKind
def
getPhaseKind
(
name
)
:
    
return
PhaseKindsByName
[
name
]
PhaseKindGraphRoots
=
[
    
addPhaseKind
(
"
MUTATOR
"
"
Mutator
Running
"
0
)
    
addPhaseKind
(
"
GC_BEGIN
"
"
Begin
Callback
"
1
)
    
addPhaseKind
(
        
"
EVICT_NURSERY_FOR_MAJOR_GC
"
        
"
Evict
Nursery
For
Major
GC
"
        
70
        
[
            
addPhaseKind
(
                
"
MARK_ROOTS
"
                
"
Mark
Roots
"
                
48
                
[
                    
addPhaseKind
(
"
MARK_CCWS
"
"
Mark
Cross
Compartment
Wrappers
"
50
)
                    
addPhaseKind
(
"
MARK_STACK
"
"
Mark
C
and
JS
stacks
"
51
)
                    
addPhaseKind
(
"
MARK_RUNTIME_DATA
"
"
Mark
Runtime
-
wide
Data
"
52
)
                    
addPhaseKind
(
"
MARK_EMBEDDING
"
"
Mark
Embedding
"
53
)
                    
addPhaseKind
(
"
MARK_COMPARTMENTS
"
"
Mark
Compartments
"
54
)
                
]
            
)
        
]
    
)
    
addPhaseKind
(
"
WAIT_BACKGROUND_THREAD
"
"
Wait
Background
Thread
"
2
)
    
addPhaseKind
(
        
"
PREPARE
"
        
"
Prepare
For
Collection
"
        
69
        
[
            
addPhaseKind
(
"
UNMARK
"
"
Unmark
"
7
)
            
addPhaseKind
(
"
UNMARK_WEAKMAPS
"
"
Unmark
WeakMaps
"
76
)
            
addPhaseKind
(
"
BUFFER_GRAY_ROOTS
"
"
Buffer
Gray
Roots
"
49
)
            
addPhaseKind
(
"
MARK_DISCARD_CODE
"
"
Mark
Discard
Code
"
3
)
            
addPhaseKind
(
"
RELAZIFY_FUNCTIONS
"
"
Relazify
Functions
"
4
)
            
addPhaseKind
(
"
PURGE
"
"
Purge
"
5
)
            
addPhaseKind
(
"
PURGE_PROP_MAP_TABLES
"
"
Purge
PropMapTables
"
60
)
            
addPhaseKind
(
"
PURGE_SOURCE_URLS
"
"
Purge
Source
URLs
"
73
)
            
addPhaseKind
(
"
JOIN_PARALLEL_TASKS
"
"
Join
Parallel
Tasks
"
67
)
        
]
    
)
    
addPhaseKind
(
        
"
MARK
"
        
"
Mark
"
        
6
        
[
getPhaseKind
(
"
MARK_ROOTS
"
)
addPhaseKind
(
"
MARK_DELAYED
"
"
Mark
Delayed
"
8
)
]
    
)
    
addPhaseKind
(
        
"
SWEEP
"
        
"
Sweep
"
        
9
        
[
            
addPhaseKind
(
                
"
SWEEP_MARK
"
                
"
Mark
During
Sweeping
"
                
10
                
[
                    
getPhaseKind
(
"
MARK_DELAYED
"
)
                    
addPhaseKind
(
                        
"
SWEEP_MARK_INCOMING_BLACK
"
"
Mark
Incoming
Black
Pointers
"
12
                    
)
                    
addPhaseKind
(
                        
"
SWEEP_MARK_WEAK
"
                        
"
Mark
Weak
"
                        
13
                        
[
                            
getPhaseKind
(
"
MARK_DELAYED
"
)
                            
addPhaseKind
(
                                
"
SWEEP_MARK_GRAY_WEAK
"
"
Mark
Gray
and
Weak
"
16
                            
)
                        
]
                    
)
                    
addPhaseKind
(
                        
"
SWEEP_MARK_INCOMING_GRAY
"
"
Mark
Incoming
Gray
Pointers
"
14
                    
)
                    
addPhaseKind
(
"
SWEEP_MARK_GRAY
"
"
Mark
Gray
"
15
)
                
]
            
)
            
addPhaseKind
(
                
"
FINALIZE_START
"
                
"
Finalize
Start
Callbacks
"
                
17
                
[
                    
addPhaseKind
(
"
WEAK_ZONES_CALLBACK
"
"
Per
-
Slice
Weak
Callback
"
57
)
                    
addPhaseKind
(
                        
"
WEAK_COMPARTMENT_CALLBACK
"
"
Per
-
Compartment
Weak
Callback
"
58
                    
)
                
]
            
)
            
addPhaseKind
(
"
UPDATE_ATOMS_BITMAP
"
"
Sweep
Atoms
Bitmap
"
68
)
            
addPhaseKind
(
"
SWEEP_ATOMS_TABLE
"
"
Sweep
Atoms
Table
"
18
)
            
addPhaseKind
(
                
"
SWEEP_COMPARTMENTS
"
                
"
Sweep
Compartments
"
                
20
                
[
                    
addPhaseKind
(
"
SWEEP_DISCARD_CODE
"
"
Sweep
Discard
Code
"
21
)
                    
addPhaseKind
(
"
SWEEP_INNER_VIEWS
"
"
Sweep
Inner
Views
"
22
)
                    
addPhaseKind
(
                        
"
SWEEP_CC_WRAPPER
"
"
Sweep
Cross
Compartment
Wrappers
"
23
                    
)
                    
addPhaseKind
(
"
SWEEP_BASE_SHAPE
"
"
Sweep
Base
Shapes
"
24
)
                    
addPhaseKind
(
"
SWEEP_INITIAL_SHAPE
"
"
Sweep
Initial
Shapes
"
25
)
                    
addPhaseKind
(
"
SWEEP_REGEXP
"
"
Sweep
Regexps
"
28
)
                    
addPhaseKind
(
"
SWEEP_COMPRESSION
"
"
Sweep
Compression
Tasks
"
62
)
                    
addPhaseKind
(
"
SWEEP_WEAKMAPS
"
"
Sweep
WeakMaps
"
63
)
                    
addPhaseKind
(
"
SWEEP_UNIQUEIDS
"
"
Sweep
Unique
IDs
"
64
)
                    
addPhaseKind
(
                        
"
SWEEP_FINALIZATION_REGISTRIES
"
                        
"
Sweep
FinalizationRegistries
"
                        
74
                    
)
                    
addPhaseKind
(
"
SWEEP_WEAKREFS
"
"
Sweep
WeakRefs
"
75
)
                    
addPhaseKind
(
"
SWEEP_JIT_DATA
"
"
Sweep
JIT
Data
"
65
)
                    
addPhaseKind
(
"
SWEEP_WEAK_CACHES
"
"
Sweep
Weak
Caches
"
66
)
                    
addPhaseKind
(
"
SWEEP_MISC
"
"
Sweep
Miscellaneous
"
29
)
                    
getPhaseKind
(
"
JOIN_PARALLEL_TASKS
"
)
                
]
            
)
            
addPhaseKind
(
"
SWEEP_OBJECT
"
"
Sweep
Object
"
33
)
            
addPhaseKind
(
"
SWEEP_STRING
"
"
Sweep
String
"
34
)
            
addPhaseKind
(
"
SWEEP_SCRIPT
"
"
Sweep
Script
"
35
)
            
addPhaseKind
(
"
SWEEP_SCOPE
"
"
Sweep
Scope
"
59
)
            
addPhaseKind
(
"
SWEEP_REGEXP_SHARED
"
"
Sweep
RegExpShared
"
61
)
            
addPhaseKind
(
"
SWEEP_SHAPE
"
"
Sweep
Shape
"
36
)
            
addPhaseKind
(
"
SWEEP_PROP_MAP
"
"
Sweep
PropMap
"
77
)
            
addPhaseKind
(
"
FINALIZE_END
"
"
Finalize
End
Callback
"
38
)
            
addPhaseKind
(
"
DESTROY
"
"
Deallocate
"
39
)
            
getPhaseKind
(
"
JOIN_PARALLEL_TASKS
"
)
        
]
    
)
    
addPhaseKind
(
        
"
COMPACT
"
        
"
Compact
"
        
40
        
[
            
addPhaseKind
(
"
COMPACT_MOVE
"
"
Compact
Move
"
41
)
            
addPhaseKind
(
                
"
COMPACT_UPDATE
"
                
"
Compact
Update
"
                
42
                
[
                    
getPhaseKind
(
"
MARK_ROOTS
"
)
                    
addPhaseKind
(
"
COMPACT_UPDATE_CELLS
"
"
Compact
Update
Cells
"
43
)
                    
getPhaseKind
(
"
JOIN_PARALLEL_TASKS
"
)
                
]
            
)
        
]
    
)
    
addPhaseKind
(
"
DECOMMIT
"
"
Decommit
"
72
)
    
addPhaseKind
(
"
GC_END
"
"
End
Callback
"
44
)
    
addPhaseKind
(
        
"
MINOR_GC
"
        
"
All
Minor
GCs
"
        
45
        
[
            
getPhaseKind
(
"
MARK_ROOTS
"
)
        
]
    
)
    
addPhaseKind
(
        
"
EVICT_NURSERY
"
        
"
Minor
GCs
to
Evict
Nursery
"
        
46
        
[
            
getPhaseKind
(
"
MARK_ROOTS
"
)
        
]
    
)
    
addPhaseKind
(
        
"
TRACE_HEAP
"
        
"
Trace
Heap
"
        
47
        
[
            
getPhaseKind
(
"
MARK_ROOTS
"
)
        
]
    
)
]
class
Phase
:
    
def
__init__
(
self
phaseKind
parent
)
:
        
self
.
phaseKind
=
phaseKind
        
self
.
parent
=
parent
        
self
.
depth
=
parent
.
depth
+
1
if
parent
else
0
        
self
.
children
=
[
]
        
self
.
nextSibling
=
None
        
self
.
nextInPhaseKind
=
None
        
self
.
path
=
re
.
sub
(
r
"
\
W
+
"
"
_
"
phaseKind
.
name
.
lower
(
)
)
        
if
parent
is
not
None
:
            
self
.
path
=
parent
.
path
+
"
.
"
+
self
.
path
def
expandPhases
(
)
:
    
phases
=
[
]
    
phasesForKind
=
collections
.
defaultdict
(
list
)
    
def
traverse
(
phaseKind
parent
)
:
        
ep
=
Phase
(
phaseKind
parent
)
        
phases
.
append
(
ep
)
        
if
phasesForKind
[
phaseKind
]
:
            
phasesForKind
[
phaseKind
]
[
-
1
]
.
nextInPhaseKind
=
ep
        
phasesForKind
[
phaseKind
]
.
append
(
ep
)
        
for
child
in
phaseKind
.
children
:
            
child_ep
=
traverse
(
child
ep
)
            
if
ep
.
children
:
                
ep
.
children
[
-
1
]
.
nextSibling
=
child_ep
            
ep
.
children
.
append
(
child_ep
)
        
return
ep
    
for
phaseKind
in
PhaseKindGraphRoots
:
        
traverse
(
phaseKind
None
)
    
return
phases
phasesForKind
AllPhases
PhasesForPhaseKind
=
expandPhases
(
)
for
phaseKind
in
AllPhaseKinds
:
    
phases
=
PhasesForPhaseKind
[
phaseKind
]
    
if
len
(
phases
)
=
=
1
:
        
phases
[
0
]
.
name
=
"
%
s
"
%
phaseKind
.
name
    
else
:
        
for
index
phase
in
enumerate
(
phases
)
:
            
phase
.
name
=
"
%
s_
%
d
"
%
(
phaseKind
.
name
index
+
1
)
MaxPhaseNesting
=
max
(
phase
.
depth
for
phase
in
AllPhases
)
+
1
MaxBucket
=
max
(
kind
.
bucket
for
kind
in
AllPhaseKinds
)
def
writeList
(
out
items
)
:
    
if
items
:
        
out
.
write
(
"
\
n
"
.
join
(
"
"
+
item
for
item
in
items
)
+
"
\
n
"
)
def
writeEnumClass
(
out
name
type
items
extraItems
)
:
    
items
=
[
"
FIRST
"
]
+
list
(
items
)
+
[
"
LIMIT
"
]
+
list
(
extraItems
)
    
items
[
1
]
+
=
"
=
"
+
items
[
0
]
    
out
.
write
(
"
enum
class
%
s
:
%
s
{
\
n
"
%
(
name
type
)
)
    
writeList
(
out
items
)
    
out
.
write
(
"
}
;
\
n
"
)
def
generateHeader
(
out
)
:
    
phaseKindNames
=
map
(
lambda
phaseKind
:
phaseKind
.
name
AllPhaseKinds
)
    
extraPhaseKinds
=
[
        
"
NONE
=
LIMIT
"
        
"
EXPLICIT_SUSPENSION
=
LIMIT
"
        
"
IMPLICIT_SUSPENSION
"
    
]
    
writeEnumClass
(
out
"
PhaseKind
"
"
uint8_t
"
phaseKindNames
extraPhaseKinds
)
    
out
.
write
(
"
\
n
"
)
    
phaseNames
=
map
(
lambda
phase
:
phase
.
name
AllPhases
)
    
extraPhases
=
[
"
NONE
=
LIMIT
"
"
EXPLICIT_SUSPENSION
=
LIMIT
"
"
IMPLICIT_SUSPENSION
"
]
    
writeEnumClass
(
out
"
Phase
"
"
uint8_t
"
phaseNames
extraPhases
)
    
out
.
write
(
"
\
n
"
)
    
out
.
write
(
"
static
const
size_t
MAX_PHASE_NESTING
=
%
d
;
\
n
"
%
MaxPhaseNesting
)
def
generateCpp
(
out
)
:
    
out
.
write
(
"
static
constexpr
PhaseKindTable
phaseKinds
=
{
\
n
"
)
    
for
phaseKind
in
AllPhaseKinds
:
        
phase
=
PhasesForPhaseKind
[
phaseKind
]
[
0
]
        
out
.
write
(
            
'
/
*
PhaseKind
:
:
%
s
*
/
PhaseKindInfo
{
Phase
:
:
%
s
%
d
"
%
s
"
}
\
n
'
            
%
(
phaseKind
.
name
phase
.
name
phaseKind
.
bucket
phaseKind
.
name
)
        
)
    
out
.
write
(
"
}
;
\
n
"
)
    
out
.
write
(
"
\
n
"
)
    
def
name
(
phase
)
:
        
return
"
Phase
:
:
"
+
phase
.
name
if
phase
else
"
Phase
:
:
NONE
"
    
out
.
write
(
"
static
constexpr
PhaseTable
phases
=
{
\
n
"
)
    
for
phase
in
AllPhases
:
        
firstChild
=
phase
.
children
[
0
]
if
phase
.
children
else
None
        
phaseKind
=
phase
.
phaseKind
        
out
.
write
(
            
'
/
*
%
s
*
/
PhaseInfo
{
%
s
%
s
%
s
%
s
PhaseKind
:
:
%
s
%
d
"
%
s
"
"
%
s
"
}
\
n
'
            
%
(
                
name
(
phase
)
                
name
(
phase
.
parent
)
                
name
(
firstChild
)
                
name
(
phase
.
nextSibling
)
                
name
(
phase
.
nextInPhaseKind
)
                
phaseKind
.
name
                
phase
.
depth
                
phaseKind
.
descr
                
phase
.
path
            
)
        
)
    
out
.
write
(
"
}
;
\
n
"
)
    
out
.
write
(
"
/
/
The
next
available
phase
kind
number
is
:
%
d
\
n
"
%
(
MaxBucket
+
1
)
)
