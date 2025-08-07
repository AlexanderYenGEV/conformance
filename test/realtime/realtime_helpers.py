from datetime import datetime
from test.helpers import TrolieClient

def get_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/realtime-snapshot")

def get_regional_limits_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/regional/realtime-snapshot")