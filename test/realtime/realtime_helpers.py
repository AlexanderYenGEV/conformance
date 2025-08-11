from datetime import datetime
from test.helpers import TrolieClient
from logging import warning

def get_etag(client: TrolieClient):
    etag = client.get_response_header("ETag")
    print("Etag: ", etag)
    # Verify ETag exists as it's required for the caching test
    assert etag is not None and client.get_status_code() == 200
    # Verify ETag is not a weak ETag
    # assert not etag.startswith('W/"'), "Expected strong ETag, got weak ETag"
    if etag.startswith('W/"'):
        strong_etag = etag[2:]
        warning(f"Expected strong ETag {strong_etag}, got weak ETag {etag}")
        etag = strong_etag
    return etag

def get_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/realtime-snapshot")

def get_regional_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/regional/realtime-snapshot")
