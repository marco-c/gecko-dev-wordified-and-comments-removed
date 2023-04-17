"
"
"
Translates
policy_templates
.
json
files
.
"
"
"
from
__future__
import
print_function
from
grit
.
node
import
structure
def
Format
(
root
lang
=
'
en
'
output_dir
=
'
.
'
)
:
  
policy_json
=
None
  
for
item
in
root
.
ActiveDescendants
(
)
:
    
with
item
:
      
if
(
isinstance
(
item
structure
.
StructureNode
)
and
          
item
.
attrs
[
'
type
'
]
=
=
'
policy_template_metafile
'
)
:
        
json_text
=
item
.
gatherer
.
Translate
(
            
lang
            
pseudo_if_not_available
=
item
.
PseudoIsAllowed
(
)
            
fallback_to_english
=
item
.
ShouldFallbackToEnglish
(
)
)
        
assert
not
policy_json
        
policy_json
=
json_text
  
return
policy_json
