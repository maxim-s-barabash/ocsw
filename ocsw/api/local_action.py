"""Edge Action (Local Action).

Arbitrary JavaScript function, executed when an Event is generated
from an Observation. Can transform or generate further Events.
"""

from ..errors import InvalidResource
from ..utils.query_params import query_params


class EdgeActionApiMixin:
    async def edge_actions(self, company_name=None, **query):
        """List of edge actions on device.

        https://rest.octave.dev/#listing-company-edge-actions
        """
        ctx = dict()
        if company_name:
            ctx["company_name"] = company_name

        url = self._url("{base_url}/{company_name}/local-action", **ctx)
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_edge_action(self, action_id, **query):
        """Reading an Edge Action.

        https://rest.octave.dev/#reading-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/local-action/{action_id}",
            action_id=action_id,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def create_edge_action(self, source, js_body):
        """Update an Edge Action.

        https://rest.octave.dev/#creating-an-edge-action
        """
        url = self._url("{base_url}/{company_name}/local-action")
        if not source.startswith("observation://"):
            msg = "Source always must start with observation:// not {source!r}"
            raise InvalidResource(msg)
        payload = dict(source=source, js=js_body)
        return await self._post(url, json=payload)

    async def remove_edge_action(self, action_id):
        """Delete an Edge Action.

        https://rest.octave.dev/#deleting-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/local-action/{action_id}",
            action_id=action_id,
        )
        return await self._delete(url)

    async def update_edge_action(self, action_id, fields=None, props=None):
        """Update an Edge Action.

        https://rest.octave.dev/#updating-an-edge-action
        """
        url = self._url(
            "{base_url}/{company_name}/local-action/{action_id}",
            action_id=action_id,
        )
        params = query_params(fields)
        payload = props
        return await self._put(url, params=params, json=payload)
