from pytest_bdd import given, when, then, parsers
from test.helpers import Header
from test.realtime.realtime_helpers import get_etag
from test.realtime.step_defs.proposal_formats import request_realtime_proposal_status
from test.realtime.step_defs.limits_snapshot_formats import request_realtime_snapshot, request_regional_realtime_snapshot
from datetime import datetime, timedelta

base_time = datetime.now().astimezone().isoformat()

@given("the client obtained the current real-time proposal with an ETag", target_fixture="etag")
def get_etag_for_realtime_proposal(client):
    return get_etag(request_realtime_proposal_status(client))

@given("the client obtained the current real-time snapshot with an ETag", target_fixture="etag")
def get_etag_for_realtime_snapshot(client):
    client.set_server_time(base_time)
    return get_etag(request_realtime_snapshot(client))

@given("the client obtained the current regional real-time snapshot with an ETag", target_fixture="etag")
def get_etag_for_regional_realtime_snapshot(client):
    client.set_server_time(base_time)
    return get_etag(request_regional_realtime_snapshot(client))

@when(parsers.parse("the client immediately requests the real-time snapshot with an Accept header of `{accept_header2}`"), target_fixture="etag")
def request_realtime_snapshot_with_accept_header(client, accept_header2):
    client.set_header(Header.Accept, accept_header2)
    return request_realtime_snapshot(client)

@when(parsers.parse("the client immediately requests the regional real-time snapshot with an Accept header of `{accept_header2}`"), target_fixture="etag")
def request_realtime_regional_snapshot_with_accept_header(client, accept_header2):
    client.set_header(Header.Accept, accept_header2)
    return request_regional_realtime_snapshot(client)

@when("the client obtained the current real-time proposal with an unknown ETag")
def request_realtime_proposal_with_unknown_etag(client):
    client.set_header(Header.If_None_Match, "Unknown-ETag")
    return request_realtime_proposal_status(client)

@when("the client obtained the current real-time snapshot with an unknown ETag")
def request_realtime_snapshot_with_unknown_etag(client):
    client.set_header(Header.If_None_Match, "Unknown-ETag")
    return request_realtime_snapshot(client) 

@when("the client obtained the current real-time regional snapshot with an unknown ETag")
def request_realtime_regional_snapshot_with_unknown_etag(client):
    client.set_header(Header.If_None_Match, "Unknown-ETag")
    return request_regional_realtime_snapshot(client)

@when("a new real-time snapshot is available")
def new_realtime_snapshot_available(client):
    base_time_dt = datetime.fromisoformat(base_time)
    client.set_server_time((base_time_dt - timedelta(hours=1)).isoformat())
    return request_realtime_snapshot(client)

@when("a new real-time regional snapshot is available")
def new_realtime_regional_snapshot_available(client):
    base_time_dt = datetime.fromisoformat(base_time)
    client.set_server_time((base_time_dt - timedelta(hours=1)).isoformat())
    return request_regional_realtime_snapshot(client)   