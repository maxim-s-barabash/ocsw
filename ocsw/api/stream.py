from ..utils.query_params import query_params


class StreamApiMixin:
    async def streams(self, company_name=None, **query):
        """https://rest.octave.dev/#listing-company-streams
        """
        url = self._url(
            "{base_url}/{company_name}/stream",
            company_name=company_name or self.current_company,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_stream(self, stream_id, company_name=None, **query):
        """https://rest.octave.dev/#reading-a-stream
        """
        url = self._url(
            "{base_url}/{company_name}/stream/{stream_id}",
            company_name=company_name or self.current_company,
            stream_id=stream_id,
        )
        params = query_params(**query)
        return await self._get(url, params=params)
