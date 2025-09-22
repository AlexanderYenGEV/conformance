@realtime
Feature: Provide real-time limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide real-time limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And the client is preloaded with a realtime rating snapshot
   
    # GET Limits Real-Time Snapshot
    Scenario Outline: Get limits real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |
    

    # GET Regional Limits Real-Time Snapshot
    Scenario Outline: Get regional limits real-time snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests for the current regional real-time snapshot
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power |
        | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |

       
# @test_fixture
#     Scenario: Preload client with real-time ratings proposal data
#         Given the client is preloaded with a realtime rating snapshot
