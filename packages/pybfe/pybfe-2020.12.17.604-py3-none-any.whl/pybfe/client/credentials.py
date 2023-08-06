from typing import TYPE_CHECKING

from grpc import AuthMetadataContext, AuthMetadataPlugin, AuthMetadataPluginCallback

if TYPE_CHECKING:
    from pybfe.client.session import Session


class CallCredentialsPlugin(AuthMetadataPlugin):
    """Plugin that adds BFE session credentials to every GRPC's call context"""

    def __init__(self, session: "Session") -> None:
        self._session = session

    def __call__(
        self, context: AuthMetadataContext, callback: AuthMetadataPluginCallback
    ) -> None:
        metadata = (
            []
            if self._session.access_token is None
            else list({"authorization": self._session.access_token}.items())
        )
        callback(
            metadata, None,
        )
