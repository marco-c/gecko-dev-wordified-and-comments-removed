import
sys
leading_text_example
=
"
0
:
02
.
39
"
in_include
=
False
in_files
=
False
start_trim
=
len
(
leading_text_example
)
print
(
"
cargo
run
-
-
"
)
for
line
in
sys
.
stdin
:
    
line
=
line
[
start_trim
:
-
1
]
    
if
line
.
endswith
(
"
INCLUDES
"
)
:
        
in_include
=
True
        
continue
    
if
line
.
endswith
(
"
FILES
"
)
:
        
assert
in_include
        
in_include
=
False
        
in_files
=
True
        
continue
    
if
line
.
endswith
(
"
DONE
"
)
:
        
assert
in_files
        
exit
(
0
)
    
if
in_include
:
        
print
(
"
-
I
"
line
)
    
elif
in_files
:
        
print
(
line
)
    
else
:
        
assert
False
