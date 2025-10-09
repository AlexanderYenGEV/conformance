@temporary_aar_exceptions
Feature: Provide Temporary AAR Exceptions in proper format

    As a Clearinghouse Operator
    I want to provide temporary aar exceptions in a variety of formats
    when a client sends the appropriate media type
    So that clients can obtain the data in the format they need
    Without defining a generalized query capability, like OData or GraphQL

    Background: Authenticated as a Ratings Provider
      Given a TROLIE client that has been authenticated as a Ratings Provider
      Given the Accept header is set to `application/vnd.trolie.temporary-aar-exception.v1+json`
      Given the Content-type header is set to `application/vnd.trolie.temporary-aar-exception.v1+json`
    
    # GET 
    Scenario Outline: Get Temporary AAR Exceptions
        Given the Accept header is set to `application/vnd.trolie.temporary-aar-exception-set.v1+json`
        When the client requests for Temporary AAR Exceptions
        Then the response is 200 OK
        And the Content-Type header in the response is `application/vnd.trolie.temporary-aar-exception-set.v1+json`
        # And the response is schema-valid
    
    # POST 
    Scenario Outline: Create a new Temporary AAR Exception
        Given the Temporary AAR Exception is generated for the resource <resource_id>
        When the client creates a new Temporary AAR Exception
        Then the response is 201 OK
        And the Content-Type header in the response is `application/vnd.trolie.temporary-aar-exception.v1+json`
        # And the response is schema-valid

        Examples:
        | resource_id |
        | HEARN.34562.1 |

    Scenario Outline: Creating a Temporary AAR Exception with overlapping times on the same segment should return 409 error
        Given the Temporary AAR Exception is generated for the resource <resource_id>
        And the client creates a new Temporary AAR Exception
        When the client creates an overlapping Temporary AAR Exception for the same resource <resource_id>
        Then the response is 409 Conflict: Temporary AAR Exception has overlapping times

        Examples:
        | resource_id |
        | BRIGHTON.PS2.PS2 |


    # GET
    Scenario Outline: Get specific Temporary AAR Exception by ID
        Given a Temporary AAR Exception is generated right now for the resource <resource_id>
        And the id of the created Temporary AAR Exception is obtained
        When the client requests for the specific Temporary AAR Exception by id
        Then the response is 200 OK
        And the ID in the response should match the id of the created Temporary AAR Exception
        And the Content-Type header in the response is `application/vnd.trolie.temporary-aar-exception.v1+json`
        # And the response is schema-valid

        Examples:
        | resource_id | 
        | PARKHILL.T5.T5 |

    # DELETE
    Scenario Outline: Delete a specific Temporary AAR Exception by ID that is not in use
        Given a Temporary AAR Exception is generated right now for the resource <resource_id>
        When the client deletes a specific Temporary AAR Exception by id
        Then the response is 204 OK

        Examples:
        | resource_id |
        | MOSELLE2.34591.1 |

    # bug : lets me delete if start-time is in the past but end-time is in the future
    Scenario Outline: Deleting a Temporary AAR Exception in use should return a 409 error
        Given a Temporary AAR Exception is generated right now for the resource <resource_id>
        When the client deletes the most recently created Temporary AAR Exception
        Then the response is 409 Conflict: Temporary AAR Exception in use

        Examples:
        | resource_id |
        | MOSELLE2.34591.1 |
    
    Scenario Outline: Deleting a Temporary AAR Exception in the past is not permitted and should return a 409 error
        Given a Temporary AAR Exception is generated in the past for the resource <resource_id>
        When the client deletes a specific Temporary AAR Exception created in the past
        Then the response is 409 Conflict: Temporary AAR Exception in the past

        Examples:
        | resource_id |
        | MOSELLE2.34591.1 |

    # PUT
    Scenario Outline: Update an existing Temporary AAR Exception
        Given a Temporary AAR Exception is generated right now for the resource <resource_id>
        And the id of the created Temporary AAR Exception is obtained
        And the updated Temporary AAR Exception is generated for the resource <resource_id>
        When the client updates an existing Temporary AAR Exception by id
        Then the response is 204 OK

        Examples:
        | resource_id |
        | DOUGLAS.1215.1 |

   Scenario Outline: Updating Temporary AAR Exceptions in the past only allow changing the reason
        Given a Temporary AAR Exception is generated in the past for the resource <resource_id>
        And the body contains a Temporary AAR Exception with fields other than `reason` changed
        When the client updates the past Temporary AAR Exception
        Then the response is 409 Conflict: Temporary AAR Exception in the past

        Examples:
        | resource_id |
        | PARKHILL.T2.T2 IN |


    