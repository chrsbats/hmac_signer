from distutils.core import setup

setup(
    name='hmac_signer',
    version='1.0.1',
    author='C Bates',
    author_email='chrsbats@gmail.com',
    packages=['hmac_signer'],
    scripts=[],
    url='https://github.com/chrsbats/hmac_signer',
    license='LICENSE.TXT',
    description='HMAC Sign your Requests posts and validate them in Flask',
    long_description='',
    install_requires=[
        "Flask>=0.10.1",
        "python-dateutil>=2.4.2",
        "requests>=2.7.0",
    ],
)
