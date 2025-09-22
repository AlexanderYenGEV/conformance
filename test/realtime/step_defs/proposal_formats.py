from pytest_bdd import given, when
from test.helpers import TrolieClient
from datetime import datetime, timezone, timedelta
import json


@given("the real-time rating proposal is generated")
def generate_realtime_proposal(client: TrolieClient):  
    start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    resources = ["HEARN.34562.1"]
    
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
    return

@when("the client requests for the current real-time proposal status")
def request_realtime_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/realtime")

@when("the client submits a real-time rating proposal")
def submit_realtime_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/realtime", method="POST")