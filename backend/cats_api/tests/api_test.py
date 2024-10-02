import pytest
from cats.models import Breed, Cat, Color

from .test_utils import (assert200Response, assert400Response,
                         assertJSONFormatResponse, assertPaginatedResponse)


@pytest.fixture
def precreated_breeds():
    '''
    Create three breed instances and returns breed instances.
    '''
    breeds_infos = [
        {'name': 'unique_breed'},
        {'name': 'myth_breed'},
        {'name': 'ordinary_breed'}
    ]
    breeds_list = [
        Breed(**breed_info)
        for breed_info in breeds_infos
    ]
    breeds = Breed.objects.bulk_create(breeds_list)
    return breeds


@pytest.fixture
def precreated_colors():
    '''
    Create three colors instances and returns color instances.
    '''
    colors_infos = [
        {'name': 'blue'},
        {'name': 'grey'},
        {'name': 'black'}
    ]
    colors_list = [
        Color(**color_info)
        for color_info in colors_infos
    ]
    colors = Color.objects.bulk_create(colors_list)
    return colors


@pytest.fixture
def precreated_cats(create_user, precreated_breeds, precreated_colors):
    '''
    Create three cat instances and return theirs info as list of dicts.
    '''
    user = create_user()
    cats_infos = [
        {'name': 'TommyTheCat',
            'age': 30,
            'description': 'A strange one.',
            'breed': precreated_breeds[0],
            'color': precreated_colors[0],
            'owner': user},
        {'name': 'Garfield',
            'age': 200,
            'description': 'A fat one.',
            'breed': precreated_breeds[1],
            'color': precreated_colors[1],
            'owner': user},
        {'name': 'Cheshire',
            'age': 300,
            'description': 'A mysterious one.',
            'breed': precreated_breeds[2],
            'color': precreated_colors[2],
            'owner': user}
    ]
    cats = [
        Cat(**cat_info)
        for cat_info in cats_infos
    ]
    Cat.objects.bulk_create(cats)
    return cats_infos


class TestBreedAPI:
    '''
    Test endpoints related to breed instances.

    Endpoits:
    GET /api/breeds/ Get all cats breed instances.
    POST /api/breeds/ Make new breed instance.

    DELETE /api/breeds/1/ Delete specific breed instance.
    '''
    BASE_URL = '/api/breeds/'
    BreedModel = Breed

    @pytest.mark.django_db
    def test_get_list_of_breeds(self, client, precreated_breeds):
        '''Check that any user can get paginated list of breed instances.'''
        # Arrange
        url = self.BASE_URL
        # Act
        response = client.get(url)
        # Assert
        assert200Response(response)
        assertJSONFormatResponse(response)
        assertPaginatedResponse(response, expected_count=3)

        expected_names = [breed_info['name'] for breed_info
                          in precreated_breeds]
        returned_names = [breed['name'] for breed in response.data['results']]
        assert sorted(returned_names) == sorted(expected_names), (
            'Returned breed names do not match expected ones')

    @pytest.mark.parametrize(
        "user_client, expected_status",
        [
            ("api_client", 401),
            ("api_client_with_credentials", 403),
            ("api_staff_client_with_credentials", 201),
        ]
    )
    def test_only_staff_member_can_create_breed_instance(
            self, user_client, expected_status, request):
        # Arrange
        url = self.BASE_URL
        data = {
            'name': 'new_breed',
        }
        # Get the actual fixture
        user_client = request.getfixturevalue(user_client)
        # Act
        response = user_client.post(url, data, format='json')
        # Assert
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "error_reason, post_data",
        [('unqiue constraint violation', {"name": "ordinary_breed"}),
         ('invalid name field format', {""}),
         ('empty request load', {}),
         ]
    )
    def test_cannot_create_breed_instance_with_invalid_data(
            self, api_staff_client_with_credentials,
            precreated_breeds, post_data, error_reason):
        '''Test that request with invalid data will recieve error reponse.'''
        # Arrange
        url = self.BASE_URL
        client = api_staff_client_with_credentials
        # Act
        response = client.post(url, post_data, format='json')
        # Assert
        assert400Response(response, message=('Breed must not be created '
                                             'because request data has '
                                             f'{error_reason}'))

    @pytest.mark.parametrize(
        "user_client, expected_status",
        [
            ("client", 401),
            ("api_client_with_credentials", 403),
            ("api_staff_client_with_credentials", 204),
        ]
    )
    @pytest.mark.django_db
    def test_only_staff_member_can_delete_breed_instance(
            self, user_client, expected_status, request, precreated_breeds):
        # Arrange
        url = f'{self.BASE_URL}1/'
        # Get the actual fixture
        user_client = request.getfixturevalue(user_client)
        # Act
        response = user_client.delete(url)
        # Assert
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_client, expected_status",
        [
            ("client", 401),
            ("api_client_with_credentials", 403),
            ("api_staff_client_with_credentials", 200),
        ]
    )
    @pytest.mark.django_db
    def test_only_staff_member_can_update_breed_instance(
        self, user_client, expected_status, request, precreated_breeds
    ):
        # Arrange
        url = f'{self.BASE_URL}1/'
        data = {
            'name': 'new_breed',
        }
        # Get the actual fixture
        user_client = request.getfixturevalue(user_client)
        # Act
        response = user_client.put(url, data)
        # Assert
        assert response.status_code == expected_status


class TestCatAPI:
    '''
    Test endpoints related to cats instances.

    Endpoints:
    GET /api/cats/ Get all cats instances.
    POST /api/cats/ Make new cat instance.

    GET /api/cats/id/ Get specific cat instance.
    PATCH /api/cats/id/ Update specific cat instance.
    PUT /api/cats/id/ Replace specific cat instance.
    DELETE /api/cats/id/ Delete specific cat isntance.
    '''

    BASE_URL = '/api/cats/'
    CatModel = Cat

    def test_get_list_of_cat_instances(self, client, precreated_cats):
        # Arrange
        url = self.BASE_URL
        # Act
        response = client.get(url)
        # Assert
        assert200Response(response)
        assertJSONFormatResponse(response)
        assertPaginatedResponse(response, expected_count=3)

        expected_names = [cat_info['name'] for cat_info in precreated_cats]
        returned_names = [cat['name'] for cat in response.data['results']]
        assert sorted(returned_names) == sorted(expected_names), (
            'Returned cat names do not match expected ones')

    def test_owner_field_is_string(self, client, precreated_cats):
        '''Test that owner field in each instance of cat returns as a string'''
        # Arrange
        url = self.BASE_URL
        # Act
        response = client.get(url)
        # Assert
        assert200Response(response)
        assertJSONFormatResponse(response)
        assertPaginatedResponse(response, expected_count=3)

        returned_owner = response.data['results'][0]['owner']
        assert isinstance(returned_owner, str), (
            '"Owner" field must be string, not link or id'
        )

    def test_color_field_is_string(self, client, precreated_cats):
        '''Test that color field in each instance of cat returns as a string'''
        # Arrange
        url = self.BASE_URL
        # Act
        response = client.get(url)
        # Assert
        assert200Response(response)
        assertJSONFormatResponse(response)
        assertPaginatedResponse(response, expected_count=3)

        returned_color = response.data['results'][0]['color']
        assert isinstance(returned_color, str), (
            '"Owner" field must be string, not link or id'
        )


    """
    @pytest.mark.parametrize("url, expected_status_code, err_msg", [
        ('api/cats/1/', 200, 'User must be able to get specific cat info'),
        ('api/cats/9999/', 404, 'User must get 404 error when'
                              'trying to get non-existing cat')
    ])
    def test_get_a_specific_cat_instance(self, client, pre_created_cats):
        # Act
        response = client.get(url)
        # Asserts
        assert response.status_code == expected_status_code
        if expected_status_code == 200:
            assert pre_created_cats[0] in response.data['results'], (
                'Specific cat info must to be in response data.'
            )


    def test_make_a_new_cat_instance_with_valid_data(
            self, auto_login_user, client):
        # Arrange
        authenticated_client, user = auto_login_user()
        url = self.BASE_URL
        cat_data = {
            'name': 'Felix The Cat',
            'age': 100,
            'description': 'An old one cat.',
        }
        # Act
        response = client.get(url, cat_data)
        # Assert
        assert response.status_code == 204
        new_created_cat = self.CatModel.objects.get(name=cat_data['name'])
        assert new_created_cat.age == cat_data['age']
        assert new_created_cat.description == cat_data['description']
        assert new_created_cat.owner == user, ('Request user must  be'
                                               'a cat owner.')

    @pytest.mark.parametrize("url, expected_status_code, err_msg",[
    ('/api/cats/1/', 200, 'User must be able to get info about existing car'),
    ('/api/cars/9999/', 404,)
    ])
    def test_make_a_new_cat_instance_with_invalid_data(
    )
    """