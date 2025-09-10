from test.helpers import TrolieClient, get_period, warning, Role
from datetime import datetime, timedelta, timezone
import pytest, os

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

# Creates a ratings proposal for the next available window. This is used to preload data for tests.
@pytest.fixture(scope="session")
def preload_forecast_limits_snapshot_data_helper():
    client = TrolieClient(role=Role.RATINGS_PROVIDER)
    start_time = get_next_available_window()
    continuous_rating = 350
    emergency_rating = 400
    load_shed_rating = 450
    dal_rating = 500
    resource_id = "HEARN.34562.1"
    proposal_header = {
        "source": {
            "last-updated": datetime.now(timezone.utc).isoformat()[:-9] + "Z",
            "provider": "TO1",
            "origin-id": "5aeacb25-9b65-4738-8a00-ac10afa63640"
        },
        "begins": start_time.isoformat().replace("+00:00", ".000Z"),
        "default-emergency-durations": [
            {"name": "EMERG", "duration-minutes": 120},
            {"name": "LDSHD", "duration-minutes": 15},
            {"name": "DAL", "duration-minutes": 5}
        ],
        "power-system-resources": [
            {"resource-id": resource_id}
        ]
    }

    ratings_periods = []
    period_start = start_time

    for _ in range(240):
        period_end = period_start + timedelta(hours=1)
        ratings_periods.append({
            "period-start": period_start.isoformat().replace("+00:00", ".000Z"),
            "period-end": period_end.isoformat().replace("+00:00", ".000Z"),
            "continuous-operating-limit": {"mva": continuous_rating},
            "emergency-operating-limits": [
                {"duration-name": "EMERG", "limit": {"mva": emergency_rating}},
                {"duration-name": "LDSHD", "limit": {"mva": load_shed_rating}},
                {"duration-name": "DAL", "limit": {"mva": dal_rating}}
            ]
        })
        period_start = period_end

    payload = {
        "proposal-header": proposal_header,
        "ratings": [
            {
                "resource-id": resource_id,
                "periods": ratings_periods
            }
        ]
    }

    client.set_body(payload)
    client.set_header("Content-Type", "application/vnd.trolie.rating-forecast-proposal.v1+json")
    client.request("/rating-proposals/forecast", method="PATCH")
    # Job Runner
    os.environ["TROLIE_BASE_URL"] = "http://localhost:8081"
    client.request("/lep-jobs/clearing-house/forecast/phase1", method="POST")
    os.environ["TROLIE_BASE_URL"] = "https://service.env-alex-ingress.local/lep-operations"


