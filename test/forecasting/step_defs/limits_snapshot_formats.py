import json
from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient, Header
from test.forecasting.forecast_helpers import (
    get_forecast_limits_snapshot,
    get_todays_iso8601_for,
)

@when("the client requests the current Forecast Limits Snapshot")
@given("the client requests the current Forecast Limits Snapshot")
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

