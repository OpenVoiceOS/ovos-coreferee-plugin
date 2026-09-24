# START_VERSION_BLOCK
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_BUILD = 1
VERSION_ALPHA = 1
# END_VERSION_BLOCK

# Computed from the block above, which the release automation edits.
# `pyproject.toml` reads this attribute, so the two stay in step and the
# version lives in one place.
__version__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_BUILD}"
if VERSION_ALPHA:
    __version__ += f"a{VERSION_ALPHA}"
