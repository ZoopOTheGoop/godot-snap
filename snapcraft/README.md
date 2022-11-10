# Snapcraft directory

This directory contains files that are necessary outside the actual Snapcraft build pipeline.

In practice this more or less exclusively means `icon_outlined.svg` has to be here. I'd prefer
to pull it from the Godot repository programatically like we do with the desktop icon
rather than vendoring it for several reasons (if they change it it'd automatically be picked up, 
don't have to deal with potential copyright issues, etc), but as
far as I can tell `snapcraft` requires this file to actually exist locally.