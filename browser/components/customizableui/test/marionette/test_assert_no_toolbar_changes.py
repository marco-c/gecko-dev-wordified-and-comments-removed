from
marionette_harness
import
MarionetteTestCase
class
TestNoToolbarChanges
(
MarionetteTestCase
)
:
    
"
"
"
    
Test
that
toolbar
widgets
remain
in
the
same
order
over
several
restarts
of
the
browser
    
"
"
"
    
have_seen_import_button
=
False
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
    
def
get_area_widgets
(
self
area
)
:
        
return
self
.
marionette
.
execute_script
(
            
f
"
return
CustomizableUI
.
getWidgetIdsInArea
(
CustomizableUI
.
{
area
}
)
.
map
(
id
=
>
id
.
includes
(
'
spring
'
)
?
'
spring
'
:
id
)
"
        
)
    
def
get_area_default_placements
(
self
area
)
:
        
return
self
.
marionette
.
execute_script
(
            
f
"
return
CustomizableUI
.
getDefaultPlacementsForArea
(
CustomizableUI
.
{
area
}
)
"
        
)
    
def
check_toolbar_placements
(
self
)
:
        
self
.
assertEqual
(
            
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
            
self
.
get_area_default_placements
(
"
AREA_TABSTRIP
"
)
            
msg
=
"
AREA_TABSTRIP
placements
are
as
expected
"
        
)
        
navbarPlacements
=
self
.
get_area_default_placements
(
"
AREA_NAVBAR
"
)
        
navbarPlacements
.
append
(
"
unified
-
extensions
-
button
"
)
        
self
.
assertEqual
(
            
self
.
get_area_widgets
(
"
AREA_NAVBAR
"
)
            
navbarPlacements
            
msg
=
"
AREA_NAVBAR
placements
are
as
expected
"
        
)
        
actualBookmarkPlacements
=
self
.
get_area_widgets
(
"
AREA_BOOKMARKS
"
)
        
bookmarkPlacements
=
self
.
get_area_default_placements
(
"
AREA_BOOKMARKS
"
)
        
self
.
have_seen_import_button
=
(
            
self
.
have_seen_import_button
or
"
import
-
button
"
in
actualBookmarkPlacements
        
)
        
if
self
.
have_seen_import_button
:
            
self
.
assertEqual
(
                
actualBookmarkPlacements
                
[
"
import
-
button
"
]
+
bookmarkPlacements
                
msg
=
"
AREA_BOOKMARKS
placements
are
as
expected
"
            
)
        
else
:
            
self
.
assertEqual
(
                
actualBookmarkPlacements
                
bookmarkPlacements
                
msg
=
"
AREA_BOOKMARKS
placements
are
as
expected
"
            
)
        
self
.
assertEqual
(
            
self
.
get_area_widgets
(
"
AREA_ADDONS
"
)
            
self
.
get_area_default_placements
(
"
AREA_ADDONS
"
)
            
msg
=
"
AREA_ADDONS
placements
are
as
expected
"
        
)
        
self
.
assertEqual
(
            
self
.
get_area_widgets
(
"
AREA_FIXED_OVERFLOW_PANEL
"
)
            
self
.
get_area_default_placements
(
"
AREA_FIXED_OVERFLOW_PANEL
"
)
            
msg
=
"
AREA_FIXED_OVERFLOW_PANEL
placements
are
as
expected
"
        
)
    
def
test_no_toolbar_changes
(
self
)
:
        
self
.
check_toolbar_placements
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
check_toolbar_placements
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
check_toolbar_placements
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
check_toolbar_placements
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
check_toolbar_placements
(
)
        
self
.
marionette
.
restart
(
)
        
self
.
check_toolbar_placements
(
)
