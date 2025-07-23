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
)


@given(parsers.parse("the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., {server_time}"))
def clearinghouse_wall_clock_today_at_11amGMT(server_time, client: TrolieClient):
    client.set_header(
        "X-TROLIE-Testing-Current-DateTime",
        get_todays_iso8601_for(server_time),
    )

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

@when(parsers.parse("the client requests forecast limits with `offset-period-start` for an hour from then at {request_offset_time}"))
def forecast_snapshot_request_filter_offset_period_start(request_offset_time, client: TrolieClient):
    client.set_query_param("offset-period-start", get_todays_iso8601_for(request_offset_time))
    get_forecast_limits_snapshot(client)


@when(parsers.parse("the client requests forecast limits with period-end {request_last_period}"))
def forecast_snapshot_request_filter_last_period(request_last_period, client: TrolieClient):
    client.set_query_param("period-end", get_todays_iso8601_for(request_last_period))
    get_forecast_limits_snapshot(client)

@when(parsers.parse("the client requests historical forecast limits with period-end {request_last_period}"))
def historical_forecast_snapshot_request_filter_last_period(request_last_period, client: TrolieClient):
    client.set_query_param("period-end", get_todays_iso8601_for(request_last_period))
    get_historical_limits_forecast_snapshot(client)

@when(parsers.parse("the client requests regional forecast limits with period-end {request_last_period}"))
def regional_forecast_snapshot_request_filter_last_period(request_last_period, client: TrolieClient):
    client.set_query_param("period-end", get_todays_iso8601_for(request_last_period))
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

@then(parsers.parse("the response should only include forecast limits starting at the `offset-period-start` in the server's time zone, i.e., {response_first_period}"))
def forecast_snapshot_request_first_period_starts_on(response_first_period, client: TrolieClient):
    expected_start = get_todays_iso8601_for(response_first_period)
    # print(client.get_json())
    limits = client.get_json()["limits"]
    targets = ((entry["resource-id"], entry["periods"][0]["period-start"]) for entry in limits)
    for resource_id, period_start in targets:
        assert parser.isoparse(expected_start) == parser.isoparse(period_start), f"Failed for resource {resource_id}"


@then(parsers.parse("the response should include forecast limits up to {response_last_period} in the server's time zone"))
def forecast_snapshot_request_last_period_includes(response_last_period, client: TrolieClient):
    expected_end = get_todays_iso8601_for(response_last_period)
    limits = client.get_json()["limits"]
    targets = ((limits_entry["resource-id"], limits_entry["periods"][-1]["period-end"]) for limits_entry in limits)
    for resource_id, period_end in targets:
        assert parser.isoparse(expected_end) == parser.isoparse(period_end), f"Failed for resource {resource_id}"


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

#todo
@then(parsers.parse("see output {response_first_period}"))
def forecase_snapshot_request_past_period(response_first_period, client: TrolieClient):
    expected_start = get_todays_iso8601_for(response_first_period)
    print("Expected value: ", expected_start)
    limits = client.get_json()["limits"]
    print(limits)
    targets = ((entry["resource-id"], entry["periods"][0]["period-start"]) for entry in limits)
    for resource_id, period_start in targets:
        assert expected_start == period_start, f"Failed for resource {resource_id}"


