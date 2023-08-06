import json

import pytest
import responses

from datarobot._experimental.models.user_blueprints import UserBlueprint


@pytest.fixture
def user_blueprint_id():
    return "556cdfbb100d2b0e88585182"


@pytest.fixture
def blueprint_id():
    return "886cdfbb100d2b0e88585182"


@pytest.fixture
def mocked_add_to_menu_response(user_blueprint_id, blueprint_id):
    return {"id": blueprint_id}


@pytest.fixture
def make_user_blueprints_add_to_repo_url(unittest_endpoint):
    def _make_user_blueprints_add_to_repo_url(project_id):
        return "{}/projects/{}/blueprints/fromUserBlueprint/".format(unittest_endpoint, project_id)

    return _make_user_blueprints_add_to_repo_url


@responses.activate
def test_add_to_menu(
    make_user_blueprints_add_to_repo_url,
    project_id,
    user_blueprint_id,
    blueprint_id,
    mocked_add_to_menu_response,
):
    url = make_user_blueprints_add_to_repo_url(project_id)
    responses.add(
        responses.POST,
        url,
        status=201,
        content_type="application/json",
        body=json.dumps(mocked_add_to_menu_response),
    )

    repository_blueprint_id = UserBlueprint.add_to_repository(
        project_id=project_id, user_blueprint_id=user_blueprint_id
    )
    assert repository_blueprint_id == blueprint_id
    assert responses.calls[0].request.method == "POST"
    assert responses.calls[0].request.url == url
