# HMAC JupyterHub Authenticator #

Special authenticator for [JupyterHub](http://github.com/jupyter/jupyterhub/)
that allows all user logins where the password matches the hex SHA512 HMAC of the
username keyed with a secret, shared 512-bit key.

## WHAT?! ##

This is a variant of [DummyAuthenticator](https://github.com/yuvipanda/jupyterhub-dummyauthenticator)
but more secure and meant to be made available over the internet for testing purposes.

If you want to create a large number of JupyterHub users dynamically (for load testing purposes)
in a machine compatible way, this is a great fit. You can share just the secret key between
the JupyterHub and your load testing client, and create as many users as you would like

## Installation ##

```
pip install jupyterhub-hmacauthenticator
```

Should install it. It has no additional dependencies beyond JupyterHub.

You can then use this as your authenticator by adding the following line to
your `jupyterhub_config.py`:

```
c.JupyterHub.authenticator_class = 'hmacauthenticator.HMACAuthenticator'

c.HMACAuthenticator.secret_key = bytes.fromhex('secret-key-here')
```

You can generate a 512-bit secret key with:

```
openssl rand -hex 64
```

## Generating the password on client side ##

This snippet of code would generate the password on the client side:

```python
secret_key = bytearray.fromhex('same-secret-key')

username = "your-username".encode('utf-8')
password = hmac.new(secret_key, username, hashlib.sha512).hexdigest()
```
