
# Common assertions:
def assert200Response(response, message='200 Response must be returned'):
    assert response.status_code == 200, message


def assert400Response(response, message='400 Response must be returned'):
    assert response.status_code == 400, message


def assertJSONFormatResponse(response,
                             message='Response must to be in JSON format'):
    assert response.headers['Content-Type'] == 'application/json', message


def assertPaginatedResponse(response, expected_count,
                            message='Response should contain paginated data'
                            ):
    assert 'results' in response.data, message
    if expected_count:
        assert len(response.data['results']) == expected_count, (
            f'Expected {expected_count} items in the results')
