import
functools
import
logging
import
os
import
unittest
from
pylib
.
symbols
import
elf_symbolizer
from
pylib
.
symbols
import
mock_addr2line
_MOCK_A2L_PATH
=
os
.
path
.
join
(
os
.
path
.
dirname
(
mock_addr2line
.
__file__
)
                              
'
mock_addr2line
'
)
_INCOMPLETE_MOCK_ADDR
=
1024
*
1024
_UNKNOWN_MOCK_ADDR
=
2
*
1024
*
1024
_INLINE_MOCK_ADDR
=
3
*
1024
*
1024
class
ELFSymbolizerTest
(
unittest
.
TestCase
)
:
  
def
setUp
(
self
)
:
    
self
.
_callback
=
functools
.
partial
(
        
ELFSymbolizerTest
.
_SymbolizeCallback
self
)
    
self
.
_resolved_addresses
=
set
(
)
    
logging
.
getLogger
(
)
.
setLevel
(
logging
.
ERROR
)
  
def
testParallelism1
(
self
)
:
    
self
.
_RunTest
(
max_concurrent_jobs
=
1
num_symbols
=
100
)
  
def
testParallelism4
(
self
)
:
    
self
.
_RunTest
(
max_concurrent_jobs
=
4
num_symbols
=
100
)
  
def
testParallelism8
(
self
)
:
    
self
.
_RunTest
(
max_concurrent_jobs
=
8
num_symbols
=
100
)
  
def
testCrash
(
self
)
:
    
os
.
environ
[
'
MOCK_A2L_CRASH_EVERY
'
]
=
'
99
'
    
self
.
_RunTest
(
max_concurrent_jobs
=
1
num_symbols
=
100
)
    
os
.
environ
[
'
MOCK_A2L_CRASH_EVERY
'
]
=
'
0
'
  
def
testHang
(
self
)
:
    
os
.
environ
[
'
MOCK_A2L_HANG_EVERY
'
]
=
'
99
'
    
self
.
_RunTest
(
max_concurrent_jobs
=
1
num_symbols
=
100
)
    
os
.
environ
[
'
MOCK_A2L_HANG_EVERY
'
]
=
'
0
'
  
def
testInlines
(
self
)
:
    
"
"
"
Stimulate
the
inline
processing
logic
.
"
"
"
    
symbolizer
=
elf_symbolizer
.
ELFSymbolizer
(
        
elf_file_path
=
'
/
path
/
doesnt
/
matter
/
mock_lib1
.
so
'
        
addr2line_path
=
_MOCK_A2L_PATH
        
callback
=
self
.
_callback
        
inlines
=
True
        
max_concurrent_jobs
=
4
)
    
for
addr
in
range
(
1000
)
:
      
exp_inline
=
False
      
exp_unknown
=
False
      
if
addr
<
100
:
        
addr
+
=
_INLINE_MOCK_ADDR
        
exp_inline
=
True
      
elif
addr
<
200
:
        
pass
      
elif
addr
<
300
:
        
if
addr
&
1
:
          
addr
+
=
_INLINE_MOCK_ADDR
          
exp_inline
=
True
      
elif
addr
<
400
:
        
if
addr
&
1
:
          
addr
+
=
_INLINE_MOCK_ADDR
          
exp_inline
=
True
        
else
:
          
addr
+
=
_UNKNOWN_MOCK_ADDR
          
exp_unknown
=
True
      
exp_name
=
'
mock_sym_for_addr_
%
d
'
%
addr
if
not
exp_unknown
else
None
      
exp_source_path
=
'
mock_src
/
mock_lib1
.
so
.
c
'
if
not
exp_unknown
else
None
      
exp_source_line
=
addr
if
not
exp_unknown
else
None
      
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
exp_inline
)
      
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
symbolizer
.
Join
(
)
  
def
testIncompleteSyminfo
(
self
)
:
    
"
"
"
Stimulate
the
symbol
-
not
-
resolved
logic
.
"
"
"
    
symbolizer
=
elf_symbolizer
.
ELFSymbolizer
(
        
elf_file_path
=
'
/
path
/
doesnt
/
matter
/
mock_lib1
.
so
'
        
addr2line_path
=
_MOCK_A2L_PATH
        
callback
=
self
.
_callback
        
max_concurrent_jobs
=
1
)
    
addr
=
_INCOMPLETE_MOCK_ADDR
    
exp_name
=
'
mock_sym_for_addr_
%
d
'
%
addr
    
exp_source_path
=
None
    
exp_source_line
=
None
    
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
False
)
    
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
addr
=
_UNKNOWN_MOCK_ADDR
    
exp_name
=
None
    
exp_source_path
=
None
    
exp_source_line
=
None
    
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
False
)
    
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
symbolizer
.
Join
(
)
  
def
testWaitForIdle
(
self
)
:
    
symbolizer
=
elf_symbolizer
.
ELFSymbolizer
(
        
elf_file_path
=
'
/
path
/
doesnt
/
matter
/
mock_lib1
.
so
'
        
addr2line_path
=
_MOCK_A2L_PATH
        
callback
=
self
.
_callback
        
max_concurrent_jobs
=
1
)
    
addr
=
_INCOMPLETE_MOCK_ADDR
    
exp_name
=
'
mock_sym_for_addr_
%
d
'
%
addr
    
exp_source_path
=
None
    
exp_source_line
=
None
    
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
False
)
    
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
symbolizer
.
WaitForIdle
(
)
    
addr
=
_UNKNOWN_MOCK_ADDR
    
exp_name
=
None
    
exp_source_path
=
None
    
exp_source_line
=
None
    
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
False
)
    
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
symbolizer
.
Join
(
)
  
def
_RunTest
(
self
max_concurrent_jobs
num_symbols
)
:
    
symbolizer
=
elf_symbolizer
.
ELFSymbolizer
(
        
elf_file_path
=
'
/
path
/
doesnt
/
matter
/
mock_lib1
.
so
'
        
addr2line_path
=
_MOCK_A2L_PATH
        
callback
=
self
.
_callback
        
max_concurrent_jobs
=
max_concurrent_jobs
        
addr2line_timeout
=
0
.
5
)
    
for
addr
in
range
(
num_symbols
)
:
      
exp_name
=
'
mock_sym_for_addr_
%
d
'
%
addr
      
exp_source_path
=
'
mock_src
/
mock_lib1
.
so
.
c
'
      
exp_source_line
=
addr
      
cb_arg
=
(
addr
exp_name
exp_source_path
exp_source_line
False
)
      
symbolizer
.
SymbolizeAsync
(
addr
cb_arg
)
    
symbolizer
.
Join
(
)
    
for
addr
in
range
(
num_symbols
)
:
      
self
.
assertIn
(
addr
self
.
_resolved_addresses
)
      
self
.
_resolved_addresses
.
remove
(
addr
)
    
self
.
assertEqual
(
len
(
self
.
_resolved_addresses
)
0
)
  
def
_SymbolizeCallback
(
self
sym_info
cb_arg
)
:
    
self
.
assertTrue
(
isinstance
(
sym_info
elf_symbolizer
.
ELFSymbolInfo
)
)
    
self
.
assertTrue
(
isinstance
(
cb_arg
tuple
)
)
    
self
.
assertEqual
(
len
(
cb_arg
)
5
)
    
(
addr
exp_name
exp_source_path
exp_source_line
exp_inlines
)
=
cb_arg
    
if
exp_name
is
None
:
      
self
.
assertIsNone
(
sym_info
.
name
)
    
else
:
      
self
.
assertTrue
(
sym_info
.
name
.
startswith
(
exp_name
)
)
    
self
.
assertEqual
(
sym_info
.
source_path
exp_source_path
)
    
self
.
assertEqual
(
sym_info
.
source_line
exp_source_line
)
    
if
exp_inlines
:
      
self
.
assertEqual
(
sym_info
.
name
exp_name
+
'
_inner
'
)
      
self
.
assertEqual
(
sym_info
.
inlined_by
.
name
exp_name
+
'
_middle
'
)
      
self
.
assertEqual
(
sym_info
.
inlined_by
.
inlined_by
.
name
                       
exp_name
+
'
_outer
'
)
    
self
.
assertNotIn
(
addr
self
.
_resolved_addresses
)
    
self
.
_resolved_addresses
.
add
(
addr
)
if
__name__
=
=
'
__main__
'
:
  
unittest
.
main
(
)
