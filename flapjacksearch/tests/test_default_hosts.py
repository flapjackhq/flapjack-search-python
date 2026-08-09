from flapjacksearch.abtesting.config import AbtestingConfig
from flapjacksearch.abtesting_v3.config import AbtestingV3Config
from flapjacksearch.analytics.config import AnalyticsConfig
from flapjacksearch.composition.config import CompositionConfig
from flapjacksearch.ingestion.config import IngestionConfig
from flapjacksearch.monitoring.config import MonitoringConfig
from flapjacksearch.personalization.config import PersonalizationConfig
from flapjacksearch.query_suggestions.config import QuerySuggestionsConfig
from flapjacksearch.recommend.config import RecommendConfig


def configured_host_urls(config) -> tuple[list[str], list[str]]:
    config.set_default_hosts()
    assert config.hosts is not None
    return (
        sorted(host.url for host in config.hosts.read()),
        sorted(host.url for host in config.hosts.write()),
    )


def test_analytics_service_nil_region_default_hosts_use_flapjack_domains() -> None:
    # The nil-region branch is a distinct selector from the regional branch;
    # assert it explicitly so a regression on either side fails.
    for config_class in (AbtestingConfig, AbtestingV3Config, AnalyticsConfig):
        config = config_class("app", "key")
        assert configured_host_urls(config) == (
            ["analytics.flapjack.io"],
            ["analytics.flapjack.io"],
        )


def test_analytics_service_regional_default_hosts_use_flapjack_domains() -> None:
    cases = [
        (AbtestingConfig("app", "key", "de"), "analytics.de.flapjack.io"),
        (AbtestingV3Config("app", "key", "de"), "analytics.de.flapjack.io"),
        (AnalyticsConfig("app", "key", "us"), "analytics.us.flapjack.io"),
    ]

    for config, expected_url in cases:
        assert configured_host_urls(config) == ([expected_url], [expected_url])


def test_search_style_default_hosts_use_flapjack_domains() -> None:
    expected_read_urls = [
        "app-1.flapjack.io",
        "app-2.flapjack.io",
        "app-3.flapjack.io",
        "app-dsn.flapjack.io",
    ]
    expected_write_urls = [
        "app-1.flapjack.io",
        "app-2.flapjack.io",
        "app-3.flapjack.io",
        "app.flapjack.io",
    ]

    assert configured_host_urls(CompositionConfig("app", "key")) == (
        expected_read_urls,
        expected_write_urls,
    )
    assert configured_host_urls(RecommendConfig("app", "key")) == (
        expected_read_urls,
        expected_write_urls,
    )


def test_required_region_default_hosts_use_flapjack_domains() -> None:
    cases = [
        (IngestionConfig("app", "key", "eu"), "data.eu.flapjack.io"),
        (
            PersonalizationConfig("app", "key", "us"),
            "personalization.us.flapjack.io",
        ),
        (
            QuerySuggestionsConfig("app", "key", "eu"),
            "query-suggestions.eu.flapjack.io",
        ),
    ]

    for config, expected_url in cases:
        assert configured_host_urls(config) == ([expected_url], [expected_url])


def test_monitoring_default_hosts_use_flapjack_domains() -> None:
    assert configured_host_urls(MonitoringConfig("app", "key")) == (
        ["status.flapjack.io"],
        ["status.flapjack.io"],
    )
