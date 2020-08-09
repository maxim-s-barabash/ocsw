"""Edge Action (Local Action).

Arbitrary JavaScript function, executed when an Event is generated
from an Observation. Can transform or generate further Events.
"""

from ..errors import InvalidResource
from ..utils.query_params import query_params

OBJECT_TYPE = "local-action"


class EdgeActionApiMixin:
    async def edge_actions(self, company_name=None, **query):
        """List of edge actions on device.

        https://rest.octave.dev/#listing-company-edge-actions
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_edge_action(
        self, object_id, company_name=None, version_number=None, **query
    ):
        """Reading an Edge Action.

        https://rest.octave.dev/#reading-an-edge-action
        """
        resource = "{base_url}/{company_name}/{object_type}/{object_id}"
        if version_number is not None:
            resource = (
                "{base_url}/{company_name}/versions/"
                "{object_type}/{object_id}/{version_number}"
            )

        url = self._url(
            resource,
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
            version_number=version_number,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def create_edge_action(self, source, js_body="", company_name=None):
        """Update an Edge Action.

        https://rest.octave.dev/#creating-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
        if not source.startswith("observation://"):
            msg = "Source always must start with observation:// not {source!r}"
            raise InvalidResource(msg)
        payload = dict(source=source, js=js_body)
        return await self._post(url, json=payload)

    async def remove_edge_action(self, object_id, company_name=None):
        """Delete an Edge Action.

        https://rest.octave.dev/#deleting-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}/{object_id}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
        )
        return await self._delete(url)

    async def update_edge_action(
        self, object_id, fields=None, props=None, company_name=None
    ):
        """Update an Edge Action.

        https://rest.octave.dev/#updating-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}/{object_id}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
        )
        params = query_params(fields)
        payload = props
        return await self._put(url, params=params, json=payload)
