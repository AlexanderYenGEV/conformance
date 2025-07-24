@forecasting
Feature: Provide forecast proposal limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide forecast limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  # GET Obtain Forecast Proposal Status
  Scenario Outline: Get the forecast proposal status 
    Given the Accept header is set to `<content_type>`
    When the client requests the status of a Forecast Proposal
    Then the response is 200 OK 
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
  
    
    Examples: 
    | content_type |
    | application/vnd.trolie.rating-forecast-proposal-status.v1+json |

  # PATCH Submit a Forecast Proposal
  Scenario Outline: Submit a forecast proposal
    Given the Content-type header is set to `<response_type>`
    And the body is loaded from `<file_name>`
    When the client submits a Forecast Proposal
    Then the response is 202 OK 
    And the Content-Type header in the response is `<response_type>`
    And the response is schema-valid

    Examples: 
    | content_type                                            | file_name                   | response_type |
    | application/vnd.trolie.rating-forecast-proposal.v1+json | data/forecast_proposal.json | application/vnd.trolie.rating-forecast-proposal-status.v1+json |
    | application/vnd.trolie.rating-forecast-proposal-slim.v1+json; limit-type=apparent-power | data/forecast_proposal_slim.json |
