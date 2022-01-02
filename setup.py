from setuptools import find_packages, setup
setup(
    name='lexoffice_api',
    packages=find_packages(include=['lexoffice_api']),
    version='0.1.0',
    description='Python library for interacting with the Public API of Lexoffice',
    author='Maik Lorenz',
    license='MIT',
    install_requires=[],
    test_suite='tests',
)