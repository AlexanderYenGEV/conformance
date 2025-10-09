from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient, Header
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.seasonal_overrides.seasonal_override_helper import (
    preload_seasonal_override_data_for_filtering_helper, get_etag, 
    generate_seasonal_override_body_helper
)
from test.seasonal_overrides.step_defs.limits_formats import request_seasonal_override

import json, os

tz = os.getenv("TZ")

@given(parsers.parse("Seasonal override data is preloaded for caching"))
def preload_seasonal_override_data_for_caching(preload_seasonal_override_data_for_filtering_helper):
    pass

@given("the client obtained the current seasonal override with an ETag", target_fixture="etag")
def request_seasonal_override_and_get_etag(client:TrolieClient):
    return get_etag(request_seasonal_override(client))

@when("the client obtained the current seasonal override with an unknown ETag")
def request_seasonal_override_with_unknown_etag(client:TrolieClient):
    client.set_header(Header.If_None_Match, "Unknown-ETag")
    return request_seasonal_override(client)

@when("a seasonal override is updated")
def update_seasonal_override(client:TrolieClient, preload_seasonal_override_data_for_filtering_helper):
    id_to_update = preload_seasonal_override_data_for_filtering_helper[0]
    start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=10)
    end_time = start_time + timedelta(hours=1)
    resource_id = "DOUGLAS.1215.1"
    body = generate_seasonal_override_body_helper(start_time, end_time, resource_id)
    client.set_body(body)
    client.set_header("Content-Type", "application/vnd.trolie.seasonal-override.v1+json")
    client.request(f"/seasonal-overrides/{id_to_update}", method="PUT")
    client.set_header("Accept", "application/vnd.trolie.seasonal-override-set.v1+json")

@when("the client immediately issues a conditional GET for the same ETag")
def issue_conditional_get_for_same_etag(client:TrolieClient, etag):
    client.set_header(Header.If_None_Match, etag)
    return request_seasonal_override(client)

@then("the ETag in the response is different from the original ETag")
def check_etag_difference(client:TrolieClient, etag):
    previous_etag = etag
    current_etag = client.get_response_header("ETag")
    assert previous_etag != current_etag, f"ETag did not change after update: {previous_etag} == {current_etag}"