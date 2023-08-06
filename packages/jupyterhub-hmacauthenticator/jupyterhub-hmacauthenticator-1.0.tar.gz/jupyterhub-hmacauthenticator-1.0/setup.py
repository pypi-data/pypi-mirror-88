from setuptools import setup, find_packages

setup(
    name='jupyterhub-hmacauthenticator',
    version='1.0',
    description='Dummy Authenticator for JupyterHub',
    url='https://github.com/yuvipanda/jupyterhub-hmacauthenticator',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    python_requires=">=3.6",
)
