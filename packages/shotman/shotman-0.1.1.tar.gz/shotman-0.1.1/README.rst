shotman
=======

A simple UI for handling screenshots.

Installation
------------

- ArchLinux: ``yay install shotman``.
- Others: ``pip install shotman``.

Setup
-----

You'll generally want to bind shotman to some hotkeys. I keep this in my sway
settings::

    # Screenshots:
    # Super+P: Current window
    # Super+Shift+p: Select area
    # Super+Alt+p Current output
    # Super+Ctrl+p Select a window

    bindsym Mod4+p       exec shotman active
    bindsym Mod4+Shift+p exec shotman area
    bindsym Mod4+Mod1+p  exec shotman output
    bindsym Mod4+Ctrl+p  exec shotman window

Note: the above supercedes the recommendation given by `grimshot`. Make sure you don't
have both on your config file.

I also recommend adding settings to position it on-screen. If you skip this, the window
will show up centred, since Wayland clients cannot control their position::

    for_window [title="shotman"] move position 30 30

It is currently not clear if this application should be exceptional and use a
privileged API or not.

Usage
-----

``shotman`` runs and immediately shows the screenshot. Note that, since shotman uses
``grimshot`` under the hood, you image is saved to disk already by default.

Actions
~~~~~~~

You can execute the same actions with a mouse _or_ keyboard:

- **Done**: Exits. The screenshot images remains on disk.
  - Primary Keybinding: ``Esc``.
  - Secundary Keybindings: ``Ctrl+q``, ``Ctrl+w``, ``q``.
- **Delete**: Deletes the image file and exists immediately.
  - Keybinding: ``d``.
  - Secundary Keybindings: ``Delete``, ``Ctrl+d``.
- **Copy**: Copies the screenshot image to the clipboard. See caveats below.
  - Keybinding: ``Ctrl+C``.

If there's a good, lightweight image editor that runs well on Wayland, I'd be happy to
add an ``Edit`` button that opens the screenshot image in it.

Caveats
-------

If you're not using a clipboard manager, any copied image will be lost after closing
the window.

There are plants to keep the application running in the background until it loses the
clipboard handle to work around this.

Licence
-------

``shotman`` is licensed under the ISC licence. See LICENCE for details.
