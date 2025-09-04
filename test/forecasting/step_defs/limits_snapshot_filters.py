import json
from pytest_bdd import given, when, then, parsers
from dateutil import parser
from test.helpers import TrolieClient
from datetime import datetime, timedelta
from test.forecasting.forecast_helpers import (
    get_forecast_limits_snapshot,
    get_historical_limits_forecast_snapshot,
    get_regional_limits_forecast_snapshot,
    get_todays_iso8601_for,
    round_up_to_next_hour,
)

@given(parsers.parse("the current wall clock time at the Clearinghouse today is set to the user's current time"))
def set_clearinghouse_time_to_user_time(client: TrolieClient):
    user_time = datetime.now().astimezone()
    client.set_server_time(user_time.isoformat())

@given(parsers.parse("the period requested is set to {period_requested}"))
def set_historical_forecast_period(period_requested, client: TrolieClient):
    return client.request(f"limits/forecast-snapshot/{period_requested}")

@given(parsers.parse("the period requested is set to {period_requested}"))
def set_historical_forecast_period(period_requested, client: TrolieClient):
    return client.request(f"limits/forecast-snapshot/{period_requested}")
    
@when(parsers.parse("the client requests historical forecast limits with `offset-period-start` for an hour from then at {request_offset_time}"))
def historical_forecast_snapshot_request_filter_offset_period_start(request_offset_time, client: TrolieClient):
    client.set_query_param("offset-period-start", get_todays_iso8601_for(request_offset_time))
    get_historical_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with `offset-period-start` for an hour from then at {request_offset_time}"))
def regional_forcast_snapshot_request_filter_offset_period_start(request_offset_time, client: TrolieClient):
    client.set_query_param("offset-period-start", get_todays_iso8601_for(request_offset_time))
    get_regional_limits_forecast_snapshot(client)


@when(parsers.parse("the client requests forecast limits with `offset-period-start` set to {offset_hours} after the current time"))
def forecast_snapshot_request_filter_offset_period_start(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("offset-period-start", request_time.isoformat())
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests forecast limits with `period-end` set to {offset_hours} after the current time"))
def forecast_snapshot_request_filter_period_end(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("period-end", request_time.isoformat())
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests historical forecast limits with `offset-period-start` set to {offset_hours} after the current time"))
def historical_forecast_snapshot_request_filter_offset_period_start(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("offset-period-start", request_time.isoformat())
    get_historical_limits_forecast_snapshot(client) 

@when(parsers.parse("the client requests historical forecast limits with `period-end` set to {offset_hours} after the current time"))
def historical_forecast_snapshot_request_filter_period_end(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("period-end", request_time.isoformat())
    get_historical_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with `offset-period-start` set to {offset_hours} after the current time"))
def regional_forecast_snapshot_request_filter_offset_period_start(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("offset-period-start", request_time.isoformat())
    get_regional_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with `period-end` set to {offset_hours} after the current time"))
def regional_forecast_snapshot_request_filter_period_end(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    request_time = parser.isoparse(client.get_server_time()) + offset
    client.set_query_param("period-end", request_time.isoformat())
    get_regional_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests forecast limits with static-only set to true"))
def forecast_snapshot_request_filter_static_only(client: TrolieClient):
    client.set_query_param("static-only", "true")
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests historical forecast limits with static-only set to true"))
def historical_snapshot_request_filter_static_only(client: TrolieClient):
    client.set_query_param("static-only", "true")
    get_historical_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with static-only set to true"))
def regional_forecast_snapshot_request_filter_static_only(client: TrolieClient):
    client.set_query_param("static-only", "true")
    get_regional_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests forecast limits with monitoring-set filter {monitoring_set_id}"))
def forecast_snapshot_request_filter_monitoring_set(monitoring_set_id, client: TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set_id)
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests historical forecast limits with monitoring-set filter {monitoring_set_id}"))
def historical_forecast_snapshot_request_filter_monitoring_set(monitoring_set_id, client: TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set_id)
    get_historical_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with monitoring-set filter {monitoring_set_id}"))
def regional_forecast_snapshot_request_filter_monitoring_set(monitoring_set_id, client: TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set_id)
    get_regional_limits_forecast_snapshot(client)


@when(parsers.parse("the client requests forecast limits with resource-id filter {resource_id}"))
def forecast_snapshot_request_filter_resource_id(resource_id, client: TrolieClient):
    client.set_query_param("resource-id-filter", resource_id)
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests historical forecast limits with resource-id filter {resource_id}"))
def historical_forecast_snapshot_request_filter_resource_id(resource_id, client : TrolieClient):
    client.set_query_param("resource-id", resource_id)
    get_historical_limits_forecast_snapshot(client)
    
@when(parsers.parse("the client requests regional forecast limits with resource-id filter {resource_id}"))
def regional_forecast_snapshot_request_filter_resource_id(resource_id, client: TrolieClient):
    client.set_query_param("resource-id", resource_id)
    get_regional_limits_forecast_snapshot(client)

@then(parsers.parse("the response should include only forecast limits beginning at the current time plus {offset_hours}, in the server's time zone"))
def forecast_snapshot_request_first_period_starts_on(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    exact_expected_start = (parser.isoparse(client.get_server_time()) + offset).isoformat()
    rounded_expected_start = round_up_to_next_hour(parser.isoparse(exact_expected_start)).isoformat()
    limits = client.get_json()["limits"]
    targets = ((entry["resource-id"], entry["periods"][0]["period-start"]) for entry in limits)
    print("Expected start time: ", exact_expected_start)
    for resource_id, period_start in targets:
        print("Period start: ", period_start)
        assert parser.isoparse(rounded_expected_start) == parser.isoparse(period_start), f"Failed for resource {resource_id}"

@then(parsers.parse("the response should include forecast limits up to the current time plus {offset_hours}, in the server's time zone"))
def forecast_snapshot_request_last_period_includes(offset_hours, client: TrolieClient):
    offset = timedelta(hours=int(offset_hours))
    exact_expected_end = (parser.isoparse(client.get_server_time()) + offset).isoformat()
    rounded_expected_end = round_up_to_next_hour(parser.isoparse(exact_expected_end)).isoformat()
    limits = client.get_json()["limits"]
    targets = ((limits_entry["resource-id"], limits_entry["periods"][-1]["period-end"]) for limits_entry in limits)
    print("Expected end time: ", exact_expected_end)
    for resource_id, period_end in targets:
        print("Period end: ", period_end)
        assert parser.isoparse(rounded_expected_end) == parser.isoparse(period_end), f"Failed for resource {resource_id}"
        
@then(parsers.parse("the response should include only static forecast limits"))
def forecast_snapshot_request_only_static(client: TrolieClient):
    limits = client.get_json()["limits"]
    targets = ((limits_entry["resource-id"], limits_entry["periods"]) for limits_entry in limits)
    for resource_id, periods in targets:
        for period in periods:
            # a static-only forecast limit should have a period of at least 2 hours
            # this is more a heuristic than a guarantee, but it should be true for all static limits
            start = datetime.fromisoformat(period["period-start"])
            end = datetime.fromisoformat(period["period-end"])
            assert (end - start) >= timedelta(hours=2), f"Failed for resource {resource_id}"


monitoring_sets = {"default": ["8badf00d"]}


@then(parsers.parse("the response should include forecast limits for the monitoring set {monitoring_set_id}"))
def forecast_snapshot_request_monitoring_set_includes(monitoring_set_id, client: TrolieClient):
    resources = client.get_json()["snapshot-header"]["power-system-resources"]
    for resource in resources:
        assert resource["resource-id"] in monitoring_sets[monitoring_set_id], f"Failed for resource {resource['resource-id']}"


@then(parsers.parse("the response should include forecast limits for the resource id {resource_id}"))
def forecast_snapshot_contains_requested_resource(resource_id, client: TrolieClient):
    resources = client.get_json()["snapshot-header"]["power-system-resources"]
    assert resource_id in [resource["resource-id"] for resource in resources], f"Failed for resource {resource_id}"



