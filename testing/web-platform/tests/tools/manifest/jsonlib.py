import
re
import
json
MYPY
=
False
if
MYPY
:
    
from
typing
import
Any
AnyStr
Callable
Dict
IO
Text
__all__
=
[
"
load
"
"
dump_local
"
"
dump_local
"
"
dump_dist
"
"
dumps_dist
"
]
try
:
    
import
ujson
except
ImportError
:
    
has_ujson
=
False
else
:
    
has_ujson
=
True
if
has_ujson
:
    
load
=
ujson
.
load
else
:
    
load
=
json
.
load
if
has_ujson
:
    
loads
=
ujson
.
loads
else
:
    
loads
=
json
.
loads
_ujson_dump_local_kwargs
=
{
    
'
ensure_ascii
'
:
False
    
'
escape_forward_slashes
'
:
False
    
'
indent
'
:
1
    
'
reject_bytes
'
:
True
}
_json_dump_local_kwargs
=
{
    
'
ensure_ascii
'
:
False
    
'
indent
'
:
1
    
'
separators
'
:
(
'
'
'
:
'
)
}
if
has_ujson
:
    
def
dump_local
(
obj
fp
)
:
        
return
ujson
.
dump
(
obj
fp
*
*
_ujson_dump_local_kwargs
)
else
:
    
def
dump_local
(
obj
fp
)
:
        
return
json
.
dump
(
obj
fp
*
*
_json_dump_local_kwargs
)
if
has_ujson
:
    
def
dumps_local
(
obj
)
:
        
return
ujson
.
dumps
(
obj
*
*
_ujson_dump_local_kwargs
)
else
:
    
def
dumps_local
(
obj
)
:
        
return
json
.
dumps
(
obj
*
*
_json_dump_local_kwargs
)
_ujson_dump_dist_kwargs
=
{
    
'
sort_keys
'
:
True
    
'
indent
'
:
1
    
'
reject_bytes
'
:
True
}
_json_dump_dist_kwargs
=
{
    
'
sort_keys
'
:
True
    
'
indent
'
:
1
    
'
separators
'
:
(
'
'
'
:
'
)
}
if
has_ujson
:
    
if
ujson
.
dumps
(
[
]
indent
=
1
)
=
=
"
[
]
"
:
        
def
_ujson_fixup
(
s
)
:
            
return
s
    
else
:
        
_ujson_fixup_re
=
re
.
compile
(
r
"
(
[
\
[
{
]
)
[
\
n
\
x20
]
+
(
[
}
\
]
]
)
"
)
        
def
_ujson_fixup
(
s
)
:
            
return
_ujson_fixup_re
.
sub
(
                
lambda
m
:
m
.
group
(
1
)
+
m
.
group
(
2
)
                
s
            
)
    
def
dump_dist
(
obj
fp
)
:
        
fp
.
write
(
_ujson_fixup
(
ujson
.
dumps
(
obj
*
*
_ujson_dump_dist_kwargs
)
)
)
    
def
dumps_dist
(
obj
)
:
        
return
_ujson_fixup
(
ujson
.
dumps
(
obj
*
*
_ujson_dump_dist_kwargs
)
)
else
:
    
def
dump_dist
(
obj
fp
)
:
        
json
.
dump
(
obj
fp
*
*
_json_dump_dist_kwargs
)
    
def
dumps_dist
(
obj
)
:
        
return
json
.
dumps
(
obj
*
*
_json_dump_dist_kwargs
)
