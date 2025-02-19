from pytest_bdd import given, then, when, parsers
from test.helpers import Header, TrolieClient, Role


@given(
    "a TROLIE client that has been authenticated as a Ratings Provider",
    target_fixture="client",
)
def client_authenticated_as_ratings_provider():
    return TrolieClient(role=Role.RATINGS_PROVIDER)


@given(parsers.parse("the Accept header is set to `{content_type}`"))
def set_accept_header(content_type, client):
    client.set_header(Header.Accept, content_type)


@given(parsers.parse("the Accept-Encoding header is set to `{compression_type}`"))
def set_accept_encoding_header(compression_type, client):
    client.set_header(Header.Accept_Encoding, compression_type)


@given("the client has bad query parameters")
def bad_query_parameters(client: TrolieClient):
    client.set_query_param("bad", "value")


@given("the client has a non-empty body")
def non_empty_body(client: TrolieClient):
    client.set_body({"key": "value"})
    client.set_header("Content-Type", "application/json")


@then("the response is 200 OK")
def request_forecast_limits_snapshot(client: TrolieClient):
    assert client.get_status_code() == 200


@then("the response is 304 Not Modified")
def request_forecast_limits_snapshot_304(client: TrolieClient):
    assert client.get_status_code() == 304


@then("the response is 400 Bad Request")
def request_forecast_limits_snapshot_400(client: TrolieClient):
    assert client.get_status_code() == 400


@then("the response is 415 Unsupported Media Type")
def request_forecast_limits_snapshot_415(client: TrolieClient):
    assert client.get_status_code() == 415


@then("the response is 406 Not Acceptable")
def request_forecast_limits_snapshot_406(client: TrolieClient):
    assert client.get_status_code() == 406


@then("the response is schema-valid")
def valid_snapshot(client: TrolieClient):
    assert client.validate_response()


@when("the client issues a conditional GET for the same resource")
def conditional_get(client: TrolieClient):
    client.set_header("If-None-Match", client.get_response_header("ETag"))
    client.send()


@then("the response is empty")
def empty_response(client: TrolieClient):
    assert client.response_is_empty()


@then(parsers.parse("the Content-Type header in the response is `{content_type}`"))
def content_type_header(content_type, client):
    assert content_type == client.get_response_header(Header.ContentType)


@then("there is no Content-Type header in the response")
def no_content_type_header(content_type, client):
    assert client.get_response_header(Header.ContentType) is None
