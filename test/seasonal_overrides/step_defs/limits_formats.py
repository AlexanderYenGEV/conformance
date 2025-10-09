from pytest_bdd import given, when, parsers
from test.helpers import TrolieClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.seasonal_overrides.seasonal_override_helper import generate_seasonal_override_body_helper, preload_seasonal_override_data_helper

import json, os

tz = os.getenv("TZ")

@given(parsers.parse("the Seasonal Override body is generated"))
def generate_seasonal_override_body(client: TrolieClient):
    start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=5)
    end_time = start_time + timedelta(seconds=30)
    resource_id = "HEARN.34562.1"
    body = generate_seasonal_override_body_helper(start_time, end_time, resource_id)
    client.set_body(body)
    print(json.dumps(body, indent=2))

@given(parsers.parse("Seasonal Override data is preloaded"))
def preload_seasonal_override_data(preload_seasonal_override_data_helper):
    pass

@given(parsers.parse("a Seasonal Override is created"), target_fixture="id")
def create_seasonal_override(client: TrolieClient):
    start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)
    end_time = start_time + timedelta(hours=1)
    resource_id = "HEARN.34562.1"
    body = generate_seasonal_override_body_helper(start_time, end_time, resource_id)
    client.set_body(body)
    client.set_header("Content-Type", "application/vnd.trolie.seasonal-override.v1+json")
    response = client.request("/seasonal-overrides", method="POST")
    assert response.get_status_code() == 201
    created_id = client.get_json()["id"]
    print(f"Seasonal Override created with ID: {created_id}")
    return created_id

@given(parsers.parse("the updated body is generated for the existing seasonal override"), target_fixture="id")
def generate_updated_body_for_existing_seasonal_override(client: TrolieClient, preload_seasonal_override_data_helper):
    seasonal_override_id = preload_seasonal_override_data_helper[0]  
    start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=3)
    end_time = start_time + timedelta(hours=1)
    resource_id = "PARKHILL.T5.T5"
    body = generate_seasonal_override_body_helper(start_time, end_time, resource_id)
    client.set_body(body)
    return seasonal_override_id

@when(parsers.parse("the client deletes a seasonal override by its id"))
def delete_seasonal_override_by_id(client: TrolieClient, id):
    return client.request(f"/seasonal-overrides/{id}", method="DELETE")

@when(parsers.parse("the client requests the current seasonal override"))
def request_seasonal_override(client: TrolieClient):
    return client.request("/seasonal-overrides")

@when(parsers.parse("the client creates a new seasonal override"))
def create_seasonal_override(client: TrolieClient):
    return client.request("/seasonal-overrides", method="POST")

@when(parsers.parse("the client requests for a seasonal override by its id"))
def request_seasonal_override_by_id(client: TrolieClient, preload_seasonal_override_data_helper):
    seasonal_override_id = preload_seasonal_override_data_helper[0]  
    return client.request(f"/seasonal-overrides/{seasonal_override_id}")

@when(parsers.parse("the client updates an existing seasonal override by its id"))
def update_seasonal_override_by_id(client: TrolieClient, id):
    return client.request(f"/seasonal-overrides/{id}", method="PUT")

@when(parsers.parse("the client requests for a seasonal override with unknown id"))
def request_seasonal_override_by_unknown_id(client: TrolieClient):
    unknown_id = "unknown_id"
    return client.request(f"/seasonal-overrides/{unknown_id}")

@when(parsers.parse("the client deletes a seasonal override with unknown id"))
def delete_seasonal_override_with_unknown_id(client: TrolieClient):
    unknown_id = "unknown_id"
    return client.request(f"/seasonal-overrides/{unknown_id}", method="DELETE")

@when(parsers.parse("the client updates a seasonal override with unknown id"))
def update_seasonal_override_with_unknown_id(client: TrolieClient):
    unknown_id = "unknown_id"
    return client.request(f"/seasonal-overrides/{unknown_id}", method="PUT")
