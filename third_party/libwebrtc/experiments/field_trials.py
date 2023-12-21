import
sys
from
typing
import
FrozenSet
import
argparse
import
dataclasses
dataclasses
.
dataclass
(
frozen
=
True
)
class
FieldTrial
:
    
"
"
"
Representation
of
all
attributes
associated
with
a
field
trial
.
    
Attributes
:
      
key
:
Field
trial
key
.
    
"
"
"
    
key
:
str
REGISTERED_FIELD_TRIALS
:
FrozenSet
[
FieldTrial
]
=
frozenset
(
[
    
FieldTrial
(
'
'
)
]
)
def
registry_header
(
        
field_trials
:
FrozenSet
[
FieldTrial
]
=
REGISTERED_FIELD_TRIALS
)
-
>
str
:
    
"
"
"
Generates
a
C
+
+
header
with
all
field
trial
keys
.
    
Args
:
      
field_trials
:
Field
trials
to
include
in
the
header
.
    
Returns
:
      
String
representation
of
a
C
+
+
header
file
containing
all
field
trial
      
keys
.
    
>
>
>
trials
=
{
FieldTrial
(
'
B
'
)
FieldTrial
(
'
A
'
)
FieldTrial
(
'
B
'
)
}
    
>
>
>
print
(
registry_header
(
trials
)
)
    
/
/
This
file
was
automatically
generated
.
Do
not
edit
.
    
<
BLANKLINE
>
    
#
ifndef
GEN_REGISTERED_FIELD_TRIALS_H_
    
#
define
GEN_REGISTERED_FIELD_TRIALS_H_
    
<
BLANKLINE
>
    
#
include
"
absl
/
strings
/
string_view
.
h
"
    
<
BLANKLINE
>
    
namespace
webrtc
{
    
<
BLANKLINE
>
    
inline
constexpr
absl
:
:
string_view
kRegisteredFieldTrials
[
]
=
{
        
"
A
"
        
"
B
"
    
}
;
    
<
BLANKLINE
>
    
}
/
/
namespace
webrtc
    
<
BLANKLINE
>
    
#
endif
/
/
GEN_REGISTERED_FIELD_TRIALS_H_
    
<
BLANKLINE
>
    
"
"
"
    
registered_keys
=
[
f
.
key
for
f
in
field_trials
]
    
keys
=
'
\
n
'
.
join
(
f
'
"
{
k
}
"
'
for
k
in
sorted
(
registered_keys
)
)
    
return
(
'
/
/
This
file
was
automatically
generated
.
Do
not
edit
.
\
n
'
            
'
\
n
'
            
'
#
ifndef
GEN_REGISTERED_FIELD_TRIALS_H_
\
n
'
            
'
#
define
GEN_REGISTERED_FIELD_TRIALS_H_
\
n
'
            
'
\
n
'
            
'
#
include
"
absl
/
strings
/
string_view
.
h
"
\
n
'
            
'
\
n
'
            
'
namespace
webrtc
{
\
n
'
            
'
\
n
'
            
'
inline
constexpr
absl
:
:
string_view
kRegisteredFieldTrials
[
]
=
{
\
n
'
            
f
'
{
keys
}
\
n
'
            
'
}
;
\
n
'
            
'
\
n
'
            
'
}
/
/
namespace
webrtc
\
n
'
            
'
\
n
'
            
'
#
endif
/
/
GEN_REGISTERED_FIELD_TRIALS_H_
\
n
'
)
def
cmd_header
(
args
:
argparse
.
Namespace
)
-
>
None
:
    
args
.
output
.
write
(
registry_header
(
)
)
def
main
(
)
-
>
None
:
    
parser
=
argparse
.
ArgumentParser
(
)
    
subcommand
=
parser
.
add_subparsers
(
dest
=
'
cmd
'
)
    
parser_header
=
subcommand
.
add_parser
(
        
'
header
'
        
help
=
'
generate
C
+
+
header
file
containing
registered
field
trial
keys
'
)
    
parser_header
.
add_argument
(
'
-
-
output
'
                               
default
=
sys
.
stdout
                               
type
=
argparse
.
FileType
(
'
w
'
)
                               
required
=
False
                               
help
=
'
output
file
'
)
    
parser_header
.
set_defaults
(
cmd
=
cmd_header
)
    
args
=
parser
.
parse_args
(
)
    
if
not
args
.
cmd
:
        
parser
.
print_help
(
sys
.
stderr
)
        
sys
.
exit
(
1
)
    
args
.
cmd
(
args
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
