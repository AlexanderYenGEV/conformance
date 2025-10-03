Feature: All seasonal override ratings requests require authentication
    As a Clearinghouse Operator
    I want to ensure that requests that cannot be authenticated receive 401 Unauthorized
    when a client attempts to access any seasonal overrides resources
    So that only authorized clients can access the system
    Without processing the request beyond the authentication step
    and without revealing any information about resources that may or may not exist

    Background:
        Given a TROLIE client that has not been authenticated

    Scenario Outline: Attempt to access seasonal overrides ratings without authentication