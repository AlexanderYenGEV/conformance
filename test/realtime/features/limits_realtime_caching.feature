@realtime 
Feature: Caching of realtime snapshots and proposal supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of realtime snapshots and proposals
    So that clients can obtain the latest data without unnecessary network traffic
    when the client has already obtained the still-current realtime snapshot or proposal
    Without requiring the client to re-fetch the entire snapshot

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And the client is preloaded with a realtime rating snapshot


    Scenario Outline: Real-time proposals support conditional get
        Given the Accept header is set to `<accept_header>`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client obtained the current real-time proposal with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
        | accept_header                                                     | accept_encoding |
        | application/vnd.trolie.rating-realtime-proposal-status.v1+json    | gzip |
        | application/vnd.trolie.rating-realtime-proposal-status.v1+json    | br | 


    Scenario Outline: Real-time snapshots support conditional get
        Given the Accept header is set to `<accept_header>`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client obtained the current real-time snapshot with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
        | accept_header                                                                                             | accept_encoding |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                                   | gzip |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false                         | gzip |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                                          | gzip |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false                | gzip |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power                   | gzip |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true | gzip | 
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                                   | br |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false                         | br |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                                          | br |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false                | br |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power                   | br |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true | br | 


    Scenario Outline: Regional real-time snapshots support conditional get
        Given the Accept header is set to `<accept_header>`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client obtained the current regional real-time snapshot with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
        | accept_header                                                                              | accept_encoding |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                                   | gzip |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false                         | gzip |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                                          | gzip |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false                | gzip |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power                   | gzip |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true | gzip | 
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                                   | br |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false                         | br |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                                          | br |
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false                | br |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power                   | br |
        # | application/vnd.trolie.realtime-limits-snapshot-slim.v1+json; limit-type=apparent-power; inputs-used=true | br | 


    Scenario Outline: Different real-time snapshot accept headers should have different ETags
        Given the Accept header is set to `<accept_header1>`
        And the client obtained the current real-time snapshot with an ETag
        When the client immediately requests the real-time snapshot with an Accept header of `<accept_header2>`
        Then the etags should not match

        Examples: 
        | accept_header1                                                                    | accept_header2 |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                           | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |  

    
    Scenario Outline: Different real-time regional snapshot accept headers should have different ETags
        Given the Accept header is set to `<accept_header1>`
        And the client obtained the current regional real-time snapshot with an ETag
        When the client immediately requests the regional real-time snapshot with an Accept header of `<accept_header2>`
        Then the etags should not match

        Examples: 
        | accept_header1                                                                    | accept_header2 |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                           | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |


    Scenario Outline: Unknown ETags for real-time proposal should result in 200 OK
        Given the Accept header is set to `<accept_header>`
        When the client obtained the current real-time proposal with an unknown ETag
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | accept_header | 
        | application/vnd.trolie.rating-realtime-proposal-status.v1+json |


    Scenario Outline: Unknown ETags for real-time snapshots should result in 200 OK
        Given the Accept header is set to `<accept_header>`
        When the client obtained the current real-time snapshot with an unknown ETag
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | accept_header |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                    |                      
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false          |                    
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                           |                      
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |


    Scenario Outline: Unknown ETags for real-time regional snapshots should result in 200 OK
        Given the Accept header is set to `<accept_header>`
        When the client obtained the current real-time regional snapshot with an unknown ETag
        Then the response is 200 OK
        And the response is schema-valid

        Examples: 
        | accept_header |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                    |                      
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false          |                    
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                           |                      
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |

    @todo
    Scenario Outline: ETag changes when real-time proposal data is updated


    Scenario Outline: ETag changes when real-time snapshot data is updated
        Given the Accept header is set to `<content_type>`
        And the client obtained the current real-time snapshot with an ETag
        When a new real-time snapshot is available
        And the client immediately issues a conditional GET for the same resource
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid
        And the previous ETag should not match the new ETag

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                    |                      
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false          |                    
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                           |                      
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |


    Scenario Outline: ETag changes when real-time regional snapshot data is updated
        Given the Accept header is set to `<content_type>`
        And the client obtained the current regional real-time snapshot with an ETag
        When a new real-time regional snapshot is available
        And the client immediately issues a conditional GET for the same resource
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid
        And the previous ETag should not match the new ETag

        Examples:
        | content_type |
        | application/vnd.trolie.realtime-limits-snapshot.v1+json                                    |                      
        | application/vnd.trolie.realtime-limits-snapshot.v1+json; include-psr-header=false          |                    
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json                           |                      
        | application/vnd.trolie.realtime-limits-detailed-snapshot.v1+json; include-psr-header=false |
        
