# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# setup.py
#
# A standard Python configuration file that will provide meta information about
# this program and install dependent Python libraries.
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from setuptools import setup, find_packages

setup(
    name='website-referrals-lookup',
    version='1.0',
    packages=find_packages(exclude=['tests*']),
    license='APACHE 2.0',
    description='Looks up meta data for a list of website referrals (aka hits)',
    long_description=open('README.md').read(),
    install_requires=['PyYAML', 'requests_html'],
    url='https://github.com/LeviMichalski/WebsiteContentRetriever',
    author='Levi Michalski',
    author_email='levitmichalski@gmail.com'
)