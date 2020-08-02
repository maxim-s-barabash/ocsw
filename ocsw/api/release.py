from ..utils.query_params import query_params


class ReleaseApiMixin:
    async def release_note(self, **query):
        """https://rest.octave.dev/#listing-system-wide-release-notes
        """
        resource = "{base_url}/release-note"
        if self._company_identifer:
            resource = "{base_url}/{company_name}/release-note"
        url = self._url(resource)
        params = query_params(**query)
        return await self._get(url, params=params)
