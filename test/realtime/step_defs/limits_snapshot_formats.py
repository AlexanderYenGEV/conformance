from pytest_bdd import given, when
from test.helpers import TrolieClient
from test.realtime.realtime_helpers import preload_realtime_ratings_proposal_data_helper

@given("the client is preloaded with a realtime rating snapshot")
def preload_realtime_snapshot(preload_realtime_ratings_proposal_data_helper):
    response = preload_realtime_ratings_proposal_data_helper
    if response.get_status_code() == 202:
        print("Response Status:", response.get_status_code())
    else: 
        print(response.get_json())
    pass

@when("the client requests for the current real-time snapshot")
def request_realtime_snapshot(client: TrolieClient):
    response = client.request("/limits/realtime-snapshot")
    print(response.get_json())
    return response

@when("the client requests for the current regional real-time snapshot")
def request_regional_realtime_snapshot(client: TrolieClient):
    return client.request("/limits/regional/realtime-snapshot")