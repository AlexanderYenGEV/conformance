@realtime
Feature: Support querying subsets of the available real-time limits

    As a Clearinghouse Operator
    I want to support querying subsets of the available real-time limits
    So that clients can obtain just the data they need
    when they request a real-time limits snapshot and specify a query parameter
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And the Accept header is set to `application/vnd.trolie.realtime-limits-snapshot.v1+json`

    # GET Limits Real-Time Snapshot

    @todo
    Scenario Outline: Query limits real-time snapshot with default monitoring-set

    Scenario Outline: Query limits real-time snapshot with monitoring-set filter
        When the client requests a real-time limits snapshot with monitoring-set filter <monitoring_set>
        Then the response should include real-time limits snapshot for the monitoring-set <monitoring_set>

        Examples:
        | monitoring_set |
        | default | 
    
    Scenario Outline: Query limits real-time snapshot with resource-id filter
        When the client requests a real-time limits snapshot with resource-id filter <resource_id>
        Then the response should include real-time limits snapshot for the resource-id <resource_id> 

        Examples: 
        | resource_id |
        | HEARN.34562.1 |
        | PARKHILL.T5.T5 |
    
    # GET Regional Limits Real-Time Snapshot

    @todo
    Scenario Outline: Query limits real-time snapshot with default monitoring-set
    
    Scenario Outline: Query regional limits real-time snapshot with monitoring-set filter
        When the client requests a regional limits real-time snapshot with monitoring-set filter <monitoring_set>
        Then the response should include regional limits real-time snapshot for the monitoring-set <monitoring_set>

        Examples:
        | monitoring_set |
        | default |

    Scenario Outline: Query regional limits real-time snapshot with resource-id filter
        When the client requests a regional limits real-time snapshot with resource-id filter <resource_id>
        Then the repsonse should include regional limits real-time snapshot for the resource-id <resource_id>

        Examples:
        | resource_id |
        | HEARN.34562.1 |
        | PARKHILL.T5.T5 |

    