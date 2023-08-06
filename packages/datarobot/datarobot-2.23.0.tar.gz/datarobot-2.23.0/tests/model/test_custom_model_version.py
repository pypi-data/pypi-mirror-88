from collections import defaultdict
from copy import deepcopy
import json
import os
import uuid

import pytest
from requests_toolbelt import MultipartEncoder
import responses

from datarobot import CustomModelVersion
from datarobot.errors import InvalidUsageError
from tests.model.utils import assert_custom_model_version


@pytest.fixture
def mocked_version(mocked_custom_model_version):
    return mocked_custom_model_version


@pytest.fixture
def mocked_version_with_resources(mocked_custom_model_version_with_resources):
    return mocked_custom_model_version_with_resources


@pytest.fixture
def make_versions_url(unittest_endpoint):
    def _make_versions_url(environment_id, version_id=None):
        base_url = "{}/customModels/{}/versions/".format(unittest_endpoint, environment_id)
        if version_id is not None:
            return "{}{}/".format(base_url, version_id)
        return base_url

    return _make_versions_url


def mock_get_response(url, response):
    responses.add(
        responses.GET, url, status=200, content_type="application/json", body=json.dumps(response),
    )


def test_from_server_data(mocked_version):
    version = CustomModelVersion.from_server_data(mocked_version)
    assert_custom_model_version(version, mocked_version)


@responses.activate
@pytest.mark.parametrize(
    "version_json",
    [
        "mocked_version",
        "mocked_custom_model_version_no_dependencies",
        "mocked_custom_model_version_no_base_environment",
        "mocked_custom_model_version_future_field_in_version",
        "mocked_custom_model_version_future_field_in_dependency",
        "mocked_custom_model_version_future_field_in_constraint",
    ],
)
def test_get_version(request, version_json, make_versions_url):
    # arrange
    version_json = request.getfixturevalue(version_json)
    url = make_versions_url(version_json["customModelId"], version_json["id"])
    mock_get_response(url, version_json)

    # act
    version = CustomModelVersion.get(version_json["customModelId"], version_json["id"])

    # assert
    assert_custom_model_version(version, version_json)

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url


@responses.activate
def test_list_versions(mocked_versions, make_versions_url):
    # arrange
    custom_model_id = mocked_versions["data"][0]["customModelId"]
    url = make_versions_url(custom_model_id)
    mock_get_response(url, mocked_versions)

    # act
    versions = CustomModelVersion.list(custom_model_id)

    # assert
    assert len(versions) == len(mocked_versions["data"])
    for version, mocked_version in zip(versions, mocked_versions["data"]):
        assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url


@responses.activate
def test_list_versions_multiple_pages(mocked_versions, make_versions_url):
    # arrange
    custom_model_id = mocked_versions["data"][0]["customModelId"]

    url1 = make_versions_url(custom_model_id)
    url2 = make_versions_url(custom_model_id) + "2"

    mocked_versions_2nd = deepcopy(mocked_versions)
    mocked_versions["next"] = url2

    mock_get_response(url1, mocked_versions)
    mock_get_response(url2, mocked_versions_2nd)

    # act
    versions = CustomModelVersion.list(custom_model_id)

    # assert
    assert len(versions) == len(mocked_versions["data"]) + len(mocked_versions_2nd["data"])
    for version, mocked_version in zip(
        versions, mocked_versions["data"] + mocked_versions_2nd["data"]
    ):
        assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url1
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == url2


@responses.activate
def test_download(mocked_version, make_versions_url, tmpdir):
    # arrange
    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    mock_get_response(url, mocked_version)
    responses.add(
        responses.GET,
        url + "download/",
        status=200,
        content_type="application/json",
        body=b"content",
    )

    downloaded_file = tmpdir.mkdir("sub").join("download")
    downloaded_file_path = str(downloaded_file)

    # act
    version = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    version.download(downloaded_file_path)

    # assert
    downloaded_file.read() == b"content"

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == url + "download/"


@responses.activate
def test_update(mocked_version, make_versions_url):
    # arrange
    attrs = {"description": "xx"}

    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    mock_get_response(url, mocked_version)

    mocked_version.update(attrs)

    responses.add(
        responses.PATCH,
        url,
        status=200,
        content_type="application/json",
        body=json.dumps(mocked_version),
    )

    # act
    version = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    version.update(**attrs)

    # assert
    assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "PATCH"
    assert responses.calls[1].request.url == url
    assert responses.calls[1].request.body == json.dumps(attrs).encode()


@responses.activate
def test_refresh(mocked_version, make_versions_url):
    # arrange
    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    mock_get_response(url, mocked_version)

    mocked_version.update({"description": "xx"})

    mock_get_response(url, mocked_version)

    # act
    version = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    version.refresh()

    # assert
    assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == url


@responses.activate
@pytest.mark.parametrize("mocked_fixture_name", ["mocked_version", "mocked_version_with_resources"])
def test_create_clean(request, mocked_fixture_name, make_versions_url, tmpdir, base_environment_id):
    mocked_version = request.getfixturevalue(mocked_fixture_name)

    url = make_versions_url(mocked_version["customModelId"])

    responses.add(
        responses.POST,
        make_versions_url(mocked_version["customModelId"]),
        status=200,
        content_type="application/json",
        body=json.dumps(mocked_version),
    )

    file = tmpdir.mkdir("sub").join("file")
    file.write(b"content")
    file_path = str(file)

    version = CustomModelVersion.create_clean(
        mocked_version["customModelId"],
        base_environment_id,
        True,
        files=[(file_path, "/d/file.txt")],
        network_egress_policy=mocked_version["networkEgressPolicy"],
        desired_memory=mocked_version["desiredMemory"],
        maximum_memory=mocked_version["maximumMemory"],
        replicas=mocked_version["replicas"],
    )
    assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "POST"
    assert responses.calls[0].request.url == url


@responses.activate
def test_create_from_previous(mocked_version, make_versions_url, tmpdir, base_environment_id):
    url = make_versions_url(mocked_version["customModelId"])

    responses.add(
        responses.PATCH,
        make_versions_url(mocked_version["customModelId"]),
        status=200,
        content_type="application/json",
        body=json.dumps(mocked_version),
    )

    file = tmpdir.mkdir("sub").join("file")
    file.write(b"content")
    file_path = str(file)

    version = CustomModelVersion.create_from_previous(
        mocked_version["customModelId"],
        base_environment_id,
        True,
        files=[(file_path, "/d/file.txt")],
        files_to_delete=["2323423423423423"],
    )
    assert_custom_model_version(version, mocked_version)

    assert responses.calls[0].request.method == "PATCH"
    assert responses.calls[0].request.url == url


@responses.activate
@pytest.mark.parametrize(
    "method",
    [
        (CustomModelVersion.create_clean, "POST"),
        (CustomModelVersion.create_from_previous, "PATCH"),
    ],
)
@pytest.mark.parametrize(
    "expected_folder_paths",
    [None, [], ["a.zip", "a/a.zip", "sub/a.txt", "sub/b.pdf", "sub/sub2/c.rtf"]],
)
@pytest.mark.parametrize("expected_file_paths", [None, [], ["y.xyz", "dd/ttt.txt"]])
def test_create_folder_and_files(
    mocked_version,
    make_versions_url,
    tmpdir,
    method,
    expected_folder_paths,
    expected_file_paths,
    base_environment_id,
):
    custom_model_version_method = method[0]
    http_method = method[1]

    # arrange
    responses.add(
        http_method,
        make_versions_url(mocked_version["customModelId"]),
        status=200,
        body=json.dumps(mocked_version),
    )

    # arrange: create folder with required structure to be uploaded
    folder_path = None
    if expected_folder_paths:
        folder_path = tmpdir.mkdir(str(uuid.uuid4()))
        for expected_path in expected_folder_paths:
            path_items, file = os.path.split(expected_path)
            d = folder_path
            if path_items:
                for path_item in path_items.split("/"):
                    if os.path.exists(os.path.join(str(d), path_item)):
                        d = d.join(path_item)
                    else:
                        d = d.mkdir(path_item)
            d.join(file).write(b"content")
        folder_path = str(folder_path)

    # arrange: create files to be uploaded
    files = None
    if expected_file_paths:
        files = []
        for expected_path in expected_file_paths:
            file = tmpdir.join(str(uuid.uuid4()))
            file.write(b"content")
            files.append((str(file), expected_path))

    # act
    custom_model_version_method(
        mocked_version["customModelId"],
        base_environment_id,
        True,
        folder_path=folder_path,
        files=files,
    )

    # assert
    req = responses.calls[0].request
    assert req.method == http_method
    assert req.url == make_versions_url(mocked_version["customModelId"])
    assert isinstance(req.body, MultipartEncoder)

    # get fields submitted with request
    fields = defaultdict(list)
    for name, value in req.body.fields:
        fields[name].append(value)

    assert len(fields["isMajorUpdate"]) == 1
    assert fields["isMajorUpdate"][0] == "True"

    files = fields["file"]
    file_paths = fields["filePath"]

    # verify that files & filePaths make pairs
    assert len(files) == len(file_paths)
    for file, file_path in zip(files, file_paths):
        assert file[0] == os.path.basename(file_path)

    expected_folder_paths = expected_folder_paths or []
    expected_file_paths = expected_file_paths or []

    # There's an option to create a custom model version by passing a pass to a directory.
    # For such a directory, files are created with expected_folder_paths.
    # As there's no control in what order filesystem reads files from a such a directory,
    # convert paths to set and then assert
    assert set(file_paths) == set(expected_folder_paths) | set(expected_file_paths)


@responses.activate
def test_create_with_missing_desired_memory_resource(
    mocked_version_with_resources, make_versions_url, tmpdir, base_environment_id
):
    mocked_version = mocked_version_with_resources

    responses.add(
        responses.POST,
        make_versions_url(mocked_version["customModelId"]),
        status=200,
        content_type="application/json",
        body=json.dumps(mocked_version),
    )

    with pytest.raises(InvalidUsageError):
        CustomModelVersion.create_clean(
            mocked_version["customModelId"],
            base_environment_id,
            True,
            network_egress_policy=mocked_version["networkEgressPolicy"],
            maximum_memory=mocked_version["maximumMemory"],
            replicas=mocked_version["replicas"],
        )


@responses.activate
def test_get_feature_impact(mocked_version, make_versions_url, feature_impact_server_data):
    # arrange
    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    mock_get_response(url, mocked_version)
    responses.add(
        responses.GET,
        url + "featureImpact/",
        status=200,
        content_type="application/json",
        body=json.dumps(feature_impact_server_data),
    )

    # act
    image = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    feature_impacts = image.get_feature_impact()

    # assert
    assert feature_impacts == feature_impact_server_data["featureImpacts"]

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == url + "featureImpact/"


@responses.activate
def test_get_feature_impact_with_metadata(
    mocked_version,
    make_versions_url,
    feature_impact_server_data,
    feature_impact_server_data_filtered,
):
    # arrange
    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    mock_get_response(url, mocked_version)
    responses.add(
        responses.GET,
        url + "featureImpact/",
        status=200,
        content_type="application/json",
        body=json.dumps(feature_impact_server_data),
    )

    # act
    image = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    feature_impacts = image.get_feature_impact(with_metadata=True)

    # assert
    assert feature_impacts == feature_impact_server_data_filtered

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == url + "featureImpact/"


@responses.activate
def test_calculate_feature_impact(unittest_endpoint, mocked_version, make_versions_url):
    # arrange
    status_url = "{}/status_url".format(unittest_endpoint)
    url = make_versions_url(mocked_version["customModelId"], mocked_version["id"])
    impact_url = url + "featureImpact/"
    mock_get_response(url, mocked_version)

    responses.add(
        responses.POST,
        impact_url,
        status=200,
        content_type="application/json",
        headers={"Location": status_url},
        # this ID is ignored, we only use headers and we dont' have a real ID from the backend.
        body=json.dumps({"status_id": "5cf4d3f5f930e26daac18a1a"}),
    )

    responses.add(
        responses.GET, status_url, headers={"Location": url}, status=303,
    )

    # act
    image = CustomModelVersion.get(mocked_version["customModelId"], mocked_version["id"])
    image.calculate_feature_impact()

    # assert

    assert responses.calls[0].request.method == "GET"
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.method == "POST"
    assert responses.calls[1].request.url == impact_url
    assert responses.calls[2].request.method == "GET"
    assert responses.calls[2].request.url == status_url
