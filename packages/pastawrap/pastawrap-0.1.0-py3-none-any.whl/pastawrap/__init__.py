import sys
try:
    import rpy2
except:
    print("Failed to load rpy2! It's possible that R isn't installed.\n", file=sys.stderr)
    raise
from .utility import r_install_packages
from .utility import r_ggsave
from .pastawrap import RatPasta


__all__ = [
    "RatPasta",
    "r_ggsave",
    "r_install_packages",
]