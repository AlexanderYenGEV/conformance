@temporary_aar_exceptions @filters
Feature: Support querying subsets of the available Temporary AAR Exceptions

    As a Clearinghouse Operator
    I want to support querying subsets of the available temporary aar exceptions
    So that clients can obtain just the data they need
    when they request a temporary aar exceptions snapshot and specify a query parameter
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as ratings provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
     
    Scenario Outline: Query Temporary AAR Exceptions with period-start
        Given the Temporary AAR Exception data is preloaded
        When the client requests Temporary AAR Exceptions with `period-start` with <offset> hours from now
        Then the response should only include Temporary AAR Exceptions with `period-start` at <offset> hours or after

        Examples:
        | offset |
        | 1 |
        | 25 |
        | 30 |


    Scenario Outline: Query Temporary AAR Exceptions with period-end
        Given the Temporary AAR Exception data is preloaded
        When the client requests Temporary AAR Exceptions with `period-end` with <offset> hours from now
        Then the response should only include Temporary AAR Exceptions with `period-end` at <offset> hours or before

        Examples:
        | offset |
        | 30 | 
        | 25 |
        | 1 |

    Scenario Outline: Query Temporary AAR Exceptions with monitoring-set
        Given the Temporary AAR Exception data is preloaded
        When the client requests Temporary AAR Exceptions with query `monitoring-set` <monitoring_set>
        Then the response should only include Temporary AAR Exceptions under the `monitoring-set` <monitoring_set>

        Examples:
        | monitoring_set |
        | TO1 |

    Scenario Outline: Query Temporary AAR Exceptions with segment
        Given the Temporary AAR Exception data is preloaded
        When the client requests Temporary AAR Exceptions with `segment` query <segment>
        Then the response should only include Temporary AAR Exceptions for the segment <segment>

        Examples:
        | segment |
        | BRIGHTON.PS2.PS2 |
        | HEARN.34562.1 |
