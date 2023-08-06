import hmac
import hashlib

from jupyterhub.auth import Authenticator
from traitlets import Bytes, Unicode, Union, validate


class HMACAuthenticator(Authenticator):
    """
    JupyterHub authenticator where the password is HMAC of username + secret key.

    Useful when you want to procedurally generate many users
    to test your JupyterHub install. This is more secure
    than DummyAuthenticator and much simpler than most other
    password based authenticators.
    """

    secret_key = Union(
        [Bytes(), Unicode()],
        config=True,
        help="""
        Hex encoded secret key to use for deriving the HMAC.

        Recommend generating with `openssl rand -hex 64`,
        which provides a 512-bit secret key.
        """
    )


    @validate('secret_key')
    def _validate_secret_key(self, proposal):
        """Coerces strings with even number of hexidecimal characters to bytes."""
        r = proposal['value']
        if type(r) == str:
            try:
                return bytes.fromhex(r)
            except ValueError:
                raise ValueError("secret_key set as a string must contain an even amount of hexadecimal characters.")
        else:
            return r


    async def authenticate(self, handler, data):
        sha512_hmac = hmac.new(
            self.secret_key,
            data['username'].encode('utf-8'),
            hashlib.sha512
        )
        if hmac.compare_digest(sha512_hmac.hexdigest(), data['password']):
            return data['username']
        return None
