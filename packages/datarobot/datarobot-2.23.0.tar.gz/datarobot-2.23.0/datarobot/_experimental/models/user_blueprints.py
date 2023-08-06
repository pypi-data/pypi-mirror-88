from datarobot.models.api_object import APIObject


class UserBlueprint(APIObject):
    """A user blueprint.

    .. versionadded:: v2.21
    """

    @classmethod
    def add_to_repository(cls, project_id, user_blueprint_id):
        """Add a user blueprint to a project's repository

        .. versionadded:: v2.21

        Parameters
        ----------
        project_id: str
            the id of the project
        user_blueprint_id: str
            the id of the user blueprint

        Returns
        -------
        str or None
            blueprint_id if the user blueprint was successfully
            added to the repository. None otherwise.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        route = "projects/{}/blueprints/fromUserBlueprint/".format(project_id)
        payload = {
            "user_blueprint_id": user_blueprint_id,
        }
        response = cls._client.post(route, data=payload)
        return response.json().get("id")
