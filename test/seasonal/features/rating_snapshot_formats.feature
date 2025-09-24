Feature: Provide seasonal limits in appropriate formats

    As a Clearinghouse Operator
    I want to provide forecast limits in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

  Background: Authenticated as a Ratings Provider
    Given a TROLIE client that has been authenticated as a Ratings Provider

  Scenario Outline: Obtaining the latest seasonal snapshot
    #Given the Accept header is set to `<content_type>, application/problem+json`
    Given the Accept header is set to `<content_type>`
    When the client requests the current Seasonal Limits Snapshot
    Then the response is 200 OK
    And the Content-Type header in the response is `<content_type>`
    And the response is schema-valid
    Examples:
      | content_type |
      | application/vnd.trolie.seasonal-rating-snapshot.v1+json |
      | application/vnd.trolie.seasonal-rating-snapshot-detailed.v1+json|
      | application/vnd.trolie.seasonal-rating-snapshot-detailed.v1+json; include-psr-header=false |