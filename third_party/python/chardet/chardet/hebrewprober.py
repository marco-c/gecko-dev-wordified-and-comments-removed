from
.
charsetprober
import
CharSetProber
from
.
enums
import
ProbingState
class
HebrewProber
(
CharSetProber
)
:
    
FINAL_KAF
=
0xea
    
NORMAL_KAF
=
0xeb
    
FINAL_MEM
=
0xed
    
NORMAL_MEM
=
0xee
    
FINAL_NUN
=
0xef
    
NORMAL_NUN
=
0xf0
    
FINAL_PE
=
0xf3
    
NORMAL_PE
=
0xf4
    
FINAL_TSADI
=
0xf5
    
NORMAL_TSADI
=
0xf6
    
MIN_FINAL_CHAR_DISTANCE
=
5
    
MIN_MODEL_DISTANCE
=
0
.
01
    
VISUAL_HEBREW_NAME
=
"
ISO
-
8859
-
8
"
    
LOGICAL_HEBREW_NAME
=
"
windows
-
1255
"
    
def
__init__
(
self
)
:
        
super
(
HebrewProber
self
)
.
__init__
(
)
        
self
.
_final_char_logical_score
=
None
        
self
.
_final_char_visual_score
=
None
        
self
.
_prev
=
None
        
self
.
_before_prev
=
None
        
self
.
_logical_prober
=
None
        
self
.
_visual_prober
=
None
        
self
.
reset
(
)
    
def
reset
(
self
)
:
        
self
.
_final_char_logical_score
=
0
        
self
.
_final_char_visual_score
=
0
        
self
.
_prev
=
'
'
        
self
.
_before_prev
=
'
'
    
def
set_model_probers
(
self
logicalProber
visualProber
)
:
        
self
.
_logical_prober
=
logicalProber
        
self
.
_visual_prober
=
visualProber
    
def
is_final
(
self
c
)
:
        
return
c
in
[
self
.
FINAL_KAF
self
.
FINAL_MEM
self
.
FINAL_NUN
                     
self
.
FINAL_PE
self
.
FINAL_TSADI
]
    
def
is_non_final
(
self
c
)
:
        
return
c
in
[
self
.
NORMAL_KAF
self
.
NORMAL_MEM
                     
self
.
NORMAL_NUN
self
.
NORMAL_PE
]
    
def
feed
(
self
byte_str
)
:
        
if
self
.
state
=
=
ProbingState
.
NOT_ME
:
            
return
ProbingState
.
NOT_ME
        
byte_str
=
self
.
filter_high_byte_only
(
byte_str
)
        
for
cur
in
byte_str
:
            
if
cur
=
=
'
'
:
                
if
self
.
_before_prev
!
=
'
'
:
                    
if
self
.
is_final
(
self
.
_prev
)
:
                        
self
.
_final_char_logical_score
+
=
1
                    
elif
self
.
is_non_final
(
self
.
_prev
)
:
                        
self
.
_final_char_visual_score
+
=
1
            
else
:
                
if
(
(
self
.
_before_prev
=
=
'
'
)
and
                        
(
self
.
is_final
(
self
.
_prev
)
)
and
(
cur
!
=
'
'
)
)
:
                    
self
.
_final_char_visual_score
+
=
1
            
self
.
_before_prev
=
self
.
_prev
            
self
.
_prev
=
cur
        
return
ProbingState
.
DETECTING
    
property
    
def
charset_name
(
self
)
:
        
finalsub
=
self
.
_final_char_logical_score
-
self
.
_final_char_visual_score
        
if
finalsub
>
=
self
.
MIN_FINAL_CHAR_DISTANCE
:
            
return
self
.
LOGICAL_HEBREW_NAME
        
if
finalsub
<
=
-
self
.
MIN_FINAL_CHAR_DISTANCE
:
            
return
self
.
VISUAL_HEBREW_NAME
        
modelsub
=
(
self
.
_logical_prober
.
get_confidence
(
)
                    
-
self
.
_visual_prober
.
get_confidence
(
)
)
        
if
modelsub
>
self
.
MIN_MODEL_DISTANCE
:
            
return
self
.
LOGICAL_HEBREW_NAME
        
if
modelsub
<
-
self
.
MIN_MODEL_DISTANCE
:
            
return
self
.
VISUAL_HEBREW_NAME
        
if
finalsub
<
0
.
0
:
            
return
self
.
VISUAL_HEBREW_NAME
        
return
self
.
LOGICAL_HEBREW_NAME
    
property
    
def
language
(
self
)
:
        
return
'
Hebrew
'
    
property
    
def
state
(
self
)
:
        
if
(
self
.
_logical_prober
.
state
=
=
ProbingState
.
NOT_ME
)
and
\
           
(
self
.
_visual_prober
.
state
=
=
ProbingState
.
NOT_ME
)
:
            
return
ProbingState
.
NOT_ME
        
return
ProbingState
.
DETECTING
