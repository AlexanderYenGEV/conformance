from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient


@when(parsers.parse("the client requests for all Temporary AAR Exceptions"))
def request_temporary_aar_exception(client: TrolieClient):
    return client.request("/temporary-aar-exception")

@when(parsers.parse("the client requests for Temporary AAR Exception by ID"))
def request_temporary_aar_exception_by_id(client: TrolieClient):
    return client.request(f"/temporary-aar-exception/unknown-id")

@when(parsers.parse("the client deletes Temporary AAR Exception by ID"))
def delete_temporary_aar_exception_by_id(client: TrolieClient):
    return client.request(f"/temporary-aar-exception/unknown-id", method="DELETE")

@when(parsers.parse("the client updates Temporary AAR Exception by ID"))
def update_temporary_aar_exception_by_id(client: TrolieClient):
    return client.request(f"/temporary-aar-exception/unknown-id", method="PUT")

