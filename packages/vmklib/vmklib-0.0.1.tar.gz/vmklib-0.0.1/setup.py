# =====================================
# generator=datazen
# version=1.1.0
# hash=859b7dd9ac509e4bbc49dda6bf787c74
# =====================================

"""
vmklib - Package definition for distribution.
"""

# internal
from vmklib import PKG_NAME, VERSION, DESCRIPTION
from vmklib.setup import setup


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
)
