@seasonal_overrides
Feature: Support querying subsets of the available seasonal overrides ratings

    As a Clearinghouse Operator
    I want to support querying subsets of the available seasonal overrides ratings
    So that clients can obtain just the data they need
    when they request a forecast limits snapshot and specify a query parameter
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    Scenario Outline: Scenario Outline name