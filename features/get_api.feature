Feature: GET API Request

  Scenario: Successful GET request and response time validation
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then the response status code should be 200
    And the response time should be below 1000 milliseconds

  Scenario: Verify all items have non-empty id fields
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then each element should have a non-null,non-empty "id"
    And each episode should have type "episode"

  Scenario: Verify every episode title is present
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then each episode should have a non-empty "title"

  Scenario: Verify only one episode is marked live
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then only one episode should have "live" as true

  Scenario: Verify transmission_start is before transmission_end
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then each item's transmission_start should be before transmission_end

  Scenario: Verify the Date header is present and valid
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest"
    When I send a GET request
    Then the response should have a valid "Date" header

  Scenario: Verify the response status code is 404
    Given the API endpoint "https://testapi.io/api/RMSTest/ibltest/2023-09-11"
    When I send a GET request
    Then the response status code should be 404
    And the error object should contain 'details' and 'http_response_code'
