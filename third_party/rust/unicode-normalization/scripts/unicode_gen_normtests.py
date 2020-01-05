import
unicode
re
os
fileinput
def
load_test_data
(
f
)
:
    
outls
=
[
]
    
testRe
=
re
.
compile
(
"
^
(
.
*
?
)
;
(
.
*
?
)
;
(
.
*
?
)
;
(
.
*
?
)
;
(
.
*
?
)
;
\
s
+
#
.
*
"
)
    
unicode
.
fetch
(
f
)
    
for
line
in
fileinput
.
input
(
os
.
path
.
basename
(
f
)
)
:
        
if
len
(
line
)
<
1
or
line
[
0
:
1
]
=
=
'
#
'
or
line
[
0
:
1
]
=
=
'
'
:
            
continue
        
m
=
testRe
.
match
(
line
)
        
groups
=
[
]
        
if
not
m
:
            
print
"
error
:
no
match
on
line
where
test
was
expected
:
%
s
"
%
line
            
continue
        
has_surrogates
=
False
        
for
i
in
range
(
1
6
)
:
            
group
=
[
]
            
chs
=
m
.
group
(
i
)
.
split
(
)
            
for
ch
in
chs
:
                
intch
=
int
(
ch
16
)
                
if
unicode
.
is_surrogate
(
intch
)
:
                    
has_surrogates
=
True
                    
break
                
group
.
append
(
intch
)
            
if
has_surrogates
:
                
break
            
groups
.
append
(
group
)
        
if
has_surrogates
:
            
continue
        
outls
.
append
(
groups
)
    
return
outls
def
showfun
(
gs
)
:
    
outstr
=
'
(
'
    
gfirst
=
True
    
for
g
in
gs
:
        
if
not
gfirst
:
            
outstr
+
=
'
'
        
gfirst
=
False
        
outstr
+
=
'
"
'
        
for
ch
in
g
:
            
outstr
+
=
"
\
\
u
{
%
x
}
"
%
ch
        
outstr
+
=
'
"
'
    
outstr
+
=
'
)
'
    
return
outstr
if
__name__
=
=
"
__main__
"
:
    
d
=
load_test_data
(
"
NormalizationTest
.
txt
"
)
    
ntype
=
"
&
'
static
[
(
&
'
static
str
&
'
static
str
&
'
static
str
&
'
static
str
&
'
static
str
)
]
"
    
with
open
(
"
testdata
.
rs
"
"
w
"
)
as
nf
:
        
nf
.
write
(
unicode
.
preamble
)
        
nf
.
write
(
"
\
n
"
)
        
nf
.
write
(
"
/
/
official
Unicode
test
data
\
n
"
)
        
nf
.
write
(
"
/
/
http
:
/
/
www
.
unicode
.
org
/
Public
/
UNIDATA
/
NormalizationTest
.
txt
\
n
"
)
        
unicode
.
emit_table
(
nf
"
TEST_NORM
"
d
ntype
True
showfun
)
