from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from test.helpers import TrolieClient
import os

timezone = os.getenv("TZ")

def generate_temporary_aar_exception_helper(start_time, end_time, reason, resource_id):
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
        "reason": reason
    }

    return response

def generate_updated_temporary_aar_exception_helper(start_time, end_time, resource_id, continuous_limits, emergency_limits, id):
    response = {
        "resource": {
            "resource-id": resource_id
        },
        "start-time": start_time,
        "end-time": end_time,
        "continuous-operating-limit": {
            "mva": continuous_limits
        },
        "emergency-operating-limits": [
            {
                "duration-name": "EMERG",
                "limit": {
                    "mva": emergency_limits[0]
                }
            },
            {
                "duration-name": "LDSHD",
                "limit": {
                    "mva": emergency_limits[1]
                }
            },
            {
                "duration-name": "DAL",
                "limit": {
                    "mva": emergency_limits[2]
                }
            }
        ],
        "id": id
    }

    return response

def generate_temporary_aar_exception_for_set_time_helper(client: TrolieClient, resource_id, offset_start=2, offset_end=10):
    start_time = datetime.now(ZoneInfo(timezone)).replace(microsecond=0) + timedelta(seconds=offset_start)
    end_time = start_time + timedelta(seconds=offset_end)
    reason = "test delete Temporary AAR Exception in use"
    body = generate_temporary_aar_exception_helper(start_time, end_time, reason, resource_id)
    client.set_body(body)