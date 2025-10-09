@seasonal_overrides @auth
Feature: All seasonal override ratings requests require authentication
    As a Clearinghouse Operator
    I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
    when a client attempts to access any seasonal overrides resources
    So that only authorized clients can access the system
    Without processing the request beyond the authentication step
    and without revealing any information about resources that may or may not exist

    Background:
        Given a TROLIE client that has not been authenticated

    Scenario Outline: Get seasonal overrides
        When the client requests the current seasonal override
        Then the response is Unauthorized
        And the response is empty

    Scenario Outline: Create new seasonal overrides
        Given an empty body and no Content-Type specified
        When the client creates a new seasonal override
        Then the response is Unauthorized
        And the response is empty

    Scenario Outline: Get seasonal overrides by ID
        When the client requests for a seasonal override with unknown id
        Then the response is Unauthorized
        And the response is empty

    Scenario Outline: Delete seasonal override by ID
        When the client deletes a seasonal override with unknown id
        Then the response is Unauthorized
        And the response is empty

    Scenario Outline: Update seasonal override by ID
        When the client updates a seasonal override with unknown id
        Then the response is Unauthorized
        And the response is empty