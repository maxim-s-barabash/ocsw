from ..utils.query_params import query_params


class DeviceApiMixin:
    async def devices(self, **query):
        """List devices currently registered.

        https://rest.octave.dev/#device-object

        Returns:
            (dict): Devices information dictionary

        Raises:
            :py:class:`ocsw.errors.APIError`
                If volume failed to remove.
        """
        url = self._url("{base_url}/{company_name}/device")
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_device(self, device_identifier, **query):
        """Retrieve Device info by id or name.

        https://rest.octave.dev/#device-object

        Args:
            device_identifier (str): device name or id

        Returns:
            (dict): Device information dictionary

        Raises:
            :py:class:`ocsw.errors.APIError`
                If the server returns an error.
        """
        url = self._url(
            "{base_url}/{company_name}/device/{device_identifier}",
            device_identifier=device_identifier,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def create_device(self, name, imei, fsn):
        """Create a Device.

        https://rest.octave.dev/#creating-a-device

        Args:
            name (str): Device name
            imei (str): IMEI of the Device
            fsn (str): Serial number of the Device

        Returns:
            (dict): Provision information dictionary

        Raises:
            :py:class:`ocsw.errors.APIError`
                If volume failed to remove.
        """
        url = self._url("{base_url}/{company_name}/device/provision")
        payload = dict(name=name, imei=imei, fsn=fsn)
        return await self._post(url, json=payload)

    async def remove_device(self, device_identifier, **query):
        """Remove a Device.

        https://rest.octave.dev/#deleting-a-device

        Args:
            device_identifier (str): device name or id

        Raises:
            :py:class:`ocsw.errors.APIError`
                If volume failed to remove.
        """
        url = self._url(
            "{base_url}/{company_name}/device/{device_identifier}",
            device_identifier=device_identifier,
        )
        params = query_params(**query)
        return await self._delete(url, params=params)

    async def update_device(self, device_identifier, fields=None, props=None):
        """Update a Device.

        https://rest.octave.dev/#updating-a-device
        """
        url = self._url(
            "{base_url}/{company_name}/device/{device_identifier}",
            device_identifier=device_identifier,
        )
        params = query_params(fields)
        payload = props
        return await self._put(url, params=params, json=payload)

    async def transfer_device(self, simulate=False, props=None):
        """Moving a Device to another Company.

        https://rest.octave.dev/#moving-a-device-to-another-company
        """
        url = self._url("{base_url}/{company_name}/device/transfer")
        params = dict()
        if simulate:
            params["simulate"] = simulate
        payload = props
        return await self._put(url, params=params, json=payload)

    async def device_events(self, device_identifier, **query):
        """
        """
        url = self._url(
            "{base_url}/{company_name}/device/events/{device_identifier}",
            device_identifier=device_identifier,
        )
        params = query_params(**query)
        return await self._get(url, params=params)
