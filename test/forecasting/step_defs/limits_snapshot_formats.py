import json
from pytest_bdd import given, when, then
from test.helpers import TrolieClient, Header
from datetime import datetime, timedelta, timezone

from test.forecasting.forecast_helpers import (
    get_forecast_limits_snapshot,
    get_todays_iso8601_for,
    get_next_available_window,
)

@given("the forecast proposal is generated for the current time")
def generate_forecast_proposal(client: TrolieClient):
    start_time = get_next_available_window()
    resource_id = "HEARN.34562.1"
    continuous_rating = 350
    emergency_rating = 400
    load_shed_rating = 450
    dal_rating = 500

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

    # Convert to JSON string if needed
    body_str = json.dumps(payload, indent=2)
    print(body_str)
    client.set_body(payload)
    

@given("the client requests the current Forecast Limits Snapshot")
@when("the client requests the current Forecast Limits Snapshot")
def request_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/forecast-snapshot")

def print_forecast_snapshot(client: TrolieClient):
    print("REQUEST BODY SENT: ", json.dumps(client._TrolieClient__body, indent=2))
    print("RESPONSE CONTENT-TYPE:", client._TrolieClient__response.headers.get("Content-type"))
    print("RESPONSE STATUS:", client.get_status_code())
    print("REQUEST BODY RECIEVED: ", json.dumps(client.get_json(), indent=2))
    print("\n")

@when("the client requests a Historical Forecast Limits Snapshot at time frame {time_frame}")
def request_historical_forecast_limits_snapshot_at_period(client: TrolieClient, time_frame):
    return client.request(f"/limits/forecast-snapshot/{time_frame}")

