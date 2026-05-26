import
os
import
subprocess
from
tempfile
import
TemporaryDirectory
import
buildconfig
import
codegen
import
mozpack
.
path
as
mozpath
from
mozbuild
.
util
import
FileAvoidWrite
def
WebCompatBuildTest
(
harness
)
:
    
mach_path
=
mozpath
.
join
(
buildconfig
.
topsrcdir
"
mach
"
)
    
if
not
os
.
path
.
isfile
(
mach_path
)
or
not
os
.
access
(
mach_path
os
.
X_OK
)
:
        
raise
ValueError
(
"
Could
not
find
mach
to
run
linter
"
)
    
webcompat_reldir
=
mozpath
.
join
(
"
browser
"
"
extensions
"
"
webcompat
"
)
    
webcompat_dir
=
mozpath
.
join
(
buildconfig
.
topsrcdir
webcompat_reldir
)
    
interventions_dir
=
mozpath
.
join
(
webcompat_dir
"
data
"
"
interventions
"
)
    
generated_filenames_list
=
mozpath
.
join
(
        
webcompat_dir
"
preprocessed_intervention_files
.
mozbuild
"
    
)
    
generated_files
=
[
]
    
with
open
(
generated_filenames_list
)
as
fd
:
        
for
line
in
fd
.
read
(
)
.
splitlines
(
)
:
            
if
"
.
js
"
in
line
or
"
.
css
"
in
line
:
                
generated_files
.
append
(
line
.
strip
(
)
[
1
:
-
2
]
)
    
with
TemporaryDirectory
(
dir
=
webcompat_dir
)
as
to_lint_dir
:
        
for
filename
in
generated_files
:
            
generated_path
=
mozpath
.
join
(
to_lint_dir
filename
)
            
with
FileAvoidWrite
(
generated_path
)
as
generated_fd
:
                
codegen
.
generate_file
(
generated_fd
interventions_dir
)
        
linting_result
=
subprocess
.
run
(
            
[
mach_path
"
lint
"
to_lint_dir
]
            
stdout
=
subprocess
.
PIPE
            
check
=
False
            
text
=
True
        
)
.
stdout
        
def
parse_fragment_errors
(
linter_stdout
)
:
            
error_lines_for_current_file
=
None
            
for
line
in
linter_stdout
.
splitlines
(
)
:
                
if
"
[
error
]
"
not
in
line
:
                    
continue
                
if
webcompat_reldir
in
line
:
                    
if
error_lines_for_current_file
:
                        
yield
error_lines_for_current_file
                    
[
linted_filename
error
]
=
line
.
split
(
"
[
error
]
"
maxsplit
=
1
)
[
                        
1
                    
]
.
split
(
"
:
"
maxsplit
=
1
)
                    
linted_filename
=
mozpath
.
splitext
(
                        
mozpath
.
basename
(
linted_filename
)
                    
)
[
0
]
                    
summary_line
=
(
                        
f
"
Error
linting
generated
file
{
linted_filename
}
:
{
error
}
"
                    
)
                    
error_lines_for_current_file
=
[
summary_line
]
                
else
:
                    
error_lines_for_current_file
.
append
(
                        
line
.
split
(
"
[
error
]
"
maxsplit
=
1
)
[
1
]
                    
)
            
if
error_lines_for_current_file
:
                
yield
"
\
n
"
.
join
(
error_lines_for_current_file
)
        
bad_fragments
=
list
(
parse_fragment_errors
(
linting_result
)
)
        
if
not
bad_fragments
:
            
harness
.
ok
(
True
"
mach
lint
found
no
errors
with
generated
files
"
)
        
else
:
            
for
fragment_error
in
bad_fragments
:
                
harness
.
ok
(
False
fragment_error
)
