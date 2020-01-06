class
_dlnode
(
object
)
:
    
def
__init__
(
self
)
:
        
self
.
empty
=
True
class
lrucache
(
object
)
:
    
def
__init__
(
self
size
callback
=
None
)
:
        
self
.
callback
=
callback
        
self
.
table
=
{
}
        
self
.
head
=
_dlnode
(
)
        
self
.
head
.
next
=
self
.
head
        
self
.
head
.
prev
=
self
.
head
        
self
.
listSize
=
1
        
self
.
size
(
size
)
    
def
__len__
(
self
)
:
        
return
len
(
self
.
table
)
    
def
clear
(
self
)
:
        
for
node
in
self
.
dli
(
)
:
            
node
.
empty
=
True
            
node
.
key
=
None
            
node
.
value
=
None
        
self
.
table
.
clear
(
)
    
def
__contains__
(
self
key
)
:
        
return
key
in
self
.
table
    
def
peek
(
self
key
)
:
        
node
=
self
.
table
[
key
]
        
return
node
.
value
    
def
__getitem__
(
self
key
)
:
        
node
=
self
.
table
[
key
]
        
self
.
mtf
(
node
)
        
self
.
head
=
node
        
return
node
.
value
    
def
get
(
self
key
default
=
None
)
:
        
"
"
"
Get
an
item
-
return
default
(
None
)
if
not
present
"
"
"
        
try
:
            
return
self
[
key
]
        
except
KeyError
:
            
return
default
    
def
__setitem__
(
self
key
value
)
:
        
if
key
in
self
.
table
:
            
node
=
self
.
table
[
key
]
            
node
.
value
=
value
            
self
.
mtf
(
node
)
            
self
.
head
=
node
            
return
        
node
=
self
.
head
.
prev
        
if
not
node
.
empty
:
            
if
self
.
callback
is
not
None
:
                
self
.
callback
(
node
.
key
node
.
value
)
            
del
self
.
table
[
node
.
key
]
        
node
.
empty
=
False
        
node
.
key
=
key
        
node
.
value
=
value
        
self
.
table
[
key
]
=
node
        
self
.
head
=
node
    
def
__delitem__
(
self
key
)
:
        
node
=
self
.
table
[
key
]
        
del
self
.
table
[
key
]
        
node
.
empty
=
True
        
node
.
key
=
None
        
node
.
value
=
None
        
self
.
mtf
(
node
)
        
self
.
head
=
node
.
next
    
def
__iter__
(
self
)
:
        
for
node
in
self
.
dli
(
)
:
            
yield
node
.
key
    
def
items
(
self
)
:
        
for
node
in
self
.
dli
(
)
:
            
yield
(
node
.
key
node
.
value
)
    
def
keys
(
self
)
:
        
for
node
in
self
.
dli
(
)
:
            
yield
node
.
key
    
def
values
(
self
)
:
        
for
node
in
self
.
dli
(
)
:
            
yield
node
.
value
    
def
size
(
self
size
=
None
)
:
        
if
size
is
not
None
:
            
assert
size
>
0
            
if
size
>
self
.
listSize
:
                
self
.
addTailNode
(
size
-
self
.
listSize
)
            
elif
size
<
self
.
listSize
:
                
self
.
removeTailNode
(
self
.
listSize
-
size
)
        
return
self
.
listSize
    
def
addTailNode
(
self
n
)
:
        
for
i
in
range
(
n
)
:
            
node
=
_dlnode
(
)
            
node
.
next
=
self
.
head
            
node
.
prev
=
self
.
head
.
prev
            
self
.
head
.
prev
.
next
=
node
            
self
.
head
.
prev
=
node
        
self
.
listSize
+
=
n
    
def
removeTailNode
(
self
n
)
:
        
assert
self
.
listSize
>
n
        
for
i
in
range
(
n
)
:
            
node
=
self
.
head
.
prev
            
if
not
node
.
empty
:
                
if
self
.
callback
is
not
None
:
                    
self
.
callback
(
node
.
key
node
.
value
)
                
del
self
.
table
[
node
.
key
]
            
self
.
head
.
prev
=
node
.
prev
            
node
.
prev
.
next
=
self
.
head
            
node
.
prev
=
None
            
node
.
next
=
None
            
node
.
key
=
None
            
node
.
value
=
None
        
self
.
listSize
-
=
n
    
def
mtf
(
self
node
)
:
        
node
.
prev
.
next
=
node
.
next
        
node
.
next
.
prev
=
node
.
prev
        
node
.
prev
=
self
.
head
.
prev
        
node
.
next
=
self
.
head
.
prev
.
next
        
node
.
next
.
prev
=
node
        
node
.
prev
.
next
=
node
    
def
dli
(
self
)
:
        
node
=
self
.
head
        
for
i
in
range
(
len
(
self
.
table
)
)
:
            
yield
node
            
node
=
node
.
next
class
WriteThroughCacheManager
(
object
)
:
    
def
__init__
(
self
store
size
)
:
        
self
.
store
=
store
        
self
.
cache
=
lrucache
(
size
)
    
def
__len__
(
self
)
:
        
return
len
(
self
.
store
)
    
def
size
(
self
size
=
None
)
:
        
return
self
.
cache
.
size
(
size
)
    
def
clear
(
self
)
:
        
self
.
cache
.
clear
(
)
        
self
.
store
.
clear
(
)
    
def
__contains__
(
self
key
)
:
        
if
key
in
self
.
cache
:
            
return
True
        
if
key
in
self
.
store
:
            
return
True
        
return
False
    
def
__getitem__
(
self
key
)
:
        
try
:
            
return
self
.
cache
[
key
]
        
except
KeyError
:
            
pass
        
value
=
self
.
store
[
key
]
        
self
.
cache
[
key
]
=
value
        
return
value
    
def
get
(
self
key
default
=
None
)
:
        
"
"
"
Get
an
item
-
return
default
(
None
)
if
not
present
"
"
"
        
try
:
            
return
self
[
key
]
        
except
KeyError
:
            
return
default
    
def
__setitem__
(
self
key
value
)
:
        
self
.
cache
[
key
]
=
value
        
self
.
store
[
key
]
=
value
    
def
__delitem__
(
self
key
)
:
        
del
self
.
store
[
key
]
        
try
:
            
del
self
.
cache
[
key
]
        
except
KeyError
:
            
pass
    
def
__iter__
(
self
)
:
        
return
self
.
keys
(
)
    
def
keys
(
self
)
:
        
return
self
.
store
.
keys
(
)
    
def
values
(
self
)
:
        
return
self
.
store
.
values
(
)
    
def
items
(
self
)
:
        
return
self
.
store
.
items
(
)
class
WriteBackCacheManager
(
object
)
:
    
def
__init__
(
self
store
size
)
:
        
self
.
store
=
store
        
self
.
dirty
=
set
(
)
        
def
callback
(
key
value
)
:
            
if
key
in
self
.
dirty
:
                
self
.
store
[
key
]
=
value
                
self
.
dirty
.
remove
(
key
)
        
self
.
cache
=
lrucache
(
size
callback
)
    
def
size
(
self
size
=
None
)
:
        
return
self
.
cache
.
size
(
size
)
    
def
clear
(
self
)
:
        
self
.
cache
.
clear
(
)
        
self
.
dirty
.
clear
(
)
        
self
.
store
.
clear
(
)
    
def
__contains__
(
self
key
)
:
        
if
key
in
self
.
cache
:
            
return
True
        
if
key
in
self
.
store
:
            
return
True
        
return
False
    
def
__getitem__
(
self
key
)
:
        
try
:
            
return
self
.
cache
[
key
]
        
except
KeyError
:
            
pass
        
value
=
self
.
store
[
key
]
        
self
.
cache
[
key
]
=
value
        
return
value
    
def
get
(
self
key
default
=
None
)
:
        
"
"
"
Get
an
item
-
return
default
(
None
)
if
not
present
"
"
"
        
try
:
            
return
self
[
key
]
        
except
KeyError
:
            
return
default
    
def
__setitem__
(
self
key
value
)
:
        
self
.
cache
[
key
]
=
value
        
self
.
dirty
.
add
(
key
)
    
def
__delitem__
(
self
key
)
:
        
found
=
False
        
try
:
            
del
self
.
cache
[
key
]
            
found
=
True
            
self
.
dirty
.
remove
(
key
)
        
except
KeyError
:
            
pass
        
try
:
            
del
self
.
store
[
key
]
            
found
=
True
        
except
KeyError
:
            
pass
        
if
not
found
:
            
raise
KeyError
    
def
__iter__
(
self
)
:
        
return
self
.
keys
(
)
    
def
keys
(
self
)
:
        
for
key
in
self
.
store
.
keys
(
)
:
            
if
key
not
in
self
.
dirty
:
                
yield
key
        
for
key
in
self
.
dirty
:
            
yield
key
    
def
values
(
self
)
:
        
for
key
value
in
self
.
items
(
)
:
            
yield
value
    
def
items
(
self
)
:
        
for
key
value
in
self
.
store
.
items
(
)
:
            
if
key
not
in
self
.
dirty
:
                
yield
(
key
value
)
        
for
key
in
self
.
dirty
:
            
value
=
self
.
cache
.
peek
(
key
)
            
yield
(
key
value
)
    
def
sync
(
self
)
:
        
for
key
in
self
.
dirty
:
            
self
.
store
[
key
]
=
self
.
cache
.
peek
(
key
)
        
self
.
dirty
.
clear
(
)
    
def
flush
(
self
)
:
        
self
.
sync
(
)
        
self
.
cache
.
clear
(
)
    
def
__enter__
(
self
)
:
        
return
self
    
def
__exit__
(
self
exc_type
exc_val
exc_tb
)
:
        
self
.
sync
(
)
        
return
False
class
FunctionCacheManager
(
object
)
:
    
def
__init__
(
self
func
size
)
:
        
self
.
func
=
func
        
self
.
cache
=
lrucache
(
size
)
    
def
size
(
self
size
=
None
)
:
        
return
self
.
cache
.
size
(
size
)
    
def
clear
(
self
)
:
        
self
.
cache
.
clear
(
)
    
def
__call__
(
self
*
args
*
*
kwargs
)
:
        
kwtuple
=
tuple
(
(
key
kwargs
[
key
]
)
for
key
in
sorted
(
kwargs
.
keys
(
)
)
)
        
key
=
(
args
kwtuple
)
        
try
:
            
return
self
.
cache
[
key
]
        
except
KeyError
:
            
pass
        
value
=
self
.
func
(
*
args
*
*
kwargs
)
        
self
.
cache
[
key
]
=
value
        
return
value
def
lruwrap
(
store
size
writeback
=
False
)
:
    
if
writeback
:
        
return
WriteBackCacheManager
(
store
size
)
    
else
:
        
return
WriteThroughCacheManager
(
store
size
)
import
functools
class
lrudecorator
(
object
)
:
    
def
__init__
(
self
size
)
:
        
self
.
cache
=
lrucache
(
size
)
    
def
__call__
(
self
func
)
:
        
def
wrapper
(
*
args
*
*
kwargs
)
:
            
kwtuple
=
tuple
(
(
key
kwargs
[
key
]
)
for
key
in
sorted
(
kwargs
.
keys
(
)
)
)
            
key
=
(
args
kwtuple
)
            
try
:
                
return
self
.
cache
[
key
]
            
except
KeyError
:
                
pass
            
value
=
func
(
*
args
*
*
kwargs
)
            
self
.
cache
[
key
]
=
value
            
return
value
        
wrapper
.
cache
=
self
.
cache
        
wrapper
.
size
=
self
.
cache
.
size
        
wrapper
.
clear
=
self
.
cache
.
clear
        
return
functools
.
update_wrapper
(
wrapper
func
)
