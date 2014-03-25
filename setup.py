from distutils.core import setup

setup(
    name='TSTK_packages',
    version='0.1.0',
    author='F.M. Walinga',
    author_email='frank.walinga@intraffic.nl',
    packages=['testsystem','driver','simulator'],
    license= open('LICENSE.txt').read(),
    long_description=open('README.txt').read(),
    install_requires=[
        "pyzmq",
        "pyserial",
        "docopt",
    ],
)
