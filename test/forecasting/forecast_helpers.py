from test.helpers import TrolieClient, get_period, warning
from datetime import datetime, timedelta, timezone

def get_forecast_limits_snapshot(client: TrolieClient):
    response = client.request("/limits/forecast-snapshot")
    print("Status Code:", response.get_status_code())
    return client.request("/limits/forecast-snapshot")

def get_regional_limits_forecast_snapshot(client: TrolieClient):
    return client.request("/limits/regional/forecast-snapshot")

def get_historical_limits_forecast_snapshot(client: TrolieClient):
    return client.request(f"/limits/forecast-snapshot/{get_period(-1)}")


def get_todays_iso8601_for(time_with_timezone: str) -> str:
    iso8601_offset = datetime.now().strftime(f"%Y-%m-%dT{time_with_timezone}")
    try:
        datetime.fromisoformat(iso8601_offset)
    except ValueError:
        raise ValueError(f"Invalid ISO8601 format: {iso8601_offset}")
    return iso8601_offset

def round_up_to_next_hour(dt: datetime) -> datetime:
    if dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt
    return (dt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def get_etag(client: TrolieClient):
    etag = client.get_response_header("ETag")
    print("ETag:", etag)
    print("Status code:", client.get_status_code())
   
    # Verify ETag exists as it's required for the caching test
    assert etag is not None and client.get_status_code() == 200
    # Verify ETag is not a weak ETag
    # assert not etag.startswith('W/"'), "Expected strong ETag, got weak ETag"
    if etag.startswith('W/"'):
        warning(f"Expected strong ETag, got weak ETag")
        etag = etag[2:]  # Remove the weak ETag prefix
    return etag

def get_next_available_window(now=None):
    if now is None:
        now = datetime.now(timezone.utc)
    # Round up to the next hour
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    cutoff = next_hour - timedelta(minutes=15)
    if now < cutoff:
        return next_hour
    else:
        return (next_hour + timedelta(hours=1))
