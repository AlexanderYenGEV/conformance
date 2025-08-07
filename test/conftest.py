import os
import pytest

from test.helpers import Role, TrolieClient

from glob import glob


pytest_plugins = [
    "test.common.common_steps",
    "test.forecasting.step_defs",
    "test.realtime.step_defs",
]


def pytest_bdd_apply_tag(tag, function):
    using_mock = os.getenv("TROLIE_BASE_URL") == "http://localhost:4010"
    should_skip = tag == "prism_fail" and using_mock
    if should_skip or tag == "todo":
        reason = "Prism mock does not support this test" if using_mock else "TODO"
        marker = pytest.mark.skip(reason=reason)
        marker(function)
        return True
    else:
        # Fall back to the default behavior of pytest-bdd
        return None


def pytest_bdd_after_scenario(request, feature, scenario):
    if "skip_rate_limiting" in feature.tags or "skip_rate_limiting" in scenario.tags:
        return
    client: TrolieClient = request.getfixturevalue("client")
    if not getattr(client, "response", None):
        return
    if not request.session.shouldfail:
        if os.getenv("RATE_LIMITING"):
            if client.role == Role.UNAUTHENTICATED:
                assert client.get_response_header("X-Rate-Limit-Limit") == 0
                assert client.get_response_header("X-Rate-Limit-Remaining") == 0
                assert client.get_response_header("X-Rate-Limit-Reset") == 0
            else:
                assert client.get_response_header("X-Rate-Limit-Limit") > 0
                assert client.get_response_header("X-Rate-Limit-Remaining") > 0
                assert client.get_response_header("X-Rate-Limit-Reset") > 0

        if client.get_status_code() >= 200 and client.get_status_code() < 300:
            assert client.get_response_header("ETag")
