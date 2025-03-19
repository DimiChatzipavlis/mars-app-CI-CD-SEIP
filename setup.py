from setuptools import setup, find_packages

setup(
    name='mars_mission_control',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pytest',
        'pylint',
        'flake8',
        'requests'
    ],
)
