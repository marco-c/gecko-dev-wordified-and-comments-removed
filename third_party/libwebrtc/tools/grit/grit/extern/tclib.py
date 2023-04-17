from
__future__
import
print_function
from
grit
.
extern
import
FP
def
GenerateMessageId
(
message
meaning
=
'
'
)
:
  
fp
=
FP
.
FingerPrint
(
message
)
  
if
meaning
:
    
fp2
=
FP
.
FingerPrint
(
meaning
)
    
if
fp
<
0
:
      
fp
=
fp2
+
(
fp
<
<
1
)
+
1
    
else
:
      
fp
=
fp2
+
(
fp
<
<
1
)
  
return
str
(
fp
&
0x7fffffffffffffff
)
class
MessageTranslationError
(
Exception
)
:
  
def
__init__
(
self
args
=
'
'
)
:
    
self
.
args
=
args
class
Placeholder
(
object
)
:
  
def
__str__
(
self
)
:
    
return
'
%
s
"
%
s
"
"
%
s
"
'
%
\
           
(
self
.
__presentation
self
.
__original
self
.
__example
)
  
def
GetOriginal
(
self
)
:
    
return
self
.
__original
  
def
GetPresentation
(
self
)
:
    
return
self
.
__presentation
  
def
GetExample
(
self
)
:
    
return
self
.
__example
  
def
__eq__
(
self
other
)
:
    
return
self
.
EqualTo
(
other
strict
=
1
ignore_trailing_spaces
=
0
)
  
def
EqualTo
(
self
other
strict
=
1
ignore_trailing_spaces
=
1
)
:
    
if
type
(
other
)
is
not
Placeholder
:
      
return
0
    
if
StringEquals
(
self
.
__presentation
other
.
__presentation
                    
ignore_trailing_spaces
)
:
      
if
not
strict
or
(
StringEquals
(
self
.
__original
other
.
__original
                                     
ignore_trailing_spaces
)
and
                        
StringEquals
(
self
.
__example
other
.
__example
                                     
ignore_trailing_spaces
)
)
:
        
return
1
    
return
0
class
BaseMessage
(
object
)
:
  
def
__eq__
(
self
other
)
:
    
return
_ObjectEquals
(
self
other
[
'
_BaseMessage__source_encoding
'
]
)
  
def
GetName
(
self
)
:
    
return
self
.
__name
  
def
GetSourceEncoding
(
self
)
:
    
return
self
.
__source_encoding
  
def
AppendPlaceholder
(
self
placeholder
)
:
    
if
not
isinstance
(
placeholder
Placeholder
)
:
      
raise
MessageTranslationError
(
"
Invalid
message
placeholder
%
s
in
"
                                    
"
message
%
s
"
%
(
placeholder
self
.
GetId
(
)
)
)
    
for
other
in
self
.
GetPlaceholders
(
)
:
      
if
placeholder
.
GetPresentation
(
)
=
=
other
.
GetPresentation
(
)
:
        
if
not
placeholder
.
EqualTo
(
other
)
:
          
raise
MessageTranslationError
(
              
"
Conflicting
declarations
of
%
s
within
message
"
%
              
placeholder
.
GetPresentation
(
)
)
    
dup
=
0
    
for
item
in
self
.
__content
:
      
if
isinstance
(
item
Placeholder
)
and
placeholder
.
EqualTo
(
item
)
:
        
dup
=
1
        
break
    
if
not
dup
:
      
self
.
__placeholders
.
append
(
placeholder
)
    
self
.
__content
.
append
(
placeholder
)
  
def
Strip
(
self
)
:
    
leading
=
trailing
=
'
'
    
if
len
(
self
.
__content
)
>
0
:
      
s0
=
self
.
__content
[
0
]
      
if
not
isinstance
(
s0
Placeholder
)
:
        
s
=
s0
.
lstrip
(
)
        
leading
=
s0
[
:
-
len
(
s
)
]
        
self
.
__content
[
0
]
=
s
      
s0
=
self
.
__content
[
-
1
]
      
if
not
isinstance
(
s0
Placeholder
)
:
        
s
=
s0
.
rstrip
(
)
        
trailing
=
s0
[
len
(
s
)
:
]
        
self
.
__content
[
-
1
]
=
s
    
return
leading
trailing
  
def
GetId
(
self
)
:
    
if
self
.
__id
is
None
:
      
return
self
.
GenerateId
(
)
    
return
self
.
__id
  
def
SetId
(
self
id
)
:
    
if
id
is
None
:
      
self
.
__id
=
None
    
else
:
      
self
.
__id
=
str
(
id
)
  
def
GetContent
(
self
)
:
    
return
self
.
__content
  
def
GetPresentableContent
(
self
)
:
    
presentable_content
=
"
"
    
for
item
in
self
.
__content
:
      
if
isinstance
(
item
Placeholder
)
:
        
presentable_content
+
=
item
.
GetPresentation
(
)
      
else
:
        
presentable_content
+
=
item
    
return
presentable_content
  
def
EscapeFragment
(
self
fragment
)
:
    
return
fragment
.
replace
(
'
%
'
'
%
%
'
)
  
def
GetOriginalContent
(
self
source_msg
=
None
)
:
    
original_content
=
"
"
    
for
item
in
self
.
__content
:
      
if
isinstance
(
item
Placeholder
)
:
        
if
source_msg
:
          
ph
=
source_msg
.
GetPlaceholder
(
item
.
GetPresentation
(
)
)
          
if
not
ph
:
            
raise
MessageTranslationError
(
                
"
Placeholder
%
s
doesn
'
t
exist
in
message
:
%
s
"
%
                
(
item
.
GetPresentation
(
)
source_msg
)
)
          
original_content
+
=
ph
.
GetOriginal
(
)
        
else
:
          
original_content
+
=
item
.
GetOriginal
(
)
      
else
:
        
original_content
+
=
self
.
EscapeFragment
(
item
)
    
return
original_content
  
def
GetExampleContent
(
self
)
:
    
example_content
=
"
"
    
for
item
in
self
.
__content
:
      
if
isinstance
(
item
Placeholder
)
:
        
example_content
+
=
item
.
GetExample
(
)
      
else
:
        
example_content
+
=
item
    
return
example_content
  
def
GetPlaceholders
(
self
)
:
    
return
self
.
__placeholders
  
def
GetPlaceholder
(
self
presentation
)
:
    
for
item
in
self
.
__content
:
      
if
(
isinstance
(
item
Placeholder
)
and
          
item
.
GetPresentation
(
)
=
=
presentation
)
:
        
return
item
    
return
None
  
def
GetDescription
(
self
)
:
    
return
self
.
__description
  
def
AddSource
(
self
source
)
:
    
self
.
__sources
.
append
(
source
)
  
def
GetSources
(
self
)
:
    
return
self
.
__sources
  
def
GetSourcesAsText
(
self
delimiter
=
"
;
"
)
:
    
return
delimiter
.
join
(
self
.
__sources
)
  
def
SetObsolete
(
self
)
:
    
self
.
__obsolete
=
1
  
def
IsObsolete
(
self
)
:
    
return
self
.
__obsolete
  
def
GetSequenceNumber
(
self
)
:
    
return
self
.
__sequence_number
  
def
SetSequenceNumber
(
self
number
)
:
    
self
.
__sequence_number
=
number
  
def
AddInstance
(
self
)
:
    
self
.
__num_instances
+
=
1
  
def
GetNumInstances
(
self
)
:
    
return
self
.
__num_instances
  
def
GetErrors
(
self
from_tc
=
0
)
:
    
"
"
"
    
Returns
a
description
of
the
problem
if
the
message
is
not
    
syntactically
valid
or
None
if
everything
is
fine
.
    
Args
:
      
from_tc
:
indicates
whether
this
message
came
from
the
TC
.
We
let
      
the
TC
get
away
with
some
things
we
normally
wouldn
'
t
allow
for
      
historical
reasons
.
    
"
"
"
    
pos
=
0
    
phs
=
{
}
    
for
item
in
self
.
__content
:
      
if
isinstance
(
item
Placeholder
)
:
        
phs
[
pos
]
=
item
        
pos
+
=
len
(
item
.
GetPresentation
(
)
)
      
else
:
        
pos
+
=
len
(
item
)
    
presentation
=
self
.
GetPresentableContent
(
)
    
for
ph
in
self
.
GetPlaceholders
(
)
:
      
for
pos
in
FindOverlapping
(
presentation
ph
.
GetPresentation
(
)
)
:
        
other_ph
=
phs
.
get
(
pos
)
        
if
(
(
not
other_ph
             
and
not
IsSubstringInPlaceholder
(
pos
len
(
ph
.
GetPresentation
(
)
)
phs
)
)
            
or
            
(
other_ph
and
len
(
other_ph
.
GetPresentation
(
)
)
<
len
(
ph
.
GetPresentation
(
)
)
)
)
:
          
return
"
message
contains
placeholder
name
'
%
s
'
:
\
n
%
s
"
%
(
            
ph
.
GetPresentation
(
)
presentation
)
    
return
None
  
def
__CopyTo
(
self
other
)
:
    
"
"
"
    
Returns
a
copy
of
this
BaseMessage
.
    
"
"
"
    
assert
isinstance
(
other
self
.
__class__
)
or
isinstance
(
self
other
.
__class__
)
    
other
.
__source_encoding
=
self
.
__source_encoding
    
other
.
__content
=
self
.
__content
[
:
]
    
other
.
__description
=
self
.
__description
    
other
.
__id
=
self
.
__id
    
other
.
__num_instances
=
self
.
__num_instances
    
other
.
__obsolete
=
self
.
__obsolete
    
other
.
__name
=
self
.
__name
    
other
.
__placeholders
=
self
.
__placeholders
[
:
]
    
other
.
__sequence_number
=
self
.
__sequence_number
    
other
.
__sources
=
self
.
__sources
[
:
]
    
return
other
  
def
HasText
(
self
)
:
    
"
"
"
Returns
true
iff
this
message
has
anything
other
than
placeholders
.
"
"
"
    
for
item
in
self
.
__content
:
      
if
not
isinstance
(
item
Placeholder
)
:
        
return
True
    
return
False
class
Message
(
BaseMessage
)
:
  
def
__init__
(
self
source_encoding
text
=
None
id
=
None
               
description
=
None
meaning
=
"
"
placeholders
=
None
               
source
=
None
sequence_number
=
0
clone_from
=
None
               
time_created
=
0
name
=
None
is_hidden
=
0
)
:
    
if
clone_from
is
not
None
:
      
BaseMessage
.
__init__
(
self
None
clone_from
=
clone_from
)
      
self
.
__meaning
=
clone_from
.
__meaning
      
self
.
__time_created
=
clone_from
.
__time_created
      
self
.
__is_hidden
=
clone_from
.
__is_hidden
      
return
    
BaseMessage
.
__init__
(
self
source_encoding
text
id
description
                         
placeholders
source
sequence_number
                         
name
=
name
)
    
self
.
__meaning
=
meaning
    
self
.
__time_created
=
time_created
    
self
.
SetIsHidden
(
is_hidden
)
  
def
__str__
(
self
)
:
    
s
=
'
source
:
%
s
id
:
%
s
content
:
"
%
s
"
meaning
:
"
%
s
"
'
\
        
'
description
:
"
%
s
"
'
%
\
        
(
self
.
GetSourcesAsText
(
)
self
.
GetId
(
)
self
.
GetPresentableContent
(
)
         
self
.
__meaning
self
.
GetDescription
(
)
)
    
if
self
.
GetName
(
)
is
not
None
:
      
s
+
=
'
name
:
"
%
s
"
'
%
self
.
GetName
(
)
    
placeholders
=
self
.
GetPlaceholders
(
)
    
for
i
in
range
(
len
(
placeholders
)
)
:
      
s
+
=
"
placeholder
[
%
d
]
:
%
s
"
%
(
i
placeholders
[
i
]
)
    
return
s
  
def
Strip
(
self
)
:
    
leading
=
trailing
=
'
'
    
content
=
self
.
GetContent
(
)
    
if
len
(
content
)
>
0
:
      
s0
=
content
[
0
]
      
if
not
isinstance
(
s0
Placeholder
)
:
        
s
=
s0
.
lstrip
(
)
        
leading
=
s0
[
:
-
len
(
s
)
]
        
content
[
0
]
=
s
      
s0
=
content
[
-
1
]
      
if
not
isinstance
(
s0
Placeholder
)
:
        
s
=
s0
.
rstrip
(
)
        
trailing
=
s0
[
len
(
s
)
:
]
        
content
[
-
1
]
=
s
    
return
leading
trailing
  
def
GenerateId
(
self
)
:
    
self
.
SetId
(
GenerateMessageId
(
self
.
GetPresentableContent
(
)
                                 
self
.
__meaning
)
)
    
return
self
.
GetId
(
)
  
def
GetMeaning
(
self
)
:
    
return
self
.
__meaning
  
def
GetTimeCreated
(
self
)
:
    
return
self
.
__time_created
  
def
EqualTo
(
self
other
strict
=
1
)
:
    
if
self
.
GetId
(
)
!
=
other
.
GetId
(
)
:
      
return
0
    
if
self
.
__meaning
!
=
other
.
__meaning
:
      
return
0
    
if
self
.
GetPresentableContent
(
)
!
=
other
.
GetPresentableContent
(
)
:
      
return
0
    
if
(
strict
and
        
self
.
GetDescription
(
)
is
not
None
and
        
other
.
GetDescription
(
)
is
not
None
and
        
self
.
GetDescription
(
)
!
=
other
.
GetDescription
(
)
)
:
      
return
0
    
ph1
=
self
.
GetPlaceholders
(
)
    
ph2
=
other
.
GetPlaceholders
(
)
    
if
len
(
ph1
)
!
=
len
(
ph2
)
:
      
return
0
    
for
i
in
range
(
len
(
ph1
)
)
:
      
if
not
ph1
[
i
]
.
EqualTo
(
ph2
[
i
]
strict
)
:
        
return
0
    
return
1
  
def
Copy
(
self
)
:
    
"
"
"
    
Returns
a
copy
of
this
Message
.
    
"
"
"
    
assert
isinstance
(
self
Message
)
    
return
Message
(
None
clone_from
=
self
)
  
def
SetIsHidden
(
self
is_hidden
)
:
    
"
"
"
Sets
whether
this
message
should
be
hidden
.
    
Args
:
      
is_hidden
:
0
or
1
-
if
the
message
should
be
hidden
0
otherwise
    
"
"
"
    
if
is_hidden
not
in
[
0
1
]
:
      
raise
MessageTranslationError
(
"
is_hidden
must
be
0
or
1
got
%
s
"
)
    
self
.
__is_hidden
=
is_hidden
  
def
IsHidden
(
self
)
:
    
"
"
"
Returns
1
if
this
message
is
hidden
and
0
otherwise
.
"
"
"
    
return
self
.
__is_hidden
class
Translation
(
BaseMessage
)
:
  
def
__init__
(
self
source_encoding
text
=
None
id
=
None
               
description
=
None
placeholders
=
None
source
=
None
               
sequence_number
=
0
clone_from
=
None
ignore_ph_errors
=
0
               
name
=
None
)
:
    
if
clone_from
is
not
None
:
      
BaseMessage
.
__init__
(
self
None
clone_from
=
clone_from
)
      
return
    
BaseMessage
.
__init__
(
self
source_encoding
text
id
description
                         
placeholders
source
sequence_number
                         
ignore_ph_errors
=
ignore_ph_errors
name
=
name
)
  
def
__str__
(
self
)
:
    
s
=
'
source
:
%
s
id
:
%
s
content
:
"
%
s
"
description
:
"
%
s
"
'
%
\
        
(
self
.
GetSourcesAsText
(
)
self
.
GetId
(
)
self
.
GetPresentableContent
(
)
         
self
.
GetDescription
(
)
)
;
    
placeholders
=
self
.
GetPlaceholders
(
)
    
for
i
in
range
(
len
(
placeholders
)
)
:
      
s
+
=
"
placeholder
[
%
d
]
:
%
s
"
%
(
i
placeholders
[
i
]
)
    
return
s
  
def
EqualTo
(
self
other
strict
=
1
)
:
    
if
self
.
GetId
(
)
!
=
other
.
GetId
(
)
:
      
return
0
    
if
self
.
GetPresentableContent
(
)
!
=
other
.
GetPresentableContent
(
)
:
      
return
0
    
ph1
=
self
.
GetPlaceholders
(
)
    
ph2
=
other
.
GetPlaceholders
(
)
    
if
len
(
ph1
)
!
=
len
(
ph2
)
:
      
return
0
    
for
i
in
range
(
len
(
ph1
)
)
:
      
if
not
ph1
[
i
]
.
EqualTo
(
ph2
[
i
]
strict
)
:
        
return
0
    
return
1
  
def
Copy
(
self
)
:
    
"
"
"
    
Returns
a
copy
of
this
Translation
.
    
"
"
"
    
return
Translation
(
None
clone_from
=
self
)
