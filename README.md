Godot Snap
==========

Godot is a free, open source game engine, that can export to web, mobile, 
Linux, MacOS, Windows, Android, iOS, and, soon, several game consoles.
For more information on Godot itself, see [the main engine repository].

[the main engine repository]: https://github.com/godotengine/godot)

This snap provides a way to get Godot via `snap insall`, with the benefits
of a snap such as application sandboxing and dependency pinning. 

<!-- Uncomment below when before we officially publish to snapcraft -->
<!--To get as a user, please use `snap install godot 4.x/beta` (or `snap install godot 3.x/stable`.-->

Godot 3 and 4 are released in the same snap under different tracks. So Godot 4 is `godot 4.x/beta`
and Godot 3 is `godot 3.x/[stable|beta]`. The `latest` channel is not used as what should count as "latest"
is not clear given Godot 4 is close to release. Likely as 4 hits stable, the `latest` channel will mirror the `4.x`
channel.

## Where are my projects stored?

Since Snaps are sandboxed, Godot opens its own apparent home folder from within the Snap. 
From the perspective of a user, this should be under `$HOME/snap/godot/common/` - 
if you need to add assets to Godot, they should also be there since 
Godot can't "see" outside its environment. 

## Known/Potential Issues

- Certain game controllers are unlikely to work, this is due to a lack of custom `udev` rule support in `snapd`. 
This should not apply to exported games run outside the Snap environment, but running a preview
build from within the editor is unlikely to provide the desired results until this is sorted
out (likely within the next 6 months, it's on the roadmap).
- Some GDNative/GDPlugin extensions may not work properly if they require dynamic libraries 
that do not exist in the Snap environment. For best results, statically link your plugins where possible.
If needed, you should also be able to place the `.so` files next to your 
plugin in the `$HOME/snap/godot/common/` tree and manually set your `LD_LIBRARY_PATH` to point there.
However, in some limited cases (particularly if you link against graphics APIs), you may end up with
a version conflict if the libraries used when building are not exactly the same as those 
in the snap environment.
- This may or may not complicate certain specific workflows unless you do some tinkering, 
(untested, but pottentially various Godot-Blender tools, or VS Code Godot integration etc),  
as both of these programs as Snaps means they inhabit their own sandboxed environment and may not
be able to communicate via direct API without using either the shell or specific `dbus` interfaces.

## Github stuff

To mirror the current state of the Godot engine, the `master` branch hosts the Godot 4 `snapcraft.yaml` 
and the Godot 3 snap is on the `3.x-stable` branch. In the future, `beta` and `edge` branches 
may be added for both Godot 3 and 4 (depending on whether `3.x` is dropped and whether 
it becomes easier to automatically discover stable and beta git commits like there are 
with tags and branches for `stable`). Realistically, the only meaningful change to the `snapcraft.yaml` files
is the git tag to pull the `godot` part from.

To build as a developer, simply run `snapcraft`, and then install the 
resulting snap with `snap install --dangerous godot-<version>.snap` 
(e.g. instance `godot-4.0.0.snap`).