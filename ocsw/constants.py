from .version import VERSION

DEFAULT_CONFIG = ".octave/config.json"
DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_USER_AGENT = f"octave-sdk-python/{VERSION}"
OCTAVE_API_DEFAULT = "https://octave-api.sierrawireless.io/v5.0"
MASKED_ATTRIBUTE_VALUE = "********"

CONNECTIONS_TYPE = {
    "aws": {"label": "Amazon Web Services"},
    "azure-iothub-http-gateway-connector": {"label": "Azure IoT Hub"},
    "googlecloud": {"label": "Google Cloud"},
    "http-connector": {"label": "HTTP"},
    "ibmcloud": {"label": "IBM Cloud"},
    "salesforce": {"label": "Salesforce"},
    "sap": {"label": "SAP"},
}
