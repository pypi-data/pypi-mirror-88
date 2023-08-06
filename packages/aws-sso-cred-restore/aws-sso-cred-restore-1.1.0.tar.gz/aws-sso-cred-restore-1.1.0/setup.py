from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aws-sso-cred-restore",
    version="1.1.0",
    description="A wrapper for executing a command with AWS CLI v2 and SSO, inspired from aws2-wrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytonsilva/aws-sso-cred-restore",
    author="Clayton Silva",
    author_email="clayton.silva@pagar.me",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    license="GNU General Public License v3 (GPLv3)",
    keywords="aws profile sso assume role",
    packages=[
        "awsssocredrestore"
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'aws-sso-cred-restore = awsssocredrestore:main',
        ]
    },
    python_requires=">=3.6",
)
