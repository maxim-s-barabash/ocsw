"""Cloud Action.

A Cloud Action transforms Events and routes them between Streams.
Transformations are done via optional JavaScript.
"""

from ..errors import InvalidResource
from ..utils.query_params import query_params

OBJECT_TYPE = "connector"


class ConnectorApiMixin:
    async def connectors(self, company_name=None, **query):
        """List of company Cloud Connectors.

        https://rest.octave.dev/#listing-company-cloud-connectors
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
        )
        params = query_params(**query)
        return await self._get(url, params=params)

    async def inspect_connector(
        self, object_id, company_name=None, version_number=None, **query
    ):
        """Reading a Cloud Connectors.

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

    async def create_connector(
        self,
        source,
        js_body="",
        description=None,
        destination=None,
        disabled=False,
        routing_script=False,
        headers=None,
        properties=None,
        filter_test=None,
        company_name=None,
    ):
        """Create an Cloud Connectors.

        https://rest.octave.dev/#creating-a-cloud-connector

        description    string    optional. human-friendly description
        disabled       bool      is action disabled?
        source         string    required. path from which to read events.
        js_body        string    required. javascript function definition
                                 to create exported payload from event.
                                 This will be an a function taking 1 argument,
                                 returning an arbitrary JSON map.
        routing_script string    optional. javascript function definition
                                 to create a URL string representation from
                                 the event. This will be a function taking
                                 1 argument, returning a string.
        headers        string    required-per-type. header passed verbatim to
                                 the indicated external end-point via the
                                 connector. Typically there are specific
                                 headers per distinct connector types.
                                 Any additional custom headers not required
                                 by the connector-type is also passed verbatim.
        properties     map       required-per-type. Typically there are
                                 specific properties per distinct connector
                                 types. Properties are not passed along with
                                 the exported event -- they are only required
                                 for parameterize the operation of specific
                                 connector types.
        filter_test    string    optional. a filter which is used as
                                 a pass/fail test for evaluating whether to
                                 run new events on the source stream through
                                 the cloud action.
        company_name   string    optional. company name.
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
            properties=None,
            headers=headers,
            description=description,
            disabled=disabled,
            filter=filter_test,
            routingScript=routing_script,
        )
        return await self._post(url, json=payload)

    async def remove_connector(self, object_id, company_name=None):
        """Deleting a Cloud Connectors.

        https://rest.octave.dev/#deleting-a-cloud-connector
        """
        url = self._url(
            "{base_url}/{company_name}/{object_type}/{object_id}",
            company_name=company_name or self.current_company,
            object_type=OBJECT_TYPE,
            object_id=object_id,
        )
        return await self._delete(url)

    async def update_connector(
        self, object_id, fields=None, props=None, company_name=None,
    ):
        """Updating a Cloud Connectors.

        https://rest.octave.dev/#updating-a-cloud-connector
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
