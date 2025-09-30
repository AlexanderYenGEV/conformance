from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient
from test.realtime.realtime_helpers import (
    get_limits_realtime_snapshot,
    get_regional_limits_realtime_snapshot
)

@when(parsers.parse("the client requests a real-time limits snapshot with monitoring-set filter {monitoring_set}"))
def filter_realtime_limits_snapshot_with_monitoring_set(client: TrolieClient, monitoring_set):
    client.set_query_param("monitoring-set", monitoring_set)
    get_limits_realtime_snapshot(client)

@when(parsers.parse("the client requests a regional limits real-time snapshot with monitoring-set filter {monitoring_set}"))
def filter_realtime_regional_limits_snapshot_with_monitoring_set(client: TrolieClient, monitoring_set):
    client.set_query_param("monitoring-set", monitoring_set)
    get_regional_limits_realtime_snapshot(client)

@when(parsers.parse("the client requests a real-time limits snapshot with resource-id filter {resource_id}"))
def filter_realtime_limits_snapshot_with_resource_id(client: TrolieClient, resource_id):
    client.set_query_param("resource-id", resource_id)
    get_limits_realtime_snapshot(client)

@when(parsers.parse("the client requests a regional limits real-time snapshot with resource-id filter {resource_id}"))
def filter_realtime_regional_limits_snapshot_with_resource_id(client: TrolieClient, resource_id):
    client.set_query_param("resource-id", resource_id)
    get_regional_limits_realtime_snapshot(client)




@then(parsers.parse("the response should include real-time limits snapshot for the monitoring-set {monitoring_set}"))
def realtime_limits_snapshot_includes_monitoring_set(client: TrolieClient, monitoring_set):
    # TODO  monitoring set isn't implemented yet in TROLIE Spec
    return

@then(parsers.parse("the response should include regional limits real-time snapshot for the monitoring-set {monitoring_set}"))
def realtime_regional_limits_snapshot_includes_monitoring_set(client: TrolieClient, monitoring_set):
    # TODO  monitoring set isn't implemented yet in TROLIE Spec
    return

@then(parsers.parse("the response should include real-time limits snapshot for the resource-id {resource_id}" ))
@then(parsers.parse("the repsonse should include regional limits real-time snapshot for the resource-id {resource_id}"))
def realtime_limits_snapshot_includes_resource_id(client: TrolieClient, resource_id):
    resources = client.get_json()["snapshot-header"]["power-system-resources"]
    assert resource_id in [resource["resource-id"] for resource in resources], f"Failed for resource {resource_id}"