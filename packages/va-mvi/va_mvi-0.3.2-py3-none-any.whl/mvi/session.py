import logging
from typing import List, Callable, Any
import requests

# noqa: DAR101,DAR201,DAR401


class MVISession(requests.Session):
    def __init__(self, auth_domains: List[str] = None, log_func: Callable = None):
        """A specific requests.Session derivative for MVI

        Args:
            auth_domains (List[str]): List of domains to which redirection can safely
                be done with kept auth headers. Defaults to None.
            log_func (Callable): Callable that is called with any log messages.
                Defaults to None.

        \f
        # noqa: DAR101,DAR201,DAR401
        """
        super().__init__()
        self._auth_domains = auth_domains or list()
        self._log_func = log_func or logging.getLogger(__name__).warning

    def should_strip_auth(self, old_url: str, new_url: str) -> bool:
        """Overriding `should_strip_auth` of `request.Session` to allow for
        custom logic in terms of when auth header should be removed/kept.

        Args:
            old_url (str): Old url (before redirect)
            new_url (str): New url (suggested redirect)

        Returns:
            bool: True if auth header should be stripped, otherwise False

        \f
        # noqa: DAR101,DAR201,DAR401
        """
        new_host = requests.utils.urlparse(new_url).hostname

        if new_host in self._auth_domains:
            # If we recognize the new host name, keep the Authorization header
            return False

        # Fallback to default behavior
        return super().should_strip_auth(old_url, new_url)

    def request(self, *args, **kwargs):  # pylint: disable=signature-differs
        """Overriding the `request` method on the `Session` object so that
        we can allow retrying if the SSL certificate could not be verified as
        well as raising any errors by default.

        \f
        # noqa: DAR101,DAR201,DAR401
        """
        try:
            # Try with default (verify=True)
            response = super().request(*args, **kwargs)
        except requests.exceptions.SSLError:
            # It failed, log a warning and skip the verification
            self._log_func(
                "SSL certificate could not be verified! MVI will continue to work but"
                " this potentially makes your solution vulnerable to Man-in-the-middle"
                " attacks!"
            )
            kwargs.update({"verify": False})
            response = super().request(*args, **kwargs)

        # TODO: https://github.com/vikinganalytics/mvi/issues/394
        # Raise any non-200 codes as proper python errors
        # response.raise_for_status()
        return response


def request(*args, **kwargs) -> Any:
    """Convenience function for `MVISession`

    Returns:
        Any: Whatever `requests.request` returns

    \f
    # noqa: DAR101,DAR201,DAR401
    """

    auth_domains = kwargs.pop("auth_domains", None)
    log_func = kwargs.pop("log_func", None)

    with MVISession(auth_domains=auth_domains, log_func=log_func) as session:
        return session.request(*args, **kwargs)
