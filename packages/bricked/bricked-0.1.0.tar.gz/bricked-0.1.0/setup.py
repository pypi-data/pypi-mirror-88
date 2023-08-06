from setuptools import find_packages, setup

REQUIREMENTS = [
    "aiohttp==3.7.3",
    "jinja2==2.11.2",
    "bcrypt==3.2.0",
]

EXTRA_REQUIREMENTS = {
    "test": [
        "pytest",
        "pytest-aiohttp",
        "tox",
    ],
    "dev": [
        "black",
        "pre-commit",
        "twine",
    ],
}

setup(
    name="bricked",
    version="0.1.0",
    author="Andrew O'Brien",
    author_email="andrew@obrien.io",
    description="Asyncio MVC web framework",
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    packages=find_packages(
        exclude=[
            "bricked_test",
        ]
    ),
)
