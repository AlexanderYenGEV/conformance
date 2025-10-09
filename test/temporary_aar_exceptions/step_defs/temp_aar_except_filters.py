from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.temporary_aar_exceptions.temp_aar_except_helpers import preload_temporary_aar_exception_data_helper      
import os, json

@given("the Temporary AAR Exception data is preloaded")
def preload_temporary_aar_exception_data(preload_temporary_aar_exception_data_helper):
    pass

@when(parsers.parse("the client requests Temporary AAR Exceptions with `period-start` with {offset} hours from now"))
def request_temporary_aar_exceptions_with_query_period_start(client: TrolieClient, offset): 
    client.set_header("Accept", "application/vnd.trolie.temporary-aar-exception-set.v1+json")
    period_start = datetime.now(ZoneInfo(os.getenv("TZ"))).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1) # Current time rounded up
    period_start_offset = (period_start + timedelta(hours=int(offset))).isoformat()
    print("Period-start requested: ", period_start_offset)
    client.set_query_param("period-start", period_start_offset)
    return client.request("/temporary-aar-exceptions")

@when(parsers.parse("the client requests Temporary AAR Exceptions with `period-end` with {offset} hours from now"))
def request_temporary_aar_exceptions_with_query_period_end(client: TrolieClient, offset):
    client.set_header("Accept", "application/vnd.trolie.temporary-aar-exception-set.v1+json")
    period_end = datetime.now(ZoneInfo(os.getenv("TZ"))).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1) # Current time rounded up
    period_end_offset = (period_end + timedelta(hours=int(offset))).isoformat()
    print("Period-end requested: ", period_end_offset)
    client.set_query_param("period-end", period_end_offset)
    return client.request("/temporary-aar-exceptions")

@when(parsers.parse("the client requests Temporary AAR Exceptions with query `monitoring-set` {monitoring_set}"))
def request_temporary_aar_exceptions_with_query_monitoring_set(client: TrolieClient, monitoring_set):
    client.set_header("Accept", "application/vnd.trolie.temporary-aar-exception-set.v1+json")
    print("Monitoring-set requested: ", monitoring_set)
    client.set_query_param("monitoring-set", monitoring_set)
    return client.request("/temporary-aar-exceptions")

@when(parsers.parse("the client requests Temporary AAR Exceptions with `segment` query {segment}"))
def query_temporary_aar_exception_with_segment(client: TrolieClient, segment):
    client.set_query_param("segment", segment)
    return client.request("/temporary-aar-exceptions")

@then(parsers.parse("the response should only include Temporary AAR Exceptions with `period-start` at {offset} hours or after"))
def check_temporary_aar_exception_response_query_period_start(client: TrolieClient, offset):
    period_start = datetime.fromisoformat(client.get_query_param("period-start"))
    response = client.get_json()
    print(json.dumps(response, indent=2))
    if not response: return
    for time in response:
        assert datetime.fromisoformat(time["start-time"]) >= period_start, f"Period-start {time['start-time']} is before the queried period-start {period_start}"

@then(parsers.parse("the response should only include Temporary AAR Exceptions with `period-end` at {offset} hours or before"))
def check_temporary_aar_exception_response_query_period_end(client: TrolieClient, offset):
    period_end = datetime.fromisoformat(client.get_query_param("period-end"))
    response = client.get_json()
    print(json.dumps(response, indent=2))
    if not response: return
    for time in response:
        assert datetime.fromisoformat(time["end-time"]) <= period_end, f"Period-end {time['end-time']} is after the queried period-end {period_end}"

@then(parsers.parse("the response should only include Temporary AAR Exceptions under the `monitoring-set` {monitoring_set}"))
def check_temporary_aar_exceptions_response_query_monitoring_set(client: TrolieClient, monitoring_set):
    response = client.get_json()
    print(json.dumps(response, indent=2))
    if not response: return
    for resource in response:
        assert resource["source"]["provider"] == monitoring_set, f"Monitoring-set {resource['source']['provider']} does not match queried monitoring-set {monitoring_set}"

@then(parsers.parse("the response should only include Temporary AAR Exceptions for the segment {segment}"))
def check_temporary_aar_exception_response_query_segment(client: TrolieClient, segment):
    response = client.get_json()
    print(json.dumps(response, indent=2))
    if not response: return
    for resource in response:
        assert resource["resource"]["resource-id"] == segment, f"Resource ID {resource['resource']['resource-id']} does not match segment {segment}"