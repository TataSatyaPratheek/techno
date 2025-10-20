import os
from importlib import metadata

# Development layout keeps sources under `src/techno`. When the package
# is installed as a wheel it may include a `src/techno` directory inside
# site-packages; ensure the top-level package `techno` forwards to that
# location so `import techno` works regardless of whether code lives in
# `techno/` or `src/techno/`.
_here = os.path.dirname(__file__)
_maybe_src = os.path.join(_here, "src", "techno")
if os.path.isdir(_maybe_src) and _maybe_src not in __path__:
    __path__.insert(0, _maybe_src)

try:
    __version__ = metadata.version("techno")
except Exception:
    # fallback when running from source
    __version__ = "0.1.0"
