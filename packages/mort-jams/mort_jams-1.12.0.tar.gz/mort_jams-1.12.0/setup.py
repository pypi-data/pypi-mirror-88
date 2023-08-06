from setuptools import setup, find_packages

# DO_NOT_MODIFY_THIS_VALUE_IS_SET_BY_THE_BUILD_MACHINE
VERSION = "1.12.0"


def readme():
    with open("README.md") as f:
        return f.read()


with open("requirements.txt") as file:
    REQUIRED_MODULES = [line.strip() for line in file]

with open("requirements-dev.txt") as file:
    DEVELOPMENT_MODULES = [line.strip() for line in file]


setup(
    name="mort_jams",
    version=VERSION,
    description="cats and stuff",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="forms",
    url="https://github.com/justindujardin/mort_jams",
    author="Justin DuJardin",
    author_email="justin@dujardinconsulting.com",
    packages=find_packages(),
    install_requires=REQUIRED_MODULES,
    extras_require={"dev": DEVELOPMENT_MODULES},
    include_package_data=True,
)
