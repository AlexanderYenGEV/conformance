@forecasting
Feature: Caching of Forecast Limits Snapshots supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Forecast Limits Snapshots
    So that clients can obtain the latest data without unnecessary network traffic
    when the client has already obtained the still-current Forecast Limits Snapshot
    Without requiring the client to re-fetch the entire snapshot

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    @prism_fail
    Scenario Outline: Support Conditional GET
        Given the Accept header is set to `<accept_header>`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client has obtained the current Forecast Limits Snapshot with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
            | accept_header                                                                              | accept_encoding |
            | application/vnd.trolie.forecast-limits-snapshot.v1+json                                    | gzip            |
            | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json                           | brotli          |
            | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false          | brotli          |
            | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false | gzip            |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power, inputs-used=true |
      #| application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; inputs-used=true, limit-type=apparent-power  |

    @prism_fail
    Scenario Outline: Different representations have different ETags
        Given the Accept header is set to `<accept_header_1>`
        And the client has obtained the current Forecast Limits Snapshot with an ETag
        When the client immediately requests the Forecast Limits Snapshot with an Accept header of `<accept_header_2>`
        Then the etags should not match
        Examples:
        | accept_header_1                                                                         | accept_header_2                                                                                           |
        | application/vnd.trolie.forecast-limits-snapshot.v1+json                                 | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json                                          |
        | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power | application/vnd.trolie.forecast-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true |
        | application/vnd.trolie.forecast-limits-snapshot.v1+json                                 | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false                         |

    @todo
    Scenario Outline: Unknown ETag in conditional request results in 200 OK
        Given the Accept header is set to `<accept_header>`
        When the client requests the Forecast Limits Snapshot with an unknown If-None-Match header
        Then the server should respond with a 200 OK status code
        And the response should be schema valid

    @prism_fail
    Scenario Outline: ETag changes when data is updated
        Given the Accept header is set to `<content_type>`
        And the client has obtained the current Forecast Limits Snapshot with an ETag
        When a new Forecast is available
        And the client immediately issues a conditional GET for the same resource
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid
        And the previous ETag should not match the new ETag
        Examples:
            | content_type |
            | application/vnd.trolie.forecast-limits-snapshot.v1+json |
            | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json |
            | application/vnd.trolie.forecast-limits-snapshot.v1+json; include-psr-header=false |
            | application/vnd.trolie.forecast-limits-detailed-snapshot.v1+json; include-psr-header=false |
