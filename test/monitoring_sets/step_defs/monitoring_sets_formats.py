from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient

@when(parsers.parse("the client requests for a specific monitoring set by identifier `{identifier}`"))
def request_monitoring_set_by_identifier(identifier, client : TrolieClient):
    return client.request(f"/monitoring-sets/{identifier}")

@when(parsers.parse("the client requests for their default monitoring set"))
def request_default_monitoring_set(client: TrolieClient):
    return client.request("/default-monitoring-set")

@then(parsers.parse("the response should only power system resources by the provider `{identifier}`"))
def verify_monitoring_set_only_contains_provider(identifier, client: TrolieClient):
    id = client.get_json()["id"]
    assert id == identifier