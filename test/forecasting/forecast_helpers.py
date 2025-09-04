from datetime import datetime, timedelta
from test.helpers import TrolieClient, get_period


def get_forecast_limits_snapshot(client: TrolieClient):
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
    return etag
