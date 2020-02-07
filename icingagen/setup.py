"""icingagen package configuration."""
from setuptools import setup

setup(
    name="icingagen",
    version="0.1",
    description="SOWN Icinga 2 monitoring configuration management",
    url="https://github.com/sown/monitoring",
    author="SOWN",
    packages=["icingagen"],
    zip_safe=False,
    install_requires=[
        "pynetbox",
        "jinja2",
        "requests",
        "click",
    ],
    extras_require={
        "dev": [
            "flake8",
            "flake8-commas",
            "flake8-comprehensions",
            "flake8-debugger",
            "flake8-mutable",
            "flake8-todo",
            "flake8-docstrings",
            "flake8-isort",
        ],
    },
    entry_points={
        "console_scripts": [
            "icingagen=icingagen.cli:cli",
        ],
    },
)
