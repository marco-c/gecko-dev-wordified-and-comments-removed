import
subprocess
def
wasm2c
(
output
wasm2c_bin
wasm_lib
)
:
    
output
.
close
(
)
    
return
subprocess
.
run
(
        
[
wasm2c_bin
"
-
o
"
output
.
name
"
-
-
disable
-
simd
"
wasm_lib
]
    
)
.
returncode
