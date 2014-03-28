from distutils.core import setup

setup(
    name='TSTK',
    version='0.1.0',
    author='F.M. Walinga',
    author_email='frank.walinga@intraffic.nl',
    packages=['TSTK',],
    license= open('LICENSE.txt').read(),
    long_description=open('README.rst').read(),
    install_requires=[
        "pyzmq",
        "pyserial",
        "docopt",
    ],
)
