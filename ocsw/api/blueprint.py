from ..utils.query_params import query_params

OBJECT_TYPE = "blueprint"


class BlueprintApiMixin:
    async def blueprints(self, company_name=None, path=None, **query):
        """List blueprints.

        https://rest.octave.dev/#listing-company-blueprints
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
        params = query_params(**query)
        if path:
            params["path"] = path
        return await self._get(url, params=params)

    async def inspect_blueprint(
        self, object_id, company_name=None, version_number=None, **query
    ):
        """Retrieve Blueprint info by id.

        https://rest.octave.dev/#listing-company-blueprints
        """
        resource = "{base_url}/{company_name}/{object_type}/{object_id}"
        if version_number is not None:
            resource = (
                "{base_url}/{company_name}/versions/"
                "{object_type}/{object_id}/{version_number}"
            )

        url = self._url(
            resource,
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
            version_number=version_number,
        )
        params = query_params(**query)
        return await self._get(url, params=params)
