@temporary_aar_exceptions @auth
Feature: All Temporary AAR Exceptions requests require authentication
    As a Clearinghouse Operator
    I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
    when a client attempts to access any Forecasting resources
    So that only authorized clients can access the system
    Without processing the request beyond the authentication step
    and without revealing any information about resources that may or may not exist

    Background: a Trolie client has not been authenticated
        Given a TROLIE client that has not been authenticated

        Scenario: Get Temporary AAR Exception requires authentication
            When the client requests for all Temporary AAR Exceptions
            Then the response is Unauthorized
            And the response is empty

        Scenario: Create a new Temporary AAR Exception requires authentication
            When the client creates a new Temporary AAR Exception
            Then the response is Unauthorized
            And the response is empty

        Scenario: Get Temporary AAR Exception by ID requires authentication
            When the client requests for Temporary AAR Exception by ID
            Then the response is Unauthorized
            And the response is empty

        Scenario: Delete Temporary AAR Exception by ID requires authentication
            When the client deletes Temporary AAR Exception by ID
            Then the response is Unauthorized
            And the response is empty

        Scenario: Update Temporary AAR Exception by ID requires authentication
            When the client updates Temporary AAR Exception by ID
            Then the response is Unauthorized
            And the response is empty
