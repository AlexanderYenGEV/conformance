from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.helpers import TrolieClient, Role
from logging import warning
import os, pytest

tz = os.getenv("TZ")

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
    print("Etag: ", etag)
    return etag

@pytest.fixture(scope="session")
def preload_seasonal_override_data_helper():
    client = TrolieClient(role=Role.RATINGS_PROVIDER)
    resources = ["PARKHILL.T5.T5", "MOSELLE2.34591.1"]
    created_ids = []

    for rss in resources:
        start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        body = generate_seasonal_override_body_helper(start_time, end_time, rss)
        client.set_body(body)

        client.set_header("Content-Type", "application/vnd.trolie.seasonal-override.v1+json")
        client.request("/seasonal-overrides", method="POST")
        created_ids.append(client.get_json()["id"])
    
    print("Seasonal Overrides created: ", created_ids)
    yield created_ids

    for id in created_ids:
        client.request(f"/seasonal-overrides/{id}", method="DELETE")

@pytest.fixture(scope="session")
def preload_seasonal_override_data_for_filtering_helper():
    client = TrolieClient(role=Role.RATINGS_PROVIDER)
    resources = ["DOUGLAS.1215.1"]
    created_ids = []

    for rss in resources:
        for i in range(5):
            start_time = datetime.now(ZoneInfo(tz)).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1+i)
            end_time = start_time + timedelta(hours=1)
            body = generate_seasonal_override_body_helper(start_time, end_time, rss)
            client.set_body(body)

            client.set_header("Content-Type", "application/vnd.trolie.seasonal-override.v1+json")
            client.request("/seasonal-overrides", method="POST")
            created_ids.append(client.get_json()["id"])
    
    print("Seasonal Overrides created: ", created_ids)
    yield created_ids

    for id in created_ids:
        client.request(f"/seasonal-overrides/{id}", method="DELETE")


def generate_seasonal_override_body_helper(start_time, end_time, resource_id):
    response = {
        "resource": {
            "resource-id": resource_id
        },
        "start-time": start_time.isoformat(),
        "end-time": end_time.isoformat(),
        "continuous-operating-limit": {
            "mva": 330
        },
        "emergency-operating-limits": [
            {
                "duration-name": "EMERG",
                "limit": {
                    "mva": 350
                }
            },
            {
                "duration-name": "LDSHD",
                "limit": {
                    "mva": 450
                }
            },
            {
                "duration-name": "DAL",
                "limit": {
                    "mva": 510
                }
            }
        ],
        "reason": "reason for seasonal override"
    }
    return response