from
__future__
import
absolute_import
print_function
import
shutil
import
contextlib
import
tempfile
contextlib
.
contextmanager
def
tempdir
(
)
:
    
dest_dir
=
tempfile
.
mkdtemp
(
)
    
try
:
        
yield
dest_dir
    
finally
:
        
shutil
.
rmtree
(
dest_dir
ignore_errors
=
True
)
