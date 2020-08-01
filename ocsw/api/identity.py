from ..utils.query_params import query_params


class IdentityApiMixin:
    async def global_identity(self, **query):
        """Retrieve all information about current account.

        Including all of the groups, companies, and shares you belong to.
        https://rest.octave.dev/#authentication
        """
        url = self._url("{base_url}/global/identity")
        params = query_params(**query)
        return await self._get(url, params=params)

    async def identities(self, **query):
        """Retrieve list information about accounts on current company.
        https://rest.octave.dev/#authentication
        """
        url = self._url("{base_url}/{company_name}/identity")
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_identity(self, identity_id, **query):
        """
        https://rest.octave.dev/#identity
        """
        url = self._url(
            "{base_url}/{company_name}/identity/{identity_id}",
            identity_id=identity_id,
        )
        params = query_params(**query)
        return await self._get(url, params=params)
