from ..utils.query_params import query_params


class ReleaseApiMixin:
    async def release_note(self, **query):
        """https://rest.octave.dev/#listing-system-wide-release-notes
        """
        company = self._company_identifer
        resource = "release-note" if company else "/release-note"
        url = self._url(resource)
        params = query_params(**query)
        return await self._get(url, params=params)
