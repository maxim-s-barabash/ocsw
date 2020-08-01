from ..utils.query_params import query_params


class BlueprintApiMixin:
    async def blueprints(self, path=None, **query):
        """List blueprints.

        https://rest.octave.dev/#listing-company-blueprints
        """
        url = self._url("{base_url}/{company_name}/blueprint")
        params = query_params(**query)
        if path:
            params["path"] = path
        return await self._get(url, params=params)

    async def inspect_blueprint(self, blueprint_id, fields=None):
        """Retrieve Blueprint info by id.

        https://rest.octave.dev/#listing-company-blueprints
        """
        url = self._url(
            "{base_url}/{company_name}/blueprint/{blueprint_id}",
            blueprint_id=blueprint_id,
        )
        params = query_params(fields=fields)
        return await self._get(url, params=params)
