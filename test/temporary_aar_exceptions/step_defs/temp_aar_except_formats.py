from pytest_bdd import given, when, then, parsers
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.helpers import TrolieClient
from test.temporary_aar_exceptions.temp_aar_except_helpers import (
    generate_temporary_aar_exception_helper, 
    generate_updated_temporary_aar_exception_helper,
    generate_temporary_aar_exception_for_set_time_helper,
)
import json, time, os

timezone = os.getenv("TZ")

@given(parsers.parse("the Temporary AAR Exception is generated for the resource {resource_id}"))
def generate_temporary_aar_exception(client: TrolieClient, resource_id, offset_start=1):
    start_time = datetime.now(ZoneInfo(timezone)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=offset_start) # Gets the current time rounded up to the next hour
    end_time = start_time + timedelta(hours=1)
    reason = "reason for AAR exception"
    body = generate_temporary_aar_exception_helper(start_time, end_time, reason, resource_id)
    print(json.dumps(body, indent=2))
    client.set_body(body)

@given(parsers.parse("the updated Temporary AAR Exception is generated for the resource {resource_id}"))
def generate_updated_temporary_aar_exception(client: TrolieClient, resource_id, id_created):
    start_time = client.get_json()["start-time"] 
    end_time = (datetime.fromisoformat(client.get_json()["end-time"]) + timedelta(hours=1)).isoformat()   # Add one hour to original endtime
    continous_operating_limits = 330
    emergency_operating_limits = [350, 450, 510]
    body = generate_updated_temporary_aar_exception_helper(start_time, end_time, resource_id, continous_operating_limits, emergency_operating_limits, id_created)
    print(json.dumps(body, indent=2))
    client.set_body(body)

@given(parsers.parse("the body contains a Temporary AAR Exception with fields other than `reason` changed"))
def update_other_fields_of_body_temporary_aar_exception(client: TrolieClient):
    body = client.get_json()
    body["continuous-operating-limit"]["mva"] = 125
    client.set_body(body)

@given(parsers.parse("a Temporary AAR Exception is generated right now for the resource {resource_id}"))
def generate_and_create_temporary_aar_exception_for_resource(client: TrolieClient, resource_id):
    generate_temporary_aar_exception_for_set_time_helper(client, resource_id)
    return client.request("/temporary-aar-exceptions", method="POST")

@given(parsers.parse("a Temporary AAR Exception is generated in the past for the resource {resource_id}"))
def generate_temporary_aar_exception_for_set_times(client: TrolieClient, resource_id):
    generate_temporary_aar_exception_for_set_time_helper(client, resource_id, 2, 2)     # Generates a Temporary AAR Exception window 2 seconds in advance and 2 seconds long
    return client.request("/temporary-aar-exceptions", method="POST")

@given(parsers.parse("the id of the created Temporary AAR Exception is obtained"), target_fixture="id_created")
def obtain_temporary_aar_exception_id(client: TrolieClient):
    print(client.get_json())
    id_created = client.get_json()["id"]
    print("Obtained Temporary AAR Exception ID:", id_created)
    return id_created

@when(parsers.parse("the client requests for Temporary AAR Exceptions"))
def request_temporary_aar_exceptions(client: TrolieClient):
    return client.request("/temporary-aar-exceptions")

@when(parsers.parse("the client requests for the specific Temporary AAR Exception by id"))
def request_temporary_aar_exceptions_by_id(client: TrolieClient, id_created):
    return client.request(f"/temporary-aar-exceptions/{id_created}")

@given("the client creates a new Temporary AAR Exception")
@when("the client creates a new Temporary AAR Exception")
def create_new_temporary_aar_exception(client: TrolieClient):
    return client.request("/temporary-aar-exceptions", method="POST")

@when(parsers.parse("the client creates an overlapping Temporary AAR Exception for the same resource {resource_id}"))
def create_new_temporary_aar_exception_with_overlap(client: TrolieClient, resource_id):
    generate_temporary_aar_exception(client, resource_id, offset_start=1.5)
    return client.request("/temporary-aar-exceptions", method="POST")

@when(parsers.parse("the client deletes that Temporary AAR Exception by id"))
@when(parsers.parse("the client deletes a specific Temporary AAR Exception by id"))
def delete_temporary_aar_exception_by_id(client: TrolieClient):
    id = client.get_json()["id"]
    return client.request(f"/temporary-aar-exceptions/{id}", method="DELETE")

@when("the client deletes the most recently created Temporary AAR Exception")
@when("the client deletes a specific Temporary AAR Exception created in the past")
def delete_temporary_aar_exception_with_delay(client: TrolieClient):
    time.sleep(6)
    print(json.dumps(client.get_json(), indent=2))
    id = client.get_json()["id"]
    return client.request(f"/temporary-aar-exceptions/{id}", method="DELETE")

@when(parsers.parse("the client updates an existing Temporary AAR Exception by id"))
def update_temporary_aar_exception_by_id(client: TrolieClient):
    id = client.get_json()["id"]
    return client.request(f"/temporary-aar-exceptions/{id}", method="PUT")

@when(parsers.parse("the client updates the past Temporary AAR Exception"))
def update_past_temporary_aar_exception(client: TrolieClient):
    time.sleep(6)
    id = client.get_json()["id"]
    return client.request(f"/temporary-aar-exceptions/{id}", method="PUT")


@then(parsers.parse("the ID in the response should match the id of the created Temporary AAR Exception"))
def check_temporary_aar_exceptions_contains_id(client: TrolieClient, id_created):
    id_from_get_response = client.get_json()["id"]
    print("id: ", id_from_get_response)
    assert id_created == id_from_get_response, f"Expected ID: {id_created}, but got {id_from_get_response}"
