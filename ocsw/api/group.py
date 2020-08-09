from ..utils.query_params import query_params


class GroupApiMixin:
    async def groups(self, company_name=None, **query):
        """https://rest.octave.dev/#listing-company-groups
        """
        url = self._url(
            "{base_url}/{company_name}/group",
            company_name=company_name or self.current_company,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_group(self, group_id, company_name=None, **query):
        """https://rest.octave.dev/#listing-company-groups
        """
        url = self._url(
            "{base_url}/{company_name}/group/{group_id}",
            company_name=company_name or self.current_company,
            group_id=group_id,
        )
        params = query_params(**query)
        return await self._get(url, params=params)
