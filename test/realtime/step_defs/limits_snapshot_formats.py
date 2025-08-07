from pytest_bdd import given, when
from test.helpers import TrolieClient

@when("the client requests for the current real-time snapshot")
def request_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/realtime-snapshot")

@when("the client requests for the current regional real-time snapshot")
def request_regional_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/regional/realtime-snapshot")