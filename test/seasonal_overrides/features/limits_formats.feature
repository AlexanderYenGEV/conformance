@seasonal_overrides
Feature: Provide seasonal overrides rating in appropriate formats

    As a Clearinghouse Operator
    I want to provide seasonal overrides ratings in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
        Given a TROLIE client that has been authenticated as a Ratings Provider
        And Seasonal Override data is preloaded

    # GET
    Scenario Outline: Get seasonal overrides    
        Given the Accept header is set to `<content_type>`
        When the client requests the current seasonal override 
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid
        
        Examples:
        | content_type |
        | application/vnd.trolie.seasonal-override-set.v1+json |

    # POST
    Scenario Outline: Create a new seasonal override
        Given the Content-type header is set to `<content_type>`
        And the Seasonal Override body is generated
        When the client creates a new seasonal override
        Then the response is 201 OK
        And the Content-Type header in the response is `<content_type>`
        And the response is schema-valid

        Examples:
        | content_type |
        | application/vnd.trolie.seasonal-override.v1+json |

    # GET
    Scenario Outline: Obtain a specific temporary seasonal rating by id
        Given the Accept header is set to `<content_type>`
        When the client requests for a seasonal override by its id
        Then the response is 200 OK
        And the Content-Type header in the response is `<content_type>`
        #And the response is schema-valid
        
        Examples:
        | content_type |
        | application/vnd.trolie.seasonal-override.v1+json |

    # DELETE
    Scenario Outline: Delete a specific seasonal override by its id
        Given a Seasonal Override is created 
        When the client deletes a seasonal override by its id
        Then the response is 204 No Content

    # PUT 
    Scenario Outline: Update an existing seasonal override
        Given the updated body is generated for the existing seasonal override
        And the Content-type header is set to `<content_type>`
        When the client updates an existing seasonal override by its id
        Then the response is 204 No Content

        Examples:
        | content_type |
        | application/vnd.trolie.seasonal-override.v1+json |


