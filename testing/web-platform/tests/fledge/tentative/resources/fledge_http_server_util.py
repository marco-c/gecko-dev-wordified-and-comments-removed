def
headersToAscii
(
headers
)
:
  
header_map
=
{
}
  
for
pair
in
headers
.
items
(
)
:
      
values
=
[
]
      
for
value
in
pair
[
1
]
:
          
values
.
append
(
value
.
decode
(
"
ASCII
"
)
)
      
header_map
[
pair
[
0
]
.
decode
(
"
ASCII
"
)
]
=
values
  
return
header_map
