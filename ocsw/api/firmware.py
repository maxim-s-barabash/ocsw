from ..utils.query_params import query_params


class FirmwareApiMixin:
    async def firmwares(self, company_name=None, **query):
        """List of available firmware.

        https://rest.octave.dev/#listing-company-firmware-versions
        """
        company_name = company_name or self.current_company

        resource = "{base_url}/firmware"
        ctx = dict()
        if company_name:
            ctx["company_name"] = company_name
            resource = "{base_url}/{company_name}/firmware"

        url = self._url(resource, **ctx)
        params = query_params(**query)
        return await self._get(url, params=params)
