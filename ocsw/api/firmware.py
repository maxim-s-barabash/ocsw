from ..utils.query_params import query_params


class FirmwareApiMixin:
    async def firmwares(self, **query):
        """List of available firmware.

        https://rest.octave.dev/#listing-company-firmware-versions
        """
        resource = "{base_url}/firmware"
        if self._company_identifer:
            resource = "{base_url}/{company_name}/firmware"

        url = self._url(resource)
        params = query_params(**query)
        return await self._get(url, params=params)
