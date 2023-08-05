# =====================================
# generator=datazen
# version=1.1.1
# hash=57b1ce2b72ca3267d6c18f6f8b25a5e7
# =====================================

"""
vbinds - Package definition for distribution.
"""

# third-party
from vmklib.setup import setup  # type: ignore

# internal
from vbinds import PKG_NAME, VERSION, DESCRIPTION


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
    url_override="https://github.com/vkottler/keybinds/tree/master/wow",
    console_overrides=["bapi=vbinds.entry:main"],
)
