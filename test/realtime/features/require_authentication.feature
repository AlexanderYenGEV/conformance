@realtime
Feature: All Real-time requests require authentication
  As a Clearinghouse Operator
  I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
  when a client attempts to access any Real-time resources
  So that only authorized clients can access the system
  Without processing the request beyond the authentication step
  and without revealing any information about resources that may or may not exist

    Background:
        Given a TROLIE client that has not been authenticated

    Scenario: Get real-time proposal status 
        When the client requests for the current real-time proposal status
        Then the response is Unauthorized
        And the response is empty

    Scenario: Submitting real-time rating proposal
        Given an empty body and no Content-Type specified
        When the client submits a real-time rating proposal
        Then the response is Unauthorized
        And the response is empty    
    
    Scenario: Get limits real-time snapshot
        When the client requests for the current real-time snapshot
        Then the response is Unauthorized
        And the response is empty

    Scenario: Get regional limits real-time snapshot
        When the client requests for the current regional real-time snapshot
        Then the response is Unauthorized
        And the response is empty
