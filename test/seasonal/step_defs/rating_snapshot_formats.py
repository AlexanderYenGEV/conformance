from pytest_bdd import when
from test.helpers import TrolieClient


@when("the client requests the current Seasonal Limits Snapshot")
def request_seasonal_limits_snapshot(client: TrolieClient):
    return client.request("/seasonal-ratings/snapshot")
