@seasonal_overrides @caching
Feature: Caching of Seasonal Overrides ratings supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Seasonal Overrides ratings
    So that clients can obtain the latest data without unnecessary network traffic
    when the client has already obtained the still-current Seasonal Overrides rating
    Without requiring the client to re-fetch the entire rating

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And Seasonal override data is preloaded for caching

    Scenario Outline: Get Seasonal Overrides support conditional get  
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client obtained the current seasonal override with an ETag
        When the client immediately issues a conditional GET for the same resource
        Then the response is 304 Not Modified
        And the response is empty

        Examples:
        | accept_encoding |
        | gzip |
        | br |
    
    Scenario Outline: Unknown ETags for seasonal overrides should result in 200 OK
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        And the Accept-Encoding header is set to `<accept_encoding>`
        When the client obtained the current seasonal override with an unknown ETag
        Then the response is 200 OK
        And the response is schema-valid

        Examples:
        | accept_encoding |
        | gzip            | 
        | br              |

    Scenario Outline: Etags changes when seasonal overrides are updated
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        And the Accept-Encoding header is set to `<accept_encoding>`
        And the client obtained the current seasonal override with an ETag
        When a seasonal override is updated
        And the client immediately issues a conditional GET for the same ETag
        Then the response is 200 OK
        And the ETag in the response is different from the original ETag    
        And the response is schema-valid

        Examples:
        | accept_encoding |
        | gzip            | 
        | br              |


