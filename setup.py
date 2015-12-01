from setuptools import setup, find_packages

setup(
    name='saas',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/its-dirg/saas_test_environment',
    license='Apache 2.0 License',
    author='Rebecka Gulliksson',
    author_email='rebecka.gulliksson@umu.se',
    description='SAML-to-SAML proxy for SaaS '
)
