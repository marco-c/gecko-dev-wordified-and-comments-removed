import
sys
import
parse_histograms
import
json
from
collections
import
OrderedDict
def
main
(
argv
)
:
    
filenames
=
argv
    
all_histograms
=
OrderedDict
(
)
    
for
histogram
in
parse_histograms
.
from_files
(
filenames
)
:
        
name
=
histogram
.
name
(
)
        
parameters
=
OrderedDict
(
)
        
table
=
{
            
'
boolean
'
:
'
2
'
            
'
flag
'
:
'
3
'
            
'
enumerated
'
:
'
1
'
            
'
linear
'
:
'
1
'
            
'
exponential
'
:
'
0
'
            
'
count
'
:
'
4
'
        
}
        
parse_histograms
.
table_dispatch
(
histogram
.
kind
(
)
table
                                        
lambda
k
:
parameters
.
__setitem__
(
'
kind
'
k
)
)
        
if
histogram
.
low
(
)
=
=
0
:
            
parameters
[
'
min
'
]
=
1
        
else
:
            
parameters
[
'
min
'
]
=
histogram
.
low
(
)
        
try
:
            
buckets
=
histogram
.
ranges
(
)
            
parameters
[
'
buckets
'
]
=
buckets
            
parameters
[
'
max
'
]
=
buckets
[
-
1
]
            
parameters
[
'
bucket_count
'
]
=
len
(
buckets
)
        
except
parse_histograms
.
DefinitionException
:
            
continue
        
all_histograms
.
update
(
{
name
:
parameters
}
)
    
print
json
.
dumps
(
{
'
histograms
'
:
all_histograms
}
)
main
(
sys
.
argv
[
1
:
]
)
