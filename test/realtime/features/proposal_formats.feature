@realtime 
Feature: Provide real-time proposals in appropriate formats

    As a Clearinghouse Operator
    I want to provide real-time proposals in a variety of formats
    when a client requests and appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
    
    # GET Real-Time Proposal Status
    Scenario Outline: Get real-time proposal status
        Given the Accept header is set to `<content_type>`
        When the client requests for the current real-time proposal status
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.rating-realtime-proposal-status.v1+json |
    
    # POST Submit Real-Time Rating Proposal
    Scenario Outline: Submit real-time rating proposal
        Given the Accept header is set to `<content_type>`
        And the real-time rating proposal is generated
        When the client submits a real-time rating proposal
        Then the response is 202 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.rating-realtime-proposal.v1+json |
        | application/vnd.trolie.rating-realtime-proposal-slim.v1+json; limit-type=apparent-power |


