from
typing
import
Optional
Union
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
from
.
sbcharsetprober
import
SingleByteCharSetProber
class
HebrewProber
(
CharSetProber
)
:
    
SPACE
=
0x20
    
FINAL_KAF
=
0xEA
    
NORMAL_KAF
=
0xEB
    
FINAL_MEM
=
0xED
    
NORMAL_MEM
=
0xEE
    
FINAL_NUN
=
0xEF
    
NORMAL_NUN
=
0xF0
    
FINAL_PE
=
0xF3
    
NORMAL_PE
=
0xF4
    
FINAL_TSADI
=
0xF5
    
NORMAL_TSADI
=
0xF6
    
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
-
>
None
:
        
super
(
)
.
__init__
(
)
        
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
self
.
SPACE
        
self
.
_before_prev
=
self
.
SPACE
        
self
.
_logical_prober
:
Optional
[
SingleByteCharSetProber
]
=
None
        
self
.
_visual_prober
:
Optional
[
SingleByteCharSetProber
]
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
-
>
None
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
self
.
SPACE
        
self
.
_before_prev
=
self
.
SPACE
    
def
set_model_probers
(
        
self
        
logical_prober
:
SingleByteCharSetProber
        
visual_prober
:
SingleByteCharSetProber
    
)
-
>
None
:
        
self
.
_logical_prober
=
logical_prober
        
self
.
_visual_prober
=
visual_prober
    
def
is_final
(
self
c
:
int
)
-
>
bool
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
:
int
)
-
>
bool
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
:
Union
[
bytes
bytearray
]
)
-
>
ProbingState
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
self
.
SPACE
:
                
if
self
.
_before_prev
!
=
self
.
SPACE
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
self
.
SPACE
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
self
.
SPACE
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
-
>
str
:
        
assert
self
.
_logical_prober
is
not
None
        
assert
self
.
_visual_prober
is
not
None
        
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
-
>
str
:
        
return
"
Hebrew
"
    
property
    
def
state
(
self
)
-
>
ProbingState
:
        
assert
self
.
_logical_prober
is
not
None
        
assert
self
.
_visual_prober
is
not
None
        
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
