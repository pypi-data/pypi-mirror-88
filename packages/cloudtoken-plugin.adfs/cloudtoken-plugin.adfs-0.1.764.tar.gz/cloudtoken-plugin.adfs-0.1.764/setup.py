from setuptools import setup
import os

version = os.environ['VERSION']

setup(
    name='cloudtoken-plugin.adfs',
    version=version,
    description='Microsoft ADFS plugin for cloudtoken.',
    url='https://bitbucket.org/atlassian/cloudtoken',
    author='Atlassian Cloud Engineering',
    author_email='cloud-team@atlassian.com',
    license='Apache',
    py_modules=['cloudtoken_plugin.adfs'],
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=[
        "cloudtoken>=0.1.12",
        ],
)
