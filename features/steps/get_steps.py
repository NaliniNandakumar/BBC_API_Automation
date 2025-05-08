import requests
from behave import given, when, then
from datetime import datetime
from email.utils import parsedate_to_datetime

@given('the API endpoint "{url}"')
def step_given_api_endpoint(context, url):
    context.url = url

@when('I send a GET request')
def step_when_get_request(context):
    try:
        response = requests.get(context.url, timeout=5)  # Add timeout
        context.response = response
        context.response_time_ms = response.elapsed.total_seconds() * 1000  # convert to milliseconds
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Failed to send GET request: {str(e)}")

@then('the response status code should be {expected_status:d}')
def step_then_status_code(context, expected_status):
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected {expected_status}, got {actual_status}"

@then('the response time should be below {threshold:d} milliseconds')
def step_then_response_time(context, threshold):
    assert context.response_time_ms < threshold, \
        f"Response time was {context.response_time_ms:.2f} ms, expected under {threshold} ms"
    
@then('each element should have a non-null,non-empty "{field}"')
def step_check_element_ids(context, field):
    elements = context.response.json()["schedule"]["elements"]

    for index, item in enumerate(elements):
        value = item.get(field)
        assert value and str(value).strip(), f"Element at index {index} has invalid '{field}': {value}"

@then('each episode should have type "{expected_type}"')
def step_check_episode_type(context, expected_type):
    elements = context.response.json()["schedule"]["elements"]

    for index, item in enumerate(elements):
        episode = item.get("episode")
        assert episode is not None, f"Item at index {index} missing 'episode'"

        actual_type = episode.get("type")
        assert actual_type == expected_type, \
            f"Episode at index {index} has type '{actual_type}', expected '{expected_type}'"
        
@then('each episode should have a non-empty "{field}"')
def step_check_episode_field_not_empty(context, field):
    elements = context.response.json()["schedule"]["elements"]

    for index, item in enumerate(elements):
        episode = item.get("episode")
        assert episode is not None, f"Item at index {index} missing 'episode'"

        value = episode.get(field)
        assert value and str(value).strip(), \
            f"Episode at index {index} has empty or missing '{field}': {value}"
        
@then('only one episode should have "live" as true')
def step_check_only_one_live_episode(context):
    elements = context.response.json()["schedule"]["elements"]

    live_count = 0
    for index, item in enumerate(elements):
        episode = item.get("episode")
        if episode and episode.get("live") is True:
            live_count += 1

    assert live_count == 1, f"Expected only one episode with 'live': true, found {live_count}"

@then('each item\'s transmission_start should be before transmission_end')
def step_check_transmission_order(context):
    elements = context.response.json()["schedule"]["elements"]

    for index, item in enumerate(elements):
        start = item.get("transmission_start")
        end = item.get("transmission_end")

        assert start and end, f"Missing transmission_start or transmission_end at index {index}"

        start_time = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(end.replace("Z", "+00:00"))

        assert start_time < end_time, (
            f"transmission_start is not before transmission_end at index {index}: "
            f"{start_time} >= {end_time}"
        )

@then('the response should have a valid "Date" header')
def step_verify_date_header(context):
    date_header = context.response.headers.get("Date")

    assert date_header is not None, "Missing 'Date' header in response"

    try:
        parsed_date = parsedate_to_datetime(date_header)
    except Exception as e:
        raise AssertionError(f"Invalid 'Date' header format: {date_header} — Error: {e}")


@then("the error object should contain 'details' and 'http_response_code'")
def step_verify_error_object_properties(context):
    response_json = context.response.json()

    assert "error" in response_json, "Missing 'error' object in the response"

    error = response_json["error"]

    assert "details" in error, "Missing 'details' in the error object"
    assert "http_response_code" in error, "Missing 'http_response_code' in the error object"