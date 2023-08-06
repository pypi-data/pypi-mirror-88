def assert_version(version, version_json):
    assert version.id == version_json["id"]
    assert version.environment_id == version_json["environmentId"]
    assert version.label == version_json["label"]
    assert version.description == version_json["description"]
    assert version.build_status == version_json["buildStatus"]
    assert version.created_at == version_json["created"]


def assert_custom_model_version(version, version_json):
    assert version.id == version_json["id"]
    assert version.custom_model_id == version_json["customModelId"]
    assert version.label == version_json["label"]
    assert version.description == version_json["description"]
    assert version.version_minor == version_json["versionMinor"]
    assert version.version_major == version_json["versionMajor"]
    assert version.is_frozen == version_json["isFrozen"]
    assert version.base_environment_id == version_json.get("baseEnvironmentId")

    assert len(version.items) == len(version_json["items"])
    for item, item_json in zip(version.items, version_json["items"]):
        assert item.id == item_json["id"]
        assert item.file_name == item_json["fileName"]
        assert item.file_path == item_json["filePath"]
        assert item.file_source == item_json["fileSource"]
        assert item.created_at == item_json["created"]

    assert len(version.dependencies) == len(version_json.get("dependencies", []))
    for dependency, dependency_json in zip(
        version.dependencies, version_json.get("dependencies", [])
    ):
        assert dependency.package_name == dependency_json["packageName"]
        assert dependency.line == dependency_json["line"]
        assert dependency.line_number == dependency_json["lineNumber"]

        for constraint, constraint_json in zip(
            dependency.constraints, dependency_json["constraints"]
        ):
            assert constraint.version == constraint_json["version"]
            assert constraint.constraint_type == constraint_json["constraintType"]

    assert version.created_at == version_json["created"]
    assert version.network_egress_policy == version_json["networkEgressPolicy"]
    assert version.desired_memory == version_json["desiredMemory"]
    assert version.maximum_memory == version_json["maximumMemory"]
    assert version.replicas == version_json["replicas"]


def assert_custom_model_version_dependency_build(
    build_info, build_info_json, custom_model_id, custom_model_version_id
):
    assert build_info.custom_model_id == custom_model_id
    assert build_info.custom_model_version_id == custom_model_version_id

    assert build_info.started_at == build_info_json["buildStart"]
    assert build_info.completed_at == build_info_json["buildEnd"]
    assert build_info.build_status == build_info_json["buildStatus"]
