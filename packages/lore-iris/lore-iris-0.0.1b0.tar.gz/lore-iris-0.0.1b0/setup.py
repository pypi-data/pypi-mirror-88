import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lore-iris",
    # we will start working via alpha version numbers
    version="0.0.1b0",
    description="Programmatic access to thousands of public documents.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://api.iris.lore.ai",
    author="Lore Ai",
    author_email="iris@lore.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["lore.iris"],
    include_package_data=True,
    install_requires=["pyyaml"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)

