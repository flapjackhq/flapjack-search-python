# coding: utf-8

from importlib import import_module
from pkgutil import iter_modules

# The canonical version of the flapjacksearch package.
__version__ = "1.0.0"


def _sync_generated_subpackage_versions() -> None:
    """Keep generated subpackage runtime versions aligned with the root package.

    Generated clients stamp an OpenAPI spec version (for example ``4.36.0``)
    into each top-level subpackage ``__init__``. At runtime, consumers expect
    ``flapjacksearch.<subpackage>.__version__`` to match the distributable
    package version exposed by ``flapjacksearch.__version__``.
    """

    for module_info in iter_modules(__path__):
        if not module_info.ispkg:
            continue
        module = import_module(f"{__name__}.{module_info.name}")
        if hasattr(module, "__version__"):
            module.__version__ = __version__


_sync_generated_subpackage_versions()
