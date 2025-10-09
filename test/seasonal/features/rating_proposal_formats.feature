@seasonal
Feature: Provide seasonal proposal limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide seasonal proposal limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    Scenario Outline: Obtaining the latest seasonal proposal snapshot
        Given the Accept header is set to `<content_type>`
        When the client requests the current Seasonal Rating Proposal Status
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid
        Examples:
        | content_type |
        | application/vnd.trolie.seasonal-ratings-proposal-status.v1+json |
    
    Scenario Outline: Submiting a Seasonal Ratings proposal
        Given the Content-type header is set to `<content_type>`
        And the Seasonal Ratings Proposal is generated
        When the client submits a Seasonal Ratings Proposal
        Then the response is 202 OK
        And the Content-Type header in the response is `<response_type>`
        And the response is schema-valid

        Examples: 
        | content_type                                              | response_type                                           |
        | application/vnd.trolie.seasonal-ratings-proposal.v1+json   | application/vnd.trolie.seasonal-ratings-proposal-status.v1+json |
        | application/vnd.trolie.seasonal-ratings-proposal-slim.v1+json; limit-type=apparent-power | application/vnd.trolie.seasonal-ratings-proposal-status.v1+json |

