from pytest_bdd import given, when, parsers
from test.helpers import TrolieClient
import json


@given("the Seasonal Ratings Proposal is generated")
def generate_seasonal_ratings_proposal(client: TrolieClient):
    proposal_header = {
        "source": {
            "provider": "TO1",
            "last-updated": "2024-07-19T00:00:00-07:00",
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
        "power-system-resources": [
            {
                "resource-id": "HEARN.34562.1"
            }
        ]
    }

    ratings = [
        {
            "resource-id": "HEARN.34562.1",
            "periods": [
                {
                    "season-name": "Summer",
                    "period-start": "2025-05-27T00:00:00-07:00",
                    "period-end": "2025-08-27T00:00:00-07:00",
                    "continuous-operating-limit": {"mva": 410},
                    "emergency-operating-limits": [
                        {"duration-name": "EMERG", "limit": {"mva": 420}},
                        {"duration-name": "LDSHD", "limit": {"mva": 420}},
                        {"duration-name": "DAL",   "limit": {"mva": 430}},
                    ]
                },
                {
                    "season-name": "Fall",
                    "period-start": "2025-08-27T00:00:00-07:00",
                    "period-end": "2025-11-27T00:00:00-08:00",
                    "continuous-operating-limit": {"mva": 411},
                    "emergency-operating-limits": [
                        {"duration-name": "EMERG", "limit": {"mva": 421}},
                        {"duration-name": "LDSHD", "limit": {"mva": 421}},
                        {"duration-name": "DAL",   "limit": {"mva": 431}},
                    ]
                },
                {
                    "season-name": "Winter",
                    "period-start": "2025-11-27T00:00:00-08:00",
                    "period-end": "2026-02-27T00:00:00-08:00",
                    "continuous-operating-limit": {"mva": 412},
                    "emergency-operating-limits": [
                        {"duration-name": "EMERG", "limit": {"mva": 422}},
                        {"duration-name": "LDSHD", "limit": {"mva": 422}},
                        {"duration-name": "DAL",   "limit": {"mva": 432}},
                    ]
                },
                {
                    "season-name": "Spring",
                    "period-start": "2026-02-27T00:00:00-08:00",
                    "period-end": "2026-05-27T00:00:00-07:00",
                    "continuous-operating-limit": {"mva": 413},
                    "emergency-operating-limits": [
                        {"duration-name": "EMERG", "limit": {"mva": 423}},
                        {"duration-name": "LDSHD", "limit": {"mva": 423}},
                        {"duration-name": "DAL",   "limit": {"mva": 433}},
                    ]
                }
            ]
        }
    ]

    payload = {
        "proposal-header": proposal_header,
        "ratings": ratings
    }
    print(payload)
    client.set_body(payload)
    #print(json.dumps(payload, indent=2))

@when(parsers.parse("the client requests the current Seasonal Rating Proposal Status"))
def request_seasonal_rating_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/seasonal")

@when(parsers.parse("the client submits a Seasonal Ratings Proposal"))
def submit_seasonal_ratings_proposal(client: TrolieClient):
    response = client.request("/rating-proposals/seasonal", method="PATCH")
    print(response.get_json())
    return response
    #return client.request("/rating-proposals/seasonal", method="PATCH")