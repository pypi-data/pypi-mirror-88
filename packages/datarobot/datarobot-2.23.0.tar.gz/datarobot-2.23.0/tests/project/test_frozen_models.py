import responses

from datarobot import FrozenModel, Project


@responses.activate
def test_get_frozen_models_returns_valid_objects(frozen_models_list_response):
    responses.add(
        responses.GET,
        "https://host_name.com/projects/p-id/frozenModels/",
        json=frozen_models_list_response,
        status=200,
    )
    frozen_models = list(Project("p-id").get_frozen_models())
    assert len(frozen_models) == 2
    assert all(isinstance(frozen, FrozenModel) for frozen in frozen_models)
