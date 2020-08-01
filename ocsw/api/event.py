from ..utils.query_params import query_params


class EventApiMixin:
    async def events(self, source, **kwargs):
        func = self.events_by_stream_id
        if "/" in source:
            func = self.events_by_stream_path
        return await func(source, **kwargs)

    async def events_by_stream_id(self, stream_id, **query):
        """https://rest.octave.dev/#find-events-by-stream-id
        """
        url = self._url(
            "{base_url}/{company_name}/event/{stream_id}", stream_id=stream_id
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def events_by_stream_path(self, stream_path, **query):
        """https://rest.octave.dev/#find-events-by-stream-path
        """
        url = self._url("{base_url}/{company_name}/event")
        params = query_params(**query)
        if stream_path:
            params["path"] = stream_path
        return await self._get(url, params=params)
