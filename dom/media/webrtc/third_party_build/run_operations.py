import
os
import
subprocess
import
sys
env
=
os
.
environ
.
copy
(
)
env
[
"
HGPLAIN
"
]
=
"
1
"
def
run_hg
(
cmd
)
:
    
cmd_list
=
cmd
.
split
(
"
"
)
    
res
=
subprocess
.
run
(
        
cmd_list
        
capture_output
=
True
        
text
=
True
        
env
=
env
        
check
=
False
    
)
    
if
res
.
returncode
!
=
0
:
        
print
(
            
f
"
Hit
return
code
{
res
.
returncode
}
running
'
{
cmd
}
'
.
Aborting
.
"
            
file
=
sys
.
stderr
        
)
        
print
(
res
.
stderr
)
        
sys
.
exit
(
1
)
    
stdout
=
res
.
stdout
.
strip
(
)
    
return
[
]
if
len
(
stdout
)
=
=
0
else
stdout
.
split
(
"
\
n
"
)
def
run_git
(
cmd
working_dir
)
:
    
cmd_list
=
cmd
.
split
(
"
"
)
    
res
=
subprocess
.
run
(
        
cmd_list
        
capture_output
=
True
        
text
=
True
        
cwd
=
working_dir
        
check
=
False
    
)
    
if
res
.
returncode
!
=
0
:
        
print
(
            
f
"
Hit
return
code
{
res
.
returncode
}
running
'
{
cmd
}
'
.
Aborting
.
"
            
file
=
sys
.
stderr
        
)
        
print
(
res
.
stderr
)
        
sys
.
exit
(
1
)
    
stdout
=
res
.
stdout
.
strip
(
)
    
return
[
]
if
len
(
stdout
)
=
=
0
else
stdout
.
split
(
"
\
n
"
)
def
run_shell
(
cmd
capture_output
=
True
)
:
    
res
=
subprocess
.
run
(
        
cmd
        
shell
=
True
        
capture_output
=
capture_output
        
text
=
True
        
check
=
False
    
)
    
if
res
.
returncode
!
=
0
:
        
print
(
            
f
"
Hit
return
code
{
res
.
returncode
}
running
'
{
cmd
}
'
.
Aborting
.
"
            
file
=
sys
.
stderr
        
)
        
if
capture_output
:
            
print
(
res
.
stderr
)
        
sys
.
exit
(
1
)
    
output_lines
=
[
]
    
if
capture_output
:
        
stdout
=
res
.
stdout
.
strip
(
)
        
output_lines
=
[
]
if
len
(
stdout
)
=
=
0
else
stdout
.
split
(
"
\
n
"
)
    
return
output_lines
def
get_last_line
(
file_path
)
:
    
with
open
(
file_path
"
rb
"
)
as
f
:
        
try
:
            
f
.
seek
(
-
2
os
.
SEEK_END
)
            
while
f
.
read
(
1
)
!
=
b
"
\
n
"
:
                
f
.
seek
(
-
2
os
.
SEEK_CUR
)
        
except
OSError
:
            
f
.
seek
(
0
)
        
return
f
.
readline
(
)
.
decode
(
)
.
strip
(
)
def
update_resume_state
(
state
resume_state_filename
)
:
    
with
open
(
resume_state_filename
"
w
"
)
as
ofile
:
        
ofile
.
write
(
state
)
        
ofile
.
write
(
"
\
n
"
)
