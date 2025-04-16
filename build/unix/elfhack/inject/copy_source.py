def
copy
(
out_file
in_path
)
:
    
with
open
(
in_path
)
as
fh
:
        
out_file
.
write
(
fh
.
read
(
)
)
