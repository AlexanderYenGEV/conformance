from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.seasonal_overrides.seasonal_override_helper import preload_seasonal_override_data_for_filtering_helper

import json, os

tz = os.getenv("TZ")

@given("Seasonal override data is preloaded for filtering")
def preload_seasonal_override_data_for_filtering(preload_seasonal_override_data_for_filtering_helper):
    pass

@when(parsers.parse("the client requests a seasonal override with query period-start set to {offset} hours after the current time"))
def request_seasonal_override_with_period_start_offset(offset, client:TrolieClient):
    period_start = (datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=int(offset))).isoformat()
    client.set_query_param("period-start", period_start)
    return client.request("/seasonal-overrides")

@when(parsers.parse("the client requests a seasonal override with query period-end set to {offset} hours after the current time"))
def request_seasonal_override_with_period_end_offset(offset, client:TrolieClient):
    period_end = (datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=int(offset))).isoformat()
    client.set_query_param("period-end", period_end)
    return client.request("/seasonal-overrides")

@when(parsers.parse("the client requests a seasonal override with query monitoring-set set to {monitoring_set}"))
def request_seasonal_override_with_monitoring_set(monitoring_set, client:TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set)
    return client.request("/seasonal-overrides")

@when(parsers.parse("the client requests a seasoonal override with query segment for {segment}"))
def request_seasonal_override_with_segment(segment, client:TrolieClient):
    client.set_query_param("segment", segment)
    return client.request("/seasonal-overrides")

@then(parsers.parse("the response should include only seasonal overrides beginning at the current time plus {offset} hours"))
def verify_response_includes_only_seasonal_overrides_with_start_offset(offset, client:TrolieClient):
    expected_start_time = (datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=int(offset)))
    response = client.get_json()
    for segment in response:
        actual_start_time = datetime.fromisoformat(segment["start-time"])
        if actual_start_time >= expected_start_time:
            print(json.dumps(segment, indent=2))
        assert actual_start_time >= expected_start_time, f"Found seasonal override with start time {actual_start_time}, which is before the expected {expected_start_time}"

@then(parsers.parse("the response should include only seasonal overrides ending at the current time plus {offset} hours"))
def verify_response_includes_only_seasonal_overrides_with_end_offset(offset, client:TrolieClient):
    expected_end_time = (datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=int(offset)))
    response = client.get_json()
    for segment in response:
        actual_end_time = datetime.fromisoformat(segment["end-time"])
        if actual_end_time <= expected_end_time:
            print(json.dumps(segment, indent=2))
        assert actual_end_time <= expected_end_time, f"Found seasonal override with end time {actual_end_time}, which is after the expected {expected_end_time}"

@then(parsers.parse("the response should include only seasonal overrides for the monitoring set {monitoring_set}"))
def verify_response_includes_only_seasonal_overrides_with_monitoring_set(monitoring_set, client:TrolieClient):
    response = client.get_json()
    for segment in response:
        actual_monitoring_set = segment["source"]["provider"]
        if actual_monitoring_set == monitoring_set:
            print(json.dumps(segment, indent=2))
        assert actual_monitoring_set == monitoring_set, f"Found seasonal override with monitoring set {actual_monitoring_set}, expected {monitoring_set}"

@then(parsers.parse("the response should include only seasonal overrides for the segment {segment}"))
def verify_response_includes_only_seasonal_overrides_with_segment(segment, client:TrolieClient):
    response = client.get_json()
    for seg in response:
        actual_segment = seg["resource"]["resource-id"]
        if actual_segment == segment:
            print(json.dumps(seg, indent=2))
        assert actual_segment == segment, f"Found seasonal override with segment {actual_segment}, expected {segment}"