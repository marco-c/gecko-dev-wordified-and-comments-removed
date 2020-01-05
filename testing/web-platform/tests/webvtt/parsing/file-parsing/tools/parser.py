"
"
"
A
direct
translation
of
the
webvtt
file
parsing
algorithm
.
See
https
:
/
/
w3c
.
github
.
io
/
webvtt
/
#
file
-
parsing
for
documentation
"
"
"
import
re
import
string
SPACE_CHARACTERS
=
[
'
'
'
\
t
'
'
\
n
'
'
\
f
'
'
\
r
'
]
SPACE_SPLIT_PATTERN
=
r
"
[
{
}
]
*
"
.
format
(
'
'
.
join
(
SPACE_CHARACTERS
)
)
DIGITS
=
string
.
digits
class
DictInit
:
    
def
__init__
(
self
*
*
dict
)
:
        
self
.
__dict__
.
update
(
dict
)
class
VTTCue
(
DictInit
)
:
pass
class
VTTRegion
(
DictInit
)
:
pass
class
Stylesheet
(
DictInit
)
:
pass
class
W3CParser
:
    
input
=
None
    
position
=
None
    
def
collect_characters
(
self
condition
)
:
        
result
=
"
"
        
while
self
.
position
<
len
(
self
.
input
)
and
condition
(
self
.
input
[
self
.
position
]
)
:
            
result
+
=
self
.
input
[
self
.
position
]
            
self
.
position
+
=
1
        
return
result
    
def
skip_whitespace
(
self
)
:
        
self
.
collect_characters
(
lambda
c
:
c
in
SPACE_CHARACTERS
)
    
def
parse_percentage_string
(
self
input
)
:
        
'
parse
a
percentage
string
'
        
input
=
input
        
if
not
re
.
match
(
r
'
^
\
d
+
(
\
.
\
d
+
)
?
%
'
input
)
:
            
return
None
        
percentage
=
float
(
input
[
:
-
1
]
)
        
if
percentage
<
0
or
percentage
>
100
:
            
return
None
        
return
percentage
class
VTTParser
(
W3CParser
)
:
    
def
__init__
(
self
input
)
:
        
self
.
input
=
input
        
self
.
position
=
0
        
self
.
seen_cue
=
False
        
self
.
text_tracks
=
[
]
        
self
.
stylesheets
=
[
]
        
self
.
regions
=
[
]
        
self
.
errors
=
[
]
    
def
parse
(
self
)
:
        
'
WebVTT
parser
algorithm
'
        
self
.
input
=
self
.
input
.
replace
(
'
\
0
'
'
\
ufffd
'
)
.
replace
(
'
\
r
\
n
'
'
\
n
'
)
.
replace
(
'
\
r
'
'
\
n
'
)
        
self
.
position
=
0
        
self
.
seen_cue
=
False
        
if
len
(
self
.
input
)
<
6
:
            
self
.
errors
.
append
(
'
input
too
small
for
webvtt
'
)
            
return
        
if
len
(
self
.
input
)
=
=
6
and
self
.
input
!
=
'
WEBVTT
'
:
            
self
.
errors
.
append
(
'
invalid
webvtt
header
'
)
            
return
        
if
len
(
self
.
input
)
>
6
:
            
if
not
(
self
.
input
[
0
:
6
]
=
=
'
WEBVTT
'
and
self
.
input
[
6
]
in
[
'
\
u0020
'
'
\
u0009
'
'
\
u000A
'
]
)
:
                
self
.
errors
.
append
(
'
invalid
webvtt
header
'
)
                
return
        
self
.
collect_characters
(
lambda
c
:
c
!
=
'
\
n
'
)
        
if
self
.
position
>
=
len
(
self
.
input
)
:
            
return
        
if
self
.
input
[
self
.
position
]
=
=
'
\
n
'
:
            
self
.
position
+
=
1
        
if
self
.
position
>
=
len
(
self
.
input
)
:
            
return
        
if
self
.
input
[
self
.
position
]
!
=
'
\
n
'
:
            
self
.
collect_block
(
in_header
=
True
)
        
else
:
            
self
.
position
+
=
1
        
self
.
collect_characters
(
lambda
c
:
c
=
=
'
\
n
'
)
        
self
.
regions
=
[
]
        
while
self
.
position
<
len
(
self
.
input
)
:
            
block
=
self
.
collect_block
(
)
            
if
isinstance
(
block
VTTCue
)
:
                
self
.
text_tracks
.
append
(
block
)
            
elif
isinstance
(
block
Stylesheet
)
:
                
self
.
stylesheets
.
append
(
block
)
            
elif
isinstance
(
block
VTTRegion
)
:
                
self
.
regions
.
append
(
block
)
            
self
.
collect_characters
(
lambda
c
:
c
=
=
'
\
n
'
)
        
return
    
def
collect_block
(
self
in_header
=
False
)
:
        
'
collect
a
WebVTT
block
'
        
line_count
=
0
        
previous_position
=
self
.
position
        
line
=
"
"
        
buffer
=
"
"
        
seen_eof
=
False
        
seen_arrow
=
False
        
cue
=
None
        
stylesheet
=
None
        
region
=
None
        
while
True
:
            
line
=
self
.
collect_characters
(
lambda
c
:
c
!
=
'
\
n
'
)
            
line_count
+
=
1
            
if
self
.
position
>
=
len
(
self
.
input
)
:
                
seen_eof
=
True
            
else
:
                
self
.
position
+
=
1
            
if
'
-
-
>
'
in
line
:
                
if
not
in_header
and
(
line_count
=
=
1
or
line_count
=
=
2
and
not
seen_arrow
)
:
                    
seen_arrow
=
True
                    
previous_position
=
self
.
position
                    
cue
=
VTTCue
(
                        
id
=
buffer
                        
pause_on_exit
=
False
                        
region
=
None
                        
writing_direction
=
'
horizontal
'
                        
snap_to_lines
=
True
                        
line
=
'
auto
'
                        
line_alignment
=
'
start
alignment
'
                        
position
=
'
auto
'
                        
position_alignment
=
'
auto
'
                        
cue_size
=
100
                        
text_alignment
=
'
center
'
                        
text
=
'
'
                    
)
                    
if
not
VTTCueParser
(
self
line
cue
)
.
collect_cue_timings_and_settings
(
)
:
                        
cue
=
None
                    
else
:
                        
buffer
=
'
'
                        
self
.
seen_cue
=
True
                
else
:
                    
self
.
errors
.
append
(
'
invalid
webvtt
cue
block
'
)
                    
self
.
position
=
previous_position
                    
break
            
elif
line
=
=
'
'
:
                
break
            
else
:
                
if
not
in_header
and
line_count
=
=
2
:
                    
if
not
self
.
seen_cue
and
re
.
match
(
r
'
^
STYLE
\
s
*
'
buffer
)
:
                        
stylesheet
=
Stylesheet
(
                            
location
=
None
                            
parent
=
None
                            
owner_node
=
None
                            
owner_rule
=
None
                            
media
=
None
                            
title
=
None
                            
alternate
=
False
                            
origin_clean
=
True
                            
source
=
None
                        
)
                        
buffer
=
'
'
                    
elif
not
self
.
seen_cue
and
re
.
match
(
r
'
^
REGION
\
s
*
'
buffer
)
:
                        
region
=
VTTRegion
(
                            
id
=
'
'
                            
width
=
100
                            
lines
=
3
                            
anchor_point
=
(
0
100
)
                            
viewport_anchor_point
=
(
0
100
)
                            
scroll_value
=
None
                        
)
                        
buffer
=
'
'
                
if
buffer
!
=
'
'
:
                    
buffer
+
=
'
\
n
'
                
buffer
+
=
line
                
previous_position
=
self
.
position
            
if
seen_eof
:
                
break
        
if
cue
is
not
None
:
            
cue
.
text
=
buffer
            
return
cue
        
elif
stylesheet
is
not
None
:
            
stylesheet
.
source
=
buffer
            
return
stylesheet
        
elif
region
is
not
None
:
            
self
.
collect_region_settings
(
region
buffer
)
            
return
region
        
return
None
    
def
collect_region_settings
(
self
region
input
)
:
        
'
collect
WebVTT
region
settings
'
        
settings
=
re
.
split
(
SPACE_SPLIT_PATTERN
input
)
        
for
setting
in
settings
:
            
if
'
:
'
not
in
setting
:
                
continue
            
index
=
setting
.
index
(
'
:
'
)
            
if
index
in
[
0
len
(
setting
)
-
1
]
:
                
continue
            
name
=
setting
[
:
index
]
            
value
=
setting
[
index
+
1
:
]
            
if
name
=
=
"
id
"
:
                
region
.
id
=
value
            
elif
name
=
=
"
width
"
:
                
percentage
=
self
.
parse_percentage_string
(
value
)
                
if
percentage
is
not
None
:
                    
region
.
width
=
percentage
            
elif
name
=
=
"
lines
"
:
                
if
not
re
.
match
(
r
'
^
\
d
+
'
value
)
:
                    
continue
                
number
=
int
(
value
)
                
region
.
lines
=
number
            
elif
name
=
=
"
regionanchor
"
:
                
if
'
'
not
in
value
:
                    
continue
                
index
=
value
.
index
(
'
'
)
                
anchorX
=
value
[
:
index
]
                
anchorY
=
value
[
index
+
1
:
]
                
percentageX
=
self
.
parse_percentage_string
(
anchorX
)
                
percentageY
=
self
.
parse_percentage_string
(
anchorY
)
                
if
None
in
[
percentageX
percentageY
]
:
                    
continue
                
region
.
anchor_point
=
(
percentageX
percentageY
)
            
elif
name
=
=
"
viewportanchor
"
:
                
if
'
'
not
in
value
:
                    
continue
                
index
=
value
.
index
(
'
'
)
                
viewportanchorX
=
value
[
:
index
]
                
viewportanchorY
=
value
[
index
+
1
:
]
                
percentageX
=
self
.
parse_percentage_string
(
viewportanchorX
)
                
percentageY
=
self
.
parse_percentage_string
(
viewportanchorY
)
                
if
None
in
[
percentageX
percentageY
]
:
                    
continue
                
region
.
viewport_anchor_point
=
(
percentageX
percentageY
)
            
elif
name
=
=
"
scroll
"
:
                
if
value
=
=
"
up
"
:
                    
region
.
scroll_value
=
"
up
"
            
continue
class
VTTCueParser
(
W3CParser
)
:
    
def
__init__
(
self
parent
input
cue
)
:
        
self
.
parent
=
parent
        
self
.
errors
=
self
.
parent
.
errors
        
self
.
input
=
input
        
self
.
position
=
0
        
self
.
cue
=
cue
    
def
collect_cue_timings_and_settings
(
self
)
:
        
'
collect
WebVTT
cue
timings
and
settings
'
        
self
.
position
=
0
        
self
.
skip_whitespace
(
)
        
timestamp
=
self
.
collect_timestamp
(
)
        
if
timestamp
is
None
:
            
self
.
errors
.
append
(
'
invalid
start
time
for
VTTCue
'
)
            
return
False
        
self
.
cue
.
start_time
=
timestamp
        
self
.
skip_whitespace
(
)
        
if
self
.
input
[
self
.
position
]
!
=
'
-
'
:
            
return
False
        
self
.
position
+
=
1
        
if
self
.
input
[
self
.
position
]
!
=
'
-
'
:
            
return
False
        
self
.
position
+
=
1
        
if
self
.
input
[
self
.
position
]
!
=
'
>
'
:
            
return
False
        
self
.
position
+
=
1
        
self
.
skip_whitespace
(
)
        
timestamp
=
self
.
collect_timestamp
(
)
        
if
timestamp
is
None
:
            
self
.
errors
.
append
(
'
invalid
end
time
for
VTTCue
'
)
            
return
False
        
self
.
cue
.
end_time
=
timestamp
        
remainder
=
self
.
input
[
self
.
position
:
]
        
self
.
parse_settings
(
remainder
)
        
return
True
    
def
parse_settings
(
self
input
)
:
        
'
parse
the
WebVTT
cue
settings
'
        
settings
=
re
.
split
(
SPACE_SPLIT_PATTERN
input
)
        
for
setting
in
settings
:
            
if
'
:
'
not
in
setting
:
                
continue
            
index
=
setting
.
index
(
'
:
'
)
            
if
index
in
[
0
len
(
setting
)
-
1
]
:
                
continue
            
name
=
setting
[
:
index
]
            
value
=
setting
[
index
+
1
:
]
            
if
name
=
=
'
region
'
:
                
last_regions
=
(
region
for
region
in
reversed
(
self
.
parent
.
regions
)
if
region
.
id
=
=
value
)
                
self
.
cue
.
region
=
next
(
last_regions
None
)
            
elif
name
=
=
'
vertical
'
:
                
if
value
in
[
'
rl
'
'
lr
'
]
:
                    
self
.
cue
.
writing_direction
=
value
            
elif
name
=
=
'
line
'
:
                
if
'
'
in
value
:
                    
index
=
value
.
index
(
'
'
)
                    
linepos
=
value
[
:
index
]
                    
linealign
=
value
[
index
+
1
:
]
                
else
:
                    
linepos
=
value
                    
linealign
=
None
                
if
not
re
.
search
(
r
'
\
d
'
linepos
)
:
                    
continue
                
if
linepos
[
-
1
]
=
=
'
%
'
:
                    
number
=
self
.
parse_percentage_string
(
linepos
)
                    
if
number
is
None
:
                        
continue
                
else
:
                    
if
not
re
.
match
(
r
'
^
[
-
\
.
\
d
]
*
'
linepos
)
:
                        
continue
                    
if
'
-
'
in
linepos
[
1
:
]
:
                        
continue
                    
if
linepos
.
count
(
'
.
'
)
>
1
:
                        
continue
                    
if
'
.
'
in
linepos
:
                        
if
not
re
.
search
(
r
'
\
d
\
.
\
d
'
linepos
)
:
                            
continue
                    
number
=
float
(
linepos
)
                
if
linealign
=
=
"
start
"
:
                    
self
.
cue
.
line_alignment
=
'
start
'
                
elif
linealign
=
=
"
center
"
:
                    
self
.
cue
.
line_alignment
=
'
center
'
                
elif
linealign
=
=
"
end
"
:
                    
self
.
cue
.
line_alignment
=
'
end
'
                
elif
linealign
!
=
None
:
                    
continue
                
self
.
cue
.
line
=
number
                
if
linepos
[
-
1
]
=
=
'
%
'
:
                    
self
.
cue
.
snap_to_lines
=
False
                
else
:
                    
self
.
cue
.
snap_to_lines
=
True
            
elif
name
=
=
'
position
'
:
                
if
'
'
in
value
:
                    
index
=
value
.
index
(
'
'
)
                    
colpos
=
value
[
:
index
]
                    
colalign
=
value
[
index
+
1
:
]
                
else
:
                    
colpos
=
value
                    
colalign
=
None
                
number
=
self
.
parse_percentage_string
(
colpos
)
                
if
number
is
None
:
                    
continue
                
if
colalign
=
=
"
line
-
left
"
:
                    
self
.
cue
.
line_alignment
=
'
line
-
left
'
                
elif
colalign
=
=
"
center
"
:
                    
self
.
cue
.
line_alignment
=
'
center
'
                
elif
colalign
=
=
"
line
-
right
"
:
                    
self
.
cue
.
line_alignment
=
'
line
-
right
'
                
elif
colalign
!
=
None
:
                    
continue
                
self
.
cue
.
position
=
number
            
elif
name
=
=
'
size
'
:
                
number
=
self
.
parse_percentage_string
(
value
)
                
if
number
is
None
:
                    
continue
                
self
.
cue
.
cue_size
=
number
            
elif
name
=
=
'
align
'
:
                
if
value
=
=
'
start
'
:
                    
self
.
cue
.
text_alignment
=
'
start
'
                
if
value
=
=
'
center
'
:
                    
self
.
cue
.
text_alignment
=
'
center
'
                
if
value
=
=
'
end
'
:
                    
self
.
cue
.
text_alignment
=
'
end
'
                
if
value
=
=
'
left
'
:
                    
self
.
cue
.
text_alignment
=
'
left
'
                
if
value
=
=
'
right
'
:
                    
self
.
cue
.
text_alignment
=
'
right
'
            
continue
    
def
collect_timestamp
(
self
)
:
        
'
collect
a
WebVTT
timestamp
'
        
most_significant_units
=
'
minutes
'
        
if
self
.
position
>
=
len
(
self
.
input
)
:
            
return
None
        
if
self
.
input
[
self
.
position
]
not
in
DIGITS
:
            
return
None
        
string
=
self
.
collect_characters
(
lambda
c
:
c
in
DIGITS
)
        
value_1
=
int
(
string
)
        
if
len
(
string
)
!
=
2
or
value_1
>
59
:
            
most_significant_units
=
'
hours
'
        
if
self
.
position
>
=
len
(
self
.
input
)
or
self
.
input
[
self
.
position
]
!
=
'
:
'
:
            
return
None
        
self
.
position
+
=
1
        
string
=
self
.
collect_characters
(
lambda
c
:
c
in
DIGITS
)
        
if
len
(
string
)
!
=
2
:
            
return
None
        
value_2
=
int
(
string
)
        
if
most_significant_units
=
=
'
hours
'
or
self
.
position
<
len
(
self
.
input
)
and
self
.
input
[
self
.
position
]
=
=
'
:
'
:
            
if
self
.
position
>
=
len
(
self
.
input
)
or
self
.
input
[
self
.
position
]
!
=
'
:
'
:
                
return
None
            
self
.
position
+
=
1
            
string
=
self
.
collect_characters
(
lambda
c
:
c
in
DIGITS
)
            
if
len
(
string
)
!
=
2
:
                
return
None
            
value_3
=
int
(
string
)
        
else
:
            
value_3
=
value_2
            
value_2
=
value_1
            
value_1
=
0
        
if
self
.
position
>
=
len
(
self
.
input
)
or
self
.
input
[
self
.
position
]
!
=
'
.
'
:
            
return
None
        
self
.
position
+
=
1
        
string
=
self
.
collect_characters
(
lambda
c
:
c
in
DIGITS
)
        
if
len
(
string
)
!
=
3
:
            
return
None
        
value_4
=
int
(
string
)
        
if
value_2
>
=
59
or
value_3
>
=
59
:
            
return
None
        
result
=
value_1
*
60
*
60
+
value_2
*
60
+
value_3
+
value_4
/
1000
        
return
result
def
main
(
argv
)
:
    
files
=
[
open
(
path
'
r
'
)
for
path
in
argv
[
1
:
]
]
    
try
:
        
for
file
in
files
:
            
parser
=
VTTParser
(
file
.
read
(
)
)
            
parser
.
parse
(
)
            
print
(
"
Results
:
{
}
"
.
format
(
file
)
)
            
print
(
"
Cues
:
{
}
"
.
format
(
parser
.
text_tracks
)
)
            
print
(
"
StyleSheets
:
{
}
"
.
format
(
parser
.
stylesheets
)
)
            
print
(
"
Regions
:
{
}
"
.
format
(
parser
.
regions
)
)
            
print
(
"
Errors
:
{
}
"
.
format
(
parser
.
errors
)
)
    
finally
:
        
for
file
in
files
:
            
file
.
close
(
)
if
__name__
=
=
'
__main__
'
:
    
import
sys
    
main
(
sys
.
argv
)
;
