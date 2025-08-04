from datetime import timedelta, datetime
from pytest_bdd import given, when, then, parsers
from test.forecasting.forecast_helpers import get_forecast_limits_snapshot, get_todays_iso8601_for, get_etag
from test.helpers import Header

base_time = datetime.now().astimezone().isoformat()


@given("the client has obtained the current Forecast Limits Snapshot with an ETag", target_fixture="etag")
def get_etag_for_forecast_limits_snapshot(client):
    client.set_server_time(base_time)
    return get_etag(get_forecast_limits_snapshot(client))


@when("the client immediately issues a conditional GET for the same resource")
def request_with_if_none_match(client, etag):
    client.set_header(Header.If_None_Match, etag)
    client.send()


@when(parsers.parse("the client immediately requests the Forecast Limits Snapshot with an Accept header of `{accept_header_2}`"), target_fixture="client")
def request_forecast_limits_snapshot_with_different_accept_header(client, accept_header_2):
    client.set_header(Header.Accept, accept_header_2)
    return get_forecast_limits_snapshot(client)


@then("the etags should not match")
def etags_should_not_match(client, etag):
    new_etag = get_etag(client)
    assert etag != new_etag, "ETags should not match for different representations"

@when("a new Forecast is available")
def new_forecast_available(client):
    base_time_dt = datetime.fromisoformat(base_time)
    client.set_server_time((base_time_dt - timedelta(hours=1)).isoformat())
    get_forecast_limits_snapshot(client)
    client.send()

@when("the client requests the Forecast Limits Snapshot with an unknown If-None-Match header")
def request_forecast_limits_snapshot_with_unknown_if_none_match(client):
    client.set_header(Header.If_None_Match, "unknown-etag")
    return get_forecast_limits_snapshot(client)

@then("the previous ETag should not match the new ETag")
def previous_etag_should_not_match_new_etag(client):
    new_etag = get_etag(client)
    previous_etag = client.get_header(Header.If_None_Match)
    assert previous_etag != new_etag, "ETags should not match for different representations"
