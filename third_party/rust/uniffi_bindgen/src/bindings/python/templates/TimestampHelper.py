Timestamp
=
datetime
.
datetime
class
_UniffiConverterTimestamp
(
_UniffiConverterRustBuffer
)
:
    
staticmethod
    
def
read
(
buf
)
:
        
seconds
=
buf
.
read_i64
(
)
        
microseconds
=
buf
.
read_u32
(
)
/
1000
        
if
seconds
>
=
0
:
            
return
datetime
.
datetime
.
fromtimestamp
(
0
tz
=
datetime
.
timezone
.
utc
)
+
datetime
.
timedelta
(
seconds
=
seconds
microseconds
=
microseconds
)
        
else
:
            
return
datetime
.
datetime
.
fromtimestamp
(
0
tz
=
datetime
.
timezone
.
utc
)
-
datetime
.
timedelta
(
seconds
=
-
seconds
microseconds
=
microseconds
)
    
staticmethod
    
def
check_lower
(
value
)
:
        
pass
    
staticmethod
    
def
write
(
value
buf
)
:
        
if
value
>
=
datetime
.
datetime
.
fromtimestamp
(
0
datetime
.
timezone
.
utc
)
:
            
sign
=
1
            
delta
=
value
-
datetime
.
datetime
.
fromtimestamp
(
0
datetime
.
timezone
.
utc
)
        
else
:
            
sign
=
-
1
            
delta
=
datetime
.
datetime
.
fromtimestamp
(
0
datetime
.
timezone
.
utc
)
-
value
        
seconds
=
delta
.
seconds
+
delta
.
days
*
24
*
3600
        
nanoseconds
=
delta
.
microseconds
*
1000
        
buf
.
write_i64
(
sign
*
seconds
)
        
buf
.
write_u32
(
nanoseconds
)
