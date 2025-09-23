from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from test.helpers import TrolieClient, Role
from logging import warning
import pytest, os, json

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

def get_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/realtime-snapshot")

def get_regional_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/regional/realtime-snapshot")


@pytest.fixture(scope="session")
def preload_realtime_ratings_proposal_data_helper():
    client = TrolieClient(role=Role.RATINGS_PROVIDER)
    start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    resources = ["HEARN.34562.1", "DOUGLAS.T538.1 IN", "DOUGLAS.T538.1 OUT"]
    
    proposal_header = {
        "source": {
            "provider": "TO1",
            "last-updated": "2024-07-19T00:00:00Z",
            "origin-id": "origin"
        },
        "default-emergency-durations": [
            {
                "name": "EMERG",
                "duration-minutes": 30
            },
            {
                "name": "LDSHD",
                "duration-minutes": 20
            },
            {
                "name": "DAL",
                "duration-minutes": 10
            }
        ],
    }

    pwr_sys_rss = []

    for rss in resources:
        pwr_sys_rss.append({
            "resource-id": rss
        })
    
    proposal_header["power-system-resources"] = pwr_sys_rss
    proposal_header["begins"] = start_time.isoformat().replace("+00:00", ".00Z")

    ratings = [] 
    limit_offset = 0
    for rss in resources:
        ratings.append({
            "resource-id": rss,
            "continuous-operating-limit": {
                "mva": 330
            },
            "emergency-operating-limits": [
                {
                    "duration-name": "EMERG",
                    "limit": {
                        "mva": 350 + limit_offset
                    }
                },
                {
                    "duration-name": "LDSHD",
                    "limit": {
                        "mva": 450 + limit_offset
                    }
                },
                {
                    "duration-name": "DAL",
                    "limit": {
                        "mva": 500 + limit_offset
                    }
                }
            ]
        })
        limit_offset += 10

    payload = {
        "proposal-header": proposal_header,
        "ratings": ratings
    }

    client.set_body(payload)
    print(json.dumps(payload, indent=2))
    client.set_header("Content-Type", "application/vnd.trolie.rating-realtime-proposal.v1+json")
    response = client.request("/rating-proposals/realtime", method="POST")

    #job clearing house
    original_url = os.getenv("TROLIE_BASE_URL")
    os.environ["TROLIE_BASE_URL"] = "http://localhost:8081"
    client.request("/lep-jobs/clearing-house/realtime", method="POST")
    os.environ["TROLIE_BASE_URL"] = original_url

    return response