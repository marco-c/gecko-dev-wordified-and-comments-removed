import
socket
def
invert_dict
(
dict
)
:
    
rv
=
{
}
    
for
key
values
in
dict
.
items
(
)
:
        
for
value
in
values
:
            
if
value
in
rv
:
                
raise
ValueError
            
rv
[
value
]
=
key
    
return
rv
class
HTTPException
(
Exception
)
:
    
def
__init__
(
self
code
message
=
"
"
)
:
        
self
.
code
=
code
        
self
.
message
=
message
def
_open_socket
(
host
port
)
:
    
sock
=
socket
.
socket
(
socket
.
AF_INET
socket
.
SOCK_STREAM
)
    
if
port
!
=
0
:
        
sock
.
setsockopt
(
socket
.
SOL_SOCKET
socket
.
SO_REUSEADDR
1
)
    
sock
.
bind
(
(
host
port
)
)
    
sock
.
listen
(
5
)
    
return
sock
def
is_bad_port
(
port
)
:
    
"
"
"
    
Bad
port
as
per
https
:
/
/
fetch
.
spec
.
whatwg
.
org
/
#
port
-
blocking
    
"
"
"
    
return
port
in
[
        
1
        
7
        
9
        
11
        
13
        
15
        
17
        
19
        
20
        
21
        
22
        
23
        
25
        
37
        
42
        
43
        
53
        
77
        
79
        
87
        
95
        
101
        
102
        
103
        
104
        
109
        
110
        
111
        
113
        
115
        
117
        
119
        
123
        
135
        
139
        
143
        
179
        
389
        
427
        
465
        
512
        
513
        
514
        
515
        
526
        
530
        
531
        
532
        
540
        
548
        
556
        
563
        
587
        
601
        
636
        
993
        
995
        
2049
        
3659
        
4045
        
6000
        
6665
        
6666
        
6667
        
6668
        
6669
        
6697
    
]
def
get_port
(
host
)
:
    
port
=
0
    
while
True
:
        
free_socket
=
_open_socket
(
host
0
)
        
port
=
free_socket
.
getsockname
(
)
[
1
]
        
free_socket
.
close
(
)
        
if
not
is_bad_port
(
port
)
:
            
break
    
return
port
