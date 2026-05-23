"""Version consistency checks for root and generated subpackages."""

from importlib import import_module
from pkgutil import iter_modules

import flapjacksearch


def _generated_subpackage_names():
    """Discover current generated top-level subpackages from the package tree."""

    return tuple(
        sorted(
            module_info.name
            for module_info in iter_modules(flapjacksearch.__path__)
            if module_info.ispkg
        )
    )


def test_generated_subpackages_use_root_runtime_version():
    subpackage_names = _generated_subpackage_names()

    # Guard against a vacuous pass if package generation/output changes unexpectedly.
    assert subpackage_names

    for subpackage_name in subpackage_names:
        module = import_module(f"flapjacksearch.{subpackage_name}")
        assert module.__version__ == flapjacksearch.__version__
