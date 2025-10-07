@seasonal_overrides @filters
Feature: Support querying subsets of the available seasonal overrides ratings

    As a Clearinghouse Operator
    I want to support querying subsets of the available seasonal overrides ratings
    So that clients can obtain just the data they need
    when they request a forecast limits snapshot and specify a query parameter
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And Seasonal override data is preloaded for filtering

    Scenario Outline: Get seasonal overrides with query period-start
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        When the client requests a seasonal override with query period-start set to <offset> hours after the current time
        Then the response should include only seasonal overrides beginning at the current time plus <offset> hours

        Examples:
        | offset |
        | 1 |
        | 5 |
        | 7 |

    Scenario Outline: Get seasonal overrides with query period-end
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        When the client requests a seasonal override with query period-end set to <offset> hours after the current time
        Then the response should include only seasonal overrides ending at the current time plus <offset> hours

        Examples:
        | offset |
        | 1 |
        | 5 |
        | 7 |

    Scenario Outline: Get seasonal overrides with query monitoring-set
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        When the client requests a seasonal override with query monitoring-set set to <monitoring_set>
        Then the response should include only seasonal overrides for the monitoring set <monitoring_set>

        Examples:
        | monitoring_set |
        | TO1 |

    Scenario Outline: Get seasonal overrides with query segment
        Given the Accept header is set to `application/vnd.trolie.seasonal-override-set.v1+json`
        When the client requests a seasoonal override with query segment for <segment>
        Then the response should include only seasonal overrides for the segment <segment>

        Examples:
        | segment |
        | DOUGLAS.1215.1 |
