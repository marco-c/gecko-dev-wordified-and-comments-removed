import
mozunit
from
mozversioncontrol
import
get_repository_object
STEPS
=
{
    
"
hg
"
:
[
        
"
"
"
        
echo
"
bar
"
>
>
bar
        
echo
"
baz
"
>
foo
        
"
"
"
    
]
    
"
git
"
:
[
        
"
"
"
        
echo
"
bar
"
>
>
bar
        
echo
"
baz
"
>
foo
        
"
"
"
    
]
}
def
test_commit
(
repo
)
:
    
vcs
=
get_repository_object
(
repo
.
dir
)
    
assert
vcs
.
working_directory_clean
(
)
    
repo
.
execute_next_step
(
)
    
assert
not
vcs
.
working_directory_clean
(
)
    
vcs
.
commit
(
        
message
=
"
Modify
bar
\
n
\
nbut
not
baz
"
        
author
=
"
Testing
McTesterson
<
test
example
.
org
>
"
        
date
=
"
2017
-
07
-
14
02
:
40
:
00
UTC
"
        
paths
=
[
"
bar
"
]
    
)
    
assert
not
vcs
.
working_directory_clean
(
)
    
if
repo
.
vcs
=
=
"
git
"
:
        
log_cmd
=
[
"
log
"
"
-
1
"
"
-
-
format
=
%
an
%
ae
%
aD
%
B
"
]
        
patch_cmd
=
[
"
log
"
"
-
1
"
"
-
p
"
]
    
else
:
        
log_cmd
=
[
            
"
log
"
            
"
-
l
"
            
"
1
"
            
"
-
T
"
            
"
{
person
(
author
)
}
{
email
(
author
)
}
{
date
|
rfc822date
}
{
desc
}
"
        
]
        
patch_cmd
=
[
"
log
"
"
-
l
"
"
1
"
"
-
p
"
]
    
log
=
vcs
.
_run
(
*
log_cmd
)
.
rstrip
(
)
    
assert
log
=
=
(
        
"
Testing
McTesterson
test
example
.
org
Fri
14
"
        
"
Jul
2017
02
:
40
:
00
+
0000
Modify
bar
\
n
\
nbut
not
baz
"
    
)
    
patch
=
vcs
.
_run
(
*
patch_cmd
)
    
diffs
=
[
line
for
line
in
patch
.
splitlines
(
)
if
"
diff
-
-
git
"
in
line
]
    
assert
len
(
diffs
)
=
=
1
    
assert
diffs
[
0
]
=
=
"
diff
-
-
git
a
/
bar
b
/
bar
"
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
