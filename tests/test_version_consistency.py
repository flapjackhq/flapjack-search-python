"""Version consistency checks for root and generated subpackages."""

from importlib import import_module

import flapjacksearch


SUBPACKAGE_NAMES = (
    "abtesting",
    "abtesting_v3",
    "analytics",
    "composition",
    "http",
    "ingestion",
    "insights",
    "monitoring",
    "personalization",
    "query_suggestions",
    "recommend",
    "search",
)


def test_generated_subpackages_use_root_runtime_version():
    for subpackage_name in SUBPACKAGE_NAMES:
        module = import_module(f"flapjacksearch.{subpackage_name}")
        assert module.__version__ == flapjacksearch.__version__
