Metainfo Templates
==================

This contains some more-complicated-than-it-should-be code for programatically setting 
the description Snap description by generating a `metainfo.xml` file from the project `README`
from within the `snapcraft` environment. It also will generate a `.desktop` file that has
some sophisticated name handling (e.g. `Godot Engine 4 (beta)` rather than just `Godot Engine`).

See the comment on the `metainfo` part in the `snapcraft.yaml` for a more thorough discussion.