@seasonal_overrides
Feature: Caching of Seasonal Overrides ratings supporting conditional GET

    As a Clearinghouse Operator
    I want to support efficient caching of Seasonal Overrides ratings
    So that clients can obtain the latest data without unnecessary network traffic
    when the client has already obtained the still-current Seasonal Overrides rating
    Without requiring the client to re-fetch the entire rating

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider

    Scenario Outline: Scenario Outline name