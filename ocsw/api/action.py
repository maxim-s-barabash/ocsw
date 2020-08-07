"""Cloud Action.

A Cloud Action transforms Events and routes them between Streams.
Transformations are done via optional JavaScript.
"""

from ..errors import InvalidResource
from ..utils.query_params import query_params


class ActionApiMixin:
    async def actions(self, company_name=None, **query):
        """List of company Cloud Actions.

        https://rest.octave.dev/#listing-company-cloud-actions
        """
        ctx = dict()
        if company_name:
            ctx["company_name"] = company_name

        url = self._url("{base_url}/{company_name}/action", **ctx)
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_action(self, action_id, **query):
        """Reading a Cloud Action.

        https://rest.octave.dev/#reading-a-cloud-action
        """
        url = self._url(
            "{base_url}/{company_name}/action/{action_id}",
            action_id=action_id,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def create_action(
        self,
        source,
        js_body,
        description=None,
        destination=None,
        disabled=False,
        filter_test=None,
    ):
        """Update an Cloud Action.

        https://rest.octave.dev/#creating-a-cloud-action

        description  string  optional. human-friendly description
        destination  string  optional. event output path.
        disabled     bool    is action disabled?
        js_body      string  optional. javascript to execute.
        source       string  required. path from which to read events.
        filter_test  string  optional. a filter which is used as a pass/fail
                             test for evaluating whether to run
                             new events on the source stream through
                             the cloud action
        """
        url = self._url("{base_url}/{company_name}/action")
        if source and source[0] not in "/@":
            msg = 'Source always must start with "/" or "@" not {source!r}'
            raise InvalidResource(msg)
        payload = dict(
            source=source,
            js=js_body,
            description=description,
            destination=destination,
            disabled=disabled,
            filter=filter_test,
        )
        return await self._post(url, json=payload)

    async def remove_action(self, action_id):
        """Deleting a Cloud Action.

        https://rest.octave.dev/#deleting-a-cloud-action
        """
        url = self._url(
            "{base_url}/{company_name}/action/{action_id}",
            action_id=action_id,
        )
        return await self._delete(url)

    async def update_action(self, action_id, fields=None, props=None):
        """Updating a Cloud Action.

        https://rest.octave.dev/#updating-a-cloud-action
        """
        url = self._url(
            "{base_url}/{company_name}/action/{action_id}",
            action_id=action_id,
        )
        params = query_params(fields)
        payload = props
        return await self._put(url, params=params, json=payload)
