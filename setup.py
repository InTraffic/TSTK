from distutils.core import setup

setup(
    name='Toolkit_packages',
    version='0.1.0dev',
    packages=['cc','focon','train', 'scenarioplayer', 'testcase', 'osoap',],
    license= open('LICENCE.txt').read(),
    long_description=open('README.txt').read(),
)
