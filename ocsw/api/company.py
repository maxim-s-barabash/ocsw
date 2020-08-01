from ..utils.query_params import query_params


class CompanyApiMixin:
    async def companies(self, **query):
        """https://rest.octave.dev/#listing-company
        """
        url = self._url("{base_url}/global/company")
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_company(self, company_id, **query):
        """https://rest.octave.dev/#reading-a-company
        """
        url = self._url(
            "{base_url}/global/company/{company_id}", company_id=company_id
        )
        params = query_params(**query)
        return await self._get(url, params=params)
