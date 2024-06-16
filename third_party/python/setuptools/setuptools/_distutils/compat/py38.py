import
sys
if
sys
.
version_info
<
(
3
9
)
:
    
def
removesuffix
(
self
suffix
)
:
        
if
suffix
and
self
.
endswith
(
suffix
)
:
            
return
self
[
:
-
len
(
suffix
)
]
        
else
:
            
return
self
[
:
]
    
def
removeprefix
(
self
prefix
)
:
        
if
self
.
startswith
(
prefix
)
:
            
return
self
[
len
(
prefix
)
:
]
        
else
:
            
return
self
[
:
]
else
:
    
def
removesuffix
(
self
suffix
)
:
        
return
self
.
removesuffix
(
suffix
)
    
def
removeprefix
(
self
prefix
)
:
        
return
self
.
removeprefix
(
prefix
)
