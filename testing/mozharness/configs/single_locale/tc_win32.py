import
os
config
=
{
    
"
bootstrap_env
"
:
{
        
"
NO_MERCURIAL_SETUP_CHECK
"
:
"
1
"
        
"
MOZ_OBJDIR
"
:
"
%
(
abs_obj_dir
)
s
"
        
"
DIST
"
:
"
%
(
abs_obj_dir
)
s
"
        
"
L10NBASEDIR
"
:
"
.
.
/
.
.
/
l10n
"
        
"
TOOLTOOL_CACHE
"
:
os
.
environ
.
get
(
"
TOOLTOOL_CACHE
"
)
    
}
}
