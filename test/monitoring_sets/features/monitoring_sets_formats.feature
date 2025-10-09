@monitoring_sets
Feature: Provide monitoring sets data in appropriate formats

    As a Clearinghouse Operator
    I want to provide monitoring sets in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL
    
    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
    
    Scenario Outline: Obtain a specific monitoring set by identifier 
        Given the Accept header is set to `<content_type>`
        When the client requests for a specific monitoring set by identifier `<identifier>`
        Then the response should only power system resources by the provider `<identifier>`
        And the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples: 
        | content_type                                  | identifier |
        | application/vnd.trolie.monitoring-set.v1+json | TO1 |
        | application/vnd.trolie.monitoring-set.v1+json | TO2 |

    Scenario Outline: Obtain your default monitoring set
        Given the Accept header is set to `<content_type>`
        When the client requests for their default monitoring set
        #Then the response should only power system resources by the default provider
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples: 
        | content_type |                                
        | application/vnd.trolie.monitoring-set.v1+json |
