"""Cloud Action.

A Cloud Action transforms Events and routes them between Streams.
Transformations are done via optional JavaScript.
"""

from ..errors import InvalidResource
from ..utils.query_params import query_params

OBJECT_TYPE = "action"


class ActionApiMixin:
    async def actions(self, company_name=None, **query):
        """List of company Cloud Actions.

        https://rest.octave.dev/#listing-company-cloud-actions
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_action(
        self, object_id, company_name=None, version_number=None, **query
    ):
        """Reading a Cloud Action.

        https://rest.octave.dev/#reading-a-cloud-action
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

    async def create_action(
        self,
        source,
        js_body="",
        description=None,
        destination=None,
        disabled=False,
        filter_test=None,
        company_name=None,
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
        company_name string  optional. company name
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
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

    async def remove_action(self, object_id, company_name=None):
        """Deleting a Cloud Action.

        https://rest.octave.dev/#deleting-a-cloud-action
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}/{object_id}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
        )
        return await self._delete(url)

    async def update_action(
        self, object_id, fields=None, props=None, company_name=None,
    ):
        """Updating a Cloud Action.

        https://rest.octave.dev/#updating-a-cloud-action
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
